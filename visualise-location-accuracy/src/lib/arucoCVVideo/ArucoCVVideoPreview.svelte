<script lang="ts">
	import { arucoVideoElement, arucoVideoSource } from './';
	import { createPlayer } from '$lib/test/playbackTimes';

	let { player }: { player: ReturnType<typeof createPlayer> } = $props();

	let { currentPlayingTimeSeconds } = player;
</script>

{#if $arucoVideoSource}
	<video
		bind:this={$arucoVideoElement}
		class="w-full"
		muted
		autoplay
		src={$arucoVideoSource}
		bind:currentTime={$currentPlayingTimeSeconds}
	></video>
{:else}
	<!-- THIS VIDEO DOESN'T SHOW UP ON PAGE BUT IS USED FOR SIMULATING TIME (VIDEO TIME = test time) -->
	<!-- ONLY WORKS WHEN VIDEO TIME > TEST TIME -->
	<video
		bind:this={$arucoVideoElement}
		class="pointer-events-none invisible w-full"
		muted
		autoplay
		src="/long-video-for-time-simulation.webm"
		bind:currentTime={$currentPlayingTimeSeconds}
	></video>
{/if}
