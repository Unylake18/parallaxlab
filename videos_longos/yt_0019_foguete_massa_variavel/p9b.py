"""v9: porta o mecanismo de sincronia com a voz contínua do yt_0018 (kit.py v7) para o kit do yt_0019 (sem tocar no yt_0018)."""
from pathlib import Path
from ptch6 import patch

patch("kit.py", [
 # 1) SYNC, LEAD, plano()
 (r'''def dur(aid):
    return ANC[aid]["dur"]
''', r'''SYNC = os.environ.get("SYNC", "final")      # v9: "medir" (passe a seco: mede o tempo nominal de cada trecho) | "final" (encaixa cada trecho na voz)
LEAD = 0.12                                  # v9: a imagem começa ~0,12 s antes da palavra; tolerância -0,15 s … +0,20 s


def plano(A, W, D):
    """(escala das animações, escala das esperas) para encaixar um trecho (A s de animação + W s de espera) em D s (copiado do yt_0010/yt_0018)."""
    if A + W < 1e-6:
        return 1.0, 1.0
    if D >= A + W:
        s_ = min(1.8, max(1.0, (D / (A + W)) ** 0.5))
        return s_, (max(1.0, (D - s_ * A) / W) if W > 1e-6 else 1.0)
    wp = max(0.15 * W, D - A)
    if A + wp <= D + 1e-6:
        return 1.0, wp / W if W > 1e-6 else 1.0
    return max(0.5, (D - wp) / A), (wp / W if W > 1e-6 else 1.0)


def dur(aid):
    return ANC[aid]["dur"]
'''),
 # 2) campos de estado
 (r'''        self.alvo = 0.0
        self.log = []
        self.dica_atual = None
        self._aid, self._q0 = None, 0
        if cap:''', r'''        self.alvo = 0.0
        self.ritmo = 1.0                                    # v9: fator dos plays do trecho corrente (plano())
        self.ritmo_w = 1.0                                  # v9: fator das esperas explícitas do trecho corrente (plano())
        self._off = None                                    # v9: quadro absoluto (da voz) do quadro 0 deste lote
        self._segs, self._cur = [], {"id": "-", "A": 0.0, "W": 0.0}
        self._med, self._mi, self.faltou, self.abertas = None, 0, [], []
        if SYNC == "final" and (AQUI / f"medicao_{self.lote}.json").exists():
            self._med = json.loads((AQUI / f"medicao_{self.lote}.json").read_text(encoding="utf-8"))["marcas"]
        self.log = []
        self.dica_atual = None
        self._aid, self._q0 = None, 0
        if cap:'''),
 # 3) play com fixo e ritmo
 (r'''    def play(self, *anims, run_time=None, **kw):
        if self._pend:
            anims, self._pend = (*anims, *self._pend), []
        anims = tuple(_vivo(a) for a in anims)
        self._still()
        rt = run_time
        if rt is None:
            rt = max([getattr(a, "run_time", 1.0) for a in anims] or [1.0])
''', r'''    def play(self, *anims, run_time=None, fixo=False, **kw):
        if self._pend:
            anims, self._pend = (*anims, *self._pend), []
        anims = tuple(_vivo(a) for a in anims)
        self._still()
        rt = run_time
        if rt is None:
            rt = max([getattr(a, "run_time", 1.0) for a in anims] or [1.0])
        if not fixo:
            if SYNC == "medir":
                self._cur["A"] += rt                         # v9: tempo nominal de animação do trecho (medição)
            rt = rt * self.ritmo                             # v9: espera que anima (fixo=True) não escala; o resto acompanha o plano() do trecho
'''),
 # 4) wait
 (r'''    def wait(self, duration=1.0, *a, **kw):
        self._still()
        n = max(1, round(duration * FPS))''', r'''    def wait(self, duration=1.0, *a, interno=False, **kw):
        """Espera explícita da cena (v9: entra na medição e é esticada pelo plano do trecho); `interno=True` é a espera até um gatilho/fim de âncora."""
        if not interno:
            if SYNC == "medir":
                self._cur["W"] += duration
            else:
                duration = duration * self.ritmo_w
        self._still()
        n = max(1, round(duration * FPS))'''),
])

