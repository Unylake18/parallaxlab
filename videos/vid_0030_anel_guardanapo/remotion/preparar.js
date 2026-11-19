// Copia para public/ o que o Remotion serve via staticFile(): PNGs do 3D, fonte Space Grotesk e marca d'água (só leitura
// de assets/). A camada do Manim entra em public/manim_png/ pelo manim_png.py (o Remotion não decodifica o qtrle).
// Por que cópia e não junção: o bundler do Remotion recria links simbólicos na pasta temporária do bundle e o Windows
// sem modo desenvolvedor recusa (EPERM). Rodar de novo sempre que o 3D ou o Manim forem re-renderizados.
// Raiz do repositório por argumento ou REPO_ROOT: não dá para subir a partir de __dirname, porque neste PC videos/ é
// uma junção para outro disco.  Uso: node preparar.js C:/Users/Pichau/PycharmProjects/manim-fisica
const fs = require('fs'), path = require('path');
const UNIT = path.resolve(__dirname, '..'), PUB = path.join(__dirname, 'public');
const ROOT = process.argv[2] || process.env.REPO_ROOT;
if (!ROOT || !fs.existsSync(path.join(ROOT, 'assets'))) { console.error('uso: node preparar.js <raiz do repositório>'); process.exit(1); }
const copias = {
  frames3d: path.join(UNIT, process.argv[3] || 'frames3d_540x960'),   // master: frames3d_1080x1920
  fonts: path.join(ROOT, 'assets', 'fonts', 'space_grotesk'),
  marca: path.join(ROOT, 'assets', 'branding', 'overlays'),
};
const t0 = Date.now();
fs.mkdirSync(PUB, { recursive: true });
for (const [nome, origem] of Object.entries(copias)) {
  const p = path.join(PUB, nome);
  try { if (fs.lstatSync(p).isSymbolicLink()) fs.rmdirSync(p); } catch (e) { /* não existe */ }
  fs.rmSync(p, { recursive: true, force: true });      // só a cópia dentro de public/
  fs.cpSync(origem, p, { recursive: true, dereference: true, });
  console.log(`${nome} <- ${origem}`);
}
console.log(`cópia em ${((Date.now() - t0) / 1000).toFixed(1)} s`);
