<script lang="ts">
	import MapPosition from '$lib/areaMap/MapPosition.svelte';
	import {
		convertLocationFromFormat,
		displayLocation,
		type LocationUnits
	} from '$lib/locations/format';
	import type { createPlayer } from '$lib/test/playbackTimes';
	import { distanceDiffFromLocationDiff, locationDiff } from '$lib/test/positionAccuracy';
	import { mapImageUrls } from './area';
	import AreaMap from './AreaMap.svelte';

	let { player }: { player: ReturnType<typeof createPlayer> } = $props();

	let currentFloor = $state(Object.keys($mapImageUrls)[0]);
	let origin = $state({ x: 0, y: 0 }); // TODO: keep this in the right pixels scale too
	let rawPixelPosition = $state({ x: 0, y: 0 });
	let rawPosition = $derived(convertLocationFromFormat(rawPixelPosition, 'pixels'));

	let locationsInMetres = $derived({
		Origin: origin,
		Raw: rawPosition,
		...$player!.currentLocations
	});

	$inspect(locationsInMetres);

	let displayUnit = $state<LocationUnits>('metres');

	let locationDifference = $derived(
		locationDiff(locationsInMetres['wifinder'], locationsInMetres['aruco'])
	);

	let distanceDifference = $derived(distanceDiffFromLocationDiff(locationDifference));
</script>

<div>
	<AreaMap mapImageURL={$mapImageUrls[currentFloor]} bind:rawPosition>
		{#snippet mapLocations()}
			<!-- <MapShapeOverTime /> -->
			<MapPosition inputUnit="pixels" {displayUnit} position={locationsInMetres['Raw']} {origin} />
			<MapPosition
				{displayUnit}
				inputUnit="metres"
				position={locationsInMetres['Origin']}
				colour="oklch(62.3% 0.214 259.815)"
				{origin}
			/>

			<MapPosition
				inputUnit="metres"
				{displayUnit}
				name="WiFinder"
				position={locationsInMetres['wifinder']}
				colour="powderblue"
				{origin}
			/>

			<MapPosition
				inputUnit="metres"
				{displayUnit}
				name="CV measured location"
				position={locationsInMetres['aruco']}
				colour="#50a9be"
				{origin}
			/>
		{/snippet}
		<!-- </Map> -->
	</AreaMap>

	<h2>Debug Panel</h2>
	<div
		class="debug-panel mb-4 flex w-full flex-wrap items-start gap-2 p-6 font-semibold text-white"
	>
		<div class="widget">
			<h3>Units</h3>
			<div class="button-group">
				<button
					onclick={() => (displayUnit = 'metres')}
					class={displayUnit === 'metres' ? 'selected' : 'unselected'}>metres</button
				>
				<button
					onclick={() => (displayUnit = 'pixels')}
					class={displayUnit === 'pixels' ? 'selected' : 'unselected'}>pixels</button
				>
			</div>
		</div>

		<div class="widget">
			<fieldset>
				<h3>Origin</h3>
				<label for="x_origin_input">X</label>
				<input
					placeholder="X"
					id="x_origin_input"
					value={origin.x}
					type="number"
					oninput={(e) => {
						const x_origin_input = parseInt(e.currentTarget.value);
						if (!Number.isNaN(x_origin_input)) origin.x = x_origin_input;
					}}
				/>
				<label for="y_origin_input">Y</label>
				<input
					placeholder="Y"
					id="y_origin_input"
					value={origin.y}
					type="number"
					oninput={(e) => {
						let y_origin_input = parseInt(e.currentTarget.value);
						if (displayUnit === 'metres')
							if (!Number.isNaN(y_origin_input)) origin.y = y_origin_input;
					}}
				/>
			</fieldset>
			<label for="floor_input">Floor</label>
			<select id="floor_input" bind:value={currentFloor}>
				{#each Object.keys($mapImageUrls) as mapLabel (mapLabel)}
					<option value={mapLabel}>{mapLabel}</option>
				{/each}
			</select>
			<!-- <input
				id="floor_input"
				value={currentFloor}
				oninput={(e) => {
					const floor_input = parseInt(e.currentTarget.value);
					if (!Number.isNaN(floor_input)) currentFloor = floor_input;
				}}
				type="number"
			/> -->
		</div>

		<div class="widget min-w-96">
			<h3>Locations</h3>
			{#each Object.entries(locationsInMetres) as [locationName, location] (locationName)}
				<p>
					{locationName} | {displayLocation(
						convertLocationFromFormat(location, 'metres', displayUnit),
						displayUnit
					)}
				</p>
			{/each}
			<br />
			<p>
				Location Difference | {displayLocation(
					convertLocationFromFormat(locationDifference, 'metres', displayUnit),
					displayUnit
				)}
			</p>
			<p>Distance Difference: {distanceDifference.toFixed(3)}</p>
		</div>
	</div>
</div>
