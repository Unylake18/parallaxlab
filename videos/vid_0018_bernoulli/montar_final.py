"""Entregas H.264 CRF14/yuv420p a partir do render nativo sem perdas; AAC copiado."""
from fractions import Fraction
import importlib.util
from pathlib import Path
import av
from PIL import ImageFont

UNIT = Path(__file__).resolve().parent
ROOT = UNIT.parents[1]
spec = importlib.util.spec_from_file_location("montar", ROOT / "videos/montar_legendado.py")
montar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(montar)


def main():
    source = UNIT / "media_final/videos/cena_final/1920p30/BernoulliFinal.mp4"
    clean_path = UNIT / "media_final/master_sem_audio.mp4"
    caption_path = UNIT / "media_final/legendado_sem_audio.mp4"
    targets = UNIT / "renders"
    targets.mkdir(exist_ok=True)
    cues = montar.read_cues(UNIT / "legenda.srt")
    colors = montar.load_term_colors(UNIT / "legendas_cores.py")
    font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 58)
    with av.open(str(source)) as raw, av.open(str(clean_path), "w") as clean, av.open(str(caption_path), "w") as caption:
        incoming = raw.streams.video[0]
        assert (incoming.width, incoming.height, incoming.base_rate) == (1080, 1920, 30)
        assert incoming.codec_context.pix_fmt == "yuv444p"
        streams = []
        for output in (clean, caption):
            stream = output.add_stream("libx264", rate=30)
            stream.width, stream.height, stream.pix_fmt = 1080, 1920, "yuv420p"
            stream.options = {"crf": "14", "preset": "medium"}
            streams.append(stream)
        cue_index = 0
        for count, frame in enumerate(raw.decode(video=0)):
            at = float(frame.pts * frame.time_base)
            while cue_index < len(cues) and cues[cue_index][1] <= at:
                cue_index += 1
            lines = cues[cue_index][2] if cue_index < len(cues) and cues[cue_index][0] <= at else None
            picture = montar.draw_caption(frame, lines, font, 1080, 1920, "standard", colors)
            clean_frame = av.VideoFrame.from_image(frame.to_image())
            caption_frame = av.VideoFrame.from_image(picture)
            for output, stream, encoded in zip((clean, caption), streams, (clean_frame, caption_frame)):
                encoded.pts, encoded.time_base = count, Fraction(1, 30)
                for packet in stream.encode(encoded):
                    output.mux(packet)
            if (count + 1) % 300 == 0:
                print(f"Montagem: {count + 1}/{incoming.frames} quadros", flush=True)
        for output, stream in zip((clean, caption), streams):
            for packet in stream.encode(None):
                output.mux(packet)
        assert count + 1 == incoming.frames
    montar.mux_audio(clean_path, source, targets / "vid_0018_bernoulli_final_master_limpo.mp4")
    montar.mux_audio(caption_path, source, targets / "vid_0018_bernoulli_final_legendado.mp4")
    print("Master e legendado prontos; AAC preservado por cópia de pacotes.", flush=True)


if __name__ == "__main__":
    main()
