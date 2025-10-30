<!-- export report feature -->

<script lang="ts">
	import { averageWifinderAccuracy } from './wifinderAccuracy';
	import WiFinderAccuracyOverTimeChart from './WiFinderAccuracyOverTimeChart.svelte';
</script>

<h3>Average Accuracy: {$averageWifinderAccuracy} metres</h3>

<WiFinderAccuracyOverTimeChart />
