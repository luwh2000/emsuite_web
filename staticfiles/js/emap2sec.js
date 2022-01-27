const ASPECT_RATIO = 4 / 3;

import * as THREE from 'https://unpkg.com/three/build/three.module.js';
import { MyPDBLoader } from './MyPDBLoader.js';
import { TrackballControls } from 'https://unpkg.com/three/examples/jsm/controls/TrackballControls.js';

let root;
let controls;
let camera;

$(document).ready(function () {

    const container = document.getElementById('canvas');
    const canvasWidth = container.clientWidth;
    const canvasHeight = canvasWidth / ASPECT_RATIO;

    const scene = new THREE.Scene();

    camera = new THREE.PerspectiveCamera(70, canvasWidth / canvasHeight, 1, 5000);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setPixelRatio(window.devicePixelRatio);
    renderer.setSize(canvasWidth, canvasHeight);
    container.appendChild(renderer.domElement);

    const light1 = new THREE.DirectionalLight(0xf8f9fa, 0.7);
    scene.add(light1);

    const light = new THREE.AmbientLight(0x212529);
    scene.add(light);

    root = new THREE.Group();
    scene.add(root);

    controls = new TrackballControls(camera, renderer.domElement);

    loadMolecule('/static/visual.pdb');

    function animate() {
        requestAnimationFrame(animate);
        controls.update();
        light1.position.copy(camera.position);
        renderer.render(scene, camera);
    }
    animate();
});

function loadMolecule(url) {
    const loader = new MyPDBLoader();
    loader.load(url, function (pdb) {
        const offset = new THREE.Vector3();
        const geometryAtoms = pdb.geometryAtoms;
        const json = pdb.json;
        geometryAtoms.computeBoundingBox();
        geometryAtoms.boundingBox.getCenter(offset).negate();

        const s = geometryAtoms.boundingBox.min.distanceTo(geometryAtoms.boundingBox.max);
        camera.position.z = 0.8 * s;
        controls.minDistance = 0.4 * s;
        controls.maxDistance = 1.6 * s;

        geometryAtoms.translate(offset.x, offset.y, offset.z);
        let positions = geometryAtoms.getAttribute('position');
        const colors = geometryAtoms.getAttribute('color');
        const position = new THREE.Vector3();
        const color = new THREE.Color();
        console.log(json.atoms[0]);
        for (let i = 0; i < positions.count; i++) {

            position.x = positions.getX(i);
            position.y = positions.getY(i);
            position.z = positions.getZ(i);

            color.r = colors.getX(i);
            color.g = colors.getY(i);
            color.b = colors.getZ(i);

            const material = new THREE.MeshPhongMaterial({ color: color });
            const sphereGeometry = new THREE.IcosahedronBufferGeometry(1, 3);
            const object = new THREE.Mesh(sphereGeometry, material);
            object.position.copy(position);
            root.add(object);
        }
    });
}