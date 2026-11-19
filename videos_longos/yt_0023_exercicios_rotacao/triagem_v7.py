"""yt_0023 v7 §4: triagem do portão por evento (renders/qa.txt) → renders/v7/triagem_portao.txt
Cada evento REAL do qa23 vira (lote, tempo, classe, objetos, REAL | INTENCIONAL + motivo). Regras (por regra, não por quadro, salvo os casos
conferidos à mão, listados em MANUAL com o veredito e o motivo):"""
import re
from collections import Counter, defaultdict
from pathlib import Path
U = Path(__file__).resolve().parent
txt = (U / "renders/qa.txt").read_text(encoding="utf-8")
ev = []
lot = None
for ln in txt.splitlines():
    m = re.match(r"^  (P[A-Za-z0-9]+): eventos REAIS", ln)
    if m:
        lot = m.group(1); continue
    m = re.match(r"^\s+([\d.]+)–\s*([\d.]+) s\s+REAL\s+(.*)$", ln)
    if m and lot:
        t0, t1, resto = float(m.group(1)), float(m.group(2)), m.group(3)
        cl = None
        for c in ("TEXTO SOBRE OBJETO", "TEXTO SOBRE CAIXA", "OBJETO FORA DA MARGEM", "FORA DA MARGEM", "LINHA ÚNICA", "LINHA ÓRFÃ", "COLUNA VAZIA", "SOBREPOSICAO",
                  "ENCOSTADO", "TRÂNSITO", "SEM PALCO", "TEXTO PEQUENO", "OPACIDADE", "COR POR TOKEN", "DEGRADÊ FORA DO ⊕"):
            if resto.startswith(c):
                cl = c; break
        ev.append((lot, t0, t1, cl or resto.split()[0], resto[len(cl or ""):].strip()))
# vereditos conferidos à mão (quadro a quadro, v6/v7); chave = (lote, classe, tempo aproximado)
MANUAL = {
    ("PE1b", "SOBREPOSICAO", 253.0): ("INTENCIONAL", "destaque da trilha por cópia ampliada (ind_copia), 0,8 s; o fantasma da troca de opacidade foi eliminado (tr_acende só muda opacidade)"),
    ("PE2", "SOBREPOSICAO", 22.3): ("INTENCIONAL", "destaque da trilha por cópia ampliada (ind_copia) sobre FORÇA, 0,8 s"),
    ("PE1a", "SOBREPOSICAO", 254.7): ("INTENCIONAL", "destaque por cópia ampliada do cartão VÍNCULO / a = αr, 0,8 s"),
    ("PH", "SOBREPOSICAO", 3.7): ("INTENCIONAL", "voo da cópia do rótulo de massa (6,0 kg) até a vaga, 0,6 s"),
}
def veredito(lote, t0, t1, cl, det):
    for (l, c, t), v in MANUAL.items():
        if l == lote and c == cl and abs(t0 - t) < 1.2:
            return v
    dur = t1 - t0
    iguais = False
    m = re.match(r"'(.*?)' x '(.*?)'", det)
    if m and m.group(1) == m.group(2):
        iguais = True
    if cl in ("LINHA ÚNICA", "SOBREPOSICAO", "TRÂNSITO") and iguais and dur <= 1.0:
        return ("INTENCIONAL", "mesmo texto nos dois lados por ≤ 1,0 s: troca/cópia em voo ou destaque deliberado")
    if cl == "TRÂNSITO" and dur <= 1.0:
        return ("INTENCIONAL", "glifo em voo da origem à vaga (≤ 1,0 s)")
    if cl == "LINHA ÚNICA" and dur <= 0.2:
        return ("INTENCIONAL", "uma amostra (≤ 0,2 s) na troca de linha da CONTA")
    if cl == "SEM PALCO" and dur <= 1.5:
        return ("INTENCIONAL", "abertura/troca de seção, só texto por ≤ 1,5 s")
    if cl == "TEXTO SOBRE OBJETO":
        m = re.match(r"'(.*?)' x (Circle|Line|DashedLine|Annulus|Arc|Polygon|VMobject|RoundedRectangle)", det)
        if m and len(re.sub(r"[\{}_ ^]|mathrm|frac|tfrac|vec", "", m.group(1))) <= 6:
            return ("INTENCIONAL", "símbolo curto (R, r, M, m, l, θ, D, a_c…) preso ao próprio desenho que ele nomeia")
        return ("REAL", "texto longo cruzando um traço do desenho: conferir")
    if cl == "TEXTO PEQUENO":
        return ("INTENCIONAL", "cartão/linha pequena da lei ou da conferência, legível a 960×540 (piso da escala dos cartões)")
    if cl == "COR POR TOKEN":
        return ("INTENCIONAL", "token herda a cor do rótulo de origem no passo/voo (cor da grandeza preservada)")
    if cl == "TEXTO SOBRE CAIXA":
        return ("INTENCIONAL", "rótulo cruzando a borda da caixa do resultado durante a entrada (≤ 0,6 s)") if dur <= 0.6 else ("REAL", "texto cruzando caixa por > 0,6 s: conferir")
    if cl == "ENCOSTADO":
        return ("INTENCIONAL", "itens da mesma linha/equação com folga < 0,1 u por ≤ 0,3 s (entrada)") if dur <= 0.3 else ("REAL", "itens encostados por > 0,3 s: conferir")
    if cl in ("FORA DA MARGEM", "OBJETO FORA DA MARGEM", "OPACIDADE", "SOBREPOSICAO", "LINHA ÚNICA", "COLUNA VAZIA", "LINHA ÓRFÃ"):
        return ("REAL", "classe prioritária sem regra de dispensa: conferir/corrigir")
    return ("REAL", "sem regra")
por = defaultdict(list)
for lote, t0, t1, cl, det in ev:
    v, mot = veredito(lote, t0, t1, cl, det)
    por[cl].append((lote, t0, t1, det, v, mot))
out = ["TRIAGEM DO PORTÃO POR EVENTO (v7 §4) — classificação por regra + casos conferidos à mão",
       "Formato: lote | tempo | objetos | REAL ou INTENCIONAL + motivo. REAL = o espectador percebe (ou classe prioritária sem dispensa); INTENCIONAL = ruído do detector/efeito deliberado.", ""]
tot = Counter()
for cl in sorted(por):
    r = Counter(v for *_, v, _ in por[cl]); tot.update(r)
    out.append(f"== {cl}: REAL {r.get('REAL', 0)} · INTENCIONAL {r.get('INTENCIONAL', 0)}")
    for lote, t0, t1, det, v, mot in sorted(por[cl]):
        out.append(f"  {lote:5s} {t0:7.1f}–{t1:7.1f} s  {det[:70]:70s}  {v}: {mot}")
    out.append("")
out.append(f"REAIS restantes: {tot.get('REAL', 0)}; INTENCIONAIS: {tot.get('INTENCIONAL', 0)} (motivo por linha acima)")
(U / "renders/v7/triagem_portao.txt").write_text("\n".join(out), encoding="utf-8")
print(out[-1])
for cl in sorted(por):
    r = Counter(v for *_, v, _ in por[cl]); print(cl, dict(r))
