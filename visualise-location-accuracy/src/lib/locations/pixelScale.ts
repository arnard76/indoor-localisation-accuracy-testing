import { derived, writable } from 'svelte/store';

export const mapOnScreenWidth = writable(0);
const mapImagePixels = 1536;
export const mapImagePixelsToScreenPixelsScale = derived(
	mapOnScreenWidth,
	($mapOnScreenWidth) => $mapOnScreenWidth / mapImagePixels
);
