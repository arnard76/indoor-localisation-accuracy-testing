<script lang="ts">
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

	let areaMapImagesURL = $state<{ [key: string | number]: string }>({ 'Area Map Image': '' });
	let areaIsMultipleFloors = $state(false);
	let validAreaImages = $derived(Object.entries(areaMapImagesURL).filter((a) => a[0] && a[1]));

	localStorage.clear(); // reset area map and location inputs (because they work for one map only)

	function saveImage() {
		if (!validAreaImages.length) return;
		localStorage.setItem('area-map-urls', JSON.stringify(Object.fromEntries(validAreaImages)));
	}

	$effect(() => {
		// if the last area map image url is filled out, make another one
		if (Object.keys(areaMapImagesURL).length === validAreaImages.length) {
			const newElementNumber = validAreaImages.length;
			const newElement = {
				[areaIsMultipleFloors ? newElementNumber : `Sub-area ${newElementNumber}`]: ''
			};
			areaMapImagesURL = { ...Object.fromEntries(validAreaImages), ...newElement };
		}
	});
</script>

<form>
	<!-- {#if areaHasMultipleImages} -->

	{#each Object.entries(areaMapImagesURL) as [label, URL], index (index)}
		<div class="flex gap-4">
			{#if index === 0}
				{#if areaIsMultipleFloors}
					<div>
						<p>Floor Name</p>
						<p>Floor 0</p>
					</div>
				{:else}
					<label
						>Unique Label
						<input type="text" placeholder="Sub-area label" bind:value={areaMapImagesURL[label]} />
					</label>
				{/if}
				<label
					>URL
					<input type="text" placeholder="Sub-area Map URL" bind:value={areaMapImagesURL[label]} />
				</label>
			{:else}
				{#if areaIsMultipleFloors}
					<p>Floor {index}</p>
				{:else}
					<input type="text" placeholder="Sub-area label" bind:value={areaMapImagesURL[label]} />
				{/if}
				<input type="text" placeholder="Sub-area Map URL" bind:value={areaMapImagesURL[label]} />
			{/if}
		</div>
	{/each}
	<!-- {/if} -->

	<div class="flex gap-4">
		<label class="flex" for="area-multiple-map-floors">Sub-areas are different floors?</label>
		<input type="checkbox" id="area-multiple-map-floors" bind:checked={areaIsMultipleFloors} />
	</div>

	<!-- <div class="flex gap-4">
		<label class="flex" for="area-multiple-map-images"> Area has multiple images for the map</label>
		<input type="checkbox" id="area-multiple-map-images" bind:checked={areaHasMultipleImages} />
	</div> -->

	<div>
		<button
			onclick={() => {
				areaIsMultipleFloors = true;
				areaMapImagesURL = {
					'0': '',
					'1': '/area-images/floor 0 1536x1536.png',
					'2': '/area-images/floor 1 1536x1536.png',
					'3': '/area-images/floor 2 1536x1536.png'
				};
			}}>Use Example: Building 302 Map</button
		>
	</div>
</form>

{#if validAreaImages.length !== 0}
	<div class="max-w-2/3 flex flex-col items-start">
		<h2>Area Map Preview</h2>

		<div class="flex w-full gap-2">
			{#each validAreaImages as [label, imageURL] (label + imageURL)}
				<div>
					<p>{label}</p>
					<AreaMap mapImageLabel={label} mapImageURL={imageURL} bind:rawPosition>
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
					</AreaMap>
				</div>
			{/each}
		</div>
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
				<!-- <label for="floor_input">Floor</label>
				<input
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
				{#each Object.entries(locations) as [locationName, location] (locationName)}
					<p>{locationName} | {displayLocation(location, distanceUnit)}</p>
				{/each}
			</div>
		</div>

		<a class="button" href="/input-locations" onclick={saveImage}>
			Input locations to test this area
		</a>
	</div>
{/if}
