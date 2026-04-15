<script lang="ts">
	import { goto } from '$app/navigation';
	import ArucoCVVideoPreview from '$lib/arucoCVVideo/ArucoCVVideoPreview.svelte';
	import MapForWiFinderTest from '$lib/areaMap/MapForAccuracyTest.svelte';
	import TestControls from '$lib/test/TestControls.svelte';
	import TestResults from '$lib/test/TestResults.svelte';
	import { mapImageUrls } from '$lib/areaMap/area';
	import { createPlayer } from '$lib/test/playbackTimes';
	import { locations } from '$lib/locations/locationsData';

	$effect(() => {
		if (Object.keys($mapImageUrls).length === 0) {
			goto('/change-map');
			return;
		}
		if (!$locations.aruco || !$locations.wifinder) goto('/input-locations');
	});

	const player = createPlayer();
</script>

<main class="flex h-screen flex-col justify-between overflow-hidden bg-green-400">
	<div class="flex w-full flex-1 gap-2 overflow-y-auto">
		<div class="flex w-full">
			<MapForWiFinderTest {player} />
		</div>
		<div class="flex w-full max-w-1/2 flex-col gap-2">
			<TestResults {player} />
			<ArucoCVVideoPreview {player} />
		</div>
	</div>

	<TestControls {player} />
</main>
