import * as THREE from 'three';
import "./style.css"; //vite requires import style
import "./global.css";
import gsap from "gsap";
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls';
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";

//palette
//black1: #151515
//black2: #0a0a0a
//white: #fbfcd4
//yellow: #ffdd02
//gold: #fac402

//scene
const scene = new THREE.Scene();

//background
scene.background = new THREE.Color('#0a0a0a');

//sizes
const sizes = {
  width: window.innerWidth,
  height: window.innerHeight,
}

//create a rotation origin
const rotationCenter = new THREE.Object3D();
rotationCenter.position.set(0, 0, 0);
scene.add(rotationCenter);

//camera
const camera = new THREE.PerspectiveCamera(45, sizes.width / sizes.height, 0.1, 100);
camera.position.z = 20;
scene.add(camera);

//light
const light = new THREE.PointLight('#ffffff', 1, 1000);
light.position.set(10, 10, 10);
light.intensity = 600;
scene.add(light);
const hlight = new THREE.AmbientLight('#fac402', 0.4);
scene.add(hlight);

//start anims
const gltfLoader = new GLTFLoader();

const tlEarth = gsap.timeline({defaults: {duration : 0.5}});
gltfLoader.load('./assets/earth.gltf', (gltfScene) => {
  const loadedModel = gltfScene.scene;
  scene.add(loadedModel);

  tlEarth.fromTo(loadedModel.scale, {z: 0, x: 0, y: 0}, {z: 0.03, x: 0.03, y: 0.03});
});

const tlVehicle = gsap.timeline({defaults: {duration : 0.5}});
gltfLoader.load('./assets/vehicle.gltf', (gltfScene) => {
  const vehicleModel = gltfScene.scene;
  scene.add(vehicleModel);

  vehicleModel.translateY(3.2);
  tlVehicle.fromTo(vehicleModel.scale, {z: 0, x: 0, y: 0}, {z: 0.5, x: 0.5, y: 0.5});

  rotationCenter.add(vehicleModel);
});

const pgeometry1 = new THREE.TorusGeometry(7, 3, 16, 100);
const pmaterial1 = new THREE.PointsMaterial({
  color: '#ffdd02',
  size: 0.02,
})
const psphere1 = new THREE.Points(pgeometry1, pmaterial1);
scene.add(psphere1);
const pgeometry2 = new THREE.TorusGeometry(10, 5, 16, 100);
const pmaterial2 = new THREE.PointsMaterial({
  color: '#ffdd02',
  size: 0.02,
})
const psphere2 = new THREE.Points(pgeometry2, pmaterial2);
scene.add(psphere2);


//main timeline
const tl= gsap.timeline({defaults: {duration : 0.5}});
tl.add(tlEarth, 0.5); 
tl.add(tlVehicle, 1); 
tl.fromTo('nav', {y: '-100%'}, {y: '0%'});
tl.fromTo('.title1', {opacity: 0}, {opacity: 1}); 
tl.fromTo('.title2', {opacity: 0}, {opacity: 1}); 
tl.fromTo('.title3', {opacity: 0}, {opacity: 1}); 
tl.fromTo('.desc', {opacity: 0}, {opacity: 1}); 




//renderer
const canvas = document.querySelector('.webgl');
const renderer = new THREE.WebGLRenderer({ canvas });
renderer.setSize(sizes.width, sizes.height);
renderer.setPixelRatio(2);
renderer.render(scene, camera);

//controls
const controls = new OrbitControls(camera, canvas);
controls.enableDamping = true;
controls.enablePan = false;
controls.enableZoom = false;
controls.autoRotate = true;
controls.autoRotateSpeed = 5;


//resize window
window.addEventListener('resize', () => {
  sizes.width = window.innerWidth;
  sizes.height = window.innerHeight;
  //update camera
  camera.aspect = sizes.width / sizes.height;
  camera.updateProjectionMatrix();
  renderer.setSize(sizes.width, sizes.height);
})

//constant resize
const loop = () => {
  controls.update();
  renderer.render(scene, camera);

  rotationCenter.rotation.x += 0.01;
  psphere1.rotateY(0.01);
  psphere2.rotateZ(0.005);
  psphere2.rotateX(0.005);

  window.requestAnimationFrame(loop);
}
loop();

