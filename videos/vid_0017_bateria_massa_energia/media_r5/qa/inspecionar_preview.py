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


def sheets(items, prefix):
    for start in range(0, len(items), 8):
        canvas = Image.new("RGB", (1080, 1020), "#101827")
        draw = ImageDraw.Draw(canvas)
        for i, (label, im) in enumerate(items[start:start + 8]):
            x, y = (i % 4) * 270, (i // 4) * 510
            canvas.paste(im.convert("RGB").resize((270, 480)), (x, y + 30))
            draw.text((x + 5, y + 5), label[:29], font=FONT, fill="white")
        canvas.save(QA / f"{prefix}_{start // 8 + 1:02d}.jpg", quality=93)


states = sorted((QA / "estados").glob("*.png"))
sheets([(p.stem, Image.open(p)) for p in states], "estados")
if "--complete" not in sys.argv:
    print(json.dumps({"estados": len(states)}))
    raise SystemExit

meta = json.loads((MEDIA / "estados_preview.json").read_text(encoding="utf-8"))
fps = 15
clip_frames = []
prefix = [0]
for path in meta["partial_files"]:
    assert path is not None, "QA completo exige o preview completo"
    with av.open(path) as container:
        video = container.streams.video[0]
        count = video.frames or sum(1 for _ in container.decode(video))
        clip_frames.append(count)
        prefix.append(prefix[-1] + count)

settled = {}
for state in meta["estados"]:
    idx = state["play_index"]
    settled[state["nome"]] = round((prefix[idx] + clip_frames[idx] / 2) / fps, 3)
blocks = []
for block in meta["blocos"]:
    start, end = prefix[block["play_start"]] / fps, prefix[block["play_end"]] / fps
    blocks.append({"nome": block["nome"], "inicio": round(start, 3),
                   "fim": round(end, 3), "duracao": round(end - start, 3)})

names = ["ng_recua_para_rehook", "25_GWh", "contagem_uma_para_quatro",
         "contagem_quatro_para_dezesseis", "grade_para_1_6_bilhao",
         "divisao_para_100_milhoes_kg", "25_GWh_para_cidade",
         "SP_2_h", "SP_4_h", "SP_6_h", "SP_8_h", "cidade_recua_bateria_original"]
events = {e["nome"]: e for e in meta["transicoes"]}
requests = sorted((prefix[events[name]["play_index"]] / fps + events[name]["duration"] / 2 + delta, name)
                  for name in names for delta in (-0.3, 0, 0.3, 0.55))
movie = MEDIA / "videos/cena/960p15/BateriaMassaEnergia.mp4"
samples = []
with av.open(str(movie)) as container:
    video = container.streams.video[0]
    info = {"resolucao": [video.width, video.height], "fps_nominal": str(video.base_rate),
            "duracao_s": container.duration / av.time_base, "audio": len(container.streams.audio),
            "bytes": movie.stat().st_size, "estados": len(states)}
    cursor = count = 0
    for frame in container.decode(video):
        count += 1
        t = float(frame.pts * frame.time_base)
        while cursor < len(requests) and t >= requests[cursor][0]:
            target, name = requests[cursor]
            samples.append((f"{name[:18]} {t:.2f}s", frame.to_image()))
            cursor += 1
    assert count == prefix[-1], (count, prefix[-1])
    info["frames"] = count
sheets(samples, "movimento")

unchanged = []
for p in states:
    if int(p.name[:2]) <= 12:
        earlier = MEDIA.parent / "media_r4/qa/estados" / p.name
        assert p.read_bytes() == earlier.read_bytes(), f"Mudança na primeira parte: {p.name}"
        unchanged.append(p.stem)

info.update({"estados_iniciais_identicos_r4": unchanged,
             "estados_tempo_MP4": settled, "blocos_tempo_MP4": blocks,
             "transicoes_inspecionadas": names, "quadros_de_movimento": len(samples),
             "numeros_verificados": meta["numeros_verificados"], "fonte_SP": meta["fonte_SP"]})
previous = json.loads((MEDIA.parent / "media_r4/qa/verificacao.json").read_text(encoding="utf-8"))
info["duracao_anterior_s"] = previous["duracao_s"]
(QA / "verificacao.json").write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding="utf-8")

source = meta["fonte_SP"]
(QA / "fonte_SP.md").write_text(
    f'# Comparação de energia — município de São Paulo\n\n'
    f'{source["instituicao"]}. {source["titulo"]}, p. {source["pagina"]}.\n\n'
    f'[Documento oficial]({source["url"]})\n\n'
    'Consumo elétrico municipal em 2023: 26,91 TWh.\n\n'
    '26,91 × 1000 / 8760 = 3,071918 GWh/h.\n\n'
    '24,965422 GWh / 3,071918 GWh/h = 8,126982 h ≈ 8 horas.\n\n'
    'Comparação com o consumo elétrico médio anual, sem modelar rede ou perdas.\n', encoding="utf-8")

selected = ["01_pergunta", "03_formulacao", "04_mAh_Ah", "06_15_2_Wh", "07_54_720_J",
            "08_relacao_massa_energia", "10_substituicao", "12_0_6_ng", "13_rehook_1_g",
            "17_25_GWh", "18_bateria_15_2_Wh", "19b_dezesseis_baterias", "20_1_6_bilhao",
            "21_hipotese_massa", "22_100_milhoes_kg", "23_skyline_SP_0_h", "24_8_horas_SP",
            "25_retorno_0_6_ng", "26_CTA"]
destination = MEDIA / "frames_envio_19"
destination.mkdir(exist_ok=True)
for i, name in enumerate(selected, 1):
    p = QA / "estados" / f"{name}.png"
    assert Image.open(p).size == (540, 960)
    shutil.copy2(p, destination / f"{i:02d}_{name}.png")
assert len(list(destination.glob("*.png"))) == 19
with zipfile.ZipFile(MEDIA / "frames_envio_19.zip", "w", zipfile.ZIP_DEFLATED) as zipped:
    for p in sorted(destination.glob("*.png")):
        zipped.write(p, p.name)
with zipfile.ZipFile(MEDIA / "frames_envio_19.zip") as zipped:
    assert len(zipped.namelist()) == 19 and zipped.testzip() is None

panel = Image.new("RGB", (1080, 510), "#101827")
draw = ImageDraw.Draw(panel)
for i, (name, label) in enumerate([
    ("20_1_6_bilhao", "quantidade de baterias"), ("22_100_milhoes_kg", "massa no modelo"),
    ("24_8_horas_SP", "consumo elétrico médio"), ("26_CTA", "retorno à bateria e CTA"),
]):
    panel.paste(Image.open(QA / "estados" / f"{name}.png").convert("RGB").resize((270, 480)), (270 * i, 30))
    draw.text((270 * i + 5, 5), label, font=FONT, fill="white")
panel.save(QA / "payoffs_principais.jpg", quality=94)

phone = Image.new("RGB", (1080, 640), "#101827")
for i, name in enumerate(("20_1_6_bilhao", "24_8_horas_SP", "26_CTA")):
    phone.paste(Image.open(QA / "estados" / f"{name}.png").convert("RGB").resize((360, 640)), (360 * i, 0))
phone.save(QA / "leitura_360px.jpg", quality=94)
print(json.dumps({k: info[k] for k in ("duracao_anterior_s", "duracao_s", "frames", "audio",
      "estados", "blocos_tempo_MP4", "estados_tempo_MP4", "numeros_verificados")}, ensure_ascii=False))
