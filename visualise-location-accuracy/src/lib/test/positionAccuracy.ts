import type { LocationReading, MapLocation, MapPosition } from '$lib/locations/format';
import { locations } from '$lib/locations/locationsData';
import dayjs from 'dayjs';
import { derived, writable } from 'svelte/store';
import { findCurrentLocation } from './playbackTimes';

export const thresholdForTimestampsEquivalentToTimestamp = 250; // any CV location recorded at a time that is between wifinder_timestamp - 250ms and wifinder_timestamp + 250ms

export function areTimestampsEquivalent(time1: string | Dayjs, time2: string | Dayjs) {
	return (
		Math.abs(dayjs(time1).diff(dayjs(time2), 'milliseconds')) <=
		thresholdForTimestampsEquivalentToTimestamp
	);
}

export function calcLocationDiff(
	loc1: MapLocation | MapPosition,
	loc2: MapLocation | MapPosition
): MapLocation | MapPosition {
	let orientation = NaN;
	if (loc1.orientation !== undefined && loc2.orientation !== undefined) {
		orientation = (loc1.orientation - loc2.orientation) % 360;
		if (orientation > 180) {
			orientation -= 360;
		}
	}

	return {
		x: loc1.x - loc2.x,
		y: loc1.y - loc2.y,
		orientation
	};
}

export function distanceDiffFromLocationDiff(locDiff: MapLocation) {
	return (locDiff.x ** 2 + locDiff.y ** 2) ** 0.5;
}

export function distanceDiffFromLocations(loc1: MapLocation, loc2: MapLocation) {
	const locDiff = calcLocationDiff(loc1, loc2);
	return distanceDiffFromLocationDiff(locDiff);
}

export function calcDistanceDiffs(locations1: LocationReading[], locations2: LocationReading[]) {
	return locations1
		.map(({ x, y, timestamp: set1Timestamp, ...rest }) => {
			// TODO: remove any anomolous CV readings before average
			// INSTEAD OF REMOVING ANOMOLOUS AVERAGES!

			const averageSet2Location = findCurrentLocation(locations2, dayjs(set1Timestamp));
			if (!areTimestampsEquivalent(averageSet2Location.timestamp, set1Timestamp)) return;

			// const similarsLocationsInSet2 = locations2.filter(
			// 	({ timestamp }) =>
			// 		Math.abs(dayjs(timestamp).diff(set1Timestamp, 'milliseconds')) <
			// 		thresholdForCVTimestampsEquivalentToWifinderTimestamp
			// );

			// const totalLocation: MapLocation = { x: 0, y: 0 };
			// similarsLocationsInSet2.forEach((similarSet2Location) => {
			// 	totalLocation.y += similarSet2Location.x;
			// 	totalLocation.y += similarSet2Location.y;
			// });
			// const averageSet2Location: MapLocation = {
			// 	x: totalLocation.x / similarsLocationsInSet2.length,
			// 	y: totalLocation.y / similarsLocationsInSet2.length
			// };

			const locationDifference = calcLocationDiff({ ...rest, x, y }, averageSet2Location);

			return {
				timestamp: set1Timestamp,
				distanceDiff: distanceDiffFromLocationDiff(locationDifference),
				orientationDiff: locationDifference.orientation
			};
		})
		.filter((diff) => diff && diff.distanceDiff < 0.8);
}

export function averageOrientationDiff(
	orientationDiffs: {
		timestamp: string | dayjs.Dayjs;
		orientationDiff: number;
	}[]
) {
	const validAccuracyValues = orientationDiffs.filter(
		(accuracy) => !Number.isNaN(accuracy.orientationDiff)
	);
	let total = 0;

	validAccuracyValues.forEach((accuracy) => {
		total += Math.abs(accuracy.orientationDiff);
	});
	return Math.round((100 * total) / validAccuracyValues.length) / 100;
}

export function averageDistanceDiff(
	distanceDiffs: {
		timestamp: string | dayjs.Dayjs;
		distanceDiff: number;
	}[]
) {
	const validAccuracyValues = distanceDiffs.filter(
		(accuracy) => !Number.isNaN(accuracy.distanceDiff)
	);
	let total = 0;

	validAccuracyValues.forEach((accuracy) => {
		total += accuracy.distanceDiff;
	});
	return Math.round((100 * total) / validAccuracyValues.length) / 100;
}

export function findAccuracyFor(comparisons: Comparison[], idealSet: string, setToMeasure: string) {
	return comparisons.find((c) => c.idealSet === idealSet && setToMeasure == c.setToMeasure);
}

type LocationSets = { setToMeasure: string; idealSet: string };

export type Comparison = LocationSets & {
	diffs: any[];
	// currentDiff: number;
	average: number;
	orientationAverage: number;
};

export function createAccuracyCalculator() {
	const setsToCompare = writable<LocationSets[]>([]);

	const fullData = derived([setsToCompare, locations], ([$setsToCompare, $locations]) => {
		console.log('recalculating accuracies');
		const comparisons: Comparison[] = [];
		$setsToCompare.forEach(({ idealSet, setToMeasure }) => {
			const ideal = $locations[idealSet];
			const toMeasure = $locations[setToMeasure];
			if (!ideal || !toMeasure) return;
			console.log({ ideal, toMeasure });

			const diffsForSet = calcDistanceDiffs(toMeasure, ideal);

			const average = averageDistanceDiff(diffsForSet);
			const orientationAverage = averageOrientationDiff(diffsForSet);

			comparisons.push({
				idealSet,
				setToMeasure,
				diffs: diffsForSet,
				average,
				orientationAverage
			});
		});

		return comparisons;
	});

	return {
		...fullData,
		testNewSet(setToMeasure: string, idealSet: string) {
			setsToCompare.update((v) => [...v, { idealSet, setToMeasure }]);
		}
	};
}
