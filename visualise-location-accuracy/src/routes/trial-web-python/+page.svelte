<script lang="ts">
	import { useStoredTestInputs } from '$lib/test/testData';

	localStorage.removeItem('wifinder-locations');
	localStorage.removeItem('aruco-locations');
	localStorage.removeItem('aruco-video-url');

	let wifinderPhoneId = $state('');
	let arucoVideoMegaLink = $state('');

	let showExampleSection = $state(false);
	let status = $state<null | string>(null);
	async function onCheckInputs() {
		const logSessions = await getWifinderLogsFromPhoneId(wifinderPhoneId);
		console.log({ logSessions });
		if (arucoVideoMegaLink) {
			const linkToArucoLocations = await submitVideoToCalculateArucoCVLocations(arucoVideoMegaLink);
			console.log({ linkToArucoLocations });
		}
		if (!logSessions) return;

		if (logSessions.length === 1) {
		} else if (logSessions.length > 1) {
		} else {
		}

		showExampleSection = false;
		// saveTestInputsFromFiles(arucoTestJsonFile[0], wifinderJsonFile[0], arucoVideoURL);
	}

	async function getWifinderLogsFromPhoneId(phoneId: string) {
		const response = await fetch(
			`https://sheer-finch-arnard76-72e6944a.koyeb.app/application/wifinder-locations-logs-for-${wifinderPhoneId}`,
			{}
		);

		if (response.status !== 200) return;

		const logSessions = (await response.json()).packets;

		if (!logSessions || logSessions.length === 0) return;

		return logSessions;
	}

	async function submitVideoToCalculateArucoCVLocations(megaLink: string) {
		const response = await fetch(`http://127.0.0.1:8000`, {
			method: 'post',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({
				megaLink,
				videoStartDateTime: 'started 5s ago',
				camera: { rotation: [0, 0, 0], location: [1, 2, 3], name: 'Arnav phone' }
			})
		});

		if (response.status !== 200) return;

		const linkToArucoLocations = (await response.json()).linkToArucoLocations;

		return linkToArucoLocations;
	}

	// async function saveTestInputsFromFiles(
	// 	aruco: File,
	// 	wifinder: File,
	// 	arucoVideoURL: string | null
	// ) {
	// 	localStorage.setItem('aruco-locations', await aruco.text());
	// 	localStorage.setItem('wifinder-locations', await wifinder.text());
	// 	if (arucoVideoURL) localStorage.setItem('aruco-video-url', arucoVideoURL);
	// 	useStoredTestInputs();
	// 	status = `Saved both location files in your browser.`;
	// }
</script>

<svelte:head>
	<!-- This script tag bootstraps PyScript -->
	<script type="module" src="https://pyscript.net/releases/2025.8.1/core.js"></script>
	<script type="py" src="./aruco-cv-locator/main.py" config="./pyscript.toml"></script>
</svelte:head>

<form>
	<label>
		Phone ID
		<input id="phone-id" type="text" bind:value={wifinderPhoneId} />
		<span>WiFinder Logs (including predicted locations and WiFi RSSI scans)</span>
	</label>
	<label>
		Mega.nz link for Aruco CV Video
		<input type="text" id="mega-video-link" bind:value={arucoVideoMegaLink} />
	</label>

	<button type="submit" onclick={onCheckInputs}>Get Test Data</button>

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
