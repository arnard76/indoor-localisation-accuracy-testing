<script lang="ts">
	import { arucoVideoSource } from '$lib/arucoCVVideo';
	import {
		addToStoredLocations,
		locations,
		removeFromStoredLocations,
		useStoredLocations
	} from '$lib/locations/locationsData';
	import { useStoredTestVideo } from '$lib/test/testData';
	import Icon from '@iconify/svelte';

	let showExampleSection = $state(false);
	let status = $state<null | string>(null);

	async function saveTestInputsFromFiles(name: string, file: File) {
		addToStoredLocations(name, JSON.parse(await file.text()));
		useStoredLocations();
		status = `Saved new location file in your browser.`;
		newLocationSet = { name: '', file: null };
	}

	let locationSets: { name: string; file: File | null }[] = $derived(
		Object.keys($locations).map((a) => ({ name: a, file: null }))
	);
	let newLocationSet: { name: string; file: File | null } = $state({ name: '', file: null });
</script>

<form>
	<h2>Existing sets</h2>
	{#each locationSets as locationSet (locationSet.name)}
		<div class="flex items-center gap-2">
			<p>{locationSet.name}</p>
			<button
				class="p-1!"
				onclick={() => {
					removeFromStoredLocations(locationSet.name);
					useStoredLocations();
				}}><Icon icon="tabler:trash" /></button
			>
		</div>
	{/each}
	<input type="text" bind:value={newLocationSet['name']} placeholder="Name" />
	<input
		type="file"
		onchange={(e) => {
			if (!e.currentTarget.files) return;
			newLocationSet['file'] = e.currentTarget.files[0];
		}}
		accept=".json"
	/>
	<button
		onclick={() => {
			if (!newLocationSet.file) return;
			locationSets.push(newLocationSet);
			saveTestInputsFromFiles(newLocationSet.name, newLocationSet.file);
		}}><Icon icon="tabler:plus" /></button
	>

	<label>
		Video URL of Movements (optional)
		<input
			type="text"
			onchange={(e) => {
				const arucoVideoURL = e.currentTarget.value;
				localStorage.setItem('aruco-video-url', arucoVideoURL);
				useStoredTestVideo();
			}}
		/>

		{#if $arucoVideoSource}
			<video class="w-full" muted autoplay src={$arucoVideoSource}></video>
		{/if}
	</label>

	<div>
		<button onclick={() => (showExampleSection = !showExampleSection)}>Example files</button>
		{#if showExampleSection}
			<section class="flex flex-col">
				<a href="/example-test-inputs/wifinder-logs.json" target="_blank">WiFinder locations logs</a
				>
				<a href="/example-test-inputs/aruco-test-locations.json" target="_blank"
					>Aruco Test Locations</a
				>
				<p>/example-test-inputs/aruco-video.webm</p>
			</section>
		{/if}
	</div>
</form>

{#if status}
	<div class="flex flex-col items-start">
		<p>{status}</p>
		<a href="/" class="button">Start test</a>
	</div>
{/if}
