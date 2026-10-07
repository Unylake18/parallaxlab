"""Ponte Blender -> Manim, camada 2: usa um sólido do arsenal dentro de uma cena Manim (sandbox).

    import sys
    sys.path.insert(0, "experimentos/blender/arsenal")     # a partir da raiz do repositório
    from manim_solido3d import Solido3D

    class MinhaCena(Scene):
        def construct(self):
            fio = Solido3D("fio_infinito")                  # animado (cargas em loop) se a ficha permitir
            img = fio.mobject(cena=self, altura=5, centro=RIGHT * 3)   # ImageMobject; as cargas andam sozinhas
            self.play(FadeIn(img))
            self.wait(4)                                    # 2 loops de 2 s (periodo=2.0)
            img.pausar()                                    # congela; img.retomar() continua; img.set_fase(0.25)
            # a fase atual: img.fase_atual()

            casca = Solido3D("casca_cilindrica_oca")        # estático: um único quadro
            self.play(FadeIn(casca.mobject(altura=4)))

Como funciona: as imagens são sequências PNG RGBA geradas pelo Blender (ver `ponte.py`) e guardadas em cache em
`renders/arsenal3d/`; a primeira chamada renderiza (segundos), as seguintes leem do disco. Cada quadro é lido do
disco sob demanda (memória baixa) e o loop usa `fase` de 0 a 1: fase=1 repete a fase 0, então o loop não tem emenda.
O sentido da corrente e o sinal das cargas NÃO vêm do 3D: desenhe setas e rótulos em Manim por cima.

Resolução: por padrão a do quadro de render do Manim (`config.pixel_width x pixel_height`), então o preview
(960x540) e o final (1920x1080) usam sequências diferentes, cada uma no tamanho certo.
Para preparar antes (recomendado no final):  python experimentos/blender/arsenal/ponte.py <id> --res 1920x1080
"""

import sys
from collections import OrderedDict
from pathlib import Path

import numpy as np
from manim import ORIGIN, ImageMobject, config
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ponte  # noqa: E402


class Solido3D:
    """Sólido do arsenal pronto para uma cena Manim.

    solido: id do arsenal (ex.: "fio_infinito"). animado: None = animado se a ficha permitir. params: sobrescreve
    parâmetros da ficha (ex.: {"espaco_cargas": 0.5}). frames: quadros do loop (padrão: da ficha). res: "LxA"
    (padrão: a resolução de render do Manim). render: "auto" renderiza se faltar; "nunca" exige sequência pronta.
    """

    def __init__(self, solido, *, animado=None, params=None, frames=None, res=None, amostras=64, render="auto",
                 forcar=False):
        res = res or f"{config.pixel_width}x{config.pixel_height}"
        self.seq = ponte.sequencia(solido, params, animado=animado, frames=frames, res=res, amostras=amostras,
                                   render=render, forcar=forcar)
        self._cache = OrderedDict()                 # quadros decodificados recentes (LRU)

    @property
    def animado(self):
        return self.seq.animado

    @property
    def frames(self):
        return self.seq.frames

    def quadro(self, i):
        """Quadro `i` como array RGBA uint8 (leitura do disco, com cache LRU curto)."""
        i %= self.seq.frames
        if i not in self._cache:
            self._cache[i] = np.array(Image.open(self.seq.quadro(i)).convert("RGBA"))
            while len(self._cache) > 16:
                self._cache.popitem(last=False)
        else:
            self._cache.move_to_end(i)
        return self._cache[i]

    def indice(self, fase):
        """Quadro mais próximo da fase. Os quadros foram renderizados nas fases i/N, então arredondar (e não
        truncar) evita que 0,99999… por erro de ponto flutuante caia no quadro N-1 em vez do 0."""
        return int(round((fase % 1.0) * self.seq.frames)) % self.seq.frames

    def mobject(self, cena=None, altura=None, largura=None, centro=ORIGIN, periodo=2.0, autoplay=True, fase=0.0):
        """ImageMobject do sólido, já posicionado. Se animado, as cargas andam: um loop completo a cada `periodo`
        segundos de cena (enquanto `autoplay`). Controles no próprio mobject: `.pausar()`, `.retomar()`,
        `.set_fase(x)` e `.fase_atual()` (fase atual, 0 a 1).

        cena: a cena (`cena=self`); OBRIGATÓRIA para sólido animado. A fase é calculada a partir de `cena.time`,
        não somando `dt`: durante um FadeIn/FadeOut aplicado ao próprio mobject o Manim chama o updater duas vezes
        por quadro, e somar `dt` faria o movimento andar em dobro.
        altura/largura em unidades do Manim (o outro lado segue a proporção da imagem); sem nenhum dos dois, a
        imagem ocupa a altura do quadro. A imagem tem fundo transparente: o que estiver atrás do sólido aparece.
        """
        if self.animado and cena is None:
            raise TypeError("Solido3D.mobject(): passe cena=self para sólidos animados (a fase vem de cena.time).")
        mob = ImageMobject(self.quadro(self.indice(fase)))
        if largura is not None:
            mob.set_width(largura)
        else:
            mob.set_height(altura if altura is not None else config.frame_height)
        mob.move_to(centro)
        agora = (lambda: cena.time) if cena is not None else (lambda: 0.0)
        # fase(t) = base + (t - t_ref) / periodo enquanto ativo; congelada em `base` quando pausado
        estado = {"base": fase % 1.0, "t_ref": agora(), "ativo": bool(autoplay and self.animado)}

        def fase_atual():
            if not estado["ativo"]:
                return estado["base"] % 1.0
            return (estado["base"] + (agora() - estado["t_ref"]) / periodo) % 1.0

        def aplicar():
            arr = self.quadro(self.indice(fase_atual()))
            # Cópia: o `set_opacity` do Manim reescreve o alpha in place, e não pode contaminar o cache.
            mob.pixel_array = arr.copy()
            mob.orig_alpha_pixel_array = arr[:, :, 3]
            if mob.stroke_opacity < 1:                  # preserva FadeIn/FadeOut em andamento
                mob.pixel_array[:, :, 3] = (arr[:, :, 3] * mob.stroke_opacity).astype(mob.pixel_array.dtype)

        def passo(m, dt):
            if estado["ativo"]:
                aplicar()

        def set_fase(x):
            estado.update(base=x % 1.0, t_ref=agora())
            aplicar()
            return mob

        def pausar():
            estado.update(base=fase_atual(), ativo=False)
            return mob

        def retomar():
            if self.animado:
                estado.update(t_ref=agora(), ativo=True)
            return mob

        mob.set_fase, mob.pausar, mob.retomar, mob.fase_atual = set_fase, pausar, retomar, fase_atual
        if self.animado:
            mob.add_updater(passo)
        return mob
