<script lang="ts">
	import { type ImportableLocationReading, type LocationReading } from '$lib/locations/format';
	import { areTimestampsEquivalent, distanceDiffFromLocations } from '$lib/test/positionAccuracy';
	import { downloadSomething } from '$lib/testArtifacts/util';
	import dayjs from 'dayjs';

	export function cleanLocationObject(location?: ImportableLocationReading): LocationReading {
		if (!location) return { timestamp: '', x: NaN, y: NaN };
		const x_in_metres = location.location[0];
		const y_in_metres = location.location[2];
		return {
			timestamp: location.timestamp,
			x: x_in_metres,
			y: y_in_metres
		};
	}

	export function setOriginToFirstValue(locations: LocationReading[]): LocationReading[] {
		const origin = locations.at(0);
		if (!origin) throw Error('locations data empty');

		return locations.map(({ timestamp, x, y }) => {
			return { timestamp, x: x - origin.x, y: y - origin.y };
		});
	}

	export function trimFirst6s(locations: LocationReading[]): LocationReading[] {
		const firstFrame = locations.at(0);
		if (!firstFrame) throw Error('locations data empty');

		const validLocations = locations.filter((l) =>
			dayjs(l.timestamp).isAfter(dayjs(firstFrame.timestamp).add(6, 'seconds'))
		);

		return [{ ...firstFrame, x: validLocations[0].x, y: validLocations[0].y }, ...validLocations];
	}

	function trimFirst1m11s(locations: LocationReading[]): LocationReading[] {
		return trimFirstXs(locations, 60 + 11);
	}

	export function trimFirstXs(locations: LocationReading[], x: number): LocationReading[] {
		const firstFrame = locations.at(0);
		if (!firstFrame) throw Error('locations data empty');

		const validLocations = locations.filter((l) =>
			dayjs(l.timestamp).isAfter(dayjs(firstFrame.timestamp).add(x, 'seconds'))
		);

		return validLocations;
	}

	function arucoTrim6sOriginate(locations: ImportableLocationReading[]): LocationReading[] {
		return setOriginToFirstValue(
			trimFirst6s(locations.map((location) => cleanLocationObject(location)))
		);
	}

	function rotateVector(vec: number[], ang: number) {
		ang = -ang * (Math.PI / 180);
		var cos = Math.cos(ang);
		var sin = Math.sin(ang);
		return [
			Math.round(10000 * (vec[0] * cos - vec[1] * sin)) / 10000,
			Math.round(10000 * (vec[0] * sin + vec[1] * cos)) / 10000
		];
	}

	function rotateXDegreesFromOrigin(
		locations: LocationReading[],
		xDegrees: number
	): LocationReading[] {
		return locations.map((location) => {
			const rotated = rotateVector([location.x, location.y], xDegrees);
			const [x, y] = rotated;

			return { ...location, x, y };
		});
	}

	function reflectInXAxis(locations: LocationReading[]): LocationReading[] {
		return locations.map((location) => {
			return { ...location, x: -1 * location.x, y: location.y };
		});
	}

	function removeAnomaliesLike5mJumps(locations: LocationReading[]): LocationReading[] {
		return locations.filter((location, index) => {
			const previousReading = index > 0 ? locations.at(index - 1) : undefined;
			const nextReading = index < locations.length - 1 ? locations.at(index + 1) : undefined;

			const closeEnoughReadings = [previousReading, nextReading].filter((r) => {
				if (!r) return false;

				if (!areTimestampsEquivalent(r.timestamp, location.timestamp)) return false;

				return true;
			}) as LocationReading[];

			for (const reading of closeEnoughReadings) {
				const ms = dayjs(reading.timestamp).diff(location.timestamp, 'milliseconds');
				const speed = Math.abs((distanceDiffFromLocations(reading, location) * 1000) / ms);
				if (speed > 10) return false;
			}
			return true;
		});
	}

	function formatOdomLogs(locations: any[]) {
		return locations.map((reading) => {
			console.log({ reading });
			const formattedTimestamp = new Date(reading.time * 1000).toISOString();
			console.log(formattedTimestamp);

			return { ...reading, timestamp: formattedTimestamp, orientation: reading.yaw_deg };
		});
	}

	const formatters = {
		formatOdomLogs,
		arucoTrim6sOriginate,
		aruco: (locations: ImportableLocationReading[]) =>
			locations.map((location) => cleanLocationObject(location)),
		origin: setOriginToFirstValue,
		trimFirst1m11s,
		trim6s: trimFirst6s,
		// rotateFromOrigin,
		reflectInXAxis,
		removeAnomaliesLike5mJumps
	};

	let selectedFormat: undefined | keyof typeof formatters = $state();
	let locations: undefined | ImportableLocationReading[] = $state();
	let formattedLocations = $state('');
	let locationsFileName = $state('');

	$effect(() => {
		if (!locations || selectedFormat === undefined) return;

		formattedLocations = formatters[selectedFormat](locations);
	});

	function downloadFormattedLocations() {
		downloadSomething(
			'text/json',
			'utf-8',
			`${locationsFileName}-formatted.json`,
			encodeURIComponent(JSON.stringify(formattedLocations))
		);
	}
</script>

/* eslint-disable @typescript-eslint/no-explicit-any */
<h1>Format locations</h1>

<select bind:value={selectedFormat}>
	{#each Object.keys(formatters) as formatName (formatName)}
		<option value={formatName}>{formatName}</option>
	{/each}
</select>

<input
	type="file"
	onchange={async (e) => {
		if (!e.currentTarget.files) return;

		const file = e.currentTarget.files[0];
		locations = JSON.parse(await file.text());
		locationsFileName = file.name;
	}}
	accept=".json"
/>

{#if formattedLocations}
	<button onclick={downloadFormattedLocations}>Download formatted file</button>
{/if}
