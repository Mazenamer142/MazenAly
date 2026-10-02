// Procedural 3D Land Cruiser + small stage helper. Bundled to ../car3d.js with esbuild (see README).
import * as THREE from 'three';
import { RoomEnvironment } from 'three/examples/jsm/environments/RoomEnvironment.js';
import { RoundedBoxGeometry } from 'three/examples/jsm/geometries/RoundedBoxGeometry.js';

const L = 4.95, W = 1.95, R = 0.40;           // length, width, wheel radius (metres)

/* ---------- materials ---------- */
function makeMaterials(paintColor) {
  return {
    paint: new THREE.MeshPhysicalMaterial({ color: paintColor, metalness: 0.25, roughness: 0.3, clearcoat: 1, clearcoatRoughness: 0.08, envMapIntensity: 0.8 }),
    glass: new THREE.MeshPhysicalMaterial({ color: 0x070b10, metalness: 0.3, roughness: 0.08, clearcoat: 1, envMapIntensity: 0.55 }),
    chrome: new THREE.MeshStandardMaterial({ color: 0xe4e8ed, metalness: 1, roughness: 0.14 }),
    plastic: new THREE.MeshStandardMaterial({ color: 0x1c1e22, roughness: 0.62 }),
    rubber: new THREE.MeshStandardMaterial({ color: 0x18181a, roughness: 0.9 }),
    rim: new THREE.MeshStandardMaterial({ color: 0xcfd4da, metalness: 1, roughness: 0.22 }),
    rimDark: new THREE.MeshStandardMaterial({ color: 0x5a6068, metalness: 0.9, roughness: 0.4 }),
    lamp: new THREE.MeshStandardMaterial({ color: 0xfff7df, emissive: 0xffe6a0, emissiveIntensity: 0.15, roughness: 0.15 }),
    tail: new THREE.MeshStandardMaterial({ color: 0xb3121a, emissive: 0xff1a22, emissiveIntensity: 0.35, roughness: 0.25 }),
    plate: new THREE.MeshStandardMaterial({ color: 0xf1efe6, roughness: 0.5 }),
    black: new THREE.MeshBasicMaterial({ color: 0x050607 }),
  };
}

const rb = (w, h, d, r, mat) => new THREE.Mesh(new RoundedBoxGeometry(w, h, d, 3, r), mat);

// extrude a side profile (x = length, y = height) across the car's width, centred on z
function extrude(shape, width, bevel) {
  const depth = width - 2 * bevel;
  const g = new THREE.ExtrudeGeometry(shape, {
    depth, bevelEnabled: true, bevelThickness: bevel, bevelSize: bevel, bevelOffset: -bevel,
    bevelSegments: 5, curveSegments: 28,
  });
  g.translate(0, 0, -depth / 2);
  g.computeVertexNormals();
  return g;
}

function bodyShape() {
  const s = new THREE.Shape();
  const arc = (cx) => { s.absarc(cx, 0.40, 0.52, -0.135, Math.PI + 0.135, false); };
  s.moveTo(0.10, 0.34);
  s.lineTo(0.04, 0.50); s.lineTo(0.02, 1.00);
  s.quadraticCurveTo(0.02, 1.11, 0.15, 1.13);
  s.lineTo(3.15, 1.15); s.lineTo(4.74, 1.05);
  s.quadraticCurveTo(4.92, 1.03, 4.93, 0.88);
  s.lineTo(4.95, 0.50);
  s.quadraticCurveTo(4.95, 0.34, 4.80, 0.33);
  s.lineTo(4.415, 0.33); arc(3.90);
  s.lineTo(1.515, 0.33); arc(1.00);
  s.lineTo(0.10, 0.34);
  return s;
}
function cabinShape() {
  const g = new THREE.Shape();
  g.moveTo(0.22, 1.08); g.lineTo(0.30, 1.80);
  g.quadraticCurveTo(0.31, 1.88, 0.43, 1.88);
  g.lineTo(2.45, 1.88); g.lineTo(3.22, 1.12); g.lineTo(3.22, 1.08);
  g.closePath();
  return g;
}

