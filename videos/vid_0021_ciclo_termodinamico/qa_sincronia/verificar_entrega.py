"""Conferência técnica e frames dos quatro arquivos montados do VID21."""
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re
import sys

import av
from PIL import Image, ImageDraw

UNIT = Path(__file__).resolve().parents[1]
QA = Path(__file__).resolve().parent
sys.path.insert(0, str(UNIT.parents[1] / "videos"))
from montar_legendado import read_cues


def packet_hash(path, kind):
    result = hashlib.sha256()
    with av.open(str(path)) as c:
        stream = getattr(c.streams, kind)[0]
        for packet in c.demux(stream):
            result.update(bytes(packet))
    return result.hexdigest()


def inspect(path, width, height, fps, expected_crf):
    with av.open(str(path)) as c:
        v, a = c.streams.video[0], c.streams.audio[0]
        assert (v.width, v.height, float(v.average_rate)) == (width, height, fps)
        assert v.codec_context.name == "h264" and v.codec_context.format.name == "yuv420p"
        assert a.codec_context.name == "aac" and a.codec_context.sample_rate == 44100
        raw = b"".join(bytes(p) for _, p in zip(range(4), c.demux(v)))
        crf = float(re.search(rb"crf=([0-9.]+)", raw).group(1))
        assert crf == expected_crf
        audio_duration = float(a.duration * a.time_base)
        video_reported = float(v.duration * v.time_base)
    with av.open(str(path)) as c:
        previous, first, count = None, None, 0
        for frame in c.decode(video=0):
            at = float(frame.time)
            assert previous is None or abs(at - previous - 1/fps) < .0001
            previous = at
            first = at if first is None else first
            count += 1
        assert abs(first) < .0001
        end = previous + 1/fps
        assert abs(end - audio_duration) < 1/fps + .003
    return dict(file=str(path), width=width, height=height, fps=fps, crf=crf,
                decoded_frames=count, video_end_s=end, reported_video_duration_s=video_reported,
                audio_duration_s=audio_duration, av_end_difference_s=end-audio_duration,
                full_decode="ok", cfr="ok")


def main():
    report = {"files": []}
    for preview in (True, False):
        width, height, fps, crf = (540, 960, 15, 23) if preview else (1080, 1920, 30, 14)
        prefix = "vid_0021_preview" if preview else "vid_0021"
        master = UNIT / f"renders/{prefix}_master.mp4"
        legendado = UNIT / f"renders/{prefix}_legendado.mp4"
        for path in (master, legendado):
            report["files"].append(inspect(path, width, height, fps, crf))
            print(f"QA: {path.name} OK", flush=True)
        assert packet_hash(master, "audio") == packet_hash(legendado, "audio")
        root = "media_sincronizado" if preview else "media_final"
        visual = UNIT / f"{root}/videos/cena/{height}p{fps}/CicloTermodinamico021.mp4"
        assert packet_hash(master, "video") == packet_hash(visual, "video")
        timing = json.loads((UNIT / f"timing_{width}x{height}.json").read_text())
        assert max(e["lag"] for e in timing["events"]) < .1

    cues = read_cues(UNIT / "legenda.srt")
    text = (UNIT / "texto_narracao.txt").read_text(encoding="utf-8")
    assert " ".join(" ".join(lines) for _, _, lines in cues).split() == text.split()
    assert cues[-1][1] <= 167.76
    report.update(captions=len(cues), last_caption_end_s=cues[-1][1],
                  video_copied_to_master="ok", audio_identical_master_legendado="ok",
                  visual_cues_lag_under_100ms="ok", captions_text_integral="ok",
                  alignment_method="Pausas do WAV; tempos de palavras interpolados, sem ASR",
                  human_review="pendente")
    # Valores adimensionais em unidades de P0 V0; sinais e resultado do briefing.
    states = [(1, 1), (4, 1), (4, 4)]
    energy = [Fraction(3, 2)*p*v for v, p in states]
    works = [Fraction(3), Fraction(0), Fraction(-15, 2)]
    dus = [energy[(i+1) % 3]-energy[i] for i in range(3)]
    heats = [du+w for du, w in zip(dus, works)]
    assert heats == [Fraction(15, 2), Fraction(18), Fraction(-30)]
    assert sum(q for q in heats if q > 0) == Fraction(51, 2)
    assert sum(dus) == 0 and sum(works) == sum(heats) == Fraction(-9, 2)
    report["physics_results"] = "ok"

    times = [2, 9, 12.5, 17, 21, 29.5, 36, 45, 55.5, 64.3, 71, 81.5,
             88.5, 94.6, 113, 124, 130, 136.7, 141.5, 147, 157.5, 161.5, 164, 167]
    frames, index = [], 0
    with av.open(str(UNIT / "renders/vid_0021_legendado.mp4")) as c:
        for frame in c.decode(video=0):
            if frame.time < times[index]:
                continue
            name = f"final_{times[index]:05.1f}s.png"
            frame.to_image().save(QA / name)
            frames.append((name, float(frame.time)))
            index += 1
            if index == len(times):
                break
    assert index == len(times)
    for start in range(0, len(frames), 8):
        sheet = Image.new("RGB", (1080, 1010), "#050816")
        draw = ImageDraw.Draw(sheet)
        for j, (name, at) in enumerate(frames[start:start+8]):
            x, y = (j % 4)*270, (j // 4)*505
            sheet.paste(Image.open(QA / name).resize((270, 480)), (x, y+25))
            draw.text((x+8, y+7), f"{at:.2f} s", fill="white")
        sheet.save(QA / f"contato_final_{start//8+1}.jpg")
    report["frames"] = frames
    (QA / "relatorio_tecnico.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("QA técnico completo; revisão humana pendente.", flush=True)


if __name__ == "__main__":
    main()
