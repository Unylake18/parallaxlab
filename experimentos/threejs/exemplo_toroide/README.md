# Exemplo: camada 3D do vid_0029 (campo do toroide), V2

Snapshot de referência do primeiro curto feito com Three.js + Manim. Contém só a parte reaproveitável: `cena3d/`
(toroide de 24 espiras, rastros verdes, anéis de campo com pulsos ∝ 1/r, setas girando, contagem dentro/fora, círculo
amperiano), `timeline.json` (185 s, beats B01–B10), `render3d.js`, `compor.py`, `qa/alinhamento.js` e, em `pautas/`, o
briefing, as avaliações/handoffs v2 e v3 e o relatório do preview V2.

O `cena.py` (camada Manim) e a unidade completa vão entrar como `videos/vid_0029_*` quando o vídeo for subido. Para
rodar este 3D sozinho: `npm install` aqui e `node render3d.js --quadros 0,300,1500` (os scripts do Three.js vêm de
`../vendor/three-r128/`). No Linux, troque o `--use-angle=d3d11` do `render3d.js` pelos argumentos do SwiftShader
(ver `../modelo/render3d.js`).
