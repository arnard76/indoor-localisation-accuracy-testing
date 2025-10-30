<script lang="ts">
	import AreaMap from '$lib/areaMap/AreaMap.svelte';

	let areaMapImagesURL = $state<{ [key: string | number]: string }>({ 'Area Map Image': '' });
	let areaIsMultipleFloors = $state(false);

	localStorage.clear(); // reset area map and location inputs (because they work for one map only)

	function saveImage() {
		if (!areaMapImagesURL) return;
		const images = Object.entries(areaMapImagesURL);
		const validAreaMapImagesURL = images.filter((mapImage) => mapImage[0] && mapImage[1]);
		console.log(validAreaMapImagesURL, Object.fromEntries(validAreaMapImagesURL));
		localStorage.setItem(
			'area-map-urls',
			JSON.stringify(Object.fromEntries(validAreaMapImagesURL))
		);
	}

	$effect(() => {
		// if the last area map image url is filled out, make another one
		const images = Object.entries(areaMapImagesURL);
		const validAreaMapImagesURL = images.filter((mapImage) => mapImage[0] && mapImage[1]);
		if (images.length === validAreaMapImagesURL.length) {
			const newElementNumber = validAreaMapImagesURL.length;
			const newElement = {
				[areaIsMultipleFloors ? newElementNumber : `Sub-area ${newElementNumber}`]: ''
			};
			areaMapImagesURL = { ...Object.fromEntries(validAreaMapImagesURL), ...newElement };
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
</form>

{#if Object.entries(areaMapImagesURL).filter((a) => a[0] && a[1]).length !== 0}
	<div class="max-w-2/3 flex flex-col items-start">
		<h2>Area Map Preview</h2>
		<AreaMap mapImageLabel={areaMapImagesURL[0]} mapImageURL={areaMapImagesURL[0]} />
		<a class="button" href="/input-locations" onclick={saveImage}>
			Input locations to test this area
		</a>
	</div>
{/if}
