"""QA local: vídeo inteiro, áudio, SRT e amostras de sincronia/legendas.

Uso: python verificar_montagem.py MEDIA_DIR ARQUIVO.mp4 [--legendado]
"""
import argparse
from pathlib import Path
import hashlib
import importlib.util
import json
import re
import sys
import zipfile
import wave
from numeros_legenda import converter

import av
import numpy as np
from PIL import Image, ImageDraw, ImageFont

UNIT = Path(__file__).resolve().parent
ROOT = UNIT.parents[1]
spec = importlib.util.spec_from_file_location("montar", ROOT / "videos/montar_legendado.py")
montar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(montar)

parser = argparse.ArgumentParser()
parser.add_argument("media", type=Path)
parser.add_argument("video", type=Path)
parser.add_argument("--legendado", action="store_true")
parser.add_argument("--alta-qualidade", action="store_true")
args = parser.parse_args()
qa = args.media / ("qa_final" if args.legendado else "qa_preview")
qa.mkdir(exist_ok=True)
meta = json.loads((args.media / "estados_preview.json").read_text(encoding="utf-8"))
sync = json.loads((UNIT / "sync.json").read_text(encoding="utf-8"))
cues = montar.read_cues(UNIT / "legenda.srt")
timing = json.loads((UNIT / "palavras_tempos.json").read_text(encoding="utf-8"))
assert hashlib.sha256((UNIT / "audio/narracao_final.wav").read_bytes()).hexdigest() == sync["audio_sha256"]

with av.open(str(args.video)) as video:
    stream = video.streams.video[0]
    width, height, fps = stream.width, stream.height, float(stream.average_rate)
    assert (width, height, round(fps)) in ((540, 960, 15), (1080, 1920, 30))
    assert len(video.streams.audio) == 1
    duration = video.duration / av.time_base
    assert abs(duration - sync["video_s"]) < 0.12
    pixel_format = stream.codec_context.pix_fmt


def x264_options(path):
    with av.open(str(path)) as container:
        for packet in container.demux(video=0):
            data = bytes(packet)
            if b"x264" in data:
                info = data[data.index(b"x264"):].decode("ascii", errors="ignore")
                return dict(re.findall(r"\b(rc|crf|qp|subme|chroma_qp_offset)=([\w.]+)", info[:1800]))
    raise AssertionError("Metadados do encoder x264 ausentes")


quality = {}
if args.alta_qualidade:
    assert meta["resolucao"] == [1080, 1920] and meta["fps"] == 30
    source = meta["partial_files"][0]
    master_options = x264_options(source)
    with av.open(source) as native:
        assert native.streams.video[0].codec_context.pix_fmt == "yuv444p"
    assert master_options["qp"] == "0" and master_options["rc"] == "cqp"
    delivery_options = x264_options(args.video)
    assert delivery_options["crf"] == "14.0" and pixel_format == "yuv420p"
    quality = {"master_yuv444p_sem_perdas_de_compressao": master_options,
               "entrega_yuv420p": delivery_options, "render_nativo": [1080, 1920]}
    archival = UNIT / "renders/vid_0017_bateria_massa_energia_legendado_sem_perdas_v2.mp4"
    archival_options = x264_options(archival)
    assert archival_options["qp"] == "0" and archival_options["rc"] == "cqp"
    with av.open(str(archival)) as container:
        stream = container.streams.video[0]
        assert (stream.width, stream.height, stream.average_rate) == (1080, 1920, 30)
        assert stream.codec_context.pix_fmt == "yuv444p"
        assert sum(1 for frame in container.decode(video=0)) == 3339

    def audio_packets_hash(path):
        digest = hashlib.sha256()
        with av.open(str(path)) as container:
            for packet in container.demux(audio=0):
                if packet.dts is not None:
                    digest.update(bytes(packet))
        return digest.hexdigest()

    archival_audio = audio_packets_hash(archival)
    assert archival_audio == audio_packets_hash(args.video)
    quality["legendado_sem_perdas"] = {"arquivo": str(archival.resolve()),
        "encoder": archival_options, "quadros_decodificados": 3339,
        "pacotes_audio_sha256": archival_audio}
