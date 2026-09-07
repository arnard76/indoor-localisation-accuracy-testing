import { derived, writable } from 'svelte/store';

export const mapOnScreenWidth = writable(0);
const mapImagePixels = 1367;
export const mapImagePixelsToScreenPixelsScale = derived(
	mapOnScreenWidth,
	($mapOnScreenWidth) => $mapOnScreenWidth / mapImagePixels
);
