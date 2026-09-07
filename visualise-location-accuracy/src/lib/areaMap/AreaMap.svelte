<script lang="ts">
	import { mapImagePixelsToScreenPixelsScale, mapOnScreenWidth } from '$lib/locations/pixelScale';
	import { render } from 'svelte/server';

	let {
		mapLocations = undefined,
		rawPosition = $bindable(),
		mapImageURL,
		mapImageLabel = 'Area Map Image'
	} = $props();

	function navigateByKeyboard(event: KeyboardEvent) {
		let key = event.key;

		if (key == 'w' || key == 'ArrowUp') {
			rawPosition.y -= 1;
		} else if (key == 's' || key === 'ArrowDown') {
			rawPosition.y += 1;
		}

		if (key == 'a' || key === 'ArrowLeft') {
			rawPosition.x -= 1;
		} else if (key == 'd' || key === 'ArrowRight') {
			rawPosition.x += 1;
		}
	}

	import * as THREE from 'three';

	const scene = new THREE.Scene();
	const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);

	const renderer = new THREE.WebGLRenderer();
	renderer.setSize(window.innerWidth, window.innerHeight);

	const geometry = new THREE.SphereGeometry(1);
	const material = new THREE.MeshBasicMaterial({ color: 0x00ffff, reflectivity: 0.6 });
	const location = new THREE.Mesh(geometry, material);
	scene.add(location);

	const material2 = new THREE.LineBasicMaterial({ color: 0x0000ff });

	camera.position.z = 10;

	function animate(time) {
		renderer.render(scene, camera);
	}
	// renderer.setAnimationLoop(animate);
	// document.appendChild(renderer.domElement);
</script>

<svelte:body onkeydown={navigateByKeyboard} />

<!-- <canvas bind:this={renderer.domElement}></canvas> -->
<div class="area-map relative">
	{@render mapLocations?.()}

	<!-- svelte-ignore a11y_no_noninteractive_element_interactions -->
	<!-- svelte-ignore a11y_click_events_have_key_events -->
	<img
		bind:clientWidth={$mapOnScreenWidth}
		onclick={(event) => {
			rawPosition = {
				x: event.offsetX / $mapImagePixelsToScreenPixelsScale,
				y: event.offsetY / $mapImagePixelsToScreenPixelsScale
			};
		}}
		class="m-0 border-0 p-0"
		alt={mapImageLabel}
		src={mapImageURL}
	/>
</div>

<style>
	.area-map {
		--location-square-width: 10px;
	}
</style>
