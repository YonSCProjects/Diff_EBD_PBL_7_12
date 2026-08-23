// model.js — the Project 8 quadcopter as real 3D geometry, at its real millimetres.
// Dimensions are the same ones parts_p8.py draws from, which trace to Arduino_Project_8.md.
import * as THREE from 'three';

export const MM = 0.001;                 // work in metres so lighting/physical units behave

// ---- canonical geometry (mm) -------------------------------------------------
export const G = {
  ARM_R: 50, PLATE_T: 1.5, BODY_W: 46, BODY_D: 34,
  ARM_W_ROOT: 13, ARM_W_TIP: 10.5, RING_RO: 6.8, RING_RI: 4.35, GROMMET_H: 3.2,
  MOTOR_R: 4.25, MOTOR_H: 20, FOOT_H: 3, SHAFT_R: 0.5, SHAFT_H: 5,
  PROP_R: 32.5, PROP_HUB: 3.4, STACK_H: 15,
  DEVKIT: [51.5, 28.3, 1.4], MOSFET: [50, 40, 1.6], MT: [36, 17, 1.4],
  IMU: [21.2, 15.7, 1.2], BAT: [52, 30, 9],
};
// arms point along the axes: FRONT is -x, BACK +x, LEFT -z, RIGHT +z (y is up)
export const ARMS = {
  front: [-G.ARM_R, 0], back: [G.ARM_R, 0], left: [0, -G.ARM_R], right: [0, G.ARM_R],
};
export const SPIN = { front: 'cw', back: 'cw', left: 'ccw', right: 'ccw' };

// ---- materials ---------------------------------------------------------------
const phys = (o) => new THREE.MeshPhysicalMaterial(o);
export const MAT = {
  carbon: phys({ color: 0x23262c, roughness: 0.34, metalness: 0.15, clearcoat: 0.9, clearcoatRoughness: 0.18 }),
  pcbGreen: phys({ color: 0x0e6b3d, roughness: 0.52, metalness: 0.05, clearcoat: 0.5, clearcoatRoughness: 0.35 }),
  pcbBlack: phys({ color: 0x191c21, roughness: 0.48, metalness: 0.06, clearcoat: 0.45 }),
  pcbBlue: phys({ color: 0x18569c, roughness: 0.5, metalness: 0.05, clearcoat: 0.5 }),
  alu: phys({ color: 0xc9ced4, roughness: 0.28, metalness: 1.0 }),
  steel: phys({ color: 0x9aa0a6, roughness: 0.32, metalness: 1.0 }),
  gold: phys({ color: 0xd4a437, roughness: 0.3, metalness: 1.0 }),
  copper: phys({ color: 0xb87333, roughness: 0.34, metalness: 1.0 }),
  rubber: phys({ color: 0x121417, roughness: 0.92, metalness: 0.0 }),
  propDark: phys({ color: 0x1b2027, roughness: 0.40, metalness: 0.0, clearcoat: 0.55, side: THREE.DoubleSide }),
  propRed: phys({ color: 0x8c2b36, roughness: 0.40, metalness: 0.0, clearcoat: 0.55, side: THREE.DoubleSide }),
  lipo: phys({ color: 0x2b313a, roughness: 0.38, metalness: 0.25, clearcoat: 0.7 }),
  chipBlack: phys({ color: 0x0e1013, roughness: 0.45, metalness: 0.1 }),
  shield: phys({ color: 0xb8bdc4, roughness: 0.36, metalness: 0.95 }),
  wireRed: phys({ color: 0xc21b1b, roughness: 0.55 }),
  wireBlack: phys({ color: 0x15181c, roughness: 0.6 }),
  wireBlue: phys({ color: 0x2f6fd0, roughness: 0.55 }),
  wireWhite: phys({ color: 0xe8edf2, roughness: 0.55 }),
  wireYellow: phys({ color: 0xd8b430, roughness: 0.55 }),
  wireOrange: phys({ color: 0xe07a1a, roughness: 0.55 }),
  wireGreen: phys({ color: 0x27a83c, roughness: 0.55 }),
  wireGrey: phys({ color: 0x8b939d, roughness: 0.55 }),
  paint: phys({ color: 0xe0651a, roughness: 0.5 }),
  foam: phys({ color: 0xbfc5cc, roughness: 0.95 }),
};

