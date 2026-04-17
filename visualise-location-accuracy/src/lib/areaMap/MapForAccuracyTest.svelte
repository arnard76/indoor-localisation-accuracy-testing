<script lang="ts">
	import MapPosition from '$lib/areaMap/MapPosition.svelte';
	import {
		convertLocationFromFormat,
		displayLocation,
		type LocationUnits,
		type MapLocation
	} from '$lib/locations/format';
	import { locations } from '$lib/locations/locationsData';
	import type { createPlayer } from '$lib/test/playbackTimes';
	import { createAccuracyCalculator } from '$lib/test/positionAccuracy';
	import { mapImageUrls } from './area';
	import AreaMap from './AreaMap.svelte';

	let {
		player,
		accuracyCalculator
	}: {
		player: ReturnType<typeof createPlayer>;

		accuracyCalculator: ReturnType<typeof createAccuracyCalculator>;
	} = $props();

	let currentFloor = $state(Object.keys($mapImageUrls)[0]);
	let origin = $state({ x: 22, y: 23 }); // TODO: keep this in the right pixels scale too
	let rawPixelPosition = $state({ x: 0, y: 0 });
	let rawPosition = $derived(convertLocationFromFormat(rawPixelPosition, 'pixels'));

	let locationsInMetres = $derived<Record<string, MapLocation>>({
		Origin: origin,
		Raw: rawPosition,
		...$player!.currentLocations
	});

	let locationColours = $derived<Record<string, string>>({
		...Object.fromEntries(
			Object.keys($locations).map((setName) => [setName, `hsl(${Math.random() * 360}, 85%, 70%)`])
		),

		Origin: 'red',
		Raw: 'lightblue'
	});

	let displayUnit = $state<LocationUnits>('metres');
</script>

<div class="flex flex-wrap">
	<AreaMap mapImageURL={$mapImageUrls[currentFloor]} bind:rawPosition>
		{#snippet mapLocations()}
			<!-- <MapShapeOverTime /> -->
			<MapPosition
				inputUnit="metres"
				{displayUnit}
				position={locationsInMetres['Origin']}
				origin={{ x: 0, y: 0 }}
				fixed
			/>
			<!-- <MapPosition inputUnit="metres" {displayUnit} position={locationsInMetres['Raw']} {origin} /> -->

			{#each Object.entries($locations) as [name] (name)}
				<MapPosition
					inputUnit="metres"
					{displayUnit}
					position={$player.currentLocations[name]}
					orientation={$player.currentLocations[name].orientation}
					colour={locationColours[name]}
					{origin}
				/>
			{/each}
		{/snippet}
		<!-- </Map> -->
	</AreaMap>
	<div>
		<h2>Debug Panel</h2>
		<div
			class="debug-panel mb-4 flex w-min flex-wrap items-start gap-2 p-6 font-semibold text-white"
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
				<h3>Locations in {displayUnit}</h3>
				{#each Object.entries(locationsInMetres) as [locationName, location] (locationName)}
					<p
						style="background-color: {locationColours[locationName]}; color: black;"
						class="rounded-sm p-2"
					>
						{locationName}
						{displayLocation(
							convertLocationFromFormat(location, 'metres', displayUnit),
							displayUnit
						)}
					</p>
				{/each}
				<br />

				<!-- {#each $accuracyCalculator as comparison (comparison.idealSet + comparison.setToMeasure)}
					<p>
						Location Difference | {displayLocation(
							convertLocationFromFormat(
								calcLocationDiff(
									$player.currentLocations[comparison.idealSet],
									$player.currentLocations[comparison.setToMeasure]
								),
								'metres',
								displayUnit
							),
							displayUnit
						)}
					</p>
					<p>
						Distance Difference: {distanceDiffFromLocations(
							$player.currentLocations[comparison.idealSet],
							$player.currentLocations[comparison.setToMeasure]
						).toFixed(3)}
					</p>
				{/each} -->
			</div>
		</div>
	</div>
</div>
