<script lang="ts">
	import { displayLocation } from '$lib/locations/format';

	let {
		position,
		displayedPosition = position,
		colour = 'chocolate',
		unit,
		name = '',
		tooltipClasses = '',
		tooltipStyle = ''
	} = $props();
</script>

{#if name !== ''}
	<p
		class="tooltip {tooltipClasses}"
		style="background-color: {colour};transform: translate({position.x}px, calc({position.y}px - 50% - (3 * var(--location-square-width))));{tooltipStyle}"
	>
		{name} | {displayLocation(displayedPosition, unit)}
	</p>
{/if}

<p
	class="location_square"
	style="background-color: {colour}; transform: translate(calc({position.x}px - 50%), calc({position.y}px - 50%));"
></p>

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