# 5) gat / ate / resta / an / _fecha / fim  (blocos inteiros)
p = Path(__file__).resolve().parent / "kit.py"
s = p.read_text(encoding="utf-8")
i = s.index("    def gat(self, frase):")
j = s.index("    # cabeçalho ----")
novo = r'''    # v9: marcas de sincronia (início de âncora, gatilho, fração) e plano de cada trecho entre marcas ---------------------
    def _k_frase(self, aid, frase):
        import re as _r
        fala = ANC.get(aid, {}).get("fala", "").split()
        alvo = _r.findall(r"\w+", frase.lower())
        return next((i for i in range(len(fala)) if fala[i:i + len(alvo)] == alvo), None)

    def _tgt(self, kid):
        """Quadro (local do lote) em que a marca `kid` deve acontecer; None se não houver alvo."""
        kind, aid, arg = kid.split(":", 2)
        a = ANC.get(aid)
        if a is None:
            return None
        if kind == "gat":
            k = self._k_frase(aid, arg)
            if k is None:
                return None
            rel = max(0.0, a["t"][k] - LEAD)
        else:
            rel = max(0.0, self.t_ate_aid(aid, float(arg)) - LEAD)
        return round(a["ini"] * FPS) - self._off + rel * FPS

    def _marca(self, kid):
        if SYNC == "medir":
            self._cur = {"id": kid, "A": 0.0, "W": 0.0}
            self._segs.append(self._cur)
        elif self._med is not None and kid != "fim":
            self._plano_para(kid)

    def _plano_para(self, kid):
        """Acha a marca na medição e fixa ritmo/ritmo_w do trecho que começa agora (plano() do yt_0010, por trecho entre marcas)."""
        marcas = self._med
        i = next((j for j in range(self._mi, min(len(marcas), self._mi + 8)) if marcas[j]["id"] == kid), None)
        if i is None:
            self.faltou.append(kid)
            self.ritmo = self.ritmo_w = 1.0
            return
        self._mi = i + 1
        agora = self.nq
        A = W = 0.0
        j, tgt = i, self.alvo
        while j < len(marcas):
            A += marcas[j]["A"]
            W += marcas[j]["W"]
            j += 1
            if j >= len(marcas):
                break
            nid = marcas[j]["id"]
            if nid.startswith("an:") or nid == "fim":
                break
            t_ = self._tgt(nid)
            if t_ is not None and t_ - agora >= 0.25 * FPS:
                tgt = t_
                break
        D = max(0.3, (tgt - agora) / FPS)
        self.ritmo, self.ritmo_w = plano(A, W, D)

    def gat(self, frase):
        """Gatilho de fala (v9): espera até LEAD s antes da palavra (alinhamento da voz contínua) e só então começa o evento seguinte; o plano() do trecho
        anterior já esticou as animações para chegar aqui sem sobra. Registra o instante (relativo ao início da âncora) para o QA."""
        k = self._k_frase(self._aid, frase)
        if k is not None:
            tw = ANC.get(self._aid, {}).get("t")
            prev = max(0.0, (tw[k] if tw else 0.15 + k / 2.7) - LEAD)
            agora = (self.nq - self._q0) / FPS
            if prev - agora >= 1 / FPS:
                self.wait(prev - agora, interno=True)
        else:
            print(f"[gatilho-sem-frase] {self._aid}: {frase!r}")
        print(f"[gatilho] {self._aid} {(self.nq - self._q0) / FPS:.2f} {frase}")
        self._marca(f"gat:{self._aid}:{frase}")

    def t_ate_aid(self, aid, frac):
        a = ANC.get(aid, {})
        tw, nom = a.get("t"), a.get("nominal")
        if not tw or not nom:
            return frac * a.get("dur", 0.0)
        xs = [0.0] + [0.15 + k / 2.7 for k in range(len(tw))] + [max(nom, 0.15 + len(tw) / 2.7)]
        ys = [0.0] + list(tw) + [a["dur"]]
        return float(np.interp(frac * nom, xs, ys))

    def t_ate(self, frac):
        """A fração `frac` (0–1) foi escrita para a janela NOMINAL (2,7 palavras/s). Devolve o instante equivalente na voz real (mesmo ponto do texto)
        menos o LEAD, em segundos desde o início da âncora."""
        return max(0.0, self.t_ate_aid(self._aid, frac) - LEAD)

    def ate(self, frac):
        """Espera até a fração `frac` (0–1) da âncora corrente (mapeada para a voz real pelo texto)."""
        alvo = self._q0 + self.t_ate(frac) * FPS
        if alvo - self.nq >= 1:
            self.wait((alvo - self.nq) / FPS, interno=True)
        self._marca(f"ate:{self._aid}:{frac}")

    def resta(self):
        """Segundos que faltam para o fim da âncora corrente."""
        return max(0.0, (self.alvo - self.nq) / FPS)

    def an(self, aid):
        """Fecha a âncora anterior (espera o resto da fala) e abre `aid`, na hora absoluta da voz (v9: a voz contínua é a régua)."""
        self._fecha()
        a = ANC[aid]
        ini_q = round(a["ini"] * FPS)
        if self._off is None:
            self._off = ini_q - self.nq
        self._aid = aid
        self._q0 = ini_q - self._off
        self.alvo = round(a["fim"] * FPS) - self._off
        self.ritmo = self.ritmo_w = 1.0
        self.abertas.append((aid, (self.nq - self._q0) / FPS))
        self._marca(f"an:{aid}")

    def _fecha(self):
        if self._aid is not None:
            if self.alvo - self.nq >= 1:
                self.wait((self.alvo - self.nq) / FPS, interno=True)
            self.log.append((self._aid, self._q0 / FPS, dur(self._aid), (self.nq - self._q0) / FPS))
            self._aid = None

    def fim(self):
        self._fecha()
        self.log.append(("FIM", self.nq / FPS, 0, 0))
        self._marca("fim")
        if SYNC == "medir":
            (AQUI / f"medicao_{self.lote}.json").write_text(json.dumps({"lote": self.lote, "marcas": self._segs}, indent=0), encoding="utf-8")

'''
s = s[:i] + novo + s[j:]
s = s.replace('''        for aid, t0, prev, real in self.log:
            print(f"[ancora] {aid} {t0:.2f}")
''', '''        for aid, t0, prev, real in self.log:
            print(f"[ancora] {aid} {t0:.2f}")
        for aid, atraso in self.abertas:
            if abs(atraso) > 0.05:
                print(f"[abertura] {aid} atrasada {atraso:+.2f} s")
        if self.faltou:
            print(f"[plano] marcas sem medição (ritmo 1): {self.faltou[:10]}")
''', 1)
p.write_text(s, encoding="utf-8", newline="\n")

