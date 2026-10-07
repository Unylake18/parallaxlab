"""Prancha de avaliação e pacote das capas, sem modificar os PNGs originais."""
import json
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
brief = json.loads((HERE / "briefing_capas.json").read_text(encoding="utf-8"))
font = ImageFont.truetype(str(ROOT / "assets/fonts/space_grotesk/SpaceGrotesk-Bold.ttf"), 26)
board = Image.new("RGB", (2000, 1520), "#101526")
draw = ImageDraw.Draw(board)
draw.text((18, 10), "10 CAPAS · VID_0015", font=font, fill="white")
records = []
for i in range(1, 11):
    path = HERE / f"capa_{i:02d}.png"
    with Image.open(path) as image:
        image.load()
        width, height = image.size
        assert image.format == "PNG" and abs(width / height - 9 / 16) < 0.005, path
        thumb = image.convert("RGB")
        thumb.thumbnail((380, 676), Image.Resampling.LANCZOS)
    x, y = 18 + ((i - 1) % 5) * 396, 52 + ((i - 1) // 5) * 730
    draw.text((x, y), f"{i:02d}", font=font, fill="#35D9FF")
    board.paste(thumb, (x, y + 36))
    records.append({"id": i, "arquivo": path.name, "chamada": brief["conceitos"][i-1][0],
                    "width": width, "height": height, "leitura_png": "ok"})
board.save(HERE / "comparativo_10_capas.jpg", quality=95)
package = HERE / "vid_0015_10_capas.zip"
with ZipFile(package, "w", compression=ZIP_DEFLATED) as archive:
    for item in records:
        archive.write(HERE / item["arquivo"], item["arquivo"])
with ZipFile(package) as archive:
    assert len(archive.namelist()) == 10 and archive.testzip() is None
qa = {"metodo": "image_gen incorporado", "capas": records,
      "inspecao_visual": "chamadas, símbolos, velocidades para direita, atração para dentro e repulsão para fora conferidos",
      "correcoes": {"01_02": "origem da força magnética superior corrigida",
                    "05": "forças removidas para destacar o limite v=c",
                    "07": "forças quase iguais; magnética menor e resultante para baixo"},
      "marca_e_tipografia": "recriadas pelo gerador a partir da referência visual",
      "originais": "PNGs copiados sem edição; apenas a prancha usa miniaturas",
      "zip": "10 PNGs, integridade conferida"}
(HERE / "qa_capas.json").write_text(json.dumps(qa, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps({"capas": len(records), "tamanhos": sorted({(r["width"], r["height"]) for r in records}),
                  "zip_bytes": package.stat().st_size}, ensure_ascii=False))
