import { useStoredMap } from '$lib/areaMap/area';
import { arucoVideoSource } from '$lib/arucoCVVideo';
import { useStoredLocations } from '$lib/locations/locationsData';

export function useStoredTestInputs() {
	useStoredMap();
	useStoredLocations();
	const arucoVideoURL = localStorage.getItem('aruco-video-url');
	arucoVideoSource.set(arucoVideoURL);
}
