"""Trajetória temporal de p para um caso (Python puro; lida pelo Blender e pelo Manim): o mesmo padrão do coaxial limpo, parametrizado por waypoints.

wps = [(p, quadros_de_pausa), ...]: intro (geometria sem gaussiana), pausa em p0, e para cada waypoint seguinte um movimento (suavização cúbica) seguido de pausa.
O quadro k do vídeo (30 fps) mostra a imagem renderizada para p(k): um arquivo por quadro em movimento, um só por pausa e um para a intro.
"""

FPS = 30
ss = lambda x: 0.0 if x <= 0 else 1.0 if x >= 1 else x * x * (3 - 2 * x)      # noqa: E731


class Traj:
    def __init__(self, wps, intro=45, mv=72):
        self.segs = [("intro", intro, None), ("h0", wps[0][1], wps[0][0])]
        for i in range(1, len(wps)):
            self.segs.append((f"m{i}", mv, (wps[i - 1][0], wps[i][0])))
            self.segs.append((f"h{i}", wps[i][1], wps[i][0]))
        self.inicio, ac = {}, 0
        for nome, n, _ in self.segs:
            self.inicio[nome] = ac
            ac += n
        self.total = ac
        self._d = {nome: (n, p) for nome, n, p in self.segs}

    def segmento(self, k):
        k = min(max(k, 0), self.total - 1)
        for nome, n, _ in reversed(self.segs):
            if k >= self.inicio[nome]:
                return nome, k - self.inicio[nome]

    def p_em_quadro(self, k):
        nome, j = self.segmento(k)
        n, p = self._d[nome]
        if p is None:
            return None
        if isinstance(p, tuple):
            return p[0] + (p[1] - p[0]) * ss(j / n)
        return p

    def chave(self, k):
        nome, j = self.segmento(k)
        return f"{nome}_{j:03d}" if nome.startswith("m") else nome

    def quadros_unicos(self):
        vistos, out = set(), []
        for k in range(self.total):
            c = self.chave(k)
            if c not in vistos:
                vistos.add(c)
                out.append((c, self.p_em_quadro(k)))
        return out


# p = raio da gaussiana (cilindros e esferas) ou posição da tampa direita do pillbox (planares); az/el = câmera ortográfica fixa
CASOS = {
    "linha":      dict(wps=[(0.35, 36), (1.0, 48), (1.7, 54)],  az=-32, el=18, margem=0.035),
    "casca_cil":  dict(wps=[(0.45, 36), (1.3, 54), (1.75, 54)], az=-32, el=18, margem=0.035),
    "macico_cil": dict(wps=[(0.45, 36), (0.85, 48), (1.6, 54)], az=-32, el=18, margem=0.035),
    "folha":      dict(wps=[(0.3, 36), (1.0, 48), (1.8, 54)],   az=-62, el=16, margem=0.04),
    "placa":      dict(wps=[(0.3, 36), (0.55, 48), (1.7, 54)],  az=-62, el=16, margem=0.04),
    "duas":       dict(wps=[(-1.7, 36), (0.0, 54), (1.75, 54)], az=-62, el=16, margem=0.04),
    "face":       dict(wps=[(0.25, 36), (1.0, 48), (1.7, 54)],  az=-62, el=16, margem=0.04),
    "casca_esf":  dict(wps=[(0.4, 36), (1.3, 54), (1.7, 54)],   az=-23, el=17, margem=0.03),
    "macico_esf": dict(wps=[(0.4, 36), (0.8, 48), (1.5, 54)],   az=-23, el=17, margem=0.03),
    "cap_esf":    dict(wps=[(0.4, 36), (1.15, 54), (1.85, 54)], az=-23, el=17, margem=0.03),
}
ORDEM = list(CASOS)