function makeWheel(m, flip) {
  const wheel = new THREE.Group();
  const spin = new THREE.Group();
  const pts = [[0.2, -0.14], [0.33, -0.152], [0.385, -0.12], [0.40, -0.06], [0.40, 0.06], [0.385, 0.12], [0.33, 0.152], [0.2, 0.14]]
    .map(([r, y]) => new THREE.Vector2(r, y));
  const tire = new THREE.Mesh(new THREE.LatheGeometry(pts, 48), m.rubber);
  tire.rotation.x = Math.PI / 2;
  const hub = new THREE.Mesh(new THREE.CylinderGeometry(0.255, 0.255, 0.28, 40), m.rim);
  hub.rotation.x = Math.PI / 2;
  const dish = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.2, 0.02, 40), m.rimDark);
  dish.rotation.x = Math.PI / 2; dish.position.z = 0.135;
  spin.add(tire, hub, dish);
  for (let i = 0; i < 6; i++) {
    const sp = rb(0.055, 0.2, 0.03, 0.012, m.rim);
    const a = (i / 6) * Math.PI * 2;
    sp.position.set(Math.sin(a) * 0.12, Math.cos(a) * 0.12, 0.15);
    sp.rotation.z = -a;
    spin.add(sp);
  }
  const cap = new THREE.Mesh(new THREE.CylinderGeometry(0.06, 0.06, 0.04, 24), m.chrome);
  cap.rotation.x = Math.PI / 2; cap.position.z = 0.15;
  spin.add(cap);
  wheel.add(spin);
  if (flip) wheel.rotation.y = Math.PI;
  wheel.traverse(o => { if (o.isMesh) o.castShadow = true; });
  return { wheel, spin, sign: flip ? -1 : 1 };
}

