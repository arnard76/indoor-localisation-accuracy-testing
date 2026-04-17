<script lang="ts">
	let { menuPreview, children } = $props();

	let showMenu = $state(false);
</script>

<div
	onmouseenter={() => (showMenu = true)}
	onmouseleave={() => (showMenu = false)}
	role="navigation"
>
	{@render menuPreview()}

	<menu class:hidden={!showMenu} class="absolute bottom-0 flex w-fit flex-col gap-4">
		{@render children()}
	</menu>
</div>
