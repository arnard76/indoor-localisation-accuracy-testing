<script lang="ts">
	import { useStoredTestInputs } from '$lib/test/testData';

	localStorage.removeItem('wifinder-locations');
	localStorage.removeItem('aruco-locations');
	localStorage.removeItem('aruco-video-url');

	let wifinderJsonFile = $state<null | FileList>(null);
	let arucoTestJsonFile = $state<null | FileList>(null);
	let arucoVideoURL = $state<null | string>(null);

	let showExampleSection = $state(false);
	let status = $state<null | string>(null);
	$effect(() => {
		if (
			arucoTestJsonFile === null ||
			wifinderJsonFile === null ||
			arucoTestJsonFile.length === 0 ||
			wifinderJsonFile.length === 0
		)
			return;

		showExampleSection = false;
		saveTestInputsFromFiles(arucoTestJsonFile[0], wifinderJsonFile[0], arucoVideoURL);
	});

	async function saveTestInputsFromFiles(
		aruco: File,
		wifinder: File,
		arucoVideoURL: string | null
	) {
		localStorage.setItem('aruco-locations', await aruco.text());
		localStorage.setItem('wifinder-locations', await wifinder.text());
		if (arucoVideoURL) localStorage.setItem('aruco-video-url', arucoVideoURL);
		useStoredTestInputs();
		status = `Saved both location files in your browser.`;
	}
</script>

<form>
	<label>
		Actual Location Logs (from localisation app)
		<input type="file" bind:files={wifinderJsonFile} accept=".json" />
	</label>
	<label>
		Aruco Test Locations
		<input type="file" bind:files={arucoTestJsonFile} accept=".json" />
	</label>

	<label>
		Aruco Video URL (optional)
		<input type="text" bind:value={arucoVideoURL} />
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
	<p>{status}</p>
	<a href="/" class="button">Start test</a>
{/if}
