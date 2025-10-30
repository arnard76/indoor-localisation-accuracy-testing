<script lang="ts">
	import { mapImagePixelsToScreenPixelsScale, mapOnScreenWidth } from '$lib/locations/pixelScale';

	let {
		mapLocations = undefined,
		rawPosition = $bindable(),
		mapImageURL,
		mapImageLabel = 'Area Map Image'
	} = $props();

	function navigateByKeyboard(event: KeyboardEvent) {
		let key = event.key;

		if (key == 'w' || key == 'ArrowUp') {
			rawPosition.y -= 1;
		} else if (key == 's' || key === 'ArrowDown') {
			rawPosition.y += 1;
		}

		if (key == 'a' || key === 'ArrowLeft') {
			rawPosition.x -= 1;
		} else if (key == 'd' || key === 'ArrowRight') {
			rawPosition.x += 1;
		}
	}
</script>

<svelte:body onkeydown={navigateByKeyboard} />

<div class="area-map relative">
	{@render mapLocations?.()}

	<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
	<!-- svelte-ignore a11y_click_events_have_key_events -->
	<img
		bind:clientWidth={$mapOnScreenWidth}
		onclick={(event) => {
			rawPosition = {
				x: event.offsetX / $mapImagePixelsToScreenPixelsScale,
				y: event.offsetY / $mapImagePixelsToScreenPixelsScale
			};
		}}
		class="m-0 border-0 p-0"
		alt={mapImageLabel}
		src={mapImageURL}
	/>
</div>

<style>
	.area-map {
		--location-square-width: 10px;
	}
</style>
