import { nullLocation, type LocationReading } from '$lib/locations/format';
import dayjs, { Dayjs } from 'dayjs';
import { derived, get, writable } from 'svelte/store';
import { locations } from '../locations/locationsData';
import type { createAccuracyCalculator } from './positionAccuracy';

export function findCurrentObject<Type extends { timestamp: Dayjs | string }>(
	objects: Type[],
	currentPlayingTimestamp: Dayjs
): Type | undefined {
	return objects.findLast(
		({ timestamp }) =>
			dayjs(timestamp).isSame(currentPlayingTimestamp) ||
			dayjs(timestamp).isBefore(currentPlayingTimestamp)
	);
}

export function findCurrentLocation(
	locations: LocationReading[],
	currentPlayingTimestamp: Dayjs
): LocationReading {
	return (
		findCurrentObject(locations, currentPlayingTimestamp) || {
			...nullLocation,
			timestamp: currentPlayingTimestamp
		}
	);
}

export function createPlayer(accuracyCalculator: ReturnType<typeof createAccuracyCalculator>) {
	const currentPlayingTimeSeconds = writable(0);

	const fullData = derived(
		[currentPlayingTimeSeconds, locations, accuracyCalculator],
		([$currentPlayingTimeSeconds, $locations, $accuracyCalculator]) => {
			if (Object.keys($locations).length === 0) throw Error("locations aren't defined");

			const startTimeForTestPreview = Object.values($locations)
				.map((locationReadings) => dayjs(locationReadings.at(0)?.timestamp))
				.sort((a, b) => (a.isAfter(b) ? 1 : -1))
				.at(0);

			const endTimeForTestPreview = Object.values($locations)
				.map((locationReadings) => dayjs(locationReadings.at(-1)?.timestamp))
				.sort((a, b) => (a.isBefore(b) ? 1 : -1))
				.at(0);

			const currentPlayingTimeMilliseconds = Math.round($currentPlayingTimeSeconds * 1000);
			const currentPlayingTimestamp = startTimeForTestPreview?.add(currentPlayingTimeMilliseconds);

			const currentLocations: Record<string, LocationReading> = Object.fromEntries(
				Object.entries($locations).map(([groupName, locationsInGroup]) => {
					const currentLocation = currentPlayingTimestamp
						? findCurrentLocation(locationsInGroup, currentPlayingTimestamp)
						: { ...nullLocation, timestamp: '' };
					return [groupName, currentLocation];
				})
			);

			return {
				currentPlayingTimeSeconds: get(currentPlayingTimeSeconds),
				currentPlayingTimeMilliseconds,
				startTimeForTestPreview,
				endTimeForTestPreview,
				currentPlayingTimestamp,
				totalPlayingTimeMilliseconds: dayjs(endTimeForTestPreview).diff(
					startTimeForTestPreview,
					'milliseconds'
				),
				currentLocations
				// currentAccuracy
			};
		},
		{
			currentPlayingTimeSeconds: 0,
			currentPlayingTimeMilliseconds: 0,
			startTimeForTestPreview: dayjs(),
			endTimeForTestPreview: dayjs(),
			currentPlayingTimestamp: dayjs(),
			totalPlayingTimeMilliseconds: 0,
			currentLocations: {} as Record<string, LocationReading>
		}
	);

	return {
		subscribe: fullData.subscribe,
		currentPlayingTimeSeconds,
		setTime(timeInSeconds: number) {
			currentPlayingTimeSeconds.set(timeInSeconds);
		},
		resetTime() {
			currentPlayingTimeSeconds.set(0);
		},
		addTime(timeInSeconds: number) {
			currentPlayingTimeSeconds.update((c) => c + timeInSeconds);
		}
	};
}
