<script lang="ts">
	import { goto } from '$app/navigation';
	import ArucoCVVideoPreview from '$lib/arucoCVVideo/ArucoCVVideoPreview.svelte';
	import MapForWiFinderTest from '$lib/areaMap/MapForAccuracyTest.svelte';
	import TestControls from '$lib/test/TestControls.svelte';
	import TestResults from '$lib/test/TestResults.svelte';
	import { arucoLocationData, wiFinderLocationData } from '$lib/locations/locationsData';
	import { mapImageUrls } from '$lib/areaMap/area';

	$effect(() => {
		if (Object.keys($mapImageUrls).length === 0) {
			goto('/change-map');
			return;
		}
		if (!$arucoLocationData.length || !$wiFinderLocationData.length) goto('/input-locations');
	});
</script>

<main class="flex h-screen flex-col justify-between overflow-hidden bg-green-400">
	<div class="flex w-full flex-1 gap-2 overflow-y-auto">
		<div class="flex w-full">
			<MapForWiFinderTest />
		</div>
		<div class="max-w-1/2 flex w-full flex-col gap-2">
			<TestResults />
			<ArucoCVVideoPreview />
		</div>
	</div>

	<TestControls />
</main>
