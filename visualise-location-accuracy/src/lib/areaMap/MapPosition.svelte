<script lang="ts">
	import {
		convertLocationFromFormat,
		displayLocation,
		scaleLocation,
		type LocationUnits,
		type MapLocation
	} from '$lib/locations/format';
	import { mapImagePixelsToScreenPixelsScale } from '$lib/locations/pixelScale';
	import Icon from '@iconify/svelte';

	// origin & position both need to be inputUnits
	let {
		origin,
		position,
		colour = 'chocolate',
		inputUnit,
		displayUnit = 'metres' as LocationUnits,
		name = '',
		tooltipClasses = '',
		tooltipStyle = '',
		orientation,
		fixed = false
	}: {
		origin: MapLocation;
		position: MapLocation;
		inputUnit: LocationUnits;
		displayUnit?: LocationUnits;
		colour?: string;
		name?: string;
		tooltipClasses?: string;
		tooltipStyle?: string;
		orientation?: number;
		fixed?: boolean;
	} = $props();

	const positionFromOrigin = $derived({
		x: position.x + origin.x,
		y: position.y + origin.y,
		z: position.z + origin.z
	});
	const locationToShow = $derived(
		convertLocationFromFormat(positionFromOrigin, inputUnit, displayUnit)
	);
	const screenPixelLocation = $derived(
		scaleLocation(
			convertLocationFromFormat(positionFromOrigin, inputUnit, 'pixels'),
			$mapImagePixelsToScreenPixelsScale
		)
	);
</script>

{#if name !== ''}
	<p
		class="tooltip {tooltipClasses}"
		style="background-color: {colour};transform: translate({screenPixelLocation.x}px, calc({screenPixelLocation.y}px - 50% - (3 * var(--location-square-width))));{tooltipStyle}"
	>
		{name} | {displayLocation(locationToShow, displayUnit)}
	</p>
{/if}

{#if fixed === true}
	<div
		class="location_square flex items-center justify-center"
		style="color: {colour}; transform: translate(calc({screenPixelLocation.x}px - 50%), calc({screenPixelLocation.y}px - 50%)) {orientation !==
		undefined
			? `rotate(${orientation}deg)`
			: ''};"
	>
		<Icon icon="tabler:x" />
	</div>
{:else}
	<div
		class="location_square"
		style="background-color: {colour}; transform: translate(calc({screenPixelLocation.x}px - 50%), calc({screenPixelLocation.y}px - 50%)) {orientation !==
		undefined
			? `rotate(${orientation}deg)`
			: ''};"
	>
		{#if orientation !== undefined}
			<Icon
				icon="tabler:arrow-narrow-right-dashed"
				class="absolute top-1/2 left-full pl-1.5 "
				style="transform: translate(-50%, -50%);"
			/>
		{/if}
	</div>
{/if}

<style lang="postcss">
	.location_square {
		position: absolute;
		width: var(--location-square-width);
		height: var(--location-square-width);
		z-index: 2;
		padding: 0;
		margin: 0;
		left: 0px;
		top: 0px;
	}

	.tooltip {
		position: absolute;
		background-color: chocolate;
		padding: 4px 8px;
		border-radius: 4px;
		z-index: 2;
		font-size: 0.8em;

		font-weight: 600;
	}
</style>