assert cues[-1][1] < duration and cues[0][0] >= 0
assert all(len(lines) <= 2 for _, _, lines in cues)
approved = (UNIT / "texto_narracao.txt").read_text(encoding="utf-8").split()
assert [p["texto"] for p in timing["palavras"]] == approved
display, _, _ = converter(approved, [p["inicio_s"] for p in timing["palavras"]],
                         [p["fim_s"] for p in timing["palavras"]])
assert " ".join(" ".join(lines) for _, _, lines in cues).split() == " ".join(display).split()
assert "Siga o Parallax Lab." in " ".join(" ".join(lines) for _, _, lines in cues)

frames_per_clip, prefix = [], [0]
for p in meta["partial_files"]:
    assert p is not None
    with av.open(p) as clip:
        n = clip.streams.video[0].frames
    frames_per_clip.append(n)
    prefix.append(prefix[-1] + n)
assert abs(prefix[-1] / fps - sync["video_s"]) <= 1 / fps + 0.001
for item in meta["sincronizacao"]["execucao"]:
    cue = item["cue"]
    expected = round(sync["agenda"][cue]["inicio"] * round(fps))
    assert prefix[item["play_index"]] == expected, ("Desvio acumulado", cue, prefix[item["play_index"]], expected)

settled = {s["nome"]: (prefix[s["play_index"]] + frames_per_clip[s["play_index"]] / 2) / fps
           for s in meta["estados"]}
requests = [(name, t) for name, t in settled.items()]
requests += [("voz_" + name, t + sync["audio_offset_s"] + .22) for name, t in sync["anchors"] if name != "fim"]
# Amostras antes/durante/depois dos principais resultados e do CTA.
requests += [("critico_" + str(t), t) for t in (31.9, 54.4, 67.3, 76.6, 84.2, 91.55, 100.8, 107.95, 108.28, 109.32, 110.6)]
requests.sort(key=lambda a: a[1])
font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", round(29 * width / 540))
captions = []
selected = ["01_pergunta", "03_formulacao", "04_mAh_Ah", "06_15_2_Wh", "07_54_720_J",
            "08_relacao_massa_energia", "10_substituicao", "12_0_6_ng", "13_rehook_1_g",
            "17_25_GWh", "18_bateria_15_2_Wh", "19b_dezesseis_baterias", "20_1_6_bilhao",
            "21_hipotese_massa", "22_100_milhoes_kg", "23_skyline_SP_0_h", "24_8_horas_SP",
            "25_retorno_0_6_ng", "26_CTA"]
frames_dir = args.media / "frames_final_19"
if args.legendado:
    frames_dir.mkdir(exist_ok=True)
cursor = total = 0
with av.open(str(args.video)) as video:
    for frame in video.decode(video=0):
        total += 1
        at = float(frame.pts * frame.time_base)
        while cursor < len(requests) and at >= requests[cursor][1]:
            name, target = requests[cursor]
            lines = next((lines for start, end, lines in cues if start <= at < end), None)
            im = frame.to_image() if args.legendado else montar.draw_caption(frame, lines, font, width, height, "standard")
            # As miniaturas mantêm a mesma proporção para inspeção entre resoluções.
            captions.append((name, at, im.resize((270, 480))))
            if name.startswith("critico_") or name in ("20_1_6_bilhao", "22_100_milhoes_kg", "24_8_horas_SP", "26_CTA"):
                im.save(qa / f"{name}.png")
            if args.legendado and name in selected:
                im.save(frames_dir / f"{selected.index(name)+1:02d}_{name}.png")
            cursor += 1
assert cursor == len(requests)
assert total == prefix[-1], (total, prefix[-1])
if args.legendado:
    paths = sorted(frames_dir.glob("*.png"))
    assert len(paths) == 19
    with zipfile.ZipFile(args.media / "frames_final_19.zip", "w", zipfile.ZIP_DEFLATED) as zipped:
        for path in paths:
            zipped.write(path, path.name)
    with zipfile.ZipFile(args.media / "frames_final_19.zip") as zipped:
        assert len(zipped.namelist()) == 19 and zipped.testzip() is None

