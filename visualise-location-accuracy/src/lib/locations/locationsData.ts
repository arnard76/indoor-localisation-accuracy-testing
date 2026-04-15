/* eslint-disable @typescript-eslint/no-explicit-any */

import { derived, writable } from 'svelte/store';
import {
	sortLocationReadings,
	type ImportableLocationReading,
	type LocationReading
} from './format';
import { pixelsToMetresScale } from './metreScale';

export function cleanLocationObject(location?: ImportableLocationReading): LocationReading {
	if (!location) return { timestamp: '', x: NaN, y: NaN };
	const x_in_metres = location.location[0];
	const y_in_metres = location.location[2];
	return {
		timestamp: location.timestamp,
		x: x_in_metres,
		y: y_in_metres
	};
}

export const arucoLocationDataRaw = writable<LocationReading[]>([]);
const wiFinderLocationDataRaw = writable<LocationReading[]>([]);

export function useStoredLocations() {
	const storeAruco = localStorage.getItem('aruco-locations');
	const transformedAruco = (storeAruco ? JSON.parse(storeAruco) : []).map(
		(reading: ImportableLocationReading) => cleanLocationObject(reading)
	);

	arucoLocationDataRaw.set(transformedAruco);
	const storeWifinder = localStorage.getItem('wifinder-locations');
	const transformedWifinder = (storeWifinder ? JSON.parse(storeWifinder) : []).map(
		({ x, y, timestamp }: any) => ({
			x: x * pixelsToMetresScale,
			y: y * pixelsToMetresScale,
			timestamp
		})
	);
	wiFinderLocationDataRaw.set(transformedWifinder);
}

// TODO: find a way to get the start time of the video

export type LocationTypes = 'aruco' | 'wifinder';

export const locations = derived(
	[arucoLocationDataRaw, wiFinderLocationDataRaw],
	([$arucoLocationDataRaw, $wifinderLocationDataRaw], set) =>
		set({
			aruco: sortLocationReadings($arucoLocationDataRaw),
			wifinder: sortLocationReadings($wifinderLocationDataRaw)
		}),
	{} as { [key in LocationTypes]: LocationReading[] }
);