export function buildCar(paintColor = 0xf2f0ec) {
  const m = makeMaterials(paintColor);
  const group = new THREE.Group();        // world placement
  const body = new THREE.Group();         // centred model
  body.position.x = -L / 2;
  group.add(body);

  // main body + cabin glass
  body.add(new THREE.Mesh(extrude(bodyShape(), W, 0.07), m.paint));
  const cabin = new THREE.Mesh(extrude(cabinShape(), 1.74, 0.08), m.glass);
  body.add(cabin);

  // roof cap, pillars, belt trim
  const roof = rb(2.34, 0.07, 1.78, 0.03, m.paint); roof.position.set(1.40, 1.885, 0); body.add(roof);
  const pillar = (x, y0, y1, w, rotZ = 0, len) => {
    for (const s of [-1, 1]) {
      const p = rb(len ?? w, (len ? 0.1 : y1 - y0), 0.1, 0.02, m.paint);
      p.position.set(x, (y0 + y1) / 2, s * 0.865); p.rotation.z = rotZ; body.add(p);
    }
  };
  pillar(1.47, 1.08, 1.88, 0.10);                       // B
  pillar(0.62, 1.08, 1.88, 0.12);                       // C
  pillar(0.27, 1.08, 1.86, 0.10, -0.035);               // D (tailgate edge)
  pillar(2.835, 1.10, 1.88, 0, 2.3516, 1.12);           // A (raked windshield)
  const belt = rb(3.0, 0.035, 1.80, 0.015, m.chrome); belt.position.set(1.72, 1.12, 0); body.add(belt);

  // door shut lines + handles
  for (const s of [-1, 1]) {
    for (const x of [1.47, 2.70]) {
      const ln = rb(0.012, 0.74, 0.01, 0.004, m.black); ln.position.set(x, 0.74, s * (W / 2 + 0.002)); body.add(ln);
    }
    for (const x of [1.18, 2.25]) {
      const h = rb(0.22, 0.035, 0.045, 0.015, m.chrome); h.position.set(x, 0.98, s * (W / 2 + 0.012)); body.add(h);
    }
    // mirrors
    const stalk = rb(0.05, 0.05, 0.16, 0.02, m.plastic); stalk.position.set(3.10, 1.24, s * 0.97); body.add(stalk);
    const mir = rb(0.12, 0.16, 0.2, 0.05, m.paint); mir.position.set(3.08, 1.30, s * 1.08); body.add(mir);
    // lower side step / sill
    const sill = rb(1.55, 0.09, 0.08, 0.03, m.plastic); sill.position.set(2.2, 0.38, s * 0.93); body.add(sill);
    // head & tail lamps
    const hl = rb(0.1, 0.2, 0.36, 0.04, m.lamp); hl.position.set(4.89, 0.98, s * 0.70); body.add(hl);
    const drl = rb(0.06, 0.05, 0.3, 0.02, m.lamp); drl.position.set(4.92, 0.84, s * 0.70); body.add(drl);
    const fog = rb(0.08, 0.1, 0.14, 0.03, m.lamp); fog.position.set(4.90, 0.52, s * 0.78); body.add(fog);
    const tl = rb(0.06, 0.34, 0.16, 0.03, m.tail); tl.position.set(0.02, 0.97, s * 0.80); body.add(tl);
  }
  // roof rack
  for (const s of [-1, 1]) {
    const rail = new THREE.Mesh(new THREE.CylinderGeometry(0.016, 0.016, 1.9, 12), m.chrome);
    rail.rotation.z = Math.PI / 2; rail.position.set(1.4, 1.99, s * 0.7); body.add(rail);
    for (const x of [0.6, 1.4, 2.2]) {
      const leg = new THREE.Mesh(new THREE.CylinderGeometry(0.014, 0.014, 0.07, 8), m.chrome);
      leg.position.set(x, 1.955, s * 0.7); body.add(leg);
    }
  }
  for (const x of [0.75, 1.15, 1.55, 1.95]) {
    const bar = new THREE.Mesh(new THREE.CylinderGeometry(0.012, 0.012, 1.4, 10), m.chrome);
    bar.rotation.x = Math.PI / 2; bar.position.set(x, 1.99, 0); body.add(bar);
  }

  // front: grille, bumper
  const grille = rb(0.07, 0.28, 1.0, 0.03, m.chrome); grille.position.set(4.935, 0.80, 0); body.add(grille);
  const gIn = rb(0.03, 0.2, 0.88, 0.02, m.plastic); gIn.position.set(4.97, 0.80, 0); body.add(gIn);
  for (let i = 0; i < 4; i++) { const b = rb(0.02, 0.012, 0.88, 0.004, m.chrome); b.position.set(4.985, 0.73 + i * 0.047, 0); body.add(b); }
  const bumperF = rb(0.2, 0.2, 1.9, 0.06, m.plastic); bumperF.position.set(4.86, 0.47, 0); body.add(bumperF);
  const bumperR = rb(0.2, 0.2, 1.9, 0.06, m.plastic); bumperR.position.set(0.10, 0.46, 0); body.add(bumperR);
  const plate = rb(0.02, 0.15, 0.4, 0.008, m.plate); plate.position.set(-0.01, 0.62, 0); body.add(plate);
  // under-body + wheel wells
  const under = rb(4.2, 0.2, 1.6, 0.02, m.plastic); under.position.set(2.45, 0.40, 0); body.add(under);
  for (const cx of [1.0, 3.9]) {
    const well = new THREE.Mesh(new THREE.CylinderGeometry(0.46, 0.46, 1.55, 36), m.black);
    well.rotation.x = Math.PI / 2; well.position.set(cx, 0.40, 0); body.add(well);
  }

  // wheels
  const wheels = [];
  for (const cx of [1.0, 3.9]) for (const s of [-1, 1]) {
    const w = makeWheel(m, s < 0);
    w.wheel.position.set(cx, R, s * 0.80);
    body.add(w.wheel); wheels.push(w);
  }

  body.traverse(o => { if (o.isMesh) { o.castShadow = true; o.receiveShadow = false; } });

  return {
    group, body, wheels, mats: m,
    roll(dx) { wheels.forEach(w => { w.spin.rotation.z += w.sign * (-dx / R); }); },
    lights(on) { m.lamp.emissiveIntensity = on ? 2.4 : 0.15; m.tail.emissiveIntensity = on ? 0.9 : 0.35; },
  };
}

