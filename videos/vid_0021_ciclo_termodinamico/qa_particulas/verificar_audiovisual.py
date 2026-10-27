"""QA da variante com partículas; --preview ou --final."""
import argparse
import importlib.util
import json
from pathlib import Path

import av
from PIL import Image, ImageDraw

UNIT = Path(__file__).resolve().parents[1]
QA = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "verificador_vid21", UNIT / "qa_sincronia/verificar_entrega.py")
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)

parser = argparse.ArgumentParser(description=__doc__)
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--preview", action="store_true")
group.add_argument("--final", action="store_true")
args = parser.parse_args()
width, height, fps, crf = (540, 960, 15, 23) if args.preview else (1080, 1920, 30, 14)
prefix = "vid_0021_particulas_preview" if args.preview else "vid_0021_particulas"
master, captioned = [UNIT / f"renders/{prefix}_{suffix}.mp4" for suffix in ("master", "legendado")]
report = {"files": [check.inspect(p, width, height, fps, crf) for p in (master, captioned)]}
assert check.packet_hash(master, "audio") == check.packet_hash(captioned, "audio")
root = "media_particulas_preview" if args.preview else "media_particulas_final"
visual = UNIT / f"{root}/videos/cena/{height}p{fps}/CicloTermodinamico021.mp4"
assert check.packet_hash(master, "video") == check.packet_hash(visual, "video")
original = UNIT / ("renders/vid_0021_preview_master.mp4" if args.preview else "renders/vid_0021_master.mp4")
assert check.packet_hash(master, "audio") == check.packet_hash(original, "audio")
timing = json.loads((UNIT / f"timing_particulas_{width}x{height}.json").read_text())
baseline = json.loads((UNIT / f"timing_{width}x{height}.json").read_text())
assert [e["cue"] for e in timing["events"]] == [e["cue"] for e in baseline["events"]]
assert max(abs(e["lag"]) for e in timing["events"]) < .1
max_change = max(abs(new["actual"]-old["actual"])
                 for new, old in zip(timing["events"], baseline["events"]))
assert max_change < .1
cues = check.read_cues(UNIT / "legenda.srt")
assert " ".join(" ".join(lines) for _, _, lines in cues).split() == (
    UNIT / "texto_narracao.txt").read_text(encoding="utf-8").split()

times = [2, 9, 12.5, 17, 21, 29.5, 36, 45, 55.5, 64.3, 71, 81.5,
         88.5, 94.6, 113, 124, 130, 136.7, 141.5, 147, 157.5, 161.5, 164, 167]
frames, index = [], 0
tag = "preview" if args.preview else "final"
with av.open(str(captioned)) as c:
    for frame in c.decode(video=0):
        if frame.time < times[index]:
            continue
        name = f"{tag}_{times[index]:05.1f}s.png"
        frame.to_image().save(QA / name)
        frames.append((name, float(frame.time)))
        index += 1
        if index == len(times):
            break
assert len(frames) == len(times)
for start in range(0, len(frames), 8):
    sheet = Image.new("RGB", (1080, 1010), "#050816")
    draw = ImageDraw.Draw(sheet)
    for j, (name, at) in enumerate(frames[start:start+8]):
        x, y = (j % 4)*270, (j // 4)*505
        sheet.paste(Image.open(QA / name).resize((270, 480)), (x, y+25))
        draw.text((x+8, y+7), f"{at:.2f} s", fill="white")
    sheet.save(QA / f"contato_{tag}_{start//8+1}.jpg")

if args.preview:
    clips = [[], [], []]
    starts = [29.5, 55.5, 88.5]
    with av.open(str(visual)) as c:
        for frame in c.decode(video=0):
            for clip, begin in zip(clips, starts):
                if begin <= frame.time < begin+1.6:
                    clip.append(frame.to_image().crop((375, 280, 475, 412)).resize((300, 396)))
            if frame.time >= starts[-1]+1.6:
                break
    film = []
    for i in range(min(map(len, clips))):
        sheet = Image.new("RGB", (900, 430), "#050816")
        draw = ImageDraw.Draw(sheet)
        for j, label in enumerate(("A: T inicial", "B: T = 4 T inicial", "C: T = 16 T inicial")):
            draw.text((j*300+12, 10), label, fill="white")
            sheet.paste(clips[j][i], (j*300, 34))
        film.append(sheet)
    film[0].save(QA / "movimento_estados.gif", save_all=True, append_images=film[1:],
                 duration=1000/fps, loop=0)

report.update(captions=len(cues), captions_text_integral="ok", full_decode="ok",
              audio_identical_to_previous_version="ok", master_video_copied="ok",
              max_visual_timing_change_s=max_change, frames=frames,
              alignment="Pausas do WAV e interpolação silábica, preservadas; revisão humana pendente")
(QA / f"audiovisual_{height}.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(f"QA {width}x{height}: OK; {len(cues)} legendas; variação máxima dos marcos {max_change:.4f}s.")
