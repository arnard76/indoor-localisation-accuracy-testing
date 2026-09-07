/* eslint-disable @typescript-eslint/no-explicit-any */

import { writable } from 'svelte/store';
import { sortReadings, type LocationReading, type PositionReading } from './format';

export function addToStoredLocations(name: string, data: any) {
	const storedLocations = localStorage.getItem('locations') || '{}';
	const added = { ...JSON.parse(storedLocations), [name]: data };
	localStorage.setItem('locations', JSON.stringify(added));
}

export function removeFromStoredLocations(name: string) {
	const storedLocations = localStorage.getItem('locations') || '{}';
	const removed = { ...JSON.parse(storedLocations) };
	delete removed[name];
	localStorage.setItem('locations', JSON.stringify(removed));
}

export function useStoredLocations() {
	const storedLocations = localStorage.getItem('locations');
	positions.set(
		Object.fromEntries(
			Object.entries(storedLocations ? JSON.parse(storedLocations) : {}).map(
				([name, locations]) => {
					return [name, sortReadings(locations as any)];
				}
			)
		)
	);
}

// TODO: find a way to get the start time of the video
export const positions = writable<Record<string, PositionReading[]>>({});