// ---- helpers -----------------------------------------------------------------
function box(w, h, d, mat, x = 0, y = 0, z = 0, r = 0.35) {
  // rounded-ish: a plain box reads hard-edged at these sizes, so chamfer via scale-in bevel
  const g = new THREE.BoxGeometry(w * MM, h * MM, d * MM);
  const m = new THREE.Mesh(g, mat);
  m.position.set(x * MM, y * MM, z * MM);
  m.castShadow = m.receiveShadow = true;
  return m;
}
function cyl(r1, r2, h, mat, x = 0, y = 0, z = 0, seg = 48) {
  const m = new THREE.Mesh(new THREE.CylinderGeometry(r1 * MM, r2 * MM, h * MM, seg), mat);
  m.position.set(x * MM, y * MM, z * MM);
  m.castShadow = m.receiveShadow = true;
  return m;
}
function tube(pts, r, mat, seg = 64) {
  const curve = new THREE.CatmullRomCurve3(pts.map(p => new THREE.Vector3(p[0] * MM, p[1] * MM, p[2] * MM)));
  const m = new THREE.Mesh(new THREE.TubeGeometry(curve, seg, r * MM, 10, false), mat);
  m.castShadow = true;
  return m;
}
function extrude(shape2d, thick, mat) {
  const s = new THREE.Shape(shape2d.map(p => new THREE.Vector2(p[0] * MM, p[1] * MM)));
  const g = new THREE.ExtrudeGeometry(s, { depth: thick * MM, bevelEnabled: true,
    bevelThickness: 0.15 * MM, bevelSize: 0.15 * MM, bevelSegments: 2 });
  g.rotateX(-Math.PI / 2);                       // shape lies in xz, extrudes up +y
  const m = new THREE.Mesh(g, mat);
  m.castShadow = m.receiveShadow = true;
  return m;
}

// ---- the frame ---------------------------------------------------------------
function plateShape() {
  // centre body with clipped corners, plus four tapered arms, as one outline
  const b = G.BODY_W / 2, d = G.BODY_D / 2, cut = 6;
  const hr = G.ARM_W_ROOT / 2, ht = G.ARM_W_TIP / 2, R = G.ARM_R;
  return [
    [-b + cut, -d], [-hr, -d], [-ht, -R], [ht, -R], [hr, -d],       // left arm (-z)
    [b - cut, -d], [b, -d + cut],
    [b, -hr], [R, -ht], [R, ht], [b, hr],                            // back arm (+x)
    [b, d - cut], [b - cut, d],
    [hr, d], [ht, R], [-ht, R], [-hr, d],                            // right arm (+z)
    [-b + cut, d], [-b, d - cut],
    [-b, hr], [-R, ht], [-R, -ht], [-b, -hr],                        // front arm (-x)
    [-b, -d + cut],
  ];
}

export function buildFrame(root, { frontMark = true } = {}) {
  const bottom = extrude(plateShape(), G.PLATE_T, MAT.carbon);
  root.add(bottom);
  // arm rings + rubber grommets
  for (const [name, [ax, az]] of Object.entries(ARMS)) {
    const ring = new THREE.Mesh(
      new THREE.RingGeometry(G.RING_RI * MM, G.RING_RO * MM, 48), MAT.carbon);
    ring.rotateX(-Math.PI / 2);
    ring.position.set(ax * MM, (G.PLATE_T + 0.02) * MM, az * MM);
    root.add(ring);
    const gr = new THREE.Mesh(new THREE.TorusGeometry(
      (G.RING_RI + 0.8) * MM, 1.1 * MM, 12, 40), MAT.rubber);
    gr.rotateX(Math.PI / 2);
    gr.position.set(ax * MM, (G.PLATE_T + 1.2) * MM, az * MM);
    gr.castShadow = true;
    root.add(gr);
  }
  // standoffs + top plate
  for (const sx of [-1, 1]) for (const sz of [-1, 1]) {
    root.add(cyl(1.6, 1.6, G.STACK_H - G.PLATE_T, MAT.steel,
      sx * (G.BODY_W / 2 - 5), G.PLATE_T + (G.STACK_H - G.PLATE_T) / 2, sz * (G.BODY_D / 2 - 5)));
  }
  const b2 = (G.BODY_W - 4) / 2, d2 = (G.BODY_D - 2) / 2, cut = 5;
  const top = extrude([[-b2 + cut, -d2], [b2 - cut, -d2], [b2, -d2 + cut], [b2, d2 - cut],
                       [b2 - cut, d2], [-b2 + cut, d2], [-b2, d2 - cut], [-b2, -d2 + cut]],
                      G.PLATE_T, MAT.carbon);
  top.position.y = G.STACK_H * MM;
  root.add(top);
  if (frontMark) {
    const m = box(5, 0.3, 9, MAT.paint, -G.ARM_R + 14, G.PLATE_T + 0.2, 0);
    root.add(m);
  }
}

// ---- motors and props --------------------------------------------------------
export const Y_CAN = G.PLATE_T + 5.2 - G.MOTOR_H;      // bottom of the can

