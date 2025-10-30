import dayjs from 'dayjs';
import { derived } from 'svelte/store';
import { arucoLocationData, wiFinderLocationData } from './locationsData';
import { currentPlayingTimestamp } from '../test/playbackTimes';
import type { LocationReading, MapLocation } from './format';

function cleanLocationObject(location?: LocationReading): MapLocation {
	if (!location) return { x: NaN, y: NaN };
	const x_in_metres = location.location[0];
	const y_in_metres = location.location[2];
	return {
		x: x_in_metres,
		y: y_in_metres
	};
}

export const currentWifinderLocation = derived(
	[wiFinderLocationData, currentPlayingTimestamp],
	([$wiFinderLocationData, $currentPlayingTimestamp]) =>
		cleanLocationObject(
			$wiFinderLocationData.findLast(({ timestamp }) =>
				dayjs(timestamp).isBefore($currentPlayingTimestamp)
			)!
		)
);

export const currentArucoLocation = derived(
	[arucoLocationData, currentPlayingTimestamp],
	([$arucoLocationData, $currentPlayingTimestamp]) =>
		cleanLocationObject(
			$arucoLocationData.findLast(({ timestamp }) =>
				dayjs(timestamp).isBefore($currentPlayingTimestamp)
			)!
		)
);