label_font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 15)
for k in range(0, len(captions), 8):
    sheet = Image.new("RGB", (1080, 1020), "#101827")
    draw = ImageDraw.Draw(sheet)
    for i, (name, t, im) in enumerate(captions[k:k+8]):
        x, y = i % 4 * 270, i // 4 * 510
        sheet.paste(im, (x, y + 30))
        draw.text((x + 4, y + 4), f"{name[:24]} {t:.2f}", font=label_font, fill="white")
    sheet.save(qa / f"painel_{k//8+1:02d}.jpg", quality=93)

audio_frames = 0
audio_end = 0
audio_parts = []
with av.open(str(args.video)) as audio:
    stream = audio.streams.audio[0]
    codec, rate, channels = stream.codec_context.name, stream.rate, stream.codec_context.channels
    for frame in audio.decode(audio=0):
        audio_frames += frame.samples
        audio_parts.append(frame.to_ndarray().mean(axis=0))
        audio_end = max(audio_end, float(frame.pts * frame.time_base) + frame.samples / frame.sample_rate)
assert abs(audio_end - (sync["audio_s"] + sync["audio_offset_s"])) < .08
assert audio_end <= prefix[-1] / fps + .05

def envelope(signal, sample_rate):
    window = round(sample_rate * .01)
    return np.sqrt(np.mean(signal[:len(signal)//window*window].reshape(-1, window) ** 2, axis=1))

decoded = np.concatenate(audio_parts)
env_final = envelope(decoded, rate)
with wave.open(str(UNIT / "audio/narracao_final.wav")) as wav:
    original = np.frombuffer(wav.readframes(wav.getnframes()), dtype="<i2").astype(float)
    original = original.reshape(-1, wav.getnchannels()).mean(axis=1) / 32768
    env_original = envelope(original, wav.getframerate())
offset_bins = round(sync["audio_offset_s"] / .01)
# AAC introduz priming de aproximadamente 21 ms. Medir o deslocamento real,
# exigindo a mesma envoltória e diferença inferior a um quadro de 30 fps.
matches = []
for lag in range(offset_bins - 3, offset_bins + 4):
    size = min(len(env_original), len(env_final) - lag)
    value = float(np.corrcoef(env_original[:size], env_final[lag:lag+size])[0,1])
    matches.append((value, lag))
corr, measured_lag = max(matches)
assert corr > .99, ("Áudio diferente da fonte ou deslocamento incorreto", corr)
assert abs(measured_lag * .01 - sync["audio_offset_s"]) < 1/30
active = env_final > .03 * max(abs(decoded))
spoken_start = float(np.flatnonzero(active)[0] * .01)
spoken_end = float((np.flatnonzero(active)[-1] + 1) * .01)
assert abs(spoken_start - (timing["fala_inicio_s"] + sync["audio_offset_s"])) < .08
assert abs(spoken_end - (timing["fala_fim_s"] + sync["audio_offset_s"])) < .1
result = {"arquivo": str(args.video.resolve()), "resolucao": [width,height], "fps": fps,
          "duracao_s": duration, "frames": total, "audio_codec": codec, "audio_hz": rate,
          "audio_canais": channels, "audio_fim_s": audio_end, "audio_original_sha256": sync["audio_sha256"],
          "audio_envelope_correlacao": corr, "fala_inicio_s": spoken_start, "fala_fim_s": spoken_end,
          "audio_offset_medido_s": measured_lag * .01,
          "cues": len(cues), "amostras": len(captions), "legenda_grafia_numerica_verificada": True,
          "estados_s": settled, "numeros_verificados": meta["numeros_verificados"],
          "metodo_sincronia": sync["metodo"]}
result["qualidade"] = quality
(qa / "verificacao.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(result, ensure_ascii=False))