export function buildMotor(root, name, { leads = true, foot = true } = {}) {
  const [ax, az] = ARMS[name];
  const g = new THREE.Group();
  g.add(cyl(G.MOTOR_R, G.MOTOR_R, G.MOTOR_H, MAT.alu, ax, Y_CAN + G.MOTOR_H / 2, az));
  g.add(cyl(G.MOTOR_R - 0.15, G.MOTOR_R - 0.15, 1.4, MAT.chipBlack, ax, Y_CAN + G.MOTOR_H - 0.7, az));
  g.add(cyl(G.SHAFT_R, G.SHAFT_R, G.SHAFT_H, MAT.steel, ax, Y_CAN + G.MOTOR_H + G.SHAFT_H / 2, az));
  if (foot) g.add(cyl(G.MOTOR_R + 0.9, G.MOTOR_R + 0.4, G.FOOT_H, MAT.rubber, ax, Y_CAN - G.FOOT_H / 2, az));
  if (leads) {
    const cw = SPIN[name] === 'cw';
    const cols = cw ? [MAT.wireRed, MAT.wireBlue] : [MAT.wireWhite, MAT.wireBlack];
    const dirx = ax === 0 ? 0 : -Math.sign(ax), dirz = az === 0 ? 0 : -Math.sign(az);
    cols.forEach((m, i) => {
      const o = (i - 0.5) * 2.2;
      const px = ax + dirz * o, pz = az + dirx * o;
      g.add(tube([
        [px + dirx * G.MOTOR_R, Y_CAN + 7, pz + dirz * G.MOTOR_R],
        [px + dirx * 16, Y_CAN + 2, pz + dirz * 16],
        [px + dirx * 30, -1.5, pz + dirz * 30],
        [dirx * 12 + dirz * o, -3.0, dirz * 12 + dirx * o],
      ], 0.45, m));
    });
  }
  root.add(g);
  return g;
}

export function buildProp(root, name) {
  const [ax, az] = ARMS[name];
  const cw = SPIN[name] === 'cw';
  const mat = cw ? MAT.propDark : MAT.propRed;
  const y = Y_CAN + G.MOTOR_H + 1.4;
  const g = new THREE.Group();
  g.add(cyl(G.PROP_HUB, G.PROP_HUB - 0.4, 3.2, MAT.chipBlack, ax, y + 1.6, az));
  for (const a0 of [0, Math.PI]) {
    // a blade: a swept, twisted lofted strip from hub to tip
    const N = 26, pts = [];
    for (let i = 0; i <= N; i++) {
      const t = i / N;
      const r = G.PROP_HUB + (G.PROP_R - G.PROP_HUB) * t;
      const a = a0 + (cw ? 1 : -1) * THREE.MathUtils.degToRad(26) * t;
      const w = (G.PROP_R - G.PROP_HUB) * 0.155 * Math.pow(Math.sin(Math.PI * Math.pow(t, 0.86)), 0.6) + 0.45;
      const pitch = 1.9 * Math.sin(Math.PI * t) * (cw ? 1 : -1);
      const ca = Math.cos(a), sa = Math.sin(a);
      pts.push({ r, ca, sa, w, pitch });
    }
    const verts = [], idx = [];
    pts.forEach((p, i) => {
      verts.push((ax + p.ca * p.r - p.sa * p.w) * MM, (y + 3.2 + p.pitch) * MM, (az + p.sa * p.r + p.ca * p.w) * MM);
      verts.push((ax + p.ca * p.r + p.sa * p.w) * MM, (y + 3.2 - p.pitch) * MM, (az + p.sa * p.r - p.ca * p.w) * MM);
      if (i < pts.length - 1) {
        const b = i * 2;
        idx.push(b, b + 1, b + 2, b + 1, b + 3, b + 2);
      }
    });
    const geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.Float32BufferAttribute(verts, 3));
    geo.setIndex(idx);
    geo.computeVertexNormals();
    const blade = new THREE.Mesh(geo, mat);
    blade.castShadow = true;
    g.add(blade);
  }
  root.add(g);
  return g;
}

// ---- boards ------------------------------------------------------------------
function header(root, x0, y, z, n, mat = MAT.gold, along = 'x') {
  for (let i = 0; i < n; i++) {
    const dx = along === 'x' ? i * 2.54 : 0, dz = along === 'x' ? 0 : i * 2.54;
    root.add(box(0.64, 2.2, 0.64, mat, x0 + dx, y + 1.1, z + dz));
  }
}

