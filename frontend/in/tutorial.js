import * as THREE from 'three';
import "./tutorial.css"; //vite requires import style
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

const geometry = new THREE.TorusKnotGeometry( 10, 3, 750, 150 ); 
const material = new THREE.PointsMaterial({
  color: '#ffdd02',
  size: 0.01,
  opacity: 0.50,
})
const torusknot = new THREE.Points(geometry, material);
scene.add(torusknot);


//main timeline
const tl = gsap.timeline({defaults: {duration : 0.5}});
tl.fromTo('nav', {y: '-100%'}, {y: '0%'});
tl.fromTo('.title1', {opacity: 0}, {opacity: 1}); 
tl.fromTo('.title2', {opacity: 0}, {opacity: 1}); 
tl.fromTo('.regular-button', {x: '-500%'}, {x: '0%'});
tl.fromTo('.admin-button', {x: '500%'}, {x: '0%'});



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
controls.autoRotateSpeed = 1;


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

  torusknot.rotateX(0.003);
  torusknot.rotateY(0.003);
  torusknot.rotateZ(-0.003);

  window.requestAnimationFrame(loop);
}
loop();

var username = sessionStorage.getItem('username');
var username_text = document.getElementById('username-title');
username_text.textContent = username;
