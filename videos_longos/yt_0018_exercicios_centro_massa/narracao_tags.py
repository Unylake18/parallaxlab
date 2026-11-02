"""yt_0018 v5 §5: gera narracao_tags_v1_1.md (narração v1.1 = a v2.2 com os sete ajustes do handoff v5) e o diff para a v1 (narracao_tags_v1.md).
v4 §9: a narração com tags para validação, sem gerar áudio.
Uma tag por âncora (as que faltavam ganham a de base: [thoughtful] na explicação, [curious] na pergunta/virada), sem [slowly]; as pausas
([short pause], reticências) ficam como estão; as palavras-gatilho de cada âncora (todos os gat() das cenas) aparecem em **negrito**, e as do
§8 levam ⁸. Contagem de palavras e duração estimada (2,7 palavras/s, o ritmo do roteiro; e a 3,0, o teto do ElevenLabs).
uso: python narracao_tags.py"""
import difflib
import re
from pathlib import Path

U = Path(__file__).resolve().parent
t = (U / "narracao_sugestao.md").read_text(encoding="utf-8")
t = t[:t.rindex("## Números de conferência")]
TAG_NOVA = {"H2": "[curious]", "A3": "[thoughtful]", "X0-3": "[thoughtful]", "X1-3": "[thoughtful]", "X2-3": "[thoughtful]", "X3-3": "[thoughtful]",
            "X4-5": "[thoughtful]", "EN1": "[happy]"}
PAUSA = {"X5-6": ("essa aceleração para baixo: quarenta", "essa aceleração para baixo: [short pause] quarenta")}
OITO = {("A3", "pesada pelas massas"), ("A3", "se move"), ("X3-3", "a folha ganha o mesmo momento para trás"), ("X3-6", "multiplicando essa velocidade relativa"),
        ("X3-6", "o seno do dobro do ângulo"), ("X3-7", "no quase vertical"), ("X3-8", "se a folha fosse pesadíssima"), ("X4-1", "o dobro da massa"),
        ("X5-3", "qual é o sistema"), ("X5-5", "um vírgula sessenta e três")}
ARRED = [("4,23°", "quatro vírgula dois graus"), ("85,77°", "oitenta e cinco vírgula oito"), ("0,81 s", "oito décimos de segundo"),
         ("4,4 mm", "quatro milímetros"), ("81 cm", "oitenta centímetros")]

# gatilhos de fala das cenas: gat("…") depois de an("…"), na ordem do código
gat = {}
for f in ("sec_hook.py", "sec_x01.py", "sec_x2.py", "sec_x3.py", "sec_x4.py", "sec_x5.py", "sec_fim.py"):
    aid = None
    for m in re.finditer(r'self\.(an|gat)\("([^"]+)"\)', (U / f).read_text(encoding="utf-8")):
        if m.group(1) == "an":
            aid = m.group(2)
        elif aid:
            gat.setdefault(aid, []).append(m.group(2))

blocos = []
for bloco in re.split(r"^### ", t, flags=re.M)[1:]:
    cab, *resto = bloco.split("\n")
    aid = cab.split(" — ")[0].strip()
    fala = " ".join(l.strip() for l in resto if l.strip() and not l.startswith(("---", "## ", "**", ">")))
    if aid in PAUSA:
        a, b = PAUSA[aid]
        assert a in fala, (aid, a)
        fala = fala.replace(a, b)
    if not fala.startswith("["):
        fala = TAG_NOVA[aid] + " " + fala
    assert "slowly" not in fala and fala.count("[") - fala.count("[short pause]") == 1, (aid, fala[:60])
    blocos.append((aid, fala))


def marca(aid, fala):
    """Negrito nas palavras-gatilho (casa sem acento de pontuação: a frase do gat() é em minúsculas, sem vírgulas)."""
    out, faltam = fala, []
    for fr in gat.get(aid, []):
        pal = fr.split()
        rx = r"(?i)\b" + r"[\s,.;:…]+".join(re.escape(p) for p in pal) + r"\b"
        m = re.search(rx, out)
        if not m:
            faltam.append(fr)
            continue
        sup = "⁸" if (aid, fr) in OITO else ""
        out = out[:m.start()] + "**" + m.group(0) + "**" + sup + out[m.end():]
    return out, faltam


