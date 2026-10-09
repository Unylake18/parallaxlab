from pathlib import Path
import hashlib
import json
import shutil
import sys
import zipfile

import av
from PIL import Image, ImageDraw, ImageFont

MEDIA = Path(__file__).resolve().parents[1]
QA = MEDIA / "qa"
FONT = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 17)


def sheets(items, prefix, batch=8):
    for start in range(0, len(items), batch):
        canvas = Image.new("RGB", (1080, 1020), "#101827")
        draw = ImageDraw.Draw(canvas)
        for i, (label, im) in enumerate(items[start:start + batch]):
            x, y = (i % 4) * 270, (i // 4) * 510
            canvas.paste(im.convert("RGB").resize((270, 480)), (x, y + 30))
            draw.text((x + 5, y + 5), label[:29], font=FONT, fill="white")
        canvas.save(QA / f"{prefix}_{start // batch + 1:02d}.jpg", quality=92)


states = sorted((QA / "estados").glob("*.png"))
sheets([(p.stem, Image.open(p)) for p in states], "estados")
if "--complete" not in sys.argv:
    print(json.dumps({"estados": len(states)}, ensure_ascii=False))
    raise SystemExit

meta = json.loads((MEDIA / "estados_preview.json").read_text(encoding="utf-8"))
movie = MEDIA / "videos/cena/960p15/BateriaMassaEnergia.mp4"
names = ["ng_recua_para_rehook", "inversao_massa_energia", "contagem_uma_para_quatro",
         "contagem_quatro_para_dezesseis", "grade_para_1_6_bilhao",
         "divisao_para_100_milhoes_kg", "kg_para_toneladas", "baterias_recuam_navio_entra",
         "bilhao_para_trilhao", "navio_para_dez", "dez_para_cem_navios",
         "frota_colapsa_para_bateria"]
transitions = {t["nome"]: t["t"] for t in meta["transicoes"]}
# Centros conferidos no primeiro MP4; o ajuste só muda fases visuais,
# mantendo os mesmos tempos reais dos segmentos.
actual_centers = dict(zip(names, [64.43, 66.8, 82.63, 83.45, 84.33, 91.57,
                                  93.53, 96.0, 101.57, 103.56, 104.38, 108.33]))
requests = sorted((transitions[name] + delta, name)
                  for name in names for delta in (-0.3, 0, 0.3, 0.55))
requests = sorted((actual_centers[name] + delta, name)
                  for name in names for delta in (-0.3, 0, 0.3, 0.55))
# Os dois ajustes foram inspecionados também pelos tempos reais do MP4.
# Reutilizar cache pode reduzir ligeiramente os tempos indicativos da Scene.
requests.extend((t, "navio_ajuste") for t in (95.9, 96.1, 96.3, 96.5))
requests.extend((t, "trilhao_ajuste") for t in (101.3, 101.5, 101.7, 101.9))
requests.sort()
sampled = []
with av.open(str(movie)) as container:
    stream = container.streams.video[0]
    info = {"resolucao": [stream.width, stream.height], "fps_nominal": str(stream.base_rate),
            "duracao_s": float(container.duration / av.time_base), "audio": len(container.streams.audio),
            "bytes": movie.stat().st_size, "estados": len(states), "transicoes_amostradas": len(names),
            "blocos": meta["blocos"]}
    cursor = count = 0
    for fr in container.decode(stream):
        count += 1
        t = float(fr.pts * fr.time_base)
        while cursor < len(requests) and t >= requests[cursor][0]:
            target, name = requests[cursor]
            sampled.append((f"{name[:18]} {t:.2f}s", fr.to_image()))
            cursor += 1
    info["frames"] = count
sheets(sampled, "movimento")
baseline = json.loads((QA / "tempos_primeiro_render.json").read_text(encoding="utf-8"))
assert abs(info["duracao_s"] - baseline["duracao_s"]) < 0.01
info["tempos_metadata_cache_aproximados"] = info["blocos"]
# Durações do primeiro render sem cache; os dois ajustes preservam os
# mesmos run_time e o MP4 confirma a duração total, a menos de 1 ms.
info["blocos"] = baseline["blocos"]
info["quadros_de_movimento"] = len(sampled)

preserved = []
for p in states:
    if int(p.name[:2]) <= 12:
        earlier = MEDIA.parent / "media_r3/qa/estados" / p.name
        assert p.read_bytes() == earlier.read_bytes(), f"Estado inicial mudou: {p.name}"
        preserved.append(p.stem)
info["estados_iniciais_identicos_r3"] = preserved

c = 299792458
energy_wh = 15.2
gram_j = 1e-3 * c**2
gram_wh = gram_j / 3600
numbers = {"bateria_Wh": energy_wh, "bateria_J": energy_wh * 3600,
           "bateria_ng": energy_wh * 3600 / c**2 * 1e12,
           "1g_J": gram_j, "1g_GWh": gram_wh / 1e9,
           "1g_baterias": gram_wh / energy_wh, "1g_kg": gram_wh / 250,
           "1kg_baterias": gram_wh / energy_wh * 1000, "1kg_kg": gram_wh / 250 * 1000}
assert round(numbers["1g_GWh"]) == 25
assert round(numbers["1g_baterias"] / 1e9, 1) == 1.6
assert round(numbers["1kg_baterias"] / 1e12, 1) == 1.6
kg_duration = next(b["duracao"] for b in info["blocos"] if b["nome"] == "escalada_1_kg")
assert 7 <= kg_duration <= 12, kg_duration
info["QA_numerico"] = numbers
(QA / "verificacao.json").write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")

selected = ["01_pergunta", "03_formulacao", "04_mAh_Ah", "06_15_2_Wh", "07_54_720_J",
            "10_substituicao", "12_0_6_ng", "13_rehook_1_g", "17_25_GWh", "18_bateria_15_2_Wh",
            "20_1_6_bilhao", "21_hipotese_massa", "22_100_milhoes_kg", "24_1_superporta_avioes",
            "25_1_kg_vezes_1000", "26_1_6_trilhao", "27b_cem_navios_vezes_dez",
            "28_1000_superporta_avioes", "29_sim_massa_minúscula"]
destination = MEDIA / "frames_envio_19"
destination.mkdir(exist_ok=True)
for i, name in enumerate(selected, 1):
    source = QA / "estados" / f"{name}.png"
    assert Image.open(source).size == (540, 960)
    shutil.copy2(source, destination / f"{i:02d}_{name}.png")
assert len(list(destination.glob("*.png"))) == 19
with zipfile.ZipFile(MEDIA / "frames_envio_19.zip", "w", zipfile.ZIP_DEFLATED) as zipped:
    for p in sorted(destination.glob("*.png")):
        zipped.write(p, p.name)
with zipfile.ZipFile(MEDIA / "frames_envio_19.zip") as zipped:
    assert len(zipped.namelist()) == 19 and zipped.testzip() is None
sheets([(p.stem, Image.open(p)) for p in sorted(destination.glob("*.png"))], "selecao_19")
panel = Image.new("RGB", (1080, 510), "#101827")
draw = ImageDraw.Draw(panel)
for i, (name, label) in enumerate([
    ("20_1_6_bilhao", "+1 g: 1,6 bilhão"),
    ("24_1_superporta_avioes", "mesma ordem de massa"),
    ("28_1000_superporta_avioes", "+1 kg: cerca de mil navios"),
    ("29_sim_massa_minúscula", "retorno à bateria"),
]):
    panel.paste(Image.open(QA / "estados" / f"{name}.png").convert("RGB").resize((270, 480)), (i * 270, 30))
    draw.text((i * 270 + 5, 5), label, font=FONT, fill="white")
panel.save(QA / "payoffs_principais.jpg", quality=94)
print(json.dumps(info, ensure_ascii=False))
