"""yt_0030 · QA do handoff v3 §6 (relatórios novos): palco_parado_v3.txt, painel_vazio_v3.txt, leituras_v3.txt, margens_v3.txt, areas_livres_v3.txt.
O resto (prancha, origens, glyph maps, R12, R13, R5/R7/R10, holds, gatilhos, números, pausas) sai do comparar.py, qa30.py e qa_v2.py com a rodada v3.
uso: python qa_v3.py [rodada]"""
import json
import re
import sys
from pathlib import Path

import av
import numpy as np

U = Path(__file__).resolve().parent
sys.path.insert(0, str(U))
from tempos import ANC_DADOS  # noqa: E402

R = sys.argv[1] if len(sys.argv) > 1 else "v3"
OUT = U / "renders" / R / "qa"
OUT.mkdir(parents=True, exist_ok=True)
INFO = json.loads((U / "renders" / R / f"lotes_{R}.json").read_text(encoding="utf-8"))
INI = {k: v / 15 for k, v in INFO["inicio"].items()}
ORDEM = list(INFO["inicio"])
LOG = {l: (U / f"log_{l}.txt").read_text(encoding="utf-8", errors="replace") for l in ORDEM}
SOB = {l: ((U / f"log_sob_{l}.txt").read_text(encoding="utf-8", errors="replace") if (U / f"log_sob_{l}.txt").exists() else "") for l in ORDEM}
mm = lambda t: f"{int(t) // 60}:{t % 60:05.2f}"
ANC_INI = []
for l in ORDEM:
    for m in re.finditer(r"\[ancora\] (\S+) ([0-9.]+)", LOG[l]):
        ANC_INI.append((INI[l] + float(m.group(2)), m.group(1)))
ANC_INI.sort()


def fala_em(t):
    aid, t0 = None, 0
    for ti, a in ANC_INI:
        if ti <= t:
            aid, t0 = a, ti
    if aid is None:
        return "—", ""
    A = ANC_DADOS["ancoras"][aid]
    ws = [w for tt, w in zip(A["t"], A["fala"].split()) if tt >= t - t0 - 0.2][:12]
    return aid, " ".join(ws)


# ── palco parado / painel vazio: varredura do preview (960×540). Layout pelo desenho das molduras: A = palco 120–1080 × 180–900 sem moldura em
#    840 px; B = dois painéis (120–840 e 1080–1800) com molduras em 840 e 1800 px. Outros layouts (cartões, escada, cartão final) não entram.
def molduras(g):
    def borda(x):
        col = g[95:445, x - 1:x + 2].max(axis=1)
        viz = np.concatenate([g[95:445, x - 7:x - 4], g[95:445, x + 5:x + 8]], axis=1).mean(axis=1)
        return float(np.mean(col > viz + 10))
    return borda(60) > .6, borda(420) > .6, borda(540) > .6, borda(900) > .6


