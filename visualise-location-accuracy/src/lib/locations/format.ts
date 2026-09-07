import type { Dayjs } from 'dayjs';
import dayjs from 'dayjs';
import { pixelsToMetresScale } from './metreScale';

export type ImportableLocationReading = { location: number[]; timestamp: string };
export type MapLocation = { x: number; y: number; z: number };
export type MapPosition = {
	x: number;
	y: number;
	z: number;
	orientation: number;
};
export type LocationReading = MapLocation & { timestamp: string | Dayjs };
export type PositionReading = MapPosition & { timestamp: string | Dayjs };

export type LocationUnits = 'metres' | 'pixels';
export type MapLocations = { [key: string]: MapLocation };

export const nullLocation: MapLocation = { x: NaN, y: NaN, z: NaN };
export const nullPosition: MapPosition = { x: NaN, y: NaN, z: NaN, orientation: NaN };

export function scaleLocation(location: MapLocation, scale: number): MapLocation {
	return {
		x: location.x * scale,
		y: location.y * scale,
		z: location.z * scale
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
	try {
		const rounding = unit === 'pixels' ? 0 : 2;
		return `(${location.x.toFixed(rounding)}, ${location.y.toFixed(rounding)})`;
	} catch (e) {
		console.log(e);
		console.log({ location, unit });
		throw Error(e);
	}
}

/**
 * Sorts in chronological order
 * @param readings
 * @returns sorted readings (the first one is the earliest reading)
 */
export function sortReadings<ReadingType extends { timestamp: LocationReading['timestamp'] }>(
	readings: ReadingType[]
): ReadingType[] {
	return readings.sort((a, b) => (dayjs(a.timestamp).isBefore(b.timestamp) ? -1 : 1));
}
