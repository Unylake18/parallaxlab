"""yt_0031 final §8: QA de alinhamento 3D × Manim sobre o render 1080p30 (mesma lógica do qa31f.py, com os PNGs 3D em 1920×1080 e os
pedidos 3D da passada a 30 fps). Rótulos presos ao 3D: ≤ 2 px; pousos (vista de cima = chapa 2D): cantos com 0 px.
Entrada: renders/v2/qa/al/<LOTE>.json (gravado pelo render 1080p), threejs/pedidos3d/<LOTE>.json, threejs/q3d/<LOTE>_1920x1080/<cena>/pontos.json.
Saída: qa/alinhamento3d_final1080.txt"""
import json
from pathlib import Path

U = Path(__file__).resolve().parent
COM3D = ["PB1", "PB2", "PB5", "PB6", "PS"]
AL = U / "renders" / "v2" / "qa" / "al"
out, pior, nn, pior_c = [], 0.0, 0, 0.0
for l in COM3D:
    reg = json.loads((AL / f"{l}.json").read_text(encoding="utf-8")) if (AL / f"{l}.json").exists() else []
    cache, dl, nl = {}, 0.0, 0
    for lote, cena, fq, nome, x, y in reg:
        if cena not in cache:
            pp = U / "threejs" / "q3d" / f"{lote}_1920x1080" / cena / "pontos.json"
            cache[cena] = json.loads(pp.read_text(encoding="utf-8")) if pp.exists() else {}
        js = cache[cena].get(str(fq))
        if js and nome in js:
            dl, nl = max(dl, max(abs(js[nome][0] - x), abs(js[nome][1] - y))), nl + 1
    pior, nn = max(pior, dl), nn + nl
    out.append(f"{l}: {nl} amostras rótulo × ponto, pior = {dl:.2f} px")
    ped = json.loads((U / "threejs" / "pedidos3d" / f"{l}.json").read_text(encoding="utf-8"))
    esp = {"c00": (360, 780), "c20": (840, 780), "c22": (840, 300), "c02": (360, 300)}
    for cena, lista in ped["cenas"].items():
        pts = json.loads((U / "threejs" / "q3d" / f"{l}_1920x1080" / cena / "pontos.json").read_text(encoding="utf-8"))
        topo = [f for f, e in lista if abs(e["cam"]["pos"][2] - 11.575) < 0.01 and abs(e["cam"]["pos"][0] - 1) < 1e-3]
        if topo:
            dc = max(max(abs(pts[str(f)][k][0] - v[0]), abs(pts[str(f)][k][1] - v[1])) for f in topo for k, v in esp.items() if str(f) in pts)
            pior_c = max(pior_c, dc)
            out.append(f"   {cena}: pouso em {len(topo)} quadros; cantos 3D × chapa 2D: pior = {dc:.2f} px")
        else:
            out.append(f"   {cena}: sem pouso (entra/sai por troca de cena)")
txt = ("Alinhamento 3D × Manim no 1080p30 (≤ 2 px; pousos: 0 px)\n\n" + "\n".join(out)
       + f"\n\nTOTAL {nn} amostras rótulo × ponto, pior = {pior:.2f} px; pousos: pior canto = {pior_c:.2f} px\n")
(U / "qa").mkdir(exist_ok=True)
(U / "qa" / "alinhamento3d_final1080.txt").write_text(txt, encoding="utf-8")
print(txt)
