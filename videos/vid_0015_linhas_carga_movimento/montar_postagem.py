"""Monta a versão 1080×1920/30 com a voz, SRT e mapa temporal aprovados."""
from fractions import Fraction
import json
import sys
import math
import av
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from montar_preview_sync import UNIT, captions, audio_helpers, caption_image, cue_color_spans


def main():
    pairs = json.loads((UNIT / "native.json").read_text(encoding="utf-8"))["mapa_fino_audio_nativo"]
    target, source = np.array(pairs).T
    original = json.loads((UNIT / "qa_estados_v4.json").read_text(encoding="utf-8"))
    render_metadata = json.loads((UNIT / "qa_estados_postagem.json").read_text(encoding="utf-8"))
    assert original["ritmo"] == render_metadata["ritmo"], "O ritmo solicitado à cena mudou"
    # Cairo amostra alguns intervalos com um quadro extra diferente em 15/30 fps.
    # Remapeia o relógio do render para os estados/pausas efetivos da V4 aprovada.
    clock_pairs = {0.0: 0.0, original["duracao_cena_s"]: render_metadata["duracao_cena_s"]}
    for before, after in zip(original["estados"], render_metadata["estados"]):
        assert {k:v for k,v in before.items() if k!="tempo_s"} == {k:v for k,v in after.items() if k!="tempo_s"}
        for offset in (-before["pausa_s"]/2, 0, before["pausa_s"]/2):
            clock_pairs[before["tempo_s"] + offset] = after["tempo_s"] + offset
    # Preserva também os inícios das três varreduras do gráfico.
    for index, beat_index in zip(range(-3,0), (196,199,200)):
        half = original["ritmo"][beat_index]["duracao_s"] / 2
        clock_pairs[original["transicoes"][index]["tempo_s"] - half] = render_metadata["transicoes"][index]["tempo_s"] - half
    # Início/fim do movimento de retorno à conclusão, sem diluir a correção
    # nas outras animações do fechamento.
    begin_v4 = original["blocos"][-1]["inicio_s"] + original["ritmo"][202]["duracao_s"]
    begin_render = render_metadata["blocos"][-1]["inicio_s"] + render_metadata["ritmo"][202]["duracao_s"]
    clock_pairs[begin_v4] = begin_render
    mass_before = next(s for s in original["estados"] if s["estado"]=="particulas_massivas_v_menor_c")
    mass_after = next(s for s in render_metadata["estados"] if s["estado"]=="particulas_massivas_v_menor_c")
    tail = mass_before["pausa_s"]/2 + original["ritmo"][204]["duracao_s"]
    clock_pairs[mass_before["tempo_s"] - tail] = mass_after["tempo_s"] - tail
    reference_clock, render_clock = np.array(sorted(clock_pairs.items())).T
    assert np.all(np.diff(reference_clock)>0) and np.all(np.diff(render_clock)>0)
    cues = captions.read_cues(UNIT / "legenda.srt")
    spans = cue_color_spans(cues)
    font = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 58)
    visual = UNIT / "media_postagem/videos/1920p30/vid_0015_postagem_visual.mp4"
    outdir = UNIT / "renders"
    clean_path = outdir / "vid_0015_postagem_visual_sync.mp4"
    subs_path = outdir / "vid_0015_postagem_legendas_sem_audio.mp4"
    final = outdir / "vid_0015_postagem_legendado.mp4"
    clean_final = outdir / "vid_0015_postagem_master.mp4"
    frames_dir = UNIT / "frames_postagem"
    frames_dir.mkdir(exist_ok=True)
    # Estados da V4, agora com o bloco da mão direita corrigido.
    samples_native = [3.0, 25.0, 55.867, 68.0, 76.85, 78.8, 82.2, 86.267,
                      108.0, 129.99, 153.3, 163.9, 172.4]
    sample_ids = {round(float(np.interp(t, source, target)) * 30): i
                  for i, t in enumerate(samples_native, 1)}
    count = math.ceil(target[-1] * 30)
    if "--qa-only" not in sys.argv:
        with av.open(str(visual)) as inp, av.open(str(clean_path), "w") as clean, av.open(str(subs_path), "w") as subs:
            assert (inp.streams.video[0].width, inp.streams.video[0].height) == (1080, 1920)
            streams = []
            for output in (clean, subs):
                stream = output.add_stream("libx264", rate=30)
                stream.width, stream.height, stream.pix_fmt = 1080, 1920, "yuv420p"
                stream.options = {"crf": "18", "preset": "fast"}
                streams.append(stream)
            decoder = iter(inp.decode(video=0))
            current, following = next(decoder), next(decoder, None)
            cue_index = 0
            for n in range(count):
                at = n / 30
                native_time = float(np.interp(at, target, source))
                wanted = float(np.interp(native_time, reference_clock, render_clock))
                while following is not None and float(following.time) <= wanted:
                    current, following = following, next(decoder, None)
                selected = current
                if following is not None and float(following.time) - wanted < wanted - float(current.time):
                    selected = following
                while cue_index < len(cues) and cues[cue_index][1] <= at:
                    cue_index += 1
                lines = cues[cue_index][2] if cue_index < len(cues) and cues[cue_index][0] <= at else None
                decorated = caption_image(selected, lines, font, spans[cue_index] if lines else [])
                if n in sample_ids:
                    decorated.save(frames_dir / f"estado_{sample_ids[n]:02d}.jpg", quality=95)
                for output, stream, img in zip((clean, subs), streams, (selected.to_image(), decorated)):
                    frame = av.VideoFrame.from_image(img)
                    frame.pts, frame.time_base = n, Fraction(1, 30)
                    for packet in stream.encode(frame):
                        output.mux(packet)
                if n % 900 == 0:
                    print(f"Montagem: {n}/{count} quadros", flush=True)
            for output, stream in zip((clean, subs), streams):
                for packet in stream.encode(None):
                    output.mux(packet)
        audio = UNIT / "audio/narracao_preview.m4a"
        audio_helpers.mux(clean_path, audio, clean_final)
        audio_helpers.mux(subs_path, audio, final)
    qa = {"legendas": len(cues), "mapa_temporal": "native.json preservado", "estados": samples_native}
    for path in (clean_final, final):
        with av.open(str(path)) as inp:
            video, sound = inp.streams.video[0], inp.streams.audio[0]
            info = {"width": video.width, "height": video.height, "fps": float(video.average_rate),
                    "video_s": float(video.duration * video.time_base),
                    "audio_s": float(sound.duration * sound.time_base),
                    "codec_video": video.codec_context.name, "codec_audio": sound.codec_context.name,
                    "frames_decodificados": sum(1 for _ in inp.decode(video=0))}
            assert info["frames_decodificados"] == count
            assert abs(info["video_s"] - 178.66666666666666) < 0.034
            assert abs(info["audio_s"] - 178.64) < 0.001
            qa[path.name] = info
    errors = [abs(float(np.interp(after["tempo_s"],render_clock,reference_clock))-before["tempo_s"])
              for before,after in zip(original["estados"],render_metadata["estados"])]
    assert max(errors) < 0.001
    qa["duracao_render_bruto_s"] = render_metadata["duracao_cena_s"]
    qa["duracao_nativa_preservada_s"] = original["duracao_cena_s"]
    qa["correcao_amostragem_s"] = original["duracao_cena_s"] - render_metadata["duracao_cena_s"]
    qa["mapa_v4_render30"] = sorted(clock_pairs.items())
    qa["erro_maximo_timestamps_s"] = max(errors)
    qa["ritmo_e_timestamps_preservados"] = True
    qa["qa_mao_direita"] = {
        "corrente": "+x, direita",
        "acima": "+x × +y = +z; odot; B sai da tela",
        "abaixo": "+x × (-y) = -z; otimes; B entra na tela",
        "linha_2": "B_1(d) = -B z-hat",
        "forca": "+x × (-z) = +y; seta para cima, em direção à linha 1",
        "texto_apoio": "Space Grotesk pelo helper text/screen_text",
        "guia": "removida",
        "inspecao_local": "quadro inicial, superior atenuado, posição da linha 2 e produto vetorial",
        "trecho_nativo_s": [75.6, 87.2],
    }
    (UNIT / "qa_postagem.json").write_text(json.dumps(qa, indent=2, ensure_ascii=False), encoding="utf-8")
    for start in range(0, len(samples_native), 6):
        board = Image.new("RGB", (1080, 1360), "#111827")
        draw = ImageDraw.Draw(board)
        for slot, i in enumerate(range(start + 1, min(start + 7, len(samples_native) + 1))):
            img = Image.open(frames_dir / f"estado_{i:02d}.jpg")
            img.thumbnail((360, 640))
            x, y = (slot % 3) * 360, (slot // 3) * 680
            board.paste(img, (x, y + 30))
            draw.text((x + 8, y + 8), f"Estado {i:02d} | nativo {samples_native[i-1]:.2f}s", fill="white")
        board.save(frames_dir / f"prancha_{start//6+1:02d}.jpg", quality=95)
    print(json.dumps(qa, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
