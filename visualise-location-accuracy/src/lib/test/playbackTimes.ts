import dayjs from 'dayjs';
import { arucoLocationData, wiFinderLocationData } from '../locations/locationsData';
import { derived, writable } from 'svelte/store';

export const currentPlayingTimeSeconds = writable(0);
export const currentPlayingTimeMilliseconds = derived(
	currentPlayingTimeSeconds,
	($currentPlayingTimeSeconds) => Math.floor($currentPlayingTimeSeconds * 1000)
);

export function addTime(timeInSeconds: number) {
	currentPlayingTimeSeconds.update((c) => c + timeInSeconds);
}

export const startTimeForTestPreview = derived(
	[wiFinderLocationData, arucoLocationData],
	([$wifinderLocationData, $arucoLocationData]) => {
		if ($arucoLocationData.length === 0 || $wifinderLocationData.length === 0) return null;

		const firstArucoReadingTime = dayjs($arucoLocationData[0].timestamp);
		const firstWiFinderReadingTime = dayjs($wifinderLocationData[0].timestamp);
		const startTimeForTestPreview = firstArucoReadingTime.isBefore(firstWiFinderReadingTime)
			? firstArucoReadingTime
			: firstWiFinderReadingTime;

		return startTimeForTestPreview;
	},
	null
);

export const currentPlayingTimestamp = derived(
	[currentPlayingTimeMilliseconds, startTimeForTestPreview],
	([$currentPlayingTimeMilliseconds, $startTimeForTestPreview]) =>
		$startTimeForTestPreview?.add($currentPlayingTimeMilliseconds)
);

export const endTimeForTestPreview = derived(
	[wiFinderLocationData, arucoLocationData],
	([$wifinderLocationData, $arucoLocationData]) => {
		if ($arucoLocationData.length === 0 || $wifinderLocationData.length === 0) return null;
		if (!$arucoLocationData || !$wifinderLocationData) return null;

		const firstArucoReadingTime = dayjs($arucoLocationData.at(-1)!.timestamp);
		const firstWiFinderReadingTime = dayjs($wifinderLocationData.at(-1)!.timestamp);
		const startTimeForTestPreview = firstArucoReadingTime.isBefore(firstWiFinderReadingTime)
			? firstArucoReadingTime
			: firstWiFinderReadingTime;

		return startTimeForTestPreview;
	},
	null
);

export const totalPlayingTimeMilliseconds = derived(
	[startTimeForTestPreview, endTimeForTestPreview],
	([$startTimeForTestPreview, $endTimeForTestPreview]) =>
		dayjs($endTimeForTestPreview).diff($startTimeForTestPreview, 'milliseconds'),
	0
);