def varre():
    c = av.open(str(U / "renders" / R / f"yt_0030_preview_{R}_540p15.mp4"))
    reg = {"A": (62, 92, 538, 448), "B-esq": (62, 92, 418, 448), "B-dir": (542, 92, 898, 448)}
    prev = None
    parado = {k: [0, None] for k in reg}
    vazio = {k: [0, None] for k in ("B-esq", "B-dir")}
    out_p, out_v = [], []
    for i, fr in enumerate(c.decode(video=0)):
        g = np.asarray(fr.to_ndarray(format="rgb24"), np.int16)[:, :, 1]
        e0, e420, e540, e900 = molduras(g)
        lay = "B" if (e420 and e900 and e0) else ("A" if (e0 and e540 and not e420) else None)
        ativos = {"A"} if lay == "A" else ({"B-esq", "B-dir"} if lay == "B" else set())
        for k, (x0, y0, x1, y1) in reg.items():
            st = parado[k]
            if k in ativos and prev is not None and np.abs(g[y0:y1, x0:x1] - prev[y0:y1, x0:x1]).max() <= 3:
                if st[0] == 0:
                    st[1] = i - 1
                st[0] += 1
            else:
                if st[0] + 1 > 120:
                    out_p.append((k, st[1], st[0] + 1))
                st[0] = 0
        for k in ("B-esq", "B-dir"):
            x0, y0, x1, y1 = reg[k]
            st = vazio[k]
            sub = g[y0 + 6:y1 - 6, x0 + 6:x1 - 6]
            conteudo = float(np.mean(sub > np.median(sub) + 45))
            if k in ativos and conteudo < 0.003:
                if st[0] == 0:
                    st[1] = i
                st[0] += 1
            else:
                if st[0] > 30:
                    out_v.append((k, st[1], st[0]))
                st[0] = 0
        prev = g
    c.close()
    for k, st in parado.items():
        if st[0] + 1 > 120:
            out_p.append((k, st[1], st[0] + 1))
    for k, st in vazio.items():
        if st[0] > 30:
            out_v.append((k, st[1], st[0]))
    L = [f"yt_0030 {R} · palco parado (v3 §6.2): a medida dos holds só DENTRO do palco (layout A: 120–1080 × 180–900; layout B: cada painel).",
         "Trechos > 8 s sem mudança no palco. Motivo = a fala no início do trecho.", ""]
    for k, i0, n in sorted(out_p, key=lambda x: x[1]):
        aid, txt = fala_em(i0 / 15)
        L.append(f"{mm(i0 / 15)} · {n / 15:5.2f} s · {k:6s} · {aid:6s} · «{txt}…»")
    L += ["", f"total: {len(out_p)} trechos > 8 s"]
    (OUT / f"palco_parado_{R}.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
    L = [f"yt_0030 {R} · painel vazio (v3 §6.3): no layout B, painel sem conteúdo (menos de 0,3 % dos pixels acima do fundo: só a grade) por mais de 2 s.", ""]
    for k, i0, n in sorted(out_v, key=lambda x: x[1]):
        aid, txt = fala_em(i0 / 15)
        L.append(f"{mm(i0 / 15)} · {n / 15:5.2f} s · {k:6s} · {aid:6s} · «{txt}…»")
    L += ["", f"total: {len(out_v)} trechos > 2 s"]
    (OUT / f"painel_vazio_{R}.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
    return out_p, out_v


def leituras():
    L = [f"yt_0030 {R} · leitura dos símbolos (v3 §4.2, Anexo B): sublinhado fino (2 px, GEO, Create 0,3 s / FadeOut 0,3 s) sob o símbolo lido.",
         "Tempo no preview · nº do Anexo B · já estava na tela? (não = escrito a caneta nessa hora) · fala.", ""]
    vistos = set()
    for l in ORDEM:
        for m in re.finditer(r"\[leitura\] (\d+) (\S+) (\S+) ([0-9.]+) ja=(\w+) «(.+?)»", LOG[l]):
            n = int(m.group(1))
            vistos.add(n)
            L.append(f"{mm(INI[l] + float(m.group(4)))} · {n:2d} · {m.group(3):6s} · {'sim' if m.group(5) == 'True' else 'não (escrito nessa hora)'} · «{m.group(6)}»")
    falta = sorted(set(range(1, 23)) - vistos)
    L += ["", f"leituras do Anexo B cobertas: {len(vistos)}/22" + (f" · faltam {falta}" if falta else "")]
    (OUT / f"leituras_{R}.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
    return len(vistos)


def margens():
    L = [f"yt_0030 {R} · margens (v3 §6.8): nenhum texto além de 1800 px na coluna nem a menos de 60 px do rodapé; medido em cada gatilho e fim de",
         "âncora da passada de auditoria (caixas dos textos e fórmulas visíveis).", ""]
    tot = 0
    for l in ORDEM:
        oc = sorted(set(re.findall(r"\[margem\] (.+)", SOB[l])))
        tot += len(oc)
        L.append(f"{l:5s}: {len(oc)} ocorrências")
        L += [f"   {o}" for o in oc]
    L += ["", f"TOTAL: {tot}"]
    (OUT / f"margens_{R}.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
    return tot


def areas_livres():
    """Levantamento no código: toda área sem setas (skip fixo ou clareira) e o objeto que a justifica, com o instante em que ele entra."""
    L = [f"yt_0030 {R} · áreas livres (v3 §6.7): nenhuma área sem setas antes de o objeto dela existir. Cada skip/clareira do código e quando o",
         "objeto entra. 'junto' = a área abre no mesmo play em que o objeto entra (setas saem por fade na opacidade real).", ""]
    for f in sorted(U.glob("sec_*.py")):
        for k, ln in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            if ("skip=" in ln and "campo" in ln) or "clareira(" in ln or "op_seta(m, 1 - a)" in ln:
                L.append(f"{f.name}:{k}: {ln.strip()[:150]}")
    L += ["", "Revisão (v3): H (quadradinho tracejado desde o 1º quadro; disco do fio/carga até 1,6 u, o anel do 2r abre junto com o círculo 2r);",
          "D1 (origem); D2 (rótulos e retas abrem junto com o rótulo/semente); D3 (cartões com o quadradinho; α = ½: as faixas dos eixos entram junto",
          "com as linhas tracejadas); D3b (rótulo do canto junto com o campo); D4 (RAIO 2, rótulo δ, disco δ e rótulos ½ abrem junto com o objeto);",
          "D5 (quadradinho desde o início; ③: rótulos e tracejados abrem junto; quadradinhos e giros ao entrar); A1 (cantos junto com as etiquetas);",
          "A2 (gota ao entrar); A3 (rótulo CORTE PELO PLANO junto com o campo da carga)."]
    (OUT / f"areas_livres_{R}.txt").write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    p, v = varre()
    print("palco parado > 8 s:", len(p), "· painel vazio > 2 s:", len(v))
    print("leituras:", leituras(), "/ 22")
    print("margens:", margens())
    areas_livres()
    print("ok")
