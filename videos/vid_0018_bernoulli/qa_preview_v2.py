"""Extrai a prancha de estados da V2; não renderiza vídeo nem faz QA final."""
import json
from pathlib import Path

import av
import numpy as np
from PIL import Image, ImageDraw, ImageFont

UNIT = Path(__file__).resolve().parent
VIDEO = UNIT / "media_v2/videos/cena/960p15/preview_silencioso_v2.mp4"
FRAMES = UNIT / "frames_v2"


def main():
    timeline = json.loads((UNIT / "tempos_preview_v2.json").read_text(encoding="utf-8"))
    targets = sorted([
        *((name, t + (.2 if name != "pacote_em_transito" else 0)) for name, t in timeline["estados"].items()),
        ("face_varrendo_entrada", 30.0),
        ("agrupamento_em_movimento", 118.5),
    ], key=lambda p: p[1])
    FRAMES.mkdir(exist_ok=True)
    container = av.open(str(VIDEO))
    stream = container.streams.video[0]
    metadata = {
        "video": str(VIDEO), "largura": stream.width, "altura": stream.height,
        "fps_nominal": str(stream.base_rate), "fps_medio_mp4": float(stream.average_rate),
        "audio_streams": len(container.streams.audio),
        "duracao_s": float(stream.duration * stream.time_base),
        "estados_extraidos": {}, "quadros_decodificados": 0,
        "faixa_legenda": {"y_px": [735, 855], "ocupacao_por_estado": {}},
    }
    assert (stream.width, stream.height) == (540, 960)
    # A concatenação do Manim arredonda durações de trechos na base 1/15360.
    assert stream.base_rate == 15 and abs(float(stream.average_rate) - 15) < .001
    assert not container.streams.audio
    index = 0
    for frame in container.decode(stream):
        metadata["quadros_decodificados"] += 1
        t = float(frame.pts * frame.time_base)
        while index < len(targets) and t >= targets[index][1]:
            name, requested = targets[index]
            picture = frame.to_image()
            picture.save(FRAMES / f"{name}.png")
            pixels = np.asarray(picture.convert("RGB"), dtype=np.int16)
            roi = pixels[735:855]
            busy = np.max(np.abs(roi - np.array([5, 8, 22])), axis=2) > 18
            metadata["faixa_legenda"]["ocupacao_por_estado"][name] = round(float(busy.mean()), 6)
            metadata["estados_extraidos"][name] = {"pedido_s": requested, "quadro_s": round(t, 3)}
            index += 1
    assert index == len(targets)
    assert 160 <= metadata["duracao_s"] < 180
    assert metadata["quadros_decodificados"] == stream.frames
    assert max(metadata["faixa_legenda"]["ocupacao_por_estado"].values()) < .01
    container.close()
    font_path = UNIT.parents[1] / "assets/fonts/inter/Inter-Regular.ttf"
    font = ImageFont.truetype(str(font_path), 13)
    for start in range(0, len(targets), 6):
        page = Image.new("RGB", (810, 1020), "#141b2c")
        draw = ImageDraw.Draw(page)
        for n, (name, t) in enumerate(targets[start:start + 6]):
            x, y = (n % 3) * 270, (n // 3) * 510
            im = Image.open(FRAMES / f"{name}.png").convert("RGB").resize((270, 480), Image.Resampling.LANCZOS)
            page.paste(im, (x, y + 30))
            draw.text((x + 6, y + 8), f"{t:.1f}s · {name}", font=font, fill="white")
        page.save(FRAMES / f"contato_{start // 6 + 1:02}.jpg", quality=92)
    metadata["tipo"] = "verificação de preview; sem QA final de master"
    (UNIT / "qa_preview_v2.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(metadata, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
