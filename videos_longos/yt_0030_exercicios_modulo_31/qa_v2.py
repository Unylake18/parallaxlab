"""yt_0030 · QA do handoff v2 §8 (relatórios novos): origens_v2.txt (R11), glyphmaps_v2.txt, gatilhos_v2.txt (≤ 0,2 s), r12_v2.txt, r13_v2.txt.
Os demais (transições, holds, sobreposições, setas na chapa, pausas, alinhamento) saem do qa30.py com a rodada v2. uso: python qa_v2.py [rodada]"""
import json
import re
import sys
from pathlib import Path

U = Path(__file__).resolve().parent
R = sys.argv[1] if len(sys.argv) > 1 else "v2"
OUT = U / "renders" / R / "qa"
OUT.mkdir(parents=True, exist_ok=True)
INFO = json.loads((U / "renders" / R / f"lotes_{R}.json").read_text(encoding="utf-8"))
INI = {k: v / 15 for k, v in INFO["inicio"].items()}
ORDEM = list(INFO["inicio"])
LOG = {l: (U / f"log_{l}.txt").read_text(encoding="utf-8", errors="replace") for l in ORDEM}
SOB = {l: ((U / f"log_sob_{l}.txt").read_text(encoding="utf-8", errors="replace") if (U / f"log_sob_{l}.txt").exists() else "") for l in ORDEM}
mm = lambda t: f"{int(t) // 60}:{t % 60:05.2f}"
BLOCO = lambda aid: aid.split("-")[0]