/* ---------- stage ---------- */
export function createStage(container, o = {}) {
  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.setClearColor(0x000000, 0);
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = o.exposure ?? 1.02;
  renderer.shadowMap.enabled = true;
  renderer.shadowMap.type = THREE.PCFShadowMap;
  const el = renderer.domElement;
  el.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;display:block;touch-action:pan-y';
  container.appendChild(el);

  const scene = new THREE.Scene();
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
  scene.environmentIntensity = o.env ?? 0.7;

  scene.add(new THREE.HemisphereLight(0xcfe4ff, 0xd9c6a2, 0.45));
  const sun = new THREE.DirectionalLight(0xfff0d8, 1.7);
  sun.position.set(-5, 9, 6);
  sun.castShadow = true;
  sun.shadow.mapSize.set(2048, 2048);
  Object.assign(sun.shadow.camera, { left: -8, right: 8, top: 8, bottom: -8, near: 1, far: 30 });
  sun.shadow.bias = -0.0004; sun.shadow.normalBias = 0.02; sun.shadow.radius = 5;
  scene.add(sun);

  const ground = new THREE.Mesh(new THREE.PlaneGeometry(80, 80), new THREE.ShadowMaterial({ opacity: o.shadow ?? 0.3 }));
  ground.rotation.x = -Math.PI / 2; ground.receiveShadow = true; scene.add(ground);

  const car = buildCar(o.paint);
  car.group.traverse(c => { if (c.isMesh) c.castShadow = true; });
  scene.add(car.group);

  const camera = new THREE.PerspectiveCamera(o.fov ?? 28, 1, 0.1, 200);
  const cam = { az: 0.8, el: 0.14, dist: 12, target: new THREE.Vector3(0, 0.8, 0), fov: o.fov ?? 28 };
  const stage = { scene, camera, renderer, car, cam, sun, visible: true, onFrame: null, onResize: null, running: true };

  function place() {
    camera.fov = cam.fov;
    const ce = Math.cos(cam.el);
    camera.position.set(cam.target.x + cam.dist * Math.sin(cam.az) * ce, cam.target.y + cam.dist * Math.sin(cam.el), cam.target.z + cam.dist * Math.cos(cam.az) * ce);
    camera.lookAt(cam.target);
    camera.updateProjectionMatrix();
  }
  function resize() {
    const w = container.clientWidth || 1, h = container.clientHeight || 1;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    stage.onResize && stage.onResize(w, h, camera.aspect);
    place();
    stage.sunFollow();
  }
  stage.sunFollow = () => { sun.target.position.set(car.group.position.x, 0, 0); sun.target.updateMatrixWorld(); sun.position.set(car.group.position.x - 5, 9, 6); };
  // fraction (0 top .. 1 bottom) of the canvas where world ground point (0,0,0) lands
  stage.groundFrac = () => { place(); const v = new THREE.Vector3(0, 0, 0).project(camera); return (1 - v.y) / 2; };

  const ro = new ResizeObserver(resize); ro.observe(container);
  const io = new IntersectionObserver(es => { stage.visible = es[0].isIntersecting; }, { threshold: 0 }); io.observe(container);

  let last = performance.now(), raf = 0;
  function loop(now) {
    raf = requestAnimationFrame(loop);
    if (!stage.visible || document.hidden) { last = now; return; }
    const dt = Math.min(o.maxDt ?? 0.05, (now - last) / 1000); last = now;
    stage.t = (stage.t || 0) + dt;
    stage.onFrame && stage.onFrame(stage.t, dt);
    place();
    stage.sunFollow();
    renderer.render(scene, camera);
  }
  raf = requestAnimationFrame(loop);
  resize();

  stage.dispose = () => {
    cancelAnimationFrame(raf); ro.disconnect(); io.disconnect(); renderer.dispose(); pmrem.dispose(); el.remove();
  };
  return stage;
}

window.LC3D = { createStage };
