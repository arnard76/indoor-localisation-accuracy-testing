<script lang="ts">
	import type { createPlayer } from './playbackTimes';
	import { averageWifinderAccuracy } from './positionAccuracy';
	import WiFinderAccuracyOverTimeChart from './WiFinderAccuracyOverTimeChart.svelte';
	let { player }: { player: ReturnType<typeof createPlayer> } = $props();
</script>

<h3>Average Accuracy: {$averageWifinderAccuracy} metres</h3>

<WiFinderAccuracyOverTimeChart {player} />
