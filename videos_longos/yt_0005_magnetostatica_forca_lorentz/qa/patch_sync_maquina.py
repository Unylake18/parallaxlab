"""Instala na cena.py o mecanismo de sincronia com a voz (relógio em quadros inteiros, at(n), ritmo, esperas)."""
import sys

src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
falhas = []


def rep(a, b, c=1):
    global s
    if s.count(a) != c:
        falhas.append("(%d x) %s" % (s.count(a), a[:80].replace("\n", "⏎")))
        return
    s = s.replace(a, b)


rep("import math\nimport os\nimport sys\n", "import json\nimport math\nimport os\nimport sys\n")
rep("from manim import AnimationGroup, Axes,", "from manim import Wait, config\nfrom manim import AnimationGroup, Axes,")
rep('SEG = os.environ.get("SEG", "")\n', '''SEG = os.environ.get("SEG", "")
SEGS = {x for x in os.environ.get("SEGS", "").split(",") if x.strip()}      # render só destas seções (grupos paralelos do render final)

# ── Sincronia com a voz (mesmo método do yt_0001/yt_0002; ver sync_voz.py) ───────────────────────────────────────────
# `self.at(n)` marca, na cena, o instante em que COMEÇA a fala da célula n de narracao_sugestao.md (n = ordem das células com fala).
# O tempo de cada fala vem de sync.json (alinhamento medido nas pausas do WAV). A cena espera, ou pede ao áudio uma pausa extra
# (pads.json), para que o acontecimento visual e a fala caiam no mesmo quadro (a fala começa LEAD s antes do evento). Sem sync.json
# (ou com SEM_VOZ=1) a cena roda como o preview sem voz.
VOZ = (Path(__file__).resolve().parent / "sync.json").exists() and os.environ.get("SEM_VOZ") != "1"
CEL_T = [c["onset"] for c in json.loads((Path(__file__).resolve().parent / "sync.json").read_text(encoding="utf-8"))["celulas"]] if VOZ else []
FIM_VOZ = json.loads((Path(__file__).resolve().parent / "sync.json").read_text(encoding="utf-8"))["fala"][1] if VOZ else 0.0
LEAD, TOL, OFFSET0, CAUDA = 0.3, 0.1, 0.7, 2.0      # a fala precede o evento em LEAD s; 0,7 s de silêncio antes da 1ª palavra; cauda após a voz
AJUSTAR = os.environ.get("AJUSTAR") == "1"
RITMO_ARQ = Path(__file__).resolve().parent / "ritmo.json"
RITMO = {} if (AJUSTAR or not VOZ or not RITMO_ARQ.exists()) else json.loads(RITMO_ARQ.read_text(encoding="utf-8"))
P_ESPERA, P_ANIM, FOLGA = 0.4, 0.62, 0.04           # compressão máxima das esperas e das animações antes de pedir pausa ao áudio
CLOCKS_CRIT = ("tt", "tg", "tv", "tw")             # relógios das órbitas: esperas sob eles não se comprimem
''')
rep('''    def setup(self):
        self.camera.background_color = BACKGROUND_COLOR
''', '''    def setup(self):
        self.camera.background_color = BACKGROUND_COLOR
        # relógio da sincronia: T = tempo do vídeo (quadros inteiros); shift = silêncio já inserido no áudio; trecho corrente (entre âncoras)
        self.T, self.shift, self.pads, self.blocos, self.ancoras_log = 0.0, 0.0, [], {}, []
        self.seg_k, self.s0, self.base_a, self.base_w, self.base_f, self.na_at, self.ritmo = "pre", 0.0, 0.0, 0.0, 0.0, False, {}
        self._fixo = False
        if VOZ:
            self._espera(0.0, OFFSET0)                       # silêncio antes da 1ª palavra
''')
rep('''        ativo = (not SEG) or SEG == name or (SEG == "F" and name == "F2") or (SEG == "KA" and name in ("K", "Kend", "rest0", "A")) or (SEG == "B03" and name in ("B", "Bx"))
        self.next_section(name, skip_animations=not ativo)''', '''        ativo = (not SEG) or SEG == name or (SEG == "F" and name == "F2") or (SEG == "KA" and name in ("K", "Kend", "rest0", "A")) or (SEG == "B03" and name in ("B", "Bx"))
        if SEGS:
            ativo = name in SEGS
        self.next_section(name, skip_animations=not ativo)
        self.blocos[name] = round(self.T, 3)''')
