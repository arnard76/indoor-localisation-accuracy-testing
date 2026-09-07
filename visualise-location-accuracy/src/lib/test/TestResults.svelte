<script lang="ts">
	import DifferenceDistanceOverTimeChart from './DifferenceDistanceOverTimeChart.svelte';
	import DifferenceOrientationOverTimeChart from './DifferenceOrientationOverTimeChart.svelte';
	import type { createPlayer } from './playbackTimes';
	import { type createAccuracyCalculator } from './positionAccuracy';
	let {
		player,
		accuracyCalculator
	}: {
		player: ReturnType<typeof createPlayer>;
		accuracyCalculator: ReturnType<typeof createAccuracyCalculator>;
	} = $props();
</script>

{#each $accuracyCalculator as comparison (comparison.idealSet + comparison.setToMeasure)}
	<h3>
		<strong>{comparison.idealSet}/{comparison.setToMeasure}</strong><br /> average difference in
		distance (accuracy): {comparison.average}
		metres

		{#if comparison.orientationAverage !== undefined && !Number.isNaN(comparison.orientationAverage)}
			<br />
			average angle difference: {comparison.orientationAverage}°
		{/if}
	</h3>
	<DifferenceDistanceOverTimeChart
		{player}
		averageAccuracy={comparison.average}
		distanceDiffs={comparison.diffs}
	/>

	{#if comparison.orientationAverage !== undefined && !Number.isNaN(comparison.orientationAverage)}
		<DifferenceOrientationOverTimeChart
			{player}
			averageAccuracy={comparison.orientationAverage}
			orientationDiffs={comparison.diffs}
		/>
	{/if}
{/each}
