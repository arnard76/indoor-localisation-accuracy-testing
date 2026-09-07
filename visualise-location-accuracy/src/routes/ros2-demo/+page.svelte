<script lang="ts">
	import { ros, my_topic_listener } from '$lib/robot/ros2/client';
	let status = $state('N/A');
	let messages: string[] = $state([]);

	// When the Rosbridge server connects, fill the span with id "status" with "successful"
	ros.on('connection', () => {
		status = 'successful';
	});
	// When the Rosbridge server experiences an error, fill the "status" span with the returned error
	ros.on('error', (error) => {
		status = `errored out (${error})`;
	});
	// When the Rosbridge server shuts down, fill the "status" span with "closed"
	ros.on('close', () => {
		status = 'closed';
	});

	// When we receive a message on /my_topic, add its data as a list item to the "messages" ul
	my_topic_listener.subscribe((message: any) => {
		messages.push(message.data);
	});
</script>

<h1>Rosbridge demo</h1>
<p>To see this page update:</p>
<ul>
	<li>Run a Rosbridge connection at <code>ws://localhost:9090</code></li>
	<li>Start publishing ROS messages to <code>/my_topic</code></li>
</ul>
<p>Connection: <span style="font-weight: bold;">{status}</span></p>
<p><code>/my_topic</code> messages received:</p>
<ul style="font-weight: bold;">
	{#each messages as message, i (i)}
		<li>{message}</li>
	{/each}
</ul>
