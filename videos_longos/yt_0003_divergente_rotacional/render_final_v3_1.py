"""yt_0003 — render final (1920×1080, 30 fps, CRF 14) em grupos paralelos de ANIMAÇÕES (-n a,b), junção sem recompressão e voz.

    uv run --no-sync python videos_longos/yt_0003_divergente_rotacional/render_final_v3_1.py --grupos 6 --paralelo 3
    uv run --no-sync python videos_longos/yt_0003_divergente_rotacional/render_final_v3_1.py --montar-apenas

Saída: renders/yt_0003_final/master_yt0003.mp4 (vídeo + audio/narracao_montagem.wav em AAC 320 kbit/s)."""
import argparse, os, subprocess, sys, time
from fractions import Fraction
from pathlib import Path
from tempfile import TemporaryDirectory
import av

PASTA = Path(__file__).resolve().parent
RAIZ = PASTA.parents[1]
SAIDA = PASTA / "renders" / "yt_0003_final"
CENA = PASTA / "cena.py"
CLASSE = "DivergenteRotacional"
AUDIO = PASTA / "audio" / "narracao_montagem.wav"
N_ANIM = 836          # 'Played 836 animations' na passada a seco completa (relógio quantizado vt)
FPS = 30


def faixas(n):
    p = N_ANIM / n
    return [(round(i * p), round((i + 1) * p) - 1) for i in range(n)]


def trecho(i):
    return SAIDA / f"g{i}" / "videos" / "cena" / "1080p30" / f"{CLASSE}.mp4"


def colar(trechos, destino):
    ins = [av.open(str(t)) for t in trechos]
    vs = [c.streams.video[0] for c in ins]
    ref = vs[0].codec_context.extradata
    for t, v in zip(trechos, vs):
        assert (v.width, v.height, round(float(v.base_rate)), v.codec_context.name) == (1920, 1080, 30, "h264"), t
        assert v.codec_context.extradata == ref, f"parâmetros H.264 diferentes em {t}"
        assert v.time_base == vs[0].time_base, "time_base diferente entre trechos"
    out = av.open(str(destino), "w")
    vo = out.add_stream_from_template(vs[0])
    quadros, off = 0, 0
    for c, v in zip(ins, vs):
        n_pk, base = 0, None
        for pk in c.demux(v):
            if pk.dts is None:
                continue
            if base is None:
                base = pk.dts
            pk.pts = pk.pts - base + off if pk.pts is not None else None
            pk.dts = pk.dts - base + off
            pk.stream = vo
            out.mux(pk)
            n_pk += 1
        frames = v.frames or n_pk
        quadros += frames
        off += int(round(frames / FPS / v.time_base))
        print(f"  {c.name.split('yt_0003_final')[1][:6]}: {frames} quadros", flush=True)
    out.close()
    for c in ins:
        c.close()
    return quadros


def mux(video, audio, destino):
    with av.open(str(video)) as vi, av.open(str(audio)) as ai, av.open(str(destino), "w", options={"movflags": "+faststart"}) as out:
        vin = vi.streams.video[0]; vout = out.add_stream_from_template(vin)
        ain = ai.streams.audio[0]; aout = out.add_stream("aac", rate=48000); aout.layout = "stereo"; aout.bit_rate = 320_000
        rs = av.AudioResampler(format="fltp", layout="stereo", rate=48000)

        def apk():
            for fr in ai.decode(ain):
                for f2 in rs.resample(fr):
                    yield from aout.encode(f2)
            for f2 in rs.resample(None):
                yield from aout.encode(f2)
            yield from aout.encode(None)

        def vpk():
            for pk in vi.demux(vin):
                if pk.dts is not None:
                    pk.stream = vout
                    yield pk
        A, V = apk(), vpk()
        a, v = next(A, None), next(V, None)
        while a is not None or v is not None:
            ta = float(a.dts * a.time_base) if a is not None and a.dts is not None else float("inf")
            tv = float(v.dts * v.time_base) if v is not None else float("inf")
            if tv <= ta:
                out.mux(v); v = next(V, None)
            else:
                out.mux(a); a = next(A, None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--grupos", type=int, default=6)
    ap.add_argument("--paralelo", type=int, default=3)
    ap.add_argument("--apenas", default="")
    ap.add_argument("--montar-apenas", action="store_true")
    a = ap.parse_args()
    SAIDA.mkdir(parents=True, exist_ok=True)
    fx = faixas(a.grupos)
    print("grupos de animações:", fx, flush=True)
    if not a.montar_apenas:
        fila = [int(x) for x in a.apenas.split(",")] if a.apenas else list(range(len(fx)))
        ativos, falhas = [], []
        while fila or ativos:
            while fila and len(ativos) < a.paralelo:
                i = fila.pop(0)
                env = {**os.environ, "CRF": "14", "TRECHO": "", "PYTHONIOENCODING": "utf-8", "QA_LAYOUT": "0"}
                cmd = ["uv", "run", "--no-sync", "python", "-m", "manim", "-r", "1920,1080", "--fps", str(FPS), "--disable_caching",
                       "-n", f"{fx[i][0]},{fx[i][1]}", "--media_dir", str(SAIDA / f"g{i}"), str(CENA), CLASSE]
                log = open(SAIDA / f"g{i}.log", "w", encoding="utf-8")
                ativos.append((i, subprocess.Popen(cmd, cwd=RAIZ, env=env, stdout=log, stderr=subprocess.STDOUT), log))
                print(f"grupo {i} {fx[i]}: iniciado {time.strftime('%H:%M:%S')}", flush=True)
            for item in list(ativos):
                i, p, log = item
                rc = p.poll()
                if rc is not None:
                    log.close(); ativos.remove(item)
                    print(f"grupo {i}: código {rc} {time.strftime('%H:%M:%S')}", flush=True)
                    if rc != 0:
                        falhas.append(i)
            time.sleep(5)
        if falhas:
            sys.exit(f"falhou nos grupos {falhas}; veja {SAIDA}/gN.log")
    destino = SAIDA / "master_yt0003.mp4"
    with TemporaryDirectory() as d:
        mudo = Path(d) / "video.mp4"
        q = colar([trecho(i) for i in range(len(fx))], mudo)
        print(f"vídeo: {q} quadros = {q / FPS:.3f} s", flush=True)
        mux(mudo, AUDIO, destino)
    with av.open(str(destino)) as r:
        v, au = r.streams.video[0], r.streams.audio[0]
        print(f"{destino.name}: {v.width}×{v.height} {float(v.average_rate):.0f} fps, vídeo {float(v.duration * v.time_base):.3f} s, "
              f"áudio {float(au.duration * au.time_base):.3f} s ({au.codec_context.name} {au.rate} Hz), {destino.stat().st_size / 1e6:.0f} MB")


if __name__ == "__main__":
    main()
