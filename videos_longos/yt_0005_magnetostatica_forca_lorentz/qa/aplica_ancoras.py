"""Aplica na cena.py as 137 âncoras self.at(n) e os ajustes de relógio. Uso: python aplica_ancoras.py cena.py saida.py"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ancoras_parte1 import A1
from ancoras_parte2 import A2
from ancoras_parte3 import A3
try:
    from ancoras_extra import AX          # âncoras de palavra (dentro de uma célula): (n, k, trecho)
except ImportError:
    AX = []

src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
falhas = []


def rep(a, b, c=1):
    global s
    if s.count(a) != c:
        falhas.append("(%d x, esperado %d) %s" % (s.count(a), c, a[:90].replace("\n", "⏎")))
        return
    s = s.replace(a, b)


# ── ajustes de máquina ──────────────────────────────────────────────────────────────────────────────────────────────
rep('FIM_VOZ = json.loads((Path(__file__).resolve().parent / "sync.json").read_text(encoding="utf-8"))["fala"][1] if VOZ else 0.0\n',
    'FIM_VOZ = json.loads((Path(__file__).resolve().parent / "sync.json").read_text(encoding="utf-8"))["fala"][1] if VOZ else 0.0\n'
    '_SYNC = json.loads((Path(__file__).resolve().parent / "sync.json").read_text(encoding="utf-8")) if VOZ else {"celulas": [], "words": []}\n'
    'PAL_N = [c["palavra"] for c in _SYNC["celulas"]]                      # índice da 1ª palavra de cada célula\n'
    'WORD_T = [w[1] for w in _SYNC["words"]]                               # início estimado de cada palavra (âncoras dentro de uma célula)\n')
rep('CLOCKS_CRIT = ("tt", "tg", "tv", "tw")             # relógios das órbitas: esperas sob eles não se comprimem\n',
    'CLOCKS_CRIT = ("tt", "tg", "tv", "tw")             # relógios das órbitas: esperas sob eles não se comprimem\n'
    'CLOCKS_EXATOS = ("tg", "tv", "tw")                 # janelas de volta inteira: nada sob eles se comprime (esperas nem animações)\n')
rep('''            fixo = espera and self._fixo
''', '''            fixo = (espera and self._fixo) or any(self.run.get(k) for k in CLOCKS_EXATOS)
''')
novo_at = '''    def _roda(self, clock, dur):
        """Deixa um relógio de órbita correr `dur` s (dentro de uma espera de âncora)."""
        if dur < 0.5 / config.frame_rate:
            return
        self.run[clock] = True
        self.na_at = True
        self.hold(dur)
        self.na_at = False
        self.run[clock] = False

    def at(self, n, k=0, fase=None, clock="tt"):
        """A próxima animação começa quando a fala da célula n começa (+LEAD): espera até lá, ou pede pausa ao áudio se já passou.
        k > 0: âncora na k-ésima palavra da célula (início estimado). fase: termina a volta da órbita (True = relógio tt; ou uma
        função que devolve quanto falta) e a deixa estacionada (relógio parado; quem chama religa) para a próxima condição inicial."""
        if not VOZ:
            return
        tv = CEL_T[n] if k == 0 else WORD_T[PAL_N[n] + k]
        alvo = tv + (LEAD if n else -LEAD) + self.shift
        self._ajusta(alvo - self.s0)
        if fase is not None:
            rem = (self.turn_rem if fase is True else fase)()
            d0 = alvo - self.T
            vol = rem if rem > 0.02 else 0.0
            if d0 > vol:
                vol += int((d0 - vol) // T_PER) * T_PER          # enquanto couber, a órbita segue viva; só o resto fica parado
            self._roda(clock, vol)
        d = alvo - self.T
        status = "ok"
        if d > 0.5 / config.frame_rate:
            self.update_mobjects(0)
            self.na_at = True
            self.hold(d)
            self.na_at = False
            status = f"espera {d:.2f}"
        elif d < -TOL:
            self._espera(tv, -d)
            status = f"pad {-d:.2f}"
        self.ancoras_log.append([n if k == 0 else f"{n}.{k}", round(self.T, 3), round(tv, 3), round(self.shift, 3), status])
        self.seg_k, self.s0, self.base_a, self.base_w, self.base_f = (str(n) if k == 0 else f"{n}.{k}"), self.T, 0.0, 0.0, 0.0

'''
i0, i1 = s.index("    def at(self, n):"), s.index("    def construct(self):")
s = s[:i0] + novo_at + s[i1:]

# finish_turn/turn_rem visíveis para outros métodos
rep('''        def comp_overlay(vecfn, scale, color, names, trk, gh, gv):''',
    '''        self.finish_turn = finish_turn
        self.turn_rem = lambda: (lambda uu: (TP - uu) if uu > 0.02 else 0.0)(max(u_now(), 0.0) % TP)

        def comp_overlay(vecfn, scale, color, names, trk, gh, gv):''')

# relógio da órbita: 5b → 6 (estaciona na origem enquanto as condições iniciais são ditas; volta a rodar ao reiniciar t0)
rep('''        finish_turn()
        self.run["tt"] = True
        self.play(*[FadeOut(m) for m in (tS, tC, ed)], run_time=0.5)''', '''        finish_turn()
        self.play(*[FadeOut(m) for m in (tS, tC, ed)], run_time=0.5)''')
rep('''        o1.t0 = self.tt.get_value()
        ic = eq(''', '''        o1.t0 = self.tt.get_value()
        self.run["tt"] = True
        ic = eq(''')
rep('''        finish_turn()
        self.run["tt"] = True

        # ── 6 ·''', '''        finish_turn()

        # ── 6 ·''')
rep('''        self.hold(TP - 3.4)
        self.run["tt"] = False
''', '''        finish_turn()
''')
rep('''        self.hold(TP - 0.8)                                # uma volta completa do caso q > 0
        troca(True)
''', '''        self.at(47, fase=True)                             # completa a volta do caso q > 0 e estaciona na origem
        troca(True)
        self.run["tt"] = True
''')
rep('''        self.hold(TP - 1.0)                                # uma volta completa do caso q < 0
        form_y = eq(r"v_y(t)", "=", r"v_\\perp\\sin(\\omega_c t)", size=34, colors={0: VIOLET, 2: VIOLET}).move_to([RX, 2.95, 0])
        troca(False)
''', '''        finish_turn()                                      # uma volta completa do caso q < 0
        form_y = eq(r"v_y(t)", "=", r"v_\\perp\\sin(\\omega_c t)", size=34, colors={0: VIOLET, 2: VIOLET}).move_to([RX, 2.95, 0])
        troca(False)
        self.run["tt"] = True
''')
# b02_algebra: período
rep('''        o1.t0 = self.tt.get_value()                      # a trilha recomeça: a volta se desenha enquanto o cronômetro corre
''', '''        o1.t0 = self.tt.get_value()                      # a trilha recomeça: a volta se desenha enquanto o cronômetro corre
        self.run["tt"] = True
''')
rep('''        self.hold(T_PER - 2.0)                           # a volta termina com o cronômetro em T
''', '''        self.finish_turn()                               # a volta termina com o cronômetro em T
        self.run["tt"] = True
''')


# ── âncoras ─────────────────────────────────────────────────────────────────────────────────────────────────────────
def kw_txt(kw):
    if not kw:
        return ""
    if isinstance(kw, str):
        return ", " + kw
    return "".join(", %s=%s" % (k, v) for k, v in kw.items())


todas = []
for lst in (A1, A2, A3):
    for it in lst:
        n, ancora = it[0], it[1]
        occ = it[2] if len(it) > 2 else 0
        kw = it[3] if len(it) > 3 else None
        if n == 47:
            continue                                  # já inserida acima (completa a volta e estaciona)
        todas.append((n, 0, ancora, occ, kw))
for n, k, ancora in AX:
    todas.append((n, k, ancora, 0, None))

feitas = 0
for n, k, ancora, occ, kw in todas:
    # as correções acima podem ter alterado o trecho que serve de âncora (finish_turn sem a linha de relógio)
    cand = ancora
    if s.count(cand) == 0 and n == 40:
        cand = '        finish_turn()\n        self.play(*[FadeOut(m) for m in (tS, tC, ed)], run_time=0.5)'
    if s.count(cand) == 0 and n == 44:
        cand = '        finish_turn()\n\n        # ── 6 ·'
    if s.count(cand) != 1:
        falhas.append("âncora %s%s: %d ocorrências: %s" % (n, "" if k == 0 else ".%d" % k, s.count(cand), ancora[:80].replace("\n", "⏎")))
        continue
    j = s.index(cand)
    ls = s.rfind("\n", 0, j) + 1
    ind = re.match(r" *", s[ls:j + len(cand)]).group(0) if s[ls:j].strip() == "" else ""
    if s[ls:j].strip() != "":
        falhas.append("âncora %s: o trecho não começa no início da linha" % n)
        continue
    args = "%d%s%s" % (n, (", k=%d" % k) if k else "", kw_txt(kw))
    s = s[:ls] + ind + "self.at(%s)\n" % args + s[ls:]
    feitas += 1

open(dst, "w", encoding="utf-8").write(s)
print("âncoras inseridas:", feitas + 1, "(+ 47 explícita) | falhas:", len(falhas))
for f in falhas:
    print(" -", f)
