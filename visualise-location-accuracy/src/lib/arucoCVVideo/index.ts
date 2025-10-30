import { get, writable } from 'svelte/store';

export const arucoVideoSource = writable<null | string>();
export const arucoVideoElement = writable<null | HTMLVideoElement>();
export const playing = writable(true);

export function playPauseMedia() {
	const $arucoVideoElement = get(arucoVideoElement);

	if (!$arucoVideoElement) return;

	if ($arucoVideoElement.paused) {
		playing.set(true);
		$arucoVideoElement.play();
	} else {
		playing.set(false);
		$arucoVideoElement.pause();
	}
}