# 6) Prob2.wait: encaminha `interno` e escala uma só vez
patch("prob2.py", [
 (r'''    def wait(self, duration=1.0, *a, **kw):
        d = duration
        q = getattr(self, "_quieto", 0.0)''', r'''    def wait(self, duration=1.0, *a, interno=False, **kw):
        if not interno:                                  # v9: mede/escala uma só vez aqui; os pedaços abaixo são internos
            if SYNC == "medir":
                self._cur["W"] += duration
            else:
                duration = duration * self.ritmo_w
        d = duration
        q = getattr(self, "_quieto", 0.0)'''),
 (r'''                super().wait(d)
                q += d
                break
            alvo = self._destaque()''', r'''                super().wait(d, interno=True)
                q += d
                break
            alvo = self._destaque()'''),
 (r'''            if alvo is None or d - max(livre, 0.0) < 0.8:          # sem o que pulsar, ou não cabe o pulso: segue parado
                super().wait(d)''', r'''            if alvo is None or d - max(livre, 0.0) < 0.8:          # sem o que pulsar, ou não cabe o pulso: segue parado
                super().wait(d, interno=True)'''),
 (r'''            if livre > 0.05:
                super().wait(livre)''', r'''            if livre > 0.05:
                super().wait(livre, interno=True)'''),
 (r'''.scale(f, about_edge=borda), run_time=0.8)''', r'''.scale(f, about_edge=borda), run_time=0.8, fixo=True)'''),
])
print("ok")
