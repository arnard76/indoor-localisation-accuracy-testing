<script lang="ts">
	import { goto } from '$app/navigation';
	import ArucoCVVideoPreview from '$lib/arucoCVVideo/ArucoCVVideoPreview.svelte';
	import MapForWiFinderTest from '$lib/areaMap/MapForAccuracyTest.svelte';
	import TestControls from '$lib/test/TestControls.svelte';
	import TestResults from '$lib/test/TestResults.svelte';
	import { mapImageUrls } from '$lib/areaMap/area';
	import { createPlayer } from '$lib/test/playbackTimes';
	import { locations } from '$lib/locations/locationsData';
	import { createAccuracyCalculator } from '$lib/test/positionAccuracy';
	import Icon from '@iconify/svelte';
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
	accuracyCalculator.testNewSet('goal', 'cv');
	accuracyCalculator.testNewSet('odom', 'goal');
	accuracyCalculator.testNewSet('odom', 'cv');

	let setToMeasure = $state('');
	let idealSet = $state('');
</script>

<main class="flex h-screen flex-col justify-between overflow-hidden bg-green-400">
	<!-- {#each $accuracyCalculator as comparison (comparison.idealSet + comparison.setToMeasure)}
		<p>Testing {comparison.setToMeasure} using {comparison.idealSet}</p>
	{/each} -->

	<!-- <label>
		Ideal locations

		<select bind:value={idealSet}>
			{#each Object.keys($locations) as setName (setName)}
				<option value={setName}>{setName}</option>
			{/each}
		</select>
	</label>

	<label>
		Locations to measure

		<select bind:value={setToMeasure}>
			{#each Object.keys($locations) as setName (setName)}
				<option value={setName}>{setName}</option>
			{/each}
		</select>
	</label>
	<button
		onclick={() =>
			setToMeasure.length &&
			idealSet.length &&
			accuracyCalculator.testNewSet(setToMeasure, idealSet)}><Icon icon="tabler:plus" /></button
	> -->

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
