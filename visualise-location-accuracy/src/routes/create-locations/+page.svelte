<script lang="ts">
	import { mapImageUrls } from '$lib/areaMap/area';
	import AreaMap from '$lib/areaMap/AreaMap.svelte';
	import MapPosition from '$lib/areaMap/MapPosition.svelte';
	import ArucoCVVideoPreview from '$lib/arucoCVVideo/ArucoCVVideoPreview.svelte';
	import type { PositionReading } from '$lib/locations/format';
	import { locations } from '$lib/locations/locationsData';
	import { createPlayer } from '$lib/test/playbackTimes';
	import { createAccuracyCalculator } from '$lib/test/positionAccuracy';
	import type { Dayjs } from 'dayjs';
	import dayjs from 'dayjs';

	type Vector = [number, number]; // angle change in degrees, distance change in metres

	let generatedPositions: undefined | PositionReading[] = $state();

	class LocationsGenerator {
		create(
			speed: number,
			angularSpeed: number,
			startX: number,
			startY: number,
			startOrientation: number,
			startTime: Dayjs,
			path: Vector[],
			fps: number = 10 // locations generated per second
		): PositionReading[] {
			let locations: (PositionReading & { timestamp: Dayjs })[] = [];

			let startLocation = {
				x: startX,
				y: startY,
				orientation: startOrientation,
				timestamp: startTime
			};
			locations.push(startLocation);
			for (const [rotation, distance] of path) {
				let lastLocation = locations.at(-1)!;

				const rotationTime = Math.abs(rotation / angularSpeed);
				const numberOfRotationLocations = Math.floor(fps * rotationTime);

				for (let rI = 1; rI <= numberOfRotationLocations; rI += 1) {
					locations.push({
						...lastLocation,
						timestamp: lastLocation.timestamp.add((1000 * rI) / fps, 'ms'),
						orientation: lastLocation.orientation + (rotation * rI) / (fps * rotationTime)
					});
				}

				if (fps * rotationTime > numberOfRotationLocations) {
					locations.push({
						...lastLocation,
						timestamp: lastLocation.timestamp.add(1000 * rotationTime, 'ms'),
						orientation: lastLocation.orientation + rotation
					});
				}

				lastLocation = locations.at(-1)!;

				const distanceTime = distance / speed;
				const numberOfDistanceLocations = Math.floor(fps * distanceTime);

				const orientationRad = (lastLocation.orientation * Math.PI) / 180;
				const xMultiple = Math.cos(orientationRad);
				const yMultiple = Math.sin(orientationRad);

				const maxXChange = distance * xMultiple;
				const maxYChange = distance * yMultiple;
				for (let dI = 1; dI <= numberOfDistanceLocations; dI += 1) {
					const progress = dI / (fps * distanceTime);

					locations.push({
						...lastLocation,
						timestamp: lastLocation.timestamp.add(progress * distanceTime * 1000, 'ms'),
						x: lastLocation.x + progress * maxXChange,
						y: lastLocation.y + progress * maxYChange
					});
				}

				if (fps * distanceTime > numberOfDistanceLocations) {
					locations.push({
						...lastLocation,
						timestamp: lastLocation.timestamp.add(distanceTime * 1000, 'ms'),
						x: lastLocation.x + maxXChange,
						y: lastLocation.y + maxYChange
					});
				}
			}

			return locations;
		}
	}

	function downloadGeneratedLocations() {
		if (!generatedPositions) return;

		const testResultsData =
			'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(generatedPositions));
		const downloadEl = document.createElement('a');
		downloadEl.setAttribute('href', testResultsData);
		downloadEl.setAttribute(
			'download',
			`generated locations ${dayjs(generatedPositions[0].timestamp).toString()}.json`
		);
		downloadEl.click();
	}

	// square task in the middle
	const generator = new LocationsGenerator();
	generatedPositions = generator.create(
		0.2,
		90 / Math.PI,
		0,
		0,
		0,
		dayjs('2026-04-16T09:35:27.150Z'),
		[
			[0, 1],
			[-90, 1],
			[-90, 1],
			[-90, 1],
			[-90, 0]
		]
	);

	// rectangle task
	generatedPositions.push(
		...generator.create(0.2, 90 / Math.PI, 0, 0, 0, dayjs('2026-04-16T09:37:26.043Z'), [
			[0, 1],
			[-90, 2],
			[-90, 1],
			[-90, 2],
			[-90, 0]
		])
	);
	$effect(() => locations.set({ generated: generatedPositions }));

	const accuracyCalculator = createAccuracyCalculator();
	const player = createPlayer(accuracyCalculator);
	console.log($player);

	// let currentPosition = $derived(
	// 	generatedPositions.findLast(({ timestamp }) =>
	// 		dayjs(timestamp).isBefore($player.currentPlayingTimestamp)
	// 	)!
	// );
</script>

<h1>Create a set of locations over time</h1>

<p>Provide a path</p>
<div class="pointer-events-none absolute -z-10 overflow-hidden">
	<ArucoCVVideoPreview {player} />
</div>
{$player.currentPlayingTimestamp}

{#if generatedPositions}
	<AreaMap mapImageURL={$mapImageUrls[Object.keys($mapImageUrls)[0]]}>
		{#snippet mapLocations()}
			{#each generatedPositions as position (position.timestamp)}
				<MapPosition origin={{ x: 0, y: 0 }} {position} inputUnit="metres" />
			{/each}
			{#if $player.currentLocations['generated']}
				<MapPosition
					origin={{ x: 0, y: 0 }}
					position={$player.currentLocations['generated']}
					orientation={$player.currentLocations['generated'].orientation}
					inputUnit="metres"
					name="Generated Position"
					colour="#3BB9FF"
				/>
			{/if}
		{/snippet}
	</AreaMap>

	<button onclick={downloadGeneratedLocations}>Download Locations</button>
{/if}
