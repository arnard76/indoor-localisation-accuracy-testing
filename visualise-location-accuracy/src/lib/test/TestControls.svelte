<script lang="ts">
	import dayjs from 'dayjs';
	import PlaybackTest from '$lib/test/PlaybackTest.svelte';
	import type { createPlayer } from './playbackTimes';
	import { positions } from '$lib/locations/locationsData';
	import { findAccuracyFor, type createAccuracyCalculator } from './positionAccuracy';
	import { downloadSomething } from '$lib/testArtifacts/util';
	import Menu from '$lib/ui/Menu.svelte';
	import Icon from '@iconify/svelte';

	let {
		player,
		accuracyCalculator
	}: {
		player: ReturnType<typeof createPlayer>;
		accuracyCalculator: ReturnType<typeof createAccuracyCalculator>;
	} = $props();

	let idealSet = $state('');
	let setToMeasure = $state('');
	let accuracy = $derived(findAccuracyFor($accuracyCalculator, idealSet, setToMeasure));

	function downloadTestResult() {
		downloadSomething(
			'text/json',
			'utf-8',
			`${dayjs($positions['wifinder'][0].timestamp).toString()}.json`,
			encodeURIComponent(
				JSON.stringify({
					locationsToMeasure: $positions[setToMeasure],
					accuracyOfLocations: accuracy?.diffs,
					averageWifinderAccuracy: accuracy?.average
				})
			)
		);
	}
</script>

<div class="flex w-full items-center gap-4 bg-blue-400 p-2">
	<div class="flex flex-col items-start">
		<Menu>
			{#snippet menuPreview()}
				<button>
					<Icon icon="tabler:dots-vertical" />
				</button>
			{/snippet}

			<div class="mb-12 rounded-xl bg-white p-4">
				<a class="button" href="/change-map">Change Map</a>
				<a class="button" href="/create-locations">Create Locations</a>
				<a class="button" href="/format-locations">Format Locations</a>
				<a class="button" href="/input-locations">Change Locations</a>
				<button onclick={downloadTestResult}>Export Results</button>
			</div>
		</Menu>
	</div>
	<PlaybackTest {player} />
</div>
