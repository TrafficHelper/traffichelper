
/**
 * Redirects the page to ./routing.html page
 * @param none
 * @returns none
 */
function direct_routing() {
  var routing_page = '/routing.html';
  window.location.href = routing_page;
}

/**
 * Redircets page to ./queries.html page
 * @param none
 * @returns none
 */
function direct_queries() {
  var queries_page = '/queries.html';
  window.location.href = queries_page;
}

/**
 * Redirects page to ./results.html page
 * @param none
 * @returns none
 */
function direct_results() {
  var results_page = '/results.html';
  window.location.href = results_page;
}

//html element for the routing redirection button
const go_routing = document.getElementById("go-routing-button");

//if the page has go_routing html element
if(go_routing) {
  //on click, direct_routing()
  go_routing.addEventListener('click', function () {
    direct_routing();
  })
}

//html element for the queries redirection button
const go_queries = document.getElementById("go-queries-button");

//if the page has go_queries html element
if(go_queries) {
  //on click, direct_queries()
  go_queries.addEventListener('click', function() {
    direct_queries();
  })
}

//html element for results redirection button
const get_results = document.getElementById("submit-form-button");

//if the page has get_results html element
if(get_results) {
  //on click, clear the map (to avoid interference with results one) and direct_results()
  get_results.addEventListener('click', function() {
    map.remove();
    direct_results();
  })
}


//frontend required js
//scss (css) importation
import "/frontend/scss/functions.scss"; //vite requires import style
//importation of three.js library
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

//torus hologram effect geometry
const geometry = new THREE.TorusKnotGeometry( 10, 3, 100, 150 ); 
const material = new THREE.PointsMaterial({
  color: '#ffdd02',
  size: 0.01,
  opacity: 0.50,
})

//add torus to scene
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

//loop window
loop();