rep('''        (always_redraw), o wait() padrão do Manim vira imagem estática quando os updaters não usam dt''', '''        (always_redraw), o wait() padrão do Manim vira imagem estática quando os updaters não usam dt''', 0) if False else None
rep('''        self.wait(d, frozen_frame=False)
''', '''        self._fixo = self._clock_crit()                  # espera sob um relógio de órbita: não se comprime (a fase importa)
        self.wait(d, frozen_frame=False)
        self._fixo = False

    def _clock_crit(self):
        return any(getattr(self, "run", {}).get(k) for k in CLOCKS_CRIT)

    # ── sincronia: relógio em quadros inteiros, ritmo por trecho, esperas pedidas ao áudio ──────────────────────────────
    def play(self, *args, **kwargs):
        return self._tocar(self.compile_animations(*args, **kwargs))

    def _tocar(self, anims):
        """Duração em quadros inteiros: o relógio T (quadros exatos) é o que as âncoras at(n) usam, sem deriva."""
        fps = config.frame_rate
        espera = isinstance(anims[0], Wait)
        static = False
        if espera:
            w0 = anims[0]
            static = bool(w0.is_static_wait) if w0.is_static_wait is not None else False
        m = max(a.run_time for a in anims)
        rt = m
        if VOZ and not self.na_at:
            fixo = espera and self._fixo
            fa, fw = RITMO.get(self.seg_k, (1.0, 1.0))
            if espera:
                if fixo:
                    self.base_f += m
                else:
                    self.base_w += m
            else:
                self.base_a += m
            rt = m * (1.0 if fixo else (fw if espera else fa))
        n = max(1, int(round(rt * fps)))
        real = (n + 0.25) / fps if static else (n - 0.5) / fps
        for a in anims:
            a.run_time = real * a.run_time / m
        self.T += n / fps
        return super().play(*anims)

    def _espera(self, tv, d):
        self.pads.append([round(tv, 3), round(d, 3)])
        self.shift += d

    def _ajusta(self, livre):
        """Fatores (animação, espera) para que o trecho desenhado caiba em `livre` segundos de fala."""
        a, w, f = self.base_a, self.base_w, self.base_f
        sobra = a + w + f - (livre - FOLGA)
        if sobra <= 0 or a + w == 0:
            return
        fw = max(P_ESPERA, 1 - sobra / w) if w else 1.0
        sobra -= w * (1 - fw)
        fa = max(P_ANIM, 1 - sobra / a) if a and sobra > 0 else 1.0
        self.ritmo[self.seg_k] = [round(fa, 3), round(fw, 3)]

    def at(self, n):
        """A próxima animação começa quando a fala da célula n começa (+LEAD): espera até lá, ou pede pausa ao áudio se já passou."""
        if not VOZ:
            return
        tv = CEL_T[n]
        alvo = tv + (LEAD if n else -LEAD) + self.shift
        self._ajusta(alvo - self.s0)
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
        self.ancoras_log.append([n, round(self.T, 3), round(tv, 3), round(self.shift, 3), status])
        self.seg_k, self.s0, self.base_a, self.base_w, self.base_f = str(n), self.T, 0.0, 0.0, 0.0
''')
rep('''        self.bloco_09_fechamento()
''', '''        self.bloco_09_fechamento()
        if VOZ:
            fim = FIM_VOZ + self.shift + CAUDA                 # o vídeo termina CAUDA s depois da última palavra
            if self.T < fim:
                self.na_at = True
                self.hold(fim - self.T)
                self.na_at = False
            base = Path(__file__).resolve().parent
            if AJUSTAR:
                RITMO_ARQ.write_text(json.dumps(self.ritmo, indent=0), encoding="utf-8")
                print(f"ritmo.json: {len(self.ritmo)} trechos comprimidos")
            (base / "pads.json").write_text(json.dumps({"fps": config.frame_rate, "pads": self.pads}, indent=0), encoding="utf-8")
            self.blocos["fim"] = round(self.T, 3)
            (base / "blocos.json").write_text(json.dumps(self.blocos, indent=0), encoding="utf-8")
            (base / "ancoras_log.json").write_text(json.dumps(self.ancoras_log, indent=0), encoding="utf-8")
            print(f"duração total: {self.T:.2f}s · pausas pedidas ao áudio: {len(self.pads)} (+{self.shift:.2f}s)")
''')
open(dst, "w", encoding="utf-8").write(s)
print("falhas:", len(falhas))
for f in falhas:
    print(" -", f)
