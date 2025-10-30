import type { Dayjs } from 'dayjs';
import dayjs from 'dayjs';
import { pixelsToMetresScale } from './metreScale';

export type LocationReading = { location: number[]; timestamp: string | Dayjs };
export type MapLocation = { x: number; y: number };
export type LocationUnits = 'metres' | 'pixels';
export type MapLocations = { [key: string]: MapLocation };

export function scaleLocation(location: MapLocation, scale: number): MapLocation {
	return {
		x: location.x * scale,
		y: location.y * scale
	};
}

export function scaleLocations(locations: MapLocations, scale: number): MapLocations {
	const locationsInOtherFormat = { ...locations };
	Object.keys(locationsInOtherFormat).forEach(function (key) {
		locationsInOtherFormat[key] = scaleLocation(locations[key], scale);
	});
	return locationsInOtherFormat;
}

export function convertLocationFromFormat(
	location: MapLocation,
	from: LocationUnits,
	to?: LocationUnits
): MapLocation {
	if (from === to) return location;

	if (from === 'pixels') {
		return scaleLocation(location, pixelsToMetresScale);
	}

	return scaleLocation(location, 1 / pixelsToMetresScale);
}

export function convertLocationsFromFormat(locationsInFormat: MapLocations, from: LocationUnits) {
	const locationsInOtherFormat = { ...locationsInFormat };
	Object.keys(locationsInOtherFormat).forEach(function (key) {
		locationsInOtherFormat[key] = convertLocationFromFormat(locationsInFormat[key], from);
	});
	return locationsInOtherFormat;
}

export function displayLocation(location: MapLocation, unit: LocationUnits): string {
	const rounding = unit === 'pixels' ? 0 : 2;
	return `X: ${location.x.toFixed(rounding)}, Y: ${location.y.toFixed(rounding)}`;
}

/**
 * Sorts in chronological order
 * @param locationReadings
 * @returns sorted location readings (the first one is the earliest reading)
 */
export function sortLocationReadings(locationReadings: LocationReading[]): LocationReading[] {
	return locationReadings.sort((a, b) => (dayjs(a.timestamp).isBefore(b.timestamp) ? -1 : 1));
}
