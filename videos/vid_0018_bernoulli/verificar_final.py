"""QA da montagem: decode integral, voz, texto, cores e amostras visuais."""
import argparse
import hashlib
import importlib.util
import json
import re
import sys
import wave
from pathlib import Path

import av
import numpy as np
from PIL import Image, ImageDraw, ImageFont

UNIT = Path(__file__).resolve().parent
ROOT = UNIT.parents[1]
spec = importlib.util.spec_from_file_location("montar", ROOT / "videos/montar_legendado.py")
montar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(montar)
colors = montar.load_term_colors(UNIT / "legendas_cores.py")


def verificar_master(legendado):
    """Decode integral do master e identidade dos pacotes AAC nas duas entregas."""
    master = UNIT / "renders/vid_0018_bernoulli_final_master_limpo.mp4"
    native = UNIT / "media_final/videos/cena_final/1920p30/BernoulliFinal.mp4"
    results = []
    audio_hashes = []
    for path in (native, master, legendado):
        with av.open(str(path)) as source:
            video, audio = source.streams.video[0], source.streams.audio[0]
            assert (video.width, video.height, video.base_rate) == (1080, 1920, 30)
            assert video.codec_context.name == "h264" and audio.codec_context.name == "aac"
            with path.open("rb") as encoded:
                header = encoded.read(8_000_000).decode("latin1")
            if path == native:
                assert video.codec_context.pix_fmt == "yuv444p" and "qp=0" in header
            else:
                assert video.codec_context.pix_fmt == "yuv420p" and "crf=14.0" in header
            count = sum(1 for _ in source.decode(video)) if path == master else video.frames
            assert count == 5064, (path, count)
            results.append({"arquivo": str(path), "quadros": count,
                            "codec": "h264", "audio": "aac", "pixel": video.codec_context.pix_fmt})
        digest = hashlib.sha256()
        with av.open(str(path)) as source:
            for packet in source.demux(audio=0):
                if packet.size:
                    digest.update(bytes(packet))
        audio_hashes.append(digest.hexdigest())
    assert len(set(audio_hashes)) == 1, audio_hashes
    return {"arquivos": results, "pacotes_aac_sha256": audio_hashes[0],
            "aac_identico_nativo_master_legendado": True, "master_decode_integral": True}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path)
    parser.add_argument("--legendado", action="store_true")
    args = parser.parse_args()
    sync = json.loads((UNIT / "sync.json").read_text(encoding="utf-8"))
    timeline = json.loads((UNIT / "tempos_final.json").read_text(encoding="utf-8"))
    execution = json.loads((UNIT / "execucao_final.json").read_text(encoding="utf-8"))
    timing = json.loads((UNIT / "palavras_tempos.json").read_text(encoding="utf-8"))
    assert abs(execution["duracao_s"] - sync["video_s"]) < .001
    assert len(execution["cues"]) == len(sync["agenda"])
    for actual, planned in zip(execution["cues"], sync["agenda"]):
        assert abs(actual["inicio"] - planned["inicio"]) < .001
        assert abs(actual["fim"] - planned["fim"]) < .001
    cues = montar.read_cues(UNIT / "legenda.srt")
    text = (UNIT / "texto_narracao.txt").read_text(encoding="utf-8").split()
    assert " ".join(" ".join(lines) for _, _, lines in cues).split() == text
    assert [word["texto"] for word in timing["palavras"]] == text
    assert hashlib.sha256((UNIT / "audio/narracao_final.wav").read_bytes()).hexdigest() == sync["audio_sha256"]
    targets = [(f'fala_{i:02d}', (a + b) / 2) for i, (a, b, _) in enumerate(cues, 1)]
    targets += [(event["nome"], event["tempo"] + .08) for event in execution["eventos"] if event["tipo"] in ("estado", "extra")]
    targets += [(name, at) for name, at in timeline["estados"].items() if name.startswith("morph_")]
    targets.sort(key=lambda row: row[1])
    with av.open(str(args.video)) as source:
        stream = source.streams.video[0]
        width, height, fps = stream.width, stream.height, float(stream.base_rate)
        assert (width, height, fps) in ((540, 960, 15), (1080, 1920, 30))
        assert len(source.streams.audio) == 1
        duration = float(stream.duration * stream.time_base)
        assert abs(duration - sync["video_s"]) < .12
        assert cues[-1][1] < duration
        font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", round(29 * width / 540))
        for _, _, lines in cues:
            assert len(lines) <= 2
            assert max(font.getlength(line) for line in lines) <= 440 * width / 540 + 2
        folder = UNIT / ("qa_final" if args.legendado else "qa_sync_preview")
        folder.mkdir(exist_ok=True)
        n, index, busy_max = 0, 0, 0.0
        cue_index = 0
        for frame in source.decode(stream):
            n += 1
            at = float(frame.pts * frame.time_base)
            while index < len(targets) and at >= targets[index][1]:
                name, requested = targets[index]
                while cue_index < len(cues) and cues[cue_index][1] <= at:
                    cue_index += 1
                lines = cues[cue_index][2] if cue_index < len(cues) and cues[cue_index][0] <= at else None
                if not args.legendado:
                    pixels = frame.to_ndarray(format="rgb24")
                    roi = pixels[round(735 * width / 540):round(855 * width / 540)].astype(np.int16)
                    busy = float((np.max(np.abs(roi - np.array([5, 8, 22])), axis=2) > 18).mean())
                    busy_max = max(busy_max, busy)
                    assert busy < .01, (name, busy)
                picture = frame.to_image() if args.legendado else montar.draw_caption(frame, lines, font, width, height, "standard", colors)
                picture.save(folder / f"{name}.png")
                index += 1
        assert index == len(targets)
        assert n == stream.frames
        pixel_format = stream.codec_context.pix_fmt
    with wave.open(str(UNIT / "audio/narracao_final.wav")) as wav:
        rate, channels = wav.getframerate(), wav.getnchannels()
        reference = np.frombuffer(wav.readframes(wav.getnframes()), dtype=np.int16).reshape(-1, channels).mean(1) / 32768
    chunks = []
    with av.open(str(args.video)) as source:
        audio_codec = source.streams.audio[0].codec_context
        codec_padding = (audio_codec.frame_size or 1024) / audio_codec.sample_rate
        resampler = av.AudioResampler(format="fltp", layout="mono", rate=rate)
        for frame in source.decode(audio=0):
            chunks.extend(out.to_ndarray().reshape(-1) for out in resampler.resample(frame))
        chunks.extend(out.to_ndarray().reshape(-1) for out in resampler.resample(None))
    audio = np.concatenate(chunks)
    # AAC do Manim inclui um quadro de priming; menor que um quadro de vídeo.
    assert codec_padding < 1 / fps
    start = round((sync["audio_offset_s"] + codec_padding) * rate)
    observed = audio[start:start + len(reference)]
    assert len(observed) >= len(reference) - round(rate * .04), "Voz truncada"
    length = min(len(observed), len(reference))
    step = round(rate * .01)
    length = length // step * step
    rms = lambda x: np.sqrt(np.mean(x[:length].reshape(-1, step) ** 2, axis=1))
    correlation = float(np.corrcoef(rms(reference), rms(observed))[0, 1])
    assert correlation > .99, correlation
    font_small = ImageFont.truetype(str(ROOT / "assets/fonts/inter/Inter-Regular.ttf"), 13)
    for start in range(0, len(targets), 6):
        page = Image.new("RGB", (810, 1020), "#050816")
        draw = ImageDraw.Draw(page)
        for i, (name, at) in enumerate(targets[start:start + 6]):
            x, y = i % 3 * 270, i // 3 * 510
            with Image.open(folder / f"{name}.png") as picture:
                page.paste(picture.resize((270, 480), Image.Resampling.LANCZOS), (x, y + 30))
            draw.text((x + 5, y + 8), f"{at:.2f}s · {name}", font=font_small, fill="white")
        page.save(folder / f"contato_{start // 6 + 1:02d}.jpg", quality=92)
    data = {"video": str(args.video.resolve()), "resolucao": [width, height], "fps": fps,
            "duracao_s": duration, "quadros_decodificados": n, "formato_pixel": pixel_format,
            "cues_srt": len(cues), "palavras": len(text), "amostras": len(targets),
            "correlacao_envoltoria_audio": correlation, "audio_sha256": sync["audio_sha256"],
            "priming_aac_s": codec_padding,
            "voz_velocidade": 1.0, "cores": colors, "ocupacao_faixa_legenda_base": busy_max,
            "metodo_tempos": timing["metodo"], "pontos_visuais": sync["pontos_visuais"]}
    if args.legendado:
        data["validacao_master"] = verificar_master(args.video)
    (folder / "relatorio.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in data.items() if k not in ("cores", "pontos_visuais")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
