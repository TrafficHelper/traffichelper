var admin = false;

var temp = sessionStorage.getItem('usertype');

if(temp == 'admin') {
  admin = true;
}

function direct_routing() {
  var routing_page = '/routing.html';
  window.location.href = routing_page;
}

function direct_queries() {
  var queries_page = '/queries.html';
  window.location.href = queries_page;
}

const go_routing = document.getElementById("go-routing-button");

if(go_routing) {
  go_routing.addEventListener('click', function () {
    direct_routing();
  })
}

const go_queries = document.getElementById("go-queries-button");

if(go_queries) {
  go_queries.addEventListener('click', function() {
    direct_queries();
  })
}



//frontend required js

import "/frontend/scss/functions.scss"; //vite requires import style
import * as THREE from 'three';

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

const geometry = new THREE.TorusKnotGeometry( 10, 3, 100, 150 ); 
const material = new THREE.PointsMaterial({
  color: '#ffdd02',
  size: 0.01,
  opacity: 0.50,
})
const torusknot = new THREE.Points(geometry, material);
scene.add(torusknot);

//renderer
const canvas = document.querySelector('.webgl');
const renderer = new THREE.WebGLRenderer({ canvas });
renderer.setSize(sizes.width, sizes.height);
renderer.setPixelRatio(2);
renderer.render(scene, camera);


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
  renderer.render(scene, camera);

  torusknot.rotateX(0.003);
  torusknot.rotateY(0.003);
  torusknot.rotateZ(-0.003);

  window.requestAnimationFrame(loop);
}
loop();
