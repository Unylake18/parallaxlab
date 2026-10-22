"""yt_0008 — alinha audio/narracao_v4.wav ao texto_narracao.txt (sem ASR, mesmo método do yt_0005) e mapeia as 198 unidades de
narracao_ancoras (remap.py) aos eventos da cena.  Saídas: sync.json (palavras, unidades, capítulos) e sync_eventos.json (alvos).

  uv run --no-sync python videos_longos/yt_0008_magnetostatica_ampere/sync_voz.py
"""
import ast
import difflib
import importlib.util
import json
import re
from pathlib import Path

import numpy as np

PASTA = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("sync5", PASTA.parent / "yt_0005_magnetostatica_forca_lorentz" / "sync_voz.py")
s5 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(s5)

AUDIO = PASTA / "audio" / "narracao_v4.wav"
SUB = [  # LaTeX -> fala (idêntico a renders/tempos/tags.py)
    (r"\(\mathbf R=\mathbf r-\mathbf r'\)", "erre maiúsculo, igual a erre menos erre linha"),
    (r"\(\mathbf R/R^3\)", "o vetor separação dividido pela distância ao cubo"),
    (r"\(\mathbf J(\mathbf r')\)", "jota de erre linha"), (r"\(\mathbf r'\)", "erre linha"), (r"\(\mathbf r\)", "erre"),
    (r"\(\mathbf J\)", "jota"), (r"\(\mathbf F\)", "efe"), (r"\(R\)", "erre maiúsculo"), (r"\(nL\)", "ene vezes ele"),
    (r"\(n\)", "ene"), (r"\(N\)", "ene maiúsculo"), (r"\(K\)", "cá"), (r"\(L\)", "ele maiúsculo"), (r"\(C\)", "cê"),
    (r"\(S\)", "esse maiúsculo"), (r"\(s\)", "ésse"),
]
norm = lambda s: " ".join(s.split())


def tempo(s):
    m, r = s.split(":")
    return int(m) * 60 + float(r)


def unidades():
    """U de remap.py (lista literal) sem executar o script."""
    tree = ast.parse((PASTA / "renders" / "tempos" / "remap.py").read_text(encoding="utf-8"))
    for n in tree.body:
        if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "U":
            return ast.literal_eval(n.value)


def log_v6():
    """Eventos (sem marcas) do log legível, no relógio do mp4 do V6: [(t, tipo, texto)]."""
    ev = []
    for ln in (PASTA / "renders" / "tempos" / "log_legivel.txt").read_text(encoding="utf-8").split("\n"):
        m = re.match(r"=== SECAO (\S+) .*prev (\S+)", ln)
        if m:
            ev.append((tempo(m.group(2)), "secao", m.group(1)))
            continue
        m = re.match(r"(\d+:\d+\.\d+) (LEG|EQ\[\w+\]|TITULO|MARCA): (.*)", ln)
        if m:
            ev.append((tempo(m.group(1)), m.group(2)[:2], m.group(3)))
    return ev


