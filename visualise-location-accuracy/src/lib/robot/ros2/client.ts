import * as ROSLIB from 'roslib';

// Create ros object to communicate over your Rosbridge connection
export const ros = new ROSLIB.Ros({ url: 'ws://localhost:9090' });

// Create a listener for /my_topic
export const my_topic_listener = new ROSLIB.Topic({
	ros,
	name: '/my_topic',
	messageType: 'std_msgs/String'
});
