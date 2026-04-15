import { derived } from 'svelte/store';
import dayjs from 'dayjs';
import type { LocationReading, MapLocation } from '$lib/locations/format';
import { locations } from '$lib/locations/locationsData';

const thresholdForCVTimestampsEquivalentToWifinderTimestamp = 250; // any CV location recorded at a time that is between wifinder_timestamp - 250ms and wifinder_timestamp + 250ms

export function locationDiff(loc1: MapLocation, loc2: MapLocation) {
	return {
		x: loc1.x - loc2.x,
		y: loc1.y - loc2.y
	};
}

export function distanceDiffFromLocationDiff(locDiff: MapLocation) {
	return (locDiff.x ** 2 + locDiff.y ** 2) ** 0.5;
}

export function compareLocations(locations1: LocationReading[], locations2: LocationReading[]) {
	return locations1
		.map(({ x, y, timestamp: wifinderTimestamp }) => {
			// TODO: remove any anomolous CV readings before average
			// INSTEAD OF REMOVING ANOMOLOUS AVERAGES!

			// find average aruco location
			const similarArucoLocations = locations2.filter(
				({ timestamp: arucoTimestamp }) =>
					Math.abs(dayjs(arucoTimestamp).diff(wifinderTimestamp, 'milliseconds')) <
					thresholdForCVTimestampsEquivalentToWifinderTimestamp
			);

			const totalLocation: MapLocation = { x: 0, y: 0 };
			similarArucoLocations.forEach((similarArucoLocation) => {
				totalLocation.y += similarArucoLocation.x;
				totalLocation.y += similarArucoLocation.y;
			});
			const averageArucoLocation: MapLocation = {
				x: totalLocation.x / similarArucoLocations.length,
				y: totalLocation.y / similarArucoLocations.length
			};

			// calculate difference between average aruco location and wifinder location
			const locationDifference = locationDiff({ x, y }, averageArucoLocation);

			return distanceDiffFromLocationDiff(locationDifference);
		})
		.filter((average) => average < 400);
}

// accuracy of each wifinder point at every second

export const wiFinderLocationAccuracy = derived([locations], ([$locations]) =>
	compareLocations($locations['wifinder'], $locations['aruco'])
);

export const averageWifinderAccuracy = derived(
	wiFinderLocationAccuracy,
	($wiFinderLocationAccuracy) => {
		const validAccuracyValues = $wiFinderLocationAccuracy.filter(
			(accuracy) => !Number.isNaN(accuracy)
		);
		let total = 0;

		validAccuracyValues.forEach((accuracy) => {
			total += accuracy;
		});
		return Math.round((100 * total) / validAccuracyValues.length) / 100;
	},
	null
);
