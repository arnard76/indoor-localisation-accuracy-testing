/* eslint-disable @typescript-eslint/no-explicit-any */

import { derived, writable } from 'svelte/store';
import { sortLocationReadings, type LocationReading } from './format';
import { pixelsToMetresScale } from './metreScale';

export const arucoLocationDataRaw = writable<LocationReading[]>([]);
const wiFinderLocationDataRaw = writable<LocationReading[]>([]);

export function useStoredLocations() {
	const storeAruco = localStorage.getItem('aruco-locations');
	arucoLocationDataRaw.set(storeAruco ? JSON.parse(storeAruco) : []);
	const storeWifinder = localStorage.getItem('wifinder-locations');
	const transformedWifinder = (storeWifinder ? JSON.parse(storeWifinder) : []).map(
		({ x, y, timestamp }: any) => ({
			location: [x * pixelsToMetresScale, 0, y * pixelsToMetresScale],
			timestamp
		})
	);
	wiFinderLocationDataRaw.set(transformedWifinder);
}

// TODO: find a way to get the start time of the video
export const arucoLocationData = derived(arucoLocationDataRaw, ($arucoLocationDataRaw) =>
	sortLocationReadings($arucoLocationDataRaw)
);

export const wiFinderLocationData = derived(wiFinderLocationDataRaw, ($wifinderLocationDataRaw) =>
	sortLocationReadings($wifinderLocationDataRaw)
);
