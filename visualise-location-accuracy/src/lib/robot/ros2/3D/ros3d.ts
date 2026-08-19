/**
 * @author Russell Toris - rctoris@wpi.edu
 * @author David Gossow - dgossow@willowgarage.com
 */

import * as THREE from 'three';

const ROS3D = {
	REVISION: '0.17.0-SNAPSHOT',

	// Marker types
	MARKER_ARROW: 0,
	MARKER_CUBE: 1,
	MARKER_SPHERE: 2,
	MARKER_CYLINDER: 3,
	MARKER_LINE_STRIP: 4,
	MARKER_LINE_LIST: 5,
	MARKER_CUBE_LIST: 6,
	MARKER_SPHERE_LIST: 7,
	MARKER_POINTS: 8,
	MARKER_TEXT_VIEW_FACING: 9,
	MARKER_MESH_RESOURCE: 10,
	MARKER_TRIANGLE_LIST: 11,

	// Interactive marker feedback types
	INTERACTIVE_MARKER_KEEP_ALIVE: 0,
	INTERACTIVE_MARKER_POSE_UPDATE: 1,
	INTERACTIVE_MARKER_MENU_SELECT: 2,
	INTERACTIVE_MARKER_BUTTON_CLICK: 3,
	INTERACTIVE_MARKER_MOUSE_DOWN: 4,
	INTERACTIVE_MARKER_MOUSE_UP: 5,

	// Interactive marker control types
	INTERACTIVE_MARKER_NONE: 0,
	INTERACTIVE_MARKER_MENU: 1,
	INTERACTIVE_MARKER_BUTTON: 2,
	INTERACTIVE_MARKER_MOVE_AXIS: 3,
	INTERACTIVE_MARKER_MOVE_PLANE: 4,
	INTERACTIVE_MARKER_ROTATE_AXIS: 5,
	INTERACTIVE_MARKER_MOVE_ROTATE: 6,

	// Interactive marker rotation behavior
	INTERACTIVE_MARKER_INHERIT: 0,
	INTERACTIVE_MARKER_FIXED: 1,
	INTERACTIVE_MARKER_VIEW_FACING: 2,

	// Collada loader types
	COLLADA_LOADER: 1,
	COLLADA_LOADER_2: 2,

	/**
	 * Create a THREE material based on the given RGBA values.
	 *
	 * @param r - the red value
	 * @param g - the green value
	 * @param b - the blue value
	 * @param a - the alpha value
	 * @returns the THREE material
	 */
	makeColorMaterial(r: number, g: number, b: number, a: number) {
		const color = new THREE.Color();
		color.setRGB(r, g, b);
		if (a <= 0.99) {
			return new THREE.MeshBasicMaterial({
				color: color.getHex(),
				opacity: a + 0.1,
				transparent: true,
				depthWrite: true,
				blendSrc: THREE.SrcAlphaFactor,
				blendDst: THREE.OneMinusSrcAlphaFactor,
				blendEquation: THREE.ReverseSubtractEquation,
				blending: THREE.NormalBlending
			});
		} else {
			return new THREE.MeshPhongMaterial({
				color: color.getHex(),
				opacity: a,
				blending: THREE.NormalBlending
			});
		}
	},

	/**
	 * Return the intersection between the mouseray and the plane.
	 *
	 * @param mouseRay - the mouse ray
	 * @param planeOrigin - the origin of the plane
	 * @param planeNormal - the normal of the plane
	 * @returns the intersection point
	 */
	intersectPlane(mouseRay, planeOrigin, planeNormal) {
		const vector = new THREE.Vector3();
		const intersectPoint = new THREE.Vector3();
		vector.subVectors(planeOrigin, mouseRay.origin);
		const dot = mouseRay.direction.dot(planeNormal);

		// bail if ray and plane are parallel
		if (Math.abs(dot) < mouseRay.precision) {
			return undefined;
		}

		// calc distance to plane
		const scalar = planeNormal.dot(vector) / dot;

		intersectPoint.addVectors(mouseRay.origin, mouseRay.direction.clone().multiplyScalar(scalar));
		return intersectPoint;
	},

	/**
	 * Find the closest point on targetRay to any point on mouseRay. Math taken from
	 * http://paulbourke.net/geometry/lineline3d/
	 *
	 * @param targetRay - the target ray to use
	 * @param mouseRay - the mouse ray
	 * @param the closest point between the two rays
	 */
	findClosestPoint(targetRay, mouseRay) {
		const v13 = new THREE.Vector3();
		v13.subVectors(targetRay.origin, mouseRay.origin);
		const v43 = mouseRay.direction.clone();
		const v21 = targetRay.direction.clone();
		const d1343 = v13.dot(v43);
		const d4321 = v43.dot(v21);
		const d1321 = v13.dot(v21);
		const d4343 = v43.dot(v43);
		const d2121 = v21.dot(v21);

		const denom = d2121 * d4343 - d4321 * d4321;
		// check within a delta
		if (Math.abs(denom) <= 0.0001) {
			return undefined;
		}
		const numer = d1343 * d4321 - d1321 * d4343;

		const mua = numer / denom;
		return mua;
	},

	/**
	 * Find the closest point between the axis and the mouse.
	 *
	 * @param axisRay - the ray from the axis
	 * @param camera - the camera to project from
	 * @param mousePos - the mouse position
	 * @returns the closest axis point
	 */
	closestAxisPoint(axisRay, camera, mousePos) {
		// Project axis origin onto the screen
		const o = axisRay.origin.clone().project(camera);

		// Project another point along the axis onto the screen
		const o2 = axisRay.direction.clone().add(axisRay.origin).project(camera);

		// d is the axis vector in screen space
		const d = o2.clone().sub(o);

		// t is the 2D ray parameter for the perpendicular projection
		// of mousePos onto the projected axis
		const t =
			mousePos.clone().sub(new THREE.Vector2(o.x, o.y)).dot(new THREE.Vector2(d.x, d.y)) /
			(d.x * d.x + d.y * d.y);

		// Final projected mouse position
		const mp = new THREE.Vector2(o.x + d.x * t, o.y + d.y * t);

		// Convert the screen position back into a 3D point
		const vector = new THREE.Vector3(mp.x, mp.y, 0.5).unproject(camera);

		// Create a ray from the camera through that point
		const mpRay = new THREE.Ray(camera.position.clone(), vector.sub(camera.position).normalize());

		return ROS3D.findClosestPoint(axisRay, mpRay);
	}
};

export default ROS3D;
