<script lang="ts">
	import { mapImageUrls } from '$lib/areaMap/area';
	import AreaMap from '$lib/areaMap/AreaMap.svelte';
	import MapLocation from '$lib/areaMap/MapLocation.svelte';
	import {
		convertLocationsFromFormat,
		displayLocation,
		scaleLocations,
		type LocationUnits,
		type MapLocations as MapLocationsType
	} from '$lib/locations/format';
	import { mapImagePixelsToScreenPixelsScale } from '$lib/locations/pixelScale';

	let currentFloor = $state(1);
	let origin = $state({ x: 0, y: 0 }); // TODO: keep this in the right pixels scale too
	let rawPosition = $state({ x: 0, y: 0 });
	let calculated = $derived({ x: rawPosition.x - origin.x, y: origin.y - rawPosition.y });

	let locationsInPixels = $derived({
		Origin: origin,
		Raw: rawPosition,
		Calculated: calculated
	});

	let locationsInScreenPixels = $derived(
		scaleLocations(locationsInPixels, $mapImagePixelsToScreenPixelsScale)
	);
	let locationsInMetres = $derived({
		...convertLocationsFromFormat(locationsInPixels, 'pixels')
	});

	let distanceUnit = $state<LocationUnits>('metres');
	let locations = $derived<MapLocationsType>(
		distanceUnit === 'pixels' ? locationsInPixels : locationsInMetres
	);
</script>

<div>
	<AreaMap mapImageURL={$mapImageUrls[currentFloor.toString()]} bind:rawPosition>
		<!-- <Map {currentFloor} bind:rawPosition> -->
		{#snippet mapLocations()}
			<MapLocation
				unit={distanceUnit}
				name="Calculated"
				position={locationsInScreenPixels['Raw']}
				displayedPosition={locations['Calculated']}
			/>
			<MapLocation
				unit={distanceUnit}
				position={locationsInScreenPixels['Origin']}
				colour="oklch(62.3% 0.214 259.815)"
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
					onclick={() => (distanceUnit = 'metres')}
					class={distanceUnit === 'metres' ? 'selected' : 'unselected'}>metres</button
				>
				<button
					onclick={() => (distanceUnit = 'pixels')}
					class={distanceUnit === 'pixels' ? 'selected' : 'unselected'}>pixels</button
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
						if (distanceUnit === 'metres')
							if (!Number.isNaN(y_origin_input)) origin.y = y_origin_input;
					}}
				/>
			</fieldset>
			<label for="floor_input">Floor</label>
			<input
				id="floor_input"
				value={currentFloor}
				oninput={(e) => {
					const floor_input = parseInt(e.currentTarget.value);
					if (!Number.isNaN(floor_input)) currentFloor = floor_input;
				}}
				type="number"
			/>
		</div>

		<div class="widget min-w-96">
			<h3>Locations</h3>
			{#each Object.entries(locations) as [locationName, location] (locationName)}
				<p>{locationName} | {displayLocation(location, distanceUnit)}</p>
			{/each}
		</div>
	</div>
</div>