def origens():
    L = [f"yt_0030 {R} · R11 · toda linha de fórmula com a sua origem: a = caneta (sincronizada com a fala), b = voo (TransformFromCopy de uma peça visível),",
         "c = glyph map (TransformByGlyphMap da linha anterior). 'lembrança' = fórmula já vista que volta ao mesmo lugar (FadeIn), registrada à parte.", ""]
    cont = {}
    for l in ORDEM:
        for m in re.finditer(r"\[origem\] (\S+) \S+ (\S+) ([0-9.]+) (.+)", LOG[l]):
            o, aid, t, txt = m.group(1), m.group(2), float(m.group(3)), m.group(4)
            cont[o] = cont.get(o, 0) + 1
            L.append(f"{mm(INI[l] + t)}  {BLOCO(aid):4s} {o:9s} {txt[:150]}")
    sem = [(l, m.group(0)) for l in ORDEM for m in re.finditer(r"\[sem-origem\] .+", LOG[l])]
    L += ["", "TOTAIS: " + " · ".join(f"{k} = {v}" for k, v in sorted(cont.items())), f"SEM ORIGEM: {len(sem)}"] + [f"  {s}" for _, s in sem]
    (OUT / f"origens_{R}.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
    return cont, len(sem)


def glyphmaps():
    L = [f"yt_0030 {R} · TransformByGlyphMap (MF-Tools 1.4.9), todos com mapa explícito montado por chaves de peça; auto_fade nas peças sem par.",
         "Formato: tempo · bloco · pares mapeados · voos (introdutores que voam de uma peça da tela) · linha A → linha B.", ""]
    n = 0
    por = {}
    for l in ORDEM:
        for m in re.finditer(r"\[gm\] \S+ (\S+) ([0-9.]+) pares=(\d+) voos=(\d+) ?(.*?) :: (.+)", LOG[l]):
            n += 1
            b = BLOCO(m.group(1))
            por[b] = por.get(b, 0) + 1
            L.append(f"{mm(INI[l] + float(m.group(2)))} · {b:4s} · pares {int(m.group(3)):2d} · voos {m.group(4)} · auto_fade sim {m.group(5)} · {m.group(6)[:170]}")
    tms = sum(len(re.findall(r"TransformMatchingShapes\(", (U / f).read_text(encoding="utf-8"))) for f in
              ("sec_h.py", "sec_d1.py", "sec_d2.py", "sec_d3.py", "sec_d3b.py", "sec_d4.py", "sec_d5.py", "sec_a1.py", "sec_a2.py", "sec_a4.py", "sec_a3.py", "sec_s.py"))
    L += ["", f"TOTAL: {n} glyph maps (meta ≥ {145 if R not in ('v1', 'v2') else 90}) · por bloco: " + ", ".join(f"{k} {v}" for k, v in por.items()),
          f"Reserva TransformMatchingShapes no código das seções: {tms} (o motor alg30.gm não tem reserva: um mapa que não fecha levanta erro)"]
    (OUT / f"glyphmaps_{R}.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
    return n, tms


def gatilhos():
    L = [f"yt_0030 {R} · gatilhos com atraso > 0,2 s em relação à palavra (orçamento a 3 palavras/s). Tolerância do handoff v2: 0,2 s.", ""]
    tot, ruins, pior = 0, 0, 0.0
    for l in ORDEM:
        for m in re.finditer(r"\[gatilho\] (\S+) +([0-9.]+)s \(alvo +([0-9.]+)s, atraso ([+-][0-9.]+)s\) (.+)", LOG[l]):
            tot += 1
            a = float(m.group(4))
            pior = max(pior, a)
            if a > 0.2 + 1e-9:
                ruins += 1
                L.append(f"{l:5s} {m.group(1):6s} atraso {a:+.2f} s · «{m.group(5)}»")
        for m in re.finditer(r"\[estouro\] (.+)", LOG[l]):
            L.append(f"{l:5s} estouro: {m.group(1)}")
    L += ["", f"{tot} gatilhos · {ruins} acima de 0,2 s · maior atraso {pior:+.2f} s"]
    (OUT / f"gatilhos_{R}.txt").write_text("\n".join(L) + "\n", encoding="utf-8")
    return tot, ruins, pior


def r12():
    L = [f"yt_0030 {R} · R12 · todo valor de rot/div/d₁/d₂ aparece por substituição numa fórmula-mãe escrita antes (tempo da mãe ≤ tempo do valor).", ""]
    for l in ORDEM:
        maes = {}
        for m in re.finditer(r"\[origem\] (\S+) \S+ (\S+) ([0-9.]+) '(.+?)'", LOG[l]):
            tex = m.group(4)
            for k, pat in (("rot", r"\\rot}=\\Qq|\\rot}="), ("div", r"\\dv}="), ("d1", r"d_1="), ("d2", r"d_2=")):
                if re.search(pat, tex) and "=" not in tex.split("=", 1)[1][:0] and k not in maes:
                    maes[k] = float(m.group(3))
        for m in re.finditer(r"\[gm\] \S+ (\S+) ([0-9.]+) pares=\d+ voos=(\d+) .*?:: '(.+?)' → '(.+?)'", LOG[l]):
            b = m.group(5)
            for k, pat in (("rot", r"\\V{\\rot}="), ("div", r"\\D{\\dv}="), ("d1", r"d_1="), ("d2", r"d_2=")):
                if b.startswith(pat.replace("\\\\", "\\").replace("\\{", "{").replace("\\}", "}")) and b.count("=") >= 3:
                    t = float(m.group(2))
                    tm = maes.get(k)
                    ok = "ok" if tm is not None and tm <= t else "SEM MÃE ANTES"
                    L.append(f"{mm(INI[l] + t)} {l:5s} {m.group(1):6s} {k:3s} {b[:90]} · mãe em {mm(INI[l] + tm) if tm is not None else '—'} · {ok}")
    (OUT / f"r12_{R}.txt").write_text("\n".join(L) + "\n", encoding="utf-8")


def r13():
    L = [f"yt_0030 {R} · R13 medido em cada gatilho (passada de auditoria): linhas de conta na coluna (≤ 5 + enunciado), legendas SG Medium seguidas (≤ 2),",
         "linhas que começam por '=' sem a de cima visível (= 0).", ""]
    tot_orf, piores = 0, {}
    for l in ORDEM:
        for m in re.finditer(r"\[r13\] \S+ (\S+) «(.+?)» contas=(\d+) legendas_seguidas=(\d+) orfas=(\d+)", SOB[l]):
            b = BLOCO(m.group(1))
            c, lg, o = int(m.group(3)), int(m.group(4)), int(m.group(5))
            p = piores.setdefault(b, [0, 0, 0])
            p[0], p[1], p[2] = max(p[0], c), max(p[1], lg), p[2] + o
            tot_orf += o
            if c > 6 or lg > 2 or o:
                L.append(f"  {l:5s} {m.group(1):6s} «{m.group(2)}» contas {c} · legendas seguidas {lg} · órfãs {o}")
    L += ["", "POR BLOCO (máx. linhas de conta · máx. legendas seguidas · órfãs):"] + [f"  {b:4s} {p[0]} · {p[1]} · {p[2]}" for b, p in piores.items()]
    L += [f"TOTAL de órfãs: {tot_orf}"]
    (OUT / f"r13_{R}.txt").write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    print("origens:", origens())
    print("glyph maps:", glyphmaps())
    print("gatilhos:", gatilhos())
    r12()
    r13()
    print("ok")