def main():
    texto = norm((PASTA / "texto_narracao.txt").read_text(encoding="utf-8"))
    palavras = texto.split()
    raw, sr = s5.ler(AUDIO)
    print(f"{len(palavras)} palavras; áudio {len(raw) / sr:.2f} s")
    ini, fim, runs, (t0, t1), x, env = s5.alinhar(raw, sr, palavras)

    def onset(t):
        a, b = int(max(0, (t - 0.25) / 0.01)), int(min(len(env) - 1, (t + 0.25) / 0.01))
        on = [i for i in range(a + 1, b) if env[i - 1] < 0.03 <= env[i]]
        return min(on, key=lambda q: abs(q * 0.01 - t)) * 0.01 if on else t

    # unidades -> índice de palavra
    U = unidades()
    def conv(p):
        p = norm(p.replace("**", ""))
        for a, b in SUB:
            p = p.replace(a, b)
        return p
    pos, cur, un = [], 0, []
    for k, u in enumerate(U):
        frase = conv(u[3])
        i = texto.find(frase, cur)
        assert i >= 0, (k, u)
        cur = i
        j = len(texto[:i].split())
        t = float(ini[j])
        un.append({"k": k, "bloco": u[0], "ancora": u[1], "tela": u[2], "palavra": j, "t": round(t, 3), "onset": round(onset(t), 3),
                   "texto": texto[i:i + 60]})

    # unidade -> evento do log V6 (ordinal entre os eventos não-marca)
    ev = log_v6()
    for k, u in enumerate(un):
        if k < 3:
            u["evento"] = None   # abertura: eventos manuais (ver abaixo)
            continue
        if k == 3:
            u["evento"] = 0      # secao pergunta (primeiro evento do log V6)
            continue
        a = tempo(U[k][1])
        cand = [((0 if e[1] in ("LE", "EQ", "TI") else 1), abs(e[0] - a), n) for n, e in enumerate(ev) if abs(e[0] - a) <= 0.35]
        if not cand:
            cand = [(2, abs(e[0] - a), n) for n, e in enumerate(ev) if abs(e[0] - a) <= 1.0]
            print("  sem evento <=1 s: âncora", k, U[k][1], ascii(U[k][2][:30]), "mais próximo:", min((abs(e[0] - a), e[0], e[1], ascii(e[2][:30])) for e in ev))
        if not cand:
            u["evento"] = None   # sem evento próprio: acompanha a unidade anterior
            continue
        u["evento"] = min(cand)[2]
    # eventos distintos em ordem; alvo = onset da 1ª unidade que cai nele
    alvo = {}
    for u in un:
        if u["evento"] is not None and u["evento"] not in alvo:
            alvo[u["evento"]] = u["onset"]
    ords = sorted(alvo)
    assert all(alvo[a] <= alvo[b] + 0.01 for a, b in zip(ords, ords[1:])), "alvos fora de ordem"

    # eventos da abertura: frases da fala
    def palavra_de(frase):
        return round(onset(float(ini[len(texto[:texto.find(frase)].split())])), 3)
    ab = {"leg1": palavra_de("As linhas de campo dão voltas"), "eq": palavra_de("Mas, fora do fio, o rotacional"),
          "leg2": palavra_de("Como um campo pode circular"), "pergunta": un[3]["onset"]}

    # capítulos: início do 1º bloco de cada Bnn
    caps, vistos = [], set()
    for u in un:
        if u["bloco"] not in vistos:
            vistos.add(u["bloco"])
            caps.append({"bloco": u["bloco"], "t": u["onset"] if u["bloco"] != "B00" else 0.0})

    json.dump({"audio": AUDIO.name, "dur": round(len(raw) / sr, 3), "fala": [round(t0, 3), round(t1, 3)], "unidades": un, "capitulos": caps,
               "abertura": ab, "words": [[p, round(float(a), 3), round(float(b), 3)] for p, a, b in zip(palavras, ini, fim)],
               "pauses": [[round(a, 3), round(b, 3)] for a, b in runs]},
              open(PASTA / "sync.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    # tabela por ordinal de evento no log V6 (sem marcas); a cena soma o deslocamento da abertura (ver base.py)
    # ordinais do log V6 -> ordinais da cena atual (qa_timeline da fumaça: a cena tem eventos a mais, p.ex. títulos de seção e a abertura)
    K = {"secao": "secao", "legenda": "LE", "equacao": "EQ", "titulo": "TI", "marca": "MA"}
    nv = lambda t: re.sub(r"\W", "", t)[:25]
    novo = json.loads((PASTA / "renders" / "sync1" / "qa_timeline.json").read_text(encoding="utf-8"))["eventos"]
    A = [(e[1], "" if e[1] == "EQ" else nv(e[2])) for e in ev]
    B = [(K[e[2]], "" if e[2] == "equacao" else nv(e[3])) for e in novo]
    mp = {}
    for op, a0, a1, b0, b1 in difflib.SequenceMatcher(None, A, B, autojunk=False).get_opcodes():
        if op in ("equal", "replace") and a1 - a0 == b1 - b0:
            mp.update({a0 + j: b0 + j for j in range(a1 - a0)})
    tab = {}
    for n in ords:
        prox = [m for m in ords if m > n]
        w = ev[prox[0]][0] - ev[n][0] if prox else None
        tab[str(mp[n])] = {"alvo": alvo[n], "janela": round(w, 3) if w else None, "prox": alvo[prox[0]] if prox else None,
                           "tipo": ev[n][1], "texto": ev[n][2][:60]}
    json.dump({"abertura": ab, "eventos": tab, "n_eventos_v6": len(ev), "dur": round(len(raw) / sr, 3)},
              open(PASTA / "sync_eventos.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(un)} unidades, {len(tab)} eventos ancorados de {len(ev)}; abertura {ab}")
    ritmo = np.array([sum(s5.silabas(q) for q in palavras[a:b + 1]) / max(.05, fim[b] - ini[a]) for a, b in
                      zip([0] + [i + 1 for i, p in enumerate(palavras) if p[-1] in '.?!'][:-1], [i for i, p in enumerate(palavras) if p[-1] in '.?!'])])
    print(f"ritmo por frase: média {ritmo.mean():.2f} σ {ritmo.std():.2f} mín {ritmo.min():.2f} máx {ritmo.max():.2f}")


if __name__ == "__main__":
    main()
