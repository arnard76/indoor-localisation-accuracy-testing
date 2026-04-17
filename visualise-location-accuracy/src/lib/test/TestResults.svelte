<script lang="ts">
	import DifferenceDistanceOverTimeChart from './DifferenceDistanceOverTimeChart.svelte';
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
		{comparison.idealSet}/{comparison.setToMeasure} average difference in distance (accuracy): {comparison.average}
		metres
	</h3>
	<DifferenceDistanceOverTimeChart
		{player}
		averageAccuracy={comparison.average}
		distanceDiffs={comparison.diffs}
	/>
{/each}
