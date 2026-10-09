"""Extrai estados-chave do único preview; não renderiza outra variante."""
import json
from pathlib import Path

import av
from PIL import Image, ImageDraw, ImageFont

UNIT = Path(__file__).resolve().parent
VIDEO = UNIT / "media_preview/videos/cena/960p15/preview_silencioso.mp4"
FRAMES = UNIT / "frames_preview"


def main():
    timeline = json.loads((UNIT / "tempos_preview.json").read_text(encoding="utf-8"))
    targets = sorted([
        *((name, t + .6) for name, t in timeline["estados"].items()),
        ("entrada_durante_avanco", 37.0),
        ("saida_durante_avanco", 52.0),
        ("reorganizacao_em_transito", 129.0),
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
            frame.to_image().save(FRAMES / f"{name}.png")
            metadata["estados_extraidos"][name] = {"pedido_s": requested, "quadro_s": round(t, 3)}
            index += 1
    assert index == len(targets)
    assert 155 <= metadata["duracao_s"] <= 180
    assert metadata["quadros_decodificados"] == stream.frames
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
    (UNIT / "qa_preview.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(metadata, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
