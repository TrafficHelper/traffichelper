const valid_passkey = "testkey"; //review
sessionStorage.setItem('usertype', 'user')

function redirect_home() {
  var home_page = '/home.html'; 
  window.location.href = home_page;
}

function redirect_login_user() {
  window.location.href = '/login_user.html';
}

function check_login_user() {
  var username = document.getElementById('username').value;

  if (username != '') {
    sessionStorage.setItem('username', username);
    redirect_home();
  }
  else {
    window.alert('Username cannot be blank.');
  }
}

function check_login_admin() {
  var username = document.getElementById('username').value;
  var passkey = document.getElementById('passkey').value;

  if(passkey == valid_passkey) {
    sessionStorage.setItem('username', username);
    sessionStorage.setItem('usertype', 'admin')
    redirect_home();
  }
  else {
    window.alert('Invalid passkey... redirecting you to regular login.')
    redirect_login_user();
  }
}

const user_login_button = document.getElementById("user-login-button");

if(user_login_button) {
  user_login_button.addEventListener('click', function () {
    check_login_user();
  });
}

var admin_login_button = document.getElementById("admin-login-button");
if(admin_login_button) {
  admin_login_button.addEventListener('click', function () {
    check_login_admin();
  });
}

//more front end required js

import * as THREE from 'three';
import "/frontend/scss/style.scss"; //vite requires import style
import gsap from "gsap";
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls';
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";

//scene
const scene = new THREE.Scene();


//sizes
const sizes = {
    width: window.innerWidth,
    height: window.innerHeight,
}

//camera
const camera = new THREE.PerspectiveCamera(45, sizes.width / sizes.height, 0.1, 100);
camera.position.z = 20;
scene.add(camera);

//create a rotation origin
const rotationCenter = new THREE.Object3D();
rotationCenter.position.set(0, 0, 0);
scene.add(rotationCenter);

//light
const light = new THREE.PointLight('#ffffff', 1, 1000);
light.position.set(10, 10, 10);
light.intensity = 600;
scene.add(light);
const hlight = new THREE.AmbientLight('#ffffff', 0.4);
scene.add(hlight);

//start anims
const gltfLoader = new GLTFLoader();


const tlVehicle = gsap.timeline({defaults: {duration : 1}});
gltfLoader.load('/frontend/assets/models/vehicle.gltf', (gltfScene) => {
  const vehicleModel = gltfScene.scene;
  scene.add(vehicleModel);

  vehicleModel.translateY(7);
  vehicleModel.rotateY(-1.5);
  tlVehicle.fromTo(vehicleModel.scale, {z: 0, x: 0, y: 0}, {z: 0.5, x: 0.5, y: 0.5});

  rotationCenter.add(vehicleModel);
});


 //renderer
const canvas = document.querySelector('.webgl');
const renderer = new THREE.WebGLRenderer({ canvas });
renderer.setSize(sizes.width, sizes.height);
renderer.setPixelRatio(2);
renderer.render(scene, camera); 

const pgeometry = new THREE.TorusGeometry(5, 2, 16, 100);
const pmaterial = new THREE.PointsMaterial({
  color: '#ffdd02',
  size: 0.03,
})
const psphere = new THREE.Points(pgeometry, pmaterial);
scene.add(psphere);


//main timeline
const tl= gsap.timeline({defaults: {duration : 0.5}});
tl.fromTo('nav', {y: '-100%'}, {y: '0%'});
tl.fromTo(psphere.scale, {x: 0, y: 0, z: 0}, {x: 1, y: 1, z: 1});
if(user_login_button) tl.fromTo('.login-user-container', {opacity: 0}, {opacity: 1}); 
if(admin_login_button) tl.fromTo('.login-admin-container', {opacity: 0}, {opacity: 1});


//controls
const controls = new OrbitControls(camera, canvas);
controls.enableDamping = true;
controls.enableRotate = false;
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

    rotationCenter.rotateZ(0.01);


    window.requestAnimationFrame(loop);
}
loop();