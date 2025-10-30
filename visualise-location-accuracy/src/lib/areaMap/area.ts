import { writable } from 'svelte/store';

export const mapImageUrls = writable<{ [subAreaName: string]: string }>({});

export function useStoredMap() {
	const storedMap = localStorage.getItem('area-map-urls');
	if (!storedMap) return;
	mapImageUrls.set(JSON.parse(storedMap));
}