L = ["# yt_0018 — narração v1.1 com audio tags (para validação; texto final da estimativa de duração do v5)", "",
     "> Handoff v4 §9. Texto da fala âncora por âncora, com a tag do ElevenLabs v4 (uma por trecho, em inglês, sem `[slowly]`), as pausas, os "
     "números escritos como serão falados e as **palavras-gatilho** da cena em negrito (⁸ = gatilho corrigido no §8). Duração estimada a 2,7 "
     "palavras/s (ritmo do roteiro) e a 3,0 (teto da voz). **Não gerar áudio**: o Kaio valida este texto e libera a voz.", "",
     "**v1.1 (handoff v5 §5), sete ajustes de texto:** X1-3 (o furo: centro oito centímetros para a direita e oito para cima) · X1-4 (\"por que aqui ele andou pouco\") · "
     "X4-1 (massas mil e dois mil quilos; três mil joules) · X4-5 (a divisão 2 : 1 vale só no referencial do centro de massa; o total liberado não depende do referencial) · "
     "X5-1 (suporte de dois quilos; blocos de três e de um quilo) · X5-7 (\"catorze vírgula sete\") · H3 (\"cinco problemas que parecem impossíveis\"). "
     "Da v1: trocas da v2.2 (A2, X0-3, X3-8, X5-8 e EP2; X5-5 em `[emphatic]`). Tags novas onde "
     "faltavam (uma por trecho): " + ", ".join(f"{k} {v}" for k, v in TAG_NOVA.items()) + ". Pausa nova: X5-6 `[short pause]` antes dos 49 newtons.", "",
     "| Âncora | Palavras | 2,7 p/s | 3,0 p/s |", "|---|---:|---:|---:|"]
tot = 0
corpos, faltas = [], []
for aid, fala in blocos:
    n = len(re.findall(r"\w+", re.sub(r"\[[^\]]*\]", "", fala)))
    tot += n
    L.append(f"| {aid} | {n} | {n / 2.7:.1f} s | {n / 3.0:.1f} s |")
    m, falta = marca(aid, fala)
    corpos.append((aid, m, gat.get(aid, [])))
    faltas += [(aid, f) for f in falta]
L.append(f"| **total** | **{tot}** | **{tot / 2.7 / 60:.2f} min** | **{tot / 3.0 / 60:.2f} min** |")
L += ["", "## Conferência dos arredondamentos falados (a tela mostra o valor exato)", ""]
inteiro = " ".join(f for _, f in blocos)
for tela, fala in ARRED:
    L.append(f"- {tela} → \"{fala}\": {'presente' if fala in inteiro else 'FALTA'}")
L += ["", "## Fala por âncora (tags, pausas e gatilhos)", ""]
for aid, m, gs in corpos:
    L += [f"### {aid}", m, ""]
    if gs:
        L += ["Gatilhos: " + " · ".join(f"\"{g}\"" + (" (§8)" if (aid, g) in OITO else "") for g in gs), ""]
if faltas:
    L += ["Gatilhos de tela sem a frase na fala (só tela): " + "; ".join(f"{a} \"{f}\"" for a, f in faltas), ""]
L += ["## Texto corrido (para gravação)", ""]
L += [f for _, f in blocos]
antiga = {}
if (U / "narracao_tags_v1.md").exists():
    for bl in re.split(r"^### ", (U / "narracao_tags_v1.md").read_text(encoding="utf-8").split("## Fala por âncora")[-1].split("## Texto corrido")[0], flags=re.M)[1:]:
        cab, *rs = bl.split("\n")
        antiga[cab.strip()] = " ".join(x.strip() for x in rs if x.strip() and not x.startswith("Gatilhos"))
dif = ["", "## Diferenças para a v1 (narracao_tags_v1.md)", ""]
tem = False
for aid, fala in blocos:
    a_ = antiga.get(aid, "").replace("**", "").replace("⁸", "")
    if a_ and a_ != fala:
        tem = True
        pa, pb = a_.split(), fala.split()
        sm_ = difflib.SequenceMatcher(None, pa, pb)
        partes = []
        for op_, i1, i2, j1, j2 in sm_.get_opcodes():
            if op_ == "equal":
                continue
            partes.append(("− " + " ".join(pa[i1:i2]) if i2 > i1 else "") + (" → " if i2 > i1 and j2 > j1 else "") + ("+ " + " ".join(pb[j1:j2]) if j2 > j1 else ""))
        dif.append(f"- **{aid}**: " + " ｜ ".join(partes))
if not tem:
    dif.append("(sem diferenças)")
i_ = L.index("## Fala por âncora (tags, pausas e gatilhos)")
L[i_:i_] = dif[1:] + [""]
(U / "narracao_tags_v1_1.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print(f"{len(blocos)} âncoras, {tot} palavras, {tot / 2.7 / 60:.2f} min a 2,7 p/s; gatilhos sem frase na fala: {len(faltas)}")
