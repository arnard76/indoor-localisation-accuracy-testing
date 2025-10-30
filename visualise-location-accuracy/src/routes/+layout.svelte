<script lang="ts">
	import { useStoredTestInputs } from '$lib/test/testData';
	import '../app.css';

	let { children } = $props();
	useStoredTestInputs();
</script>

{@render children?.()}
