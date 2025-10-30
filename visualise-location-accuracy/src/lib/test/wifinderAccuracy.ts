import { derived } from 'svelte/store';
import { arucoLocationData, wiFinderLocationData } from '../locations/locationsData';
import dayjs from 'dayjs';

const thresholdForCVTimestampsEquivalentToWifinderTimestamp = 250; // any CV location recorded at a time that is between wifinder_timestamp - 250ms and wifinder_timestamp + 250ms

// accuracy of each wifinder point at every second
export const wiFinderLocationAccuracy = derived(
	[wiFinderLocationData, arucoLocationData],
	([$wiFinderLocationData, $arucoLocationData]) =>
		$wiFinderLocationData
			.map(({ location: wifinderLocation, timestamp: wifinderTimestamp }) => {
				// TODO: remove any anomolous CV readings before average
				// INSTEAD OF REMOVING ANOMOLOUS AVERAGES!

				// find average aruco location
				const similarArucoLocations = $arucoLocationData.filter(
					({ timestamp: arucoTimestamp }) =>
						Math.abs(dayjs(arucoTimestamp).diff(wifinderTimestamp, 'milliseconds')) <
						thresholdForCVTimestampsEquivalentToWifinderTimestamp
				);

				const total = [0, 0];
				similarArucoLocations.forEach((similarArucoLocation) => {
					total[0] += similarArucoLocation.location[0];
					total[1] += similarArucoLocation.location[2];
				});
				const averageArucoLocation = [
					total[0] / similarArucoLocations.length,
					total[1] / similarArucoLocations.length
				];

				// calculate difference between average aruco location and wifinder location
				const locationDifference = [
					wifinderLocation[0] - averageArucoLocation[0],
					wifinderLocation[2] - averageArucoLocation[1]
				];

				const [xDiff, yDiff] = locationDifference;

				const distanceBetweenTwoLocations = (xDiff ** 2 + yDiff ** 2) ** 0.5;
				return distanceBetweenTwoLocations;
			})
			.filter((average) => average < 400)
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
