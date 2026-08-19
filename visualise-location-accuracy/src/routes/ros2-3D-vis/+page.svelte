<script lang="ts">
	// import ROS3D from '@robot-web-tools/ros3djs/build/ros3d.js';
	import { ros, my_topic_listener } from '$lib/robot/ros2/client';

	setTimeout(() => {
		/**
		 * Setup all visualization elements when the page is loaded.
		 */
		// Create the main viewer.
		var viewer = new ROS3D.Viewer({
			divID: 'map',
			width: 800,
			height: 600,
			antialias: true
		});

		// Setup the marker client.
		var gridClient = new ROS3D.OccupancyGridClient({
			ros,
			rootObject: viewer.scene
		});
	}, 5000);
</script>

<h1>Simple Map Example</h1>
<p>
	Run the following commands in the terminal then refresh this page. This will load a map from the
	<tt>ros-groovy-rail-maps</tt>
	package.
</p>
<ol>
	<li><tt>roscore</tt></li>
	<li>
		<tt>ros2 run map_server map_server /opt/ros/groovy/share/rail_maps/maps/ilab.pgm 0.05</tt>
	</li>
	<li><tt>ros2 launch rosbridge_server rosbridge_websocket_launch.xml</tt></li>
</ol>
<div id="map"></div>
