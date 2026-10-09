"""Incorpora a legenda no master R7, com codificação de alta qualidade.

Uso: uv run python videos/vid_0017_bateria_massa_energia/montar_final.py
Preserva o estilo de legendas e copia o áudio sem uma nova compressão.
"""
from fractions import Fraction
import importlib.util
from pathlib import Path
import shutil

import av
from PIL import ImageFont

UNIT = Path(__file__).resolve().parent
ROOT = UNIT.parents[1]
spec = importlib.util.spec_from_file_location("montar", ROOT / "videos/montar_legendado.py")
montar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(montar)


def main():
    source = UNIT / "media_r7/videos/cena/1920p30/BateriaMassaEnergiaFinal.mp4"
    master = UNIT / "renders/vid_0017_bateria_massa_energia_final_master_limpo_v2.mp4"
    output = UNIT / "renders/vid_0017_bateria_massa_energia_final_legendado_v2.mp4"
    lossless_output = UNIT / "renders/vid_0017_bateria_massa_energia_legendado_sem_perdas_v2.mp4"
    silent = UNIT / "media_r7/legendado_sem_audio.mp4"
    silent_lossless = UNIT / "media_r7/legendado_sem_audio_sem_perdas.mp4"
    master.parent.mkdir(exist_ok=True)
    shutil.copyfile(source, master)
    cues = montar.read_cues(UNIT / "legenda.srt")
    with (av.open(str(master)) as clean, av.open(str(silent), "w") as out,
          av.open(str(silent_lossless), "w") as archive):
        video = clean.streams.video[0]
        assert (video.width, video.height, video.average_rate) == (1080, 1920, 30)
        assert video.codec_context.pix_fmt == "yuv444p"
        font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 58)
        stream = out.add_stream("libx264", rate=30)
        stream.width, stream.height, stream.pix_fmt = 1080, 1920, "yuv420p"
        stream.options = {"crf": "14", "preset": "slow"}
        archival_stream = archive.add_stream("libx264", rate=30)
        archival_stream.width, archival_stream.height = 1080, 1920
        archival_stream.pix_fmt = "yuv444p"
        archival_stream.options = {"crf": "0", "preset": "medium"}
        index = 0
        for count, frame in enumerate(clean.decode(video)):
            at = float(frame.pts * frame.time_base)
            while index < len(cues) and cues[index][1] <= at:
                index += 1
            lines = cues[index][2] if index < len(cues) and cues[index][0] <= at else None
            picture = montar.draw_caption(frame, lines, font, 1080, 1920, "standard")
            encoded = av.VideoFrame.from_image(picture)
            encoded.pts, encoded.time_base = count, Fraction(1, 30)
            for packet in stream.encode(encoded):
                out.mux(packet)
            for packet in archival_stream.encode(encoded):
                archive.mux(packet)
            if (count + 1) % 300 == 0:
                print(f"Legenda: {count+1}/3339 quadros", flush=True)
        for packet in stream.encode(None):
            out.mux(packet)
        for packet in archival_stream.encode(None):
            archive.mux(packet)
        assert count + 1 == 3339
    montar.mux_audio(silent, master, output)
    montar.mux_audio(silent_lossless, master, lossless_output)
    print(output, flush=True)
    print(lossless_output, flush=True)


if __name__ == "__main__":
    main()
