import * as THREE from 'three';
import "./loginsignup.css"; //vite requires import style
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
gltfLoader.load('./assets/vehicle.gltf', (gltfScene) => {
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
tl.fromTo('.title', {opacity: 0}, {opacity: 1}); 
tl.fromTo('.signup-container', {opacity: 0}, {opacity: 1}); 
tl.fromTo('.login-container', {opacity: 0}, {opacity: 1}); 

//controls
const controls = new OrbitControls(camera, canvas);
controls.enableRotate = false;
controls.enablePan = false;
controls.enableZoom = false;
controls.autoRotate = true;
controls.autoRotateSpeed = -5;

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


function redirect_home() {
  console.log("redirect home");
  var home_page = './in/home.html';
  window.location.href = home_page;
}

function check_signup() {
  var email = document.getElementById('email').value;
  var username = document.getElementById('username').value;
  var password = document.getElementById('password').value;
  var confirmed_pass = document.getElementById('confirmed').value;

  let val_email = email.includes("@");

  if (username != '' && password != '' && (password == confirmed_pass) && val_email) {
    sessionStorage.setItem('username', username);
    redirect_home();
  }
  else {
    window.alert('Incorrect Input');
  }
}

function check_login() {
  var username = document.getElementById('username').value;
  var password = document.getElementById('password').value;
  if (username != '' && password != '') {
    sessionStorage.setItem('username', username);
    redirect_home();
  }
  else {
    window.alert('Incorrect Username or Password');
  }
}

var login_button = document.getElementById("login-button");

if(login_button) {
  login_button.addEventListener('click', function () {
    check_login();
  });
}

var signup_button = document.getElementById("signup-button");

if(signup_button){
  signup_button.addEventListener('click', function () {
    check_signup();
  });
}
