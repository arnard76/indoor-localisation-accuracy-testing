<!-- 
Show time effect, some sort of shadow or outline as it moves.  


-->
<script lang="ts">
	import { displayLocation } from '$lib/locations/format';

	let {
		positions,
		displayedPositions = positions,
		colour = 'chocolate',
		unit,
		name = '',
		timeEffect = 'playthrough' as 'playthrough' | 'instant'
	} = $props();
</script>

<MapLocation origin={{ x: 0, y: 0 }} {position} inputUnit="metres" />

<MapLocation origin={{ x: 0, y: 0 }} {position} inputUnit="metres" />
