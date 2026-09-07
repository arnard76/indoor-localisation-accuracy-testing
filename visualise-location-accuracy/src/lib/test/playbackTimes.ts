import { nullPosition, type PositionReading } from '$lib/locations/format';
import dayjs, { Dayjs } from 'dayjs';
import { derived, get, writable } from 'svelte/store';
import { positions } from '../locations/locationsData';
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

export function createPlayer(accuracyCalculator: ReturnType<typeof createAccuracyCalculator>) {
	const currentPlayingTimeSeconds = writable(0);

	const fullData = derived(
		[currentPlayingTimeSeconds, positions, accuracyCalculator],
		([$currentPlayingTimeSeconds, $positions, $accuracyCalculator]) => {
			if (Object.keys($positions).length === 0) throw Error("locations aren't defined");

			const startTimeForTestPreview = Object.values($positions)
				.map((locationReadings) => dayjs(locationReadings.at(0)?.timestamp))
				.sort((a, b) => (a.isAfter(b) ? 1 : -1))
				.at(0);

			const endTimeForTestPreview = Object.values($positions)
				.map((locationReadings) => dayjs(locationReadings.at(-1)?.timestamp))
				.sort((a, b) => (a.isBefore(b) ? 1 : -1))
				.at(0);

			const currentPlayingTimeMilliseconds = Math.round($currentPlayingTimeSeconds * 1000);
			const currentPlayingTimestamp = startTimeForTestPreview?.add(currentPlayingTimeMilliseconds);

			const currentPositions = Object.fromEntries(
				Object.entries($positions).map(([groupName, locationsInGroup]) => {
					const currentLocation = currentPlayingTimestamp
						? findCurrentObject(locationsInGroup, currentPlayingTimestamp) || {
								...nullPosition,
								timestamp: currentPlayingTimestamp
							}
						: { ...nullPosition, timestamp: '' };
					return [groupName, currentLocation];
				})
			);

			const totalPlayingTimeMilliseconds = dayjs(endTimeForTestPreview).diff(
				startTimeForTestPreview,
				'milliseconds'
			);

			return {
				currentPlayingTimeSeconds: get(currentPlayingTimeSeconds),
				currentPlayingTimeMilliseconds,
				startTimeForTestPreview,
				endTimeForTestPreview,
				currentPlayingTimestamp,
				totalPlayingTimeMilliseconds,
				currentPositions
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
			currentPositions: {} as Record<string, PositionReading>
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
