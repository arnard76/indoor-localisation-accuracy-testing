<script lang="ts">
	import dayjs from 'dayjs';
	import { wiFinderLocationData } from '$lib/locations/locationsData';
	import PlaybackTest from '$lib/test/PlaybackTest.svelte';
	import { averageWifinderAccuracy, wiFinderLocationAccuracy } from './wifinderAccuracy';

	function downloadTestResult() {
		const testResultsData =
			'data:text/json;charset=utf-8,' +
			encodeURIComponent(
				JSON.stringify({
					wifinderLocations: $wiFinderLocationData,
					accuracyOfLocations: $wiFinderLocationAccuracy,
					averageWifinderAccuracy: $averageWifinderAccuracy
				})
			);
		const downloadEl = document.createElement('a');
		downloadEl.setAttribute('href', testResultsData);
		downloadEl.setAttribute(
			'download',
			`${dayjs($wiFinderLocationData[0].timestamp).toString()}.json`
		);
		downloadEl.click();
	}
</script>

<div class="flex w-full items-center gap-4 bg-blue-400 p-2">
	<div class="flex flex-col items-start">
		<a class="button" href="/change-map">Change Map</a>
		<a class="button" href="/input-locations">Change Locations</a>
		<button onclick={downloadTestResult}>Export Results</button>
	</div>
	<PlaybackTest />
</div>
