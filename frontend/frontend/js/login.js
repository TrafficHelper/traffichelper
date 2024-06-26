//sets valid passkeys for administrator log in (can add as list, etc)
const valid_passkey = "testkey"; 
//defaults usertype/status to regular user 
sessionStorage.setItem('usertype', 'user')

/**
 * Redirects page to ./home.html
 * @param none
 * @returns none
 */
function redirect_home() {
  var home_page = '/home.html'; 
  window.location.href = home_page;
}

/**
 * Redirect page to ./login_user.html (regular user) page
 * @param none
 * @returns none
 */
function redirect_login_user() {
  var login_page = '/login_user.html';
  window.location.href = login_page;
}

/**
 * Checks the (regular) user login username
 * @param none
 * @returns none
 */
function check_login_user() {
  //html element of username input
  var username = document.getElementById('username').value;

  //checks if username is empty, otherwise accepts
  if (username != '') {
    sessionStorage.setItem('username', username);
    redirect_home();
  }
  else {
    window.alert('Username cannot be blank.');
  }
}

/**
 * Checks the administrator login username and passkey
 * @param none
 * @returns none
 */
function check_login_admin() {
  //get html elements for user input for username and passkey
  var username = document.getElementById('username').value;
  var passkey = document.getElementById('passkey').value;

  //checks if passkey is valid and username is not empty
  if(passkey == valid_passkey & username != "") {
    sessionStorage.setItem('username', username);
    sessionStorage.setItem('usertype', 'admin')
    //if valid, redirects to home
    redirect_home();
  }
  else {
    //if passkey is invalid, automatically redirect back to regular user login (gives popup)
    window.alert('Invalid passkey... redirecting you to regular login. Contact us in the Contacts Page for a valid passkey.')
    redirect_login_user();
  }
}

//html element for user_login_button
const user_login_button = document.getElementById("user-login-button");

//if user_login_button exists
if(user_login_button) {
  //on click, validate user login
  user_login_button.addEventListener('click', function () {
    check_login_user();
  });
}

//if admin_login_button exists
var admin_login_button = document.getElementById("admin-login-button");
if(admin_login_button) {
  //on click, validate admin login
  admin_login_button.addEventListener('click', function () {
    check_login_admin();
  });
}

//front end required js
//importation of three.js library
import * as THREE from 'three';
//scss (css) import
import "/frontend/scss/style.scss"; //vite requires import style
//gsap library import
import gsap from "gsap";
//orbit controls library import
import {OrbitControls} from 'three/examples/jsm/controls/OrbitControls';
//gltf library import
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

//loads GLTF and animates model
const tlVehicle = gsap.timeline({defaults: {duration : 1}});
gltfLoader.load('/frontend/assets/models/vehicle.gltf', (gltfScene) => {
  //sets to a new gltf scene
  const vehicleModel = gltfScene.scene;
  //ådd model to scene
  scene.add(vehicleModel);
  //transitions
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

//psphere geometry and material
const pgeometry = new THREE.TorusGeometry(5, 2, 16, 100);
const pmaterial = new THREE.PointsMaterial({
  color: '#ffdd02',
  size: 0.03,
})

//adds psphere to scene
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

//loops window
loop();