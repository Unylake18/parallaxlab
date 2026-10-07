"""Extrai os estados marcados e decodifica o preview inteiro para QA técnico."""
import json
from pathlib import Path

import av
from PIL import Image, ImageDraw, ImageFont

UNIT = Path(__file__).resolve().parent
ROOT = UNIT.parents[1]
VIDEO = UNIT / "media/videos/cena/960p15/vid_0015_preview_v2_silencioso.mp4"
OUT = UNIT / "frames_preview_v2"
OUT.mkdir(exist_ok=True)
data = json.loads((UNIT / "qa_estados_v2.json").read_text(encoding="utf-8"))
states = data["estados"]
images = []
motion_times = [66.1, 66.6, 70.2, 70.7, 81.9, 82.9, 124.1, 124.8, 170.9, 172.0]
motion_images = []
target = 0
frame_count = 0
last_time = 0
intervals = []
with av.open(str(VIDEO)) as container:
    stream = container.streams.video[0]
    report = {"arquivo": str(VIDEO), "largura": stream.width, "altura": stream.height,
              "fps": str(stream.base_rate), "fps_media": float(stream.average_rate), "codec": stream.codec_context.name,
              "audio_streams": len(container.streams.audio)}
    for frame in container.decode(stream):
        if frame_count:
            intervals.append(float(frame.time) - last_time)
        last_time = float(frame.time)
        frame_count += 1
        if len(motion_images) < len(motion_times) and last_time >= motion_times[len(motion_images)]:
            motion_image = frame.to_image()
            motion_image.save(OUT / f"movimento_{len(motion_images)+1:02d}.png")
            motion_images.append(motion_image)
        if target < len(states) and last_time >= states[target]["tempo_s"]:
            img = frame.to_image()
            name = f"{target+1:02d}_{states[target]['estado']}.png"
            img.save(OUT / name)
            images.append(img)
            states[target]["frame_s"] = round(last_time, 3)
            states[target]["arquivo_frame"] = name
            target += 1
    report["quadros_decodificados"] = frame_count
    report["duracao_s"] = round(last_time + 1/float(stream.base_rate), 3)
    report["intervalo_min_s"] = min(intervals)
    report["intervalo_max_s"] = max(intervals)
report["estados_extraidos"] = target
report["estados"] = states
font = ImageFont.truetype(str(ROOT / "assets/fonts/inter/Inter-Medium.ttf"), 18)
for start in range(0, len(images), 4):
    sheet = Image.new("RGB", (1080, 2000), "#050816")
    draw = ImageDraw.Draw(sheet)
    for i, img in enumerate(images[start:start+4]):
        x, y = (i % 2)*540, (i // 2)*1000
        sheet.paste(img, (x, y+40))
        state = states[start+i]
        draw.text((x+8, y+2), f"{start+i+1:02d}  {state['frame_s']:.2f} s", font=font, fill="#35D9FF")
        draw.text((x+8, y+19), state["estado"][:34], font=font, fill="white")
    sheet.save(OUT / f"contato_{start//4+1:02d}.jpg", quality=93)
for start in range(0, len(motion_images), 4):
    sheet = Image.new("RGB", (1080, 2000), "#050816")
    draw = ImageDraw.Draw(sheet)
    for i, img in enumerate(motion_images[start:start+4]):
        x, y = (i % 2)*540, (i // 2)*1000
        sheet.paste(img, (x, y+40))
        draw.text((x+8, y+8), f"Transição · {motion_times[start+i]:.1f} s", font=font, fill="#35D9FF")
    sheet.save(OUT / f"movimento_contato_{start//4+1:02d}.jpg", quality=93)
report["quadros_adicionais_de_transicoes"] = motion_times
(UNIT / "qa_tecnico_v2.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({key: value for key, value in report.items() if key != "estados"}, ensure_ascii=False))
assert (report["largura"], report["altura"], report["fps"], report["audio_streams"]) == (540, 960, "15", 0)
# A concatenação Manim arredonda PTS nas fronteiras dos trechos. Conferir a taxa
# nominal e os intervalos reais, sem exigir igualdade exata da fração média.
assert abs(report["fps_media"] - 15) < 0.001
assert max(abs(interval - 1/15) for interval in intervals) < 0.001
assert target == len(states)
