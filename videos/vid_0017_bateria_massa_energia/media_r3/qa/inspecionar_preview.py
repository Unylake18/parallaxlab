from pathlib import Path
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
        group = items[start:start + batch]
        canvas = Image.new("RGB", (4 * 270, 2 * 510), "#101827")
        draw = ImageDraw.Draw(canvas)
        for i, (label, im) in enumerate(group):
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
windows = [
    ("carga_em_quatro_etapas", [-0.7, -0.25, 0.25, 0.7]),
    ("dados_saindo_da_bateria", [-0.5, -0.15, 0.2, 0.55]),
    ("convergencia_V_e_Ah", [-0.3, 0, 0.3]),
    ("produto_para_15_2_Wh", [-0.5, -0.2, 0.2, 0.5]),
    ("conversor_Wh_J", [-0.4, 0, 0.4]),
    ("etiqueta_J_alimenta_delta_E", [-0.4, 0, 0.4]),
    ("c_quadrado_para_denominador", [-0.6, -0.2, 0.2, 0.6]),
    ("substituicao_energia_e_c", [-0.5, -0.15, 0.2, 0.55]),
    ("regua_construida_kg_ate_ng", [-1, -0.4, 0.2, 0.8]),
    ("ng_recua_para_rehook", [-0.4, 0, 0.4]),
    ("inversao_massa_energia", [-0.4, 0, 0.4]),
    ("25_GWh_alimenta_divisao", [-0.5, -0.15, 0.2, 0.55]),
    ("divisao_para_10_8_kg", [-0.55, -0.2, 0.2, 0.6]),
    ("uma_bateria_para_quatro", [-0.5, 0, 0.5]),
    ("quatro_para_grade", [-0.4, 0, 0.4]),
    ("kg_por_extenso_e_grade_ampliada", [-0.5, -0.15, 0.2, 0.55]),
]
transitions = {t["nome"]: t["t"] for t in meta["transicoes"]}
requests = sorted((transitions[name] + delta, name, delta)
                  for name, offsets in windows for delta in offsets)
sampled = []
with av.open(str(movie)) as container:
    stream = container.streams.video[0]
    info = {"resolucao": [stream.width, stream.height],
            "fps_nominal": str(stream.base_rate),
            "duracao_s": float(container.duration / av.time_base),
            "audio": len(container.streams.audio), "bytes": movie.stat().st_size,
            "estados": len(states), "transicoes_amostradas": len(windows)}
    cursor = 0
    count = 0
    for fr in container.decode(stream):
        count += 1
        t = float(fr.pts * fr.time_base)
        while cursor < len(requests) and t >= requests[cursor][0]:
            target, name, offset = requests[cursor]
            sampled.append((f"{name[:18]} {t:.2f}s", fr.to_image()))
            cursor += 1
    info["frames"] = count
sheets(sampled, "movimento")
(QA / "verificacao.json").write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")

# Exatamente 19 arquivos para o limite de anexos informado pelo usuário.
selected = [
    "01_pergunta", "03_formulacao", "04_mAh_Ah", "05_V_Ah", "06_15_2_Wh",
    "06b_conversor_Wh_J", "07_54_720_J", "08_relacao_massa_energia",
    "10_substituicao", "12_0_6_ng", "13_rehook_1_g", "14_1_g_kg",
    "17_25_GWh", "19_divisao_bateria", "20a_uma_bateria",
    "20c_grade_media", "20d_grade_ampliada", "21_100_mil_toneladas",
    "23_fechamento_sintese",
]
destination = MEDIA / "frames_envio_19"
destination.mkdir(exist_ok=True)
for i, name in enumerate(selected, 1):
    shutil.copy2(QA / "estados" / f"{name}.png", destination / f"{i:02d}_{name}.png")
assert len(list(destination.glob("*.png"))) == 19
with zipfile.ZipFile(MEDIA / "frames_envio_19.zip", "w", zipfile.ZIP_DEFLATED) as zipped:
    for p in sorted(destination.glob("*.png")):
        zipped.write(p, p.name)
print(json.dumps(info, ensure_ascii=False))