export function buildDevkit(root, y = G.STACK_H + G.PLATE_T) {
  const [w, d, t] = G.DEVKIT;
  const g = new THREE.Group();
  g.add(box(w, t, d, MAT.pcbBlack, 0, y + t / 2, 0));
  g.add(box(8, 4.2, 10, MAT.shield, w / 2 - 6, y + t + 2.1, 0));                 // micro-USB, aft (+x)
  g.add(box(18, 2.6, 18, MAT.shield, -w / 2 + 17, y + t + 1.3, -2));             // RF can
  header(g, -w / 2 + 8, y + t, -d / 2 + 1.6, 15);
  header(g, -w / 2 + 8, y + t, d / 2 - 1.6, 15);
  g.add(box(2.6, 1.0, 1.6, MAT.paint, -6, y + t + 0.5, 6));                      // the blue LED spot
  root.add(g);
  return g;
}

export function buildMosfetBoard(root, y, { flip = true } = {}) {
  const [w, d, t] = G.MOSFET;
  const g = new THREE.Group();
  g.add(box(w, t, d, MAT.pcbGreen, 0, y + t / 2, 0));
  // rails
  g.add(box(w - 4, 1.0, 1.8, MAT.copper, 0, y + t + 0.5, -d / 2 + 3.3));
  g.add(box(w - 4, 1.0, 1.8, MAT.alu, 0, y + t + 0.5, d / 2 - 4.1));
  if (!flip) {
    for (let c = 0; c < 4; c++) {
      const cx = -w / 2 + 3.5 + c * 11.4 + 5;
      g.add(box(10.16, 4.6, 11, MAT.chipBlack, cx, y + t + 2.3, -d / 2 + 23.5));      // TO-220 body
      g.add(box(10.5, 5.0, 4.6, MAT.pcbBlue, cx, y + t + 2.5, -d / 2 + 15.6));        // heat-shrunk tab
      g.add(cyl(1.3, 1.3, 6.4, MAT.chipBlack, cx + 3.6, y + t + 1.3, -d / 2 + 10)).rotateX(Math.PI / 2);
      g.add(box(2.2, 2.2, 6, MAT.foam, cx - 4.4, y + t + 1.1, -d / 2 + 14));
    }
    g.add(cyl(4, 4, 11, MAT.pcbBlue, w / 2 - 6.5, y + t + 5.5, -d / 2 + 24));
  } else {
    for (let gx = -w / 2 + 4; gx < w / 2 - 3; gx += 4)
      for (let gz = -d / 2 + 4; gz < d / 2 - 3; gz += 4)
        g.add(cyl(0.8, 0.8, 0.5, MAT.alu, gx, y + t + 0.2, gz));                 // solder joints
  }
  root.add(g);
  return g;
}

export function buildMT3608(root, y) {
  const [w, d, t] = G.MT;
  const g = new THREE.Group();
  const z0 = -25;
  g.add(box(w, t, d, MAT.pcbBlue, 2, y + t / 2, z0));
  g.add(cyl(5, 5, 5.2, MAT.chipBlack, -6, y + t + 2.6, z0));                     // inductor
  g.add(box(8, 4.4, 8, MAT.pcbBlue, 9, y + t + 2.2, z0));                        // trimmer body
  g.add(box(2.8, 0.6, 0.9, MAT.alu, 9, y + t + 4.5, z0));                        // screw slot
  root.add(g);
  return g;
}

export function buildIMU(root, y) {
  const [w, d, t] = G.IMU;
  const g = new THREE.Group();
  const z0 = 23 + d / 2;
  g.add(box(w, t, d, MAT.pcbBlue, 0, y + t / 2, z0));
  g.add(box(5, 1.2, 5, MAT.chipBlack, 1, y + t + 0.6, z0));
  header(g, -w / 2 + 2, y + t, z0 - d / 2 + 1.4, 8);
  root.add(g);
  return g;
}

export function buildLipo(root, y) {
  const [w, d, h] = G.BAT;
  const g = new THREE.Group();
  g.add(box(w, h, d, MAT.lipo, 0, y + h / 2, 0));
  g.add(box(w - 12, 0.4, d - 8, MAT.pcbBlack, 0, y + h + 0.2, 0));
  g.add(box(5, 4, 6, MAT.foam, w / 2 + 2, y + h * 0.4, d / 2 - 4));              // PH2.0, on the diagonal
  root.add(g);
  return g;
}

export function buildDrone(root, opts = {}) {
  const { props = false, battery = true, electronics = true, leads = true } = opts;
  buildFrame(root, opts);
  for (const n of Object.keys(ARMS)) buildMotor(root, n, { leads });
  if (electronics) {
    buildMosfetBoard(root, -(2 + G.MOSFET[2]), { flip: true });
    buildDevkit(root);
    buildMT3608(root, G.STACK_H + G.PLATE_T);
    buildIMU(root, G.STACK_H + G.PLATE_T);
  }
  if (battery) buildLipo(root, -15.5);
  if (props) for (const n of Object.keys(ARMS)) buildProp(root, n);
  return root;
}
