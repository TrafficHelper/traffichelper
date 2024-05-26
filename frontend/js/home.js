var username = sessionStorage.getItem('username');
var username_text = document.getElementById('username-title');
if(username_text) {
  username_text.textContent = username;
}

var status = sessionStorage.getItem('usertype');
var status_text = document.getElementById('user-admin-status');
var admin_exclusive = document.getElementById('admin_plus');
if(status_text) {
  status_text.textContent = "Logged in as " + status.toLocaleUpperCase();
  if(status == 'admin') {
    admin_exclusive.hidden = false;
  }
}

function redirect_queries() { 
  var queries = '/queries.html';
  window.location.href = queries;
}

const queries_button = document.getElementById('queries-button');

//validating if exists fixes issue of front end js in same file not loading
if(queries_button) {
    queries_button.addEventListener('click', function () {
        redirect_queries();
    });
}

//frontend required js

import * as THREE from 'three';
import "/frontend/scss/style.scss"; //vite requires import style
import gsap from "gsap";
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls';
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";

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
if(queries_button){
  const tl = gsap.timeline({defaults: {duration : 0.5}});
  tl.fromTo('nav', {y: '-100%'}, {y: '0%'});
  tl.fromTo('.title-home1', {opacity: 0}, {opacity: 1});
  tl.fromTo('.title-home2', {opacity: 0}, {opacity: 1}); 
  tl.fromTo('.title-home3', {opacity: 0}, {opacity: 1}); 
  tl.fromTo('.queries-button', {opacity: 0}, {opacity: 1});
}


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


