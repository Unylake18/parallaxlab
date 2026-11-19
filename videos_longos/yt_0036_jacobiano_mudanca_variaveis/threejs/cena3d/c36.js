// yt_0036 · cena 3D (porte de referencia/c3d36.html, three.js r128; motor do c35.js do yt_0035). O PRODUTO VETORIAL EM PÉ (B4-2).
// Coordenadas LOCAIS do zoom: origem no canto M = φ(0,75; 0,5) = (0,3125; 0,75), unidade = Δ = 0,1 do plano x, y nos TRÊS eixos.
//   w1 = ∂φ/∂u Δu → (1,5; 1; 0) laranja · w2 = ∂φ/∂v Δv → (−1; 1,5; 0) verde-água · w1 ∧ w2 = (0, 0, 3,25) lima: altura = área (mesma escala).
// Estilo: opaco e sem luz (MeshBasicMaterial), sem sombra/névoa/brilho/transparência, outputEncoding linear, antialias, fundo transparente.
// A CÂMERA VEM DO MANIM no estado: {pos, tgt, up, cx, cy, fov} (perspectiva + setViewOffset: o alvo cai em (cx, cy) px de 1080p) ou, com
// orto = true, a OrthographicCamera de k px por unidade (a vista de cima = o 2D do zoom: M em (330, 860), 190 px por unidade local).
// Estado: cam, sobe (0..1: o vetor lima cresce de 0 a 3,25 a partir de M), rg (raio dos tubos da grade do chão: fino na vista de cima, como o papel 2D).
// As espessuras das setas e da borda casam com o 2D do Manim na vista de cima (5 px de haste, ponta de 20 px, borda de 3 px).
const T = THREE, W = window.innerWidth, H = window.innerHeight, ESC = W / 1920;
const R = new T.WebGLRenderer({ antialias: true, alpha: true, preserveDrawingBuffer: true });
R.setPixelRatio(1); R.setSize(W, H, false); R.setClearColor(0x000000, 0); R.outputEncoding = T.LinearEncoding;
document.body.appendChild(R.domElement);
T.Object3D.DefaultUp.set(0, 0, 1);
const S = new T.Scene();
const camP = new T.PerspectiveCamera(22, W / H, .05, 4000), camO = new T.OrthographicCamera(-1, 1, 1, -1, .05, 4000);
let cam = camP, G = null, PTS = {};
const UC = '#FF9440', VC = '#2EE6A6', LIMA = '#C6F26B', CHAPA = '#663A4C', MALHA = '#FFB3BC', GRADE = '#2B2558';
const C = h => new T.Color(h);
const w1 = [1.5, 1, 0], w2 = [-1, 1.5, 0], cc = [w1[0] + w2[0], w1[1] + w2[1], 0], HZ = w1[0] * w2[1] - w1[1] * w2[0];
const KT = 190;                                  // px por unidade local na vista de cima (1080p)
function aplicaCam(c) {
  if (c.orto) {
    cam = camO; const k = c.k;
    camO.left = -c.cx / k; camO.right = (1920 - c.cx) / k; camO.top = c.cy / k; camO.bottom = -(1080 - c.cy) / k;
    camO.up.set(...c.up); camO.position.set(...c.pos); camO.lookAt(...c.tgt); camO.updateProjectionMatrix(); camO.updateMatrixWorld(true);
  } else {
    cam = camP; camP.fov = c.fov || 22;
    camP.up.set(...c.up); camP.position.set(...c.pos); camP.lookAt(...c.tgt);
    camP.setViewOffset(W, H, (960 - c.cx) * ESC, (540 - c.cy) * ESC, W, H); camP.updateProjectionMatrix(); camP.updateMatrixWorld(true);
  }
}
function proj(n, v) { const q = new T.Vector3(...v).project(cam); PTS[n] = [+((q.x + 1) / 2 * 1920).toFixed(2), +((1 - q.y) / 2 * 1080).toFixed(2)]; }
function add(o) { G.add(o); return o; }
function poli(p) { const cp = new T.CurvePath(); for (let i = 0; i + 1 < p.length; i++) cp.add(new T.LineCurve3(new T.Vector3(...p[i]), new T.Vector3(...p[i + 1]))); return cp; }
const tubo = (p, r, cor) => add(new T.Mesh(new T.TubeGeometry(poli(p), Math.max(8, (p.length - 1) * 4), r, 8, false), new T.MeshBasicMaterial({ color: C(cor) })));
function seta(a, b, r, hl, hr, cor) {
  const A = new T.Vector3(...a), B = new T.Vector3(...b), d = B.clone().sub(A), L = d.length(); if (L < 1e-4) return null;
  // seta curta (vetor nascendo/sumindo): a haste e a ponta afinam na mesma proporção (sem disco da ponta sob M na vista de cima)
  if (.45 * L < hl) { const k = .45 * L / hl; r *= k; hr *= k; }
  hl = Math.min(hl, .45 * L); const g = new T.Group(), m = new T.MeshBasicMaterial({ color: C(cor) });
  const s = new T.Mesh(new T.CylinderGeometry(r, r, L - hl + .002, 16), m); s.position.y = (L - hl) / 2;
  const c = new T.Mesh(new T.ConeGeometry(hr, hl, 24), m); c.position.y = L - hl / 2; g.add(s, c);
  g.position.copy(A); g.quaternion.setFromUnitVectors(new T.Vector3(0, 1, 0), d.normalize()); add(g); return g;
}
window.setEstado = function (e) {
  if (G) { S.remove(G); G.traverse(o => { if (o.geometry) o.geometry.dispose(); }); }
  G = new T.Group(); S.add(G); PTS = {};
  aplicaCam(e.cam);
  // chão: grade de passo 0,5 local (= 0,05 de x, y), ξ deslocado 0,125 (x_M = 0,3125 não é múltiplo de 0,05); extensão = o papel 2D do zoom
  const rg = e.rg ?? .0032;
  for (let i = -2; i <= 6; i++) { const tx = i * .5 - .125; tubo([[tx, -.5, -rg - .003], [tx, 3, -rg - .003]], rg, GRADE); }
  for (let i = -1; i <= 6; i++) { const t = i * .5; tubo([[-1.125, t, -rg - .003], [2.875, t, -rg - .003]], rg, GRADE); }
  // paralelogramo: chapa + borda malha (3 px na vista de cima)
  const sh = new T.Shape([new T.Vector2(0, 0), new T.Vector2(w1[0], w1[1]), new T.Vector2(cc[0], cc[1]), new T.Vector2(w2[0], w2[1])]);
  const fill = add(new T.Mesh(new T.ShapeGeometry(sh), new T.MeshBasicMaterial({ color: C(CHAPA), side: T.DoubleSide }))); fill.position.z = .001;
  const rb = 1.5 / KT + (.016 - 1.5 / KT) * (e.th ?? 0), ez = .006;
  tubo([[0, 0, ez], [w1[0], w1[1], ez], [cc[0], cc[1], ez], [w2[0], w2[1], ez], [0, 0, ez]], rb, MALHA);
  // setas dos deslocamentos: haste 5 px, ponta 20 px de comprimento e 20 px de largura (como o seta_px do Manim)
  const th = e.th ?? 0, rh = 2.5 / KT + (.040 - 2.5 / KT) * th, hl = 20 / KT + (.40 - 20 / KT) * th, hr = 10 / KT + (.11 - 10 / KT) * th;
  seta([0, 0, .012], [w1[0], w1[1], .012], rh, hl, hr, UC); seta([0, 0, .014], [w2[0], w2[1], .014], rh, hl, hr, VC);
  // o vetor w1 ∧ w2 em pé (lima), altura 3,25 · sobe
  const sb = e.sobe ?? 0, h = HZ * sb;
  if (h > 1e-3) seta([0, 0, 0], [0, 0, h], .048, .42, .125, LIMA);
  R.render(S, cam);
  proj('M', [0, 0, 0]); proj('w1', w1); proj('w2', w2); proj('C', cc); proj('topo', [0, 0, h]);
  proj('w1_meio', [w1[0] / 2, w1[1] / 2, 0]); proj('w2_meio', [w2[0] / 2, w2[1] / 2, 0]);
  return PTS;
};
window.cenaPronta = true;
