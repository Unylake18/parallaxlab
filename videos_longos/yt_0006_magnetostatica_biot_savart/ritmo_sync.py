"""yt_0006 — calcula ritmo.json: quantos quadros (30 fps) dura cada animação/espera para que cada âncora caia no instante da voz.

  uv run --no-sync python videos_longos/yt_0006_magnetostatica_biot_savart/ritmo_sync.py

Entradas: intervalos.jsonl (todo play()/espera da cena, com a duração nominal), ancoras.json (evento ↔ instante da voz).
Entre duas âncoras, a duração disponível é a da voz. Política:
  - as esperas de leitura da prévia começam em 60% (a voz já conduz); a sobra de tempo vai primeiro para as animações
    (movimento mais lento e contínuo, até 2,4×) e só depois para as esperas;
  - falta de tempo: as esperas encolhem (até 30%), depois as animações (até 70%);
  - se ainda não couber, a voz recebe um silêncio (pad) antes da frase seguinte e o vídeo usa a duração mínima.
Os quadros são arredondados pela soma acumulada dentro do trecho, e o fim de cada trecho cai no quadro da âncora (sem deriva).
"""
import json
from pathlib import Path

PASTA = Path(__file__).resolve().parent
FPS = 30
A_CAP, A_MIN, H_BASE, H_MIN = 2.4, 0.70, 0.60, 0.30


def main():
    iv = [json.loads(l) for l in open(PASTA / "intervalos.jsonl", encoding="utf-8")]
    anc = json.load(open(PASTA / "ancoras.json", encoding="utf-8"))
    n = len(iv)
    e0 = [x["e0"] for x in iv]
    # índice do intervalo em que cada âncora começa
    idx = []
    for a in anc:
        k = min(range(n), key=lambda i: abs(e0[i] - a["e"]))
        if abs(e0[k] - a["e"]) > 0.005:
            ks = [i for i in range(n) if e0[i] >= a["e"] - 0.005]
            k = ks[0] if ks else n - 1
            print(f"aviso: {a['unidade']} e={a['e']} não cai no início de um intervalo; usando o intervalo {k} (e0={e0[k]})")
        idx.append(k)
    assert all(b > a for a, b in zip(idx, idx[1:])), "âncoras em intervalos repetidos ou fora de ordem"
    frames = [0] * n
    pads, resumo, cur, shift = [], [], 0, 0.0

    def distribui(ks, total_frames, dur):
        """reparte total_frames entre os intervalos ks proporcionalmente a dur (cumulativo, sem deriva); mínimo 1 quadro se houver duração."""
        s = sum(dur[k] for k in ks) or 1.0
        acc, last = 0.0, 0
        for k in ks:
            acc += dur[k]
            nxt = round(acc / s * total_frames)
            frames[k] = nxt - last
            last = nxt
        for k in ks:
            if iv[k]["nom"] > 0 and frames[k] < 1:
                m = max(ks, key=lambda q: frames[q])
                frames[m] -= 1 - frames[k]
                frames[k] = 1

    # trecho antes da primeira âncora (se houver): escala 1
    if idx[0] > 0:
        ks = list(range(0, idx[0]))
        tf = round(sum(iv[k]["nom"] for k in ks) * FPS)
        distribui(ks, tf, {k: iv[k]["nom"] for k in ks})
        cur += tf
    for s in range(len(anc)):
        a0 = idx[s]
        a1 = idx[s + 1] if s + 1 < len(anc) else n
        ks = list(range(a0, a1))
        if s + 1 == len(anc):
            tf = round(sum(iv[k]["nom"] for k in ks) * FPS)       # último trecho (CTA): ritmo da animação
            distribui(ks, tf, {k: iv[k]["nom"] for k in ks})
            cur += tf
            resumo.append({"unidade": anc[s]["unidade"], "T": tf / FPS, "A": sum(iv[k]["nom"] for k in ks if iv[k]["kind"] == "anim"),
                           "H": sum(iv[k]["nom"] for k in ks if iv[k]["kind"] == "hold"), "fa": 1.0, "fh": 1.0, "pad": 0.0})
            break
        A = sum(iv[k]["nom"] for k in ks if iv[k]["kind"] == "anim")
        H = sum(iv[k]["nom"] for k in ks if iv[k]["kind"] == "hold")
        T = (anc[s + 1]["v"] + shift) - (anc[s]["v"] + shift)
        fa = fh = 1.0
        pad = 0.0
        H0 = H_BASE * H                                    # com voz, a espera de leitura da prévia pode encolher
        if T >= A + H0:
            extra = T - A - H0
            ea = min(extra, (A_CAP - 1) * A)               # a animação absorve primeiro (movimento mais lento, mas contínuo)
            rem = extra - ea
            if H > 0:
                fa = 1 + ea / A if A > 0 else 1.0
                fh = H_BASE + rem / H
            else:
                fa = 1 + (ea + rem) / A if A > 0 else 1.0
        else:
            falta = A + H0 - T
            rh = min(falta, (H_BASE - H_MIN) * H)
            fh = H_BASE - rh / H if H > 0 else 1.0
            falta -= rh
            ra = min(falta, (1 - A_MIN) * A)
            fa = 1 - ra / A if A > 0 else 1.0
            falta -= ra
            if falta > 1e-6:
                pad = falta
                shift += pad
                pads.append([anc[s + 1]["v"], round(pad, 3), anc[s + 1]["unidade"]])
        dur = {k: iv[k]["nom"] * (fa if iv[k]["kind"] == "anim" else fh) for k in ks}
        total = sum(dur.values())
        end_frame = round((anc[s + 1]["v"] + shift) * FPS) if True else None
        tf = end_frame - cur
        distribui(ks, tf, dur)
        cur = end_frame
        resumo.append({"unidade": anc[s]["unidade"], "T": T, "A": A, "H": H, "fa": fa, "fh": fh, "pad": pad})
    assert sum(frames) == cur, (sum(frames), cur)
    json.dump({"fps": FPS, "frames": frames, "pads": pads,
               "total_quadros": sum(frames), "total_s": round(sum(frames) / FPS, 3)},
              open(PASTA / "ritmo.json", "w"), indent=0)
    # relatório
    print(f"{n} intervalos, {len(anc)} âncoras → {sum(frames)} quadros = {sum(frames) / FPS:.2f} s; pads: {len(pads)} (+{sum(p[1] for p in pads):.2f} s de silêncio na voz)")
    fa = [r["fa"] for r in resumo]
    fh = [r["fh"] for r in resumo]
    print(f"escala das animações: min {min(fa):.2f} média {sum(fa) / len(fa):.2f} máx {max(fa):.2f}; das esperas: min {min(fh):.2f} máx {max(fh):.2f}")
    comp = [r for r in resumo if r["fa"] < 0.95 or r["fh"] < 0.5]
    print(f"trechos comprimidos (animação<0,95 ou espera<0,5): {len(comp)}")
    for r in sorted(comp, key=lambda r: r["fa"])[:8]:
        print(f"   {r['unidade']}: T={r['T']:.1f}s nominal={r['A'] + r['H']:.1f}s fa={r['fa']:.2f} fh={r['fh']:.2f} pad={r['pad']:.2f}")
    longas = sorted(((frames[k] / FPS, k) for k in range(n) if iv[k]["kind"] == "hold"), reverse=True)[:10]
    print("maiores esperas (s, índice, e0):", [(round(d, 1), k, round(e0[k], 1)) for d, k in longas])


if __name__ == "__main__":
    main()
