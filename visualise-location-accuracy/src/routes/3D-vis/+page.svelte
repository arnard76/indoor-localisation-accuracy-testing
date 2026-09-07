<script lang="ts">
	import { goto } from '$app/navigation';
	import ArucoCVVideoPreview from '$lib/arucoCVVideo/ArucoCVVideoPreview.svelte';
	import MapForWiFinderTest from '$lib/areaMap/MapForAccuracyTest.svelte';
	import TestControls from '$lib/test/TestControls.svelte';
	import TestResults from '$lib/test/TestResults.svelte';
	import { mapImageUrls } from '$lib/areaMap/area';
	import { createPlayer } from '$lib/test/playbackTimes';
	import { positions } from '$lib/locations/locationsData';
	import { createAccuracyCalculator } from '$lib/test/positionAccuracy';
	import { resolve } from '$app/paths';

	$effect(() => {
		if (Object.keys($mapImageUrls).length === 0) {
			goto(resolve('/change-map'));
			return;
		}
		// if (!$locations.aruco || !$locations.wifinder) goto('/input-locations');
	});

	const accuracyCalculator = createAccuracyCalculator();
	const player = createPlayer(accuracyCalculator);
	// accuracyCalculator.testNewSet('goal', 'cv');
</script>

<main class="flex h-screen flex-col justify-between overflow-hidden bg-green-400">
	<div class="flex w-full flex-1 gap-2 overflow-y-auto">
		<div class="flex w-full flex-col">
			<MapForWiFinderTest {player} {accuracyCalculator} />
			<ArucoCVVideoPreview {player} />
		</div>
		<div class="flex h-fit w-full max-w-1/2 flex-col gap-2">
			<TestResults {player} {accuracyCalculator} />
		</div>
	</div>

	<TestControls {player} {accuracyCalculator} />
</main>
