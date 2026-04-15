import { nullLocation, type LocationReading } from '$lib/locations/format';
import dayjs from 'dayjs';
import { derived, get, writable } from 'svelte/store';
import { locations, type LocationTypes } from '../locations/locationsData';

export function createPlayer() {
	const currentPlayingTimeSeconds = writable(0);

	const fullData = derived(
		[currentPlayingTimeSeconds, locations],
		([$currentPlayingTimeSeconds, $locations]) => {
			if (Object.keys($locations).length === 0) throw Error("locations aren't defined");

			const startTimeForTestPreview = Object.values($locations)
				.map((locationReadings) => dayjs(locationReadings.at(0)?.timestamp))
				.sort((a, b) => (a.isAfter(b) ? -1 : 1))
				.at(0);

			const endTimeForTestPreview = Object.values($locations)
				.map((locationReadings) => dayjs(locationReadings.at(-1)?.timestamp))
				.sort((a, b) => (a.isBefore(b) ? -1 : 1))
				.at(0);

			const currentPlayingTimeMilliseconds = Math.round($currentPlayingTimeSeconds * 1000);
			const currentPlayingTimestamp = startTimeForTestPreview?.add(currentPlayingTimeMilliseconds);

			const currentLocations: Record<LocationTypes, LocationReading> = {
				aruco: { ...nullLocation, timestamp: currentPlayingTimestamp || '' },
				wifinder: { ...nullLocation, timestamp: currentPlayingTimestamp || '' }
			};

			Object.entries($locations).forEach(([groupName, locationsInGroup]) => {
				currentLocations[groupName as LocationTypes] = locationsInGroup.findLast(({ timestamp }) =>
					dayjs(timestamp).isBefore(currentPlayingTimestamp)
				)! || { x: NaN, y: NaN };
			});

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
			};
		},
		{
			currentPlayingTimeSeconds: 0,
			currentPlayingTimeMilliseconds: 0,
			startTimeForTestPreview: dayjs(),
			endTimeForTestPreview: dayjs(),
			currentPlayingTimestamp: dayjs(),
			totalPlayingTimeMilliseconds: 0,
			currentLocations: {} as Record<LocationTypes, LocationReading>
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
