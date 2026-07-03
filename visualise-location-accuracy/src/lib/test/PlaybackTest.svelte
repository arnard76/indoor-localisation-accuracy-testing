<script lang="ts">
	import Icon from '@iconify/svelte';
	import { playing, playPauseMedia } from '$lib/arucoCVVideo';
	import type { FormEventHandler } from 'svelte/elements';
	import type { createPlayer } from './playbackTimes';

	let { player }: { player: ReturnType<typeof createPlayer> } = $props();

	let loopTest = $state(true);
	// let playTestinterval: NodeJS.Timeout | null = null;
	// let lastTime = dayjs();

	function formatMillisecondsToTime(ms: number) {
		const minutes = Math.floor(ms / 60000); // 1 minute = 60,000 milliseconds
		const seconds = Math.floor((ms % 60000) / 1000); // Remaining milliseconds after minutes, divided by 1000 for seconds
		const milliseconds = ms % 1000; // Remaining milliseconds after seconds

		// Pad with leading zeros for consistent formatting
		const formattedMinutes = String(minutes).padStart(2, '0');
		const formattedSeconds = String(seconds).padStart(2, '0');
		const formattedMilliseconds = String(milliseconds).padStart(3, '0');

		return `${formattedMinutes}:${formattedSeconds}.${formattedMilliseconds}`;
	}

	// $effect(() => {
	// 	if (!playing) {
	// 		if (playTestinterval) clearInterval(playTestinterval);
	// 		playTestinterval = null;
	// 		return;
	// 	}
	// 	lastTime = dayjs();
	// 	if (playTestinterval) {
	// 		clearInterval(playTestinterval);
	// 		playTestinterval = null;
	// 	}
	// 	playTestinterval = setInterval(
	// 		() => currentPlayingTimeMilliseconds.set(dayjs().diff(lastTime)),
	// 		50
	// 	);
	// });

	$effect(() => {
		if ($player.currentPlayingTimeMilliseconds > $player.totalPlayingTimeMilliseconds) {
			player.resetTime();
			if (!loopTest) {
				playing.set(false);
				playPauseMedia();
			} else {
				playing.set(true);
			}
		}
	});

	const inputNewPlayingTime: FormEventHandler<HTMLInputElement> = (e) => {
		player.setTime(parseInt(e.currentTarget.value) / 1000);
	};

	// TODO: when no loop, the test should pause when it gets to the end
	// TODO: allow adjusting test time using the range input
</script>

<div class="flex w-full flex-col items-center gap-4">
	<input
		type="range"
		class="w-full min-w-96"
		value={$player.currentPlayingTimeMilliseconds}
		oninput={inputNewPlayingTime}
		max={$player.totalPlayingTimeMilliseconds}
	/>
	<div class="flex w-full items-center justify-between gap-4 px-4">
		<button
			style="padding: 5px 10px"
			class:active-button={loopTest}
			onclick={() => (loopTest = !loopTest)}
		>
			<Icon icon="tabler:repeat" />
		</button>

		<div class="flex items-center gap-4 px-4">
			<button onclick={() => player.addTime(-1)}><Icon icon="tabler:skip-back" /> </button>
			<button class="active-button" onclick={playPauseMedia}>
				{#if $playing}
					<Icon icon="tabler:pause" />
				{:else}
					<Icon icon="tabler:play" />
				{/if}
			</button>
			<button onclick={() => player.addTime(1)}><Icon icon="tabler:skip-forward" /></button>
		</div>
		<p class="w-64">
			{formatMillisecondsToTime($player.currentPlayingTimeMilliseconds)} /
			{formatMillisecondsToTime($player.totalPlayingTimeMilliseconds)}
		</p>

		{#if $player.currentPlayingTimestamp}
			<p>
				{$player.currentPlayingTimestamp}
			</p>
		{/if}
	</div>
</div>

<style lang="postcss">
	@reference '../../app.css';

	button {
		@apply bg-transparent p-0;
	}

	button.active-button {
		@apply rounded-2xl bg-white px-6 py-4 text-black transition duration-500 hover:bg-green-200;
	}
</style>
