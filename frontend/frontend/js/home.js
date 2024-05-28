//fetches username sessionStorage variable
var username = sessionStorage.getItem('username');
//html element for username_text
var username_text = document.getElementById('username-title');
//if username_text exists in html, set to sessionstorage username
if(username_text) username_text.textContent = username;

//fetches status sessionStorage variable
var status = sessionStorage.getItem('usertype');
//html element for status_text
var status_text = document.getElementById('user-admin-status');
//html element for admin exclusive navigation
var admin_exclusive = document.getElementById('admin_plus');
//if status_text html element exists
if(status_text) {
  //shows user status in home page
  status_text.textContent = "Logged in as " + status.toLocaleUpperCase();
  //if user is an admin, show the admin-exclusive navigation
  if(status == 'admin') {
    //shows permissions (this is defaulted to hidden)
    admin_exclusive.hidden = false;
  }
}

/**
 * Redirects page to ./queries.html page
 * @param none
 * @returns none
 */
function redirect_queries() { 
  var queries = '/queries.html';
  window.location.href = queries;
}

//html element for go queries button
const queries_button = document.getElementById('queries-button');

//validating if exists fixes issue of front end js in same file not loading
if(queries_button) {
  //listens for click event and redirects to queries on click
  queries_button.addEventListener('click', function () {
    redirect_queries();
  });
}

//frontend required js
//importation of three.js library
import * as THREE from 'three';
//scss (css) import
import "/frontend/scss/style.scss"; //vite requires import style
//gsap library import
import gsap from "gsap";
//orbit controls library import
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls';

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

//sets geometry and material for torus model
const geometry = new THREE.TorusKnotGeometry( 10, 3, 750, 150 ); 
const material = new THREE.PointsMaterial({
  color: '#ffdd02',
  size: 0.01,
  opacity: 0.50,
})

//adds torus to scene
const torusknot = new THREE.Points(geometry, material);
scene.add(torusknot);


//main timeline for animations using gsap library
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

//loops window
loop();


