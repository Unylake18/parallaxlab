"""Qualidade de render padrão do Parallax Lab: H.264 com CRF 14 nos renders finais (1080p ou maior).

Por que CRF 14: medido num trecho denso (gráfico e linhas finas), abaixo disso o ganho é desprezível (+0,1 dB, +12–25% de arquivo) e
acima disso as linhas finas degradam (SSIM do pior bloco: 0,88 em 14, 0,78 em 16, 0,56 em 20, 0,48 em 23). O Manim grava com CRF 23 fixo;
este módulo troca só o CRF (mesmo codec, pix_fmt e fps).

Ligação automática: `template/config.py` chama `aplicar()` ao ser importado (todo `cena.py` importa o template). Regras:
  - variável de ambiente `CRF` definida  → usa esse valor (ex.: `CRF=0` para fonte sem perdas, `CRF=18` para teste);
  - senão, render com largura ou altura ≥ 1080 → CRF 14;
  - senão (preview 540p etc.) → não mexe (CRF 23 do Manim, mais rápido).
`CRF_PADRAO` é o único lugar onde o número mora.
"""

import os

from manim import config

CRF_PADRAO = "14"


def _trocar_crf(crf):
    import av as _av
    import manim.scene.scene_file_writer as _sfw

    class _Saida:
        def __init__(self, c):
            self._c = c

        def add_stream(self, codec, *a, options=None, **k):
            if options and "crf" in options:
                options = {**options, "crf": crf}
            return self._c.add_stream(codec, *a, options=options, **k)

        def __getattr__(self, n):
            return getattr(self._c, n)

        def __enter__(self):
            return self

        def __exit__(self, *e):
            return self._c.__exit__(*e)

    class _AV:
        def __getattr__(self, n):
            return getattr(_av, n)

        def open(self, *a, **k):
            c = _av.open(*a, **k)
            return _Saida(c) if k.get("mode", a[1] if len(a) > 1 else "r") == "w" else c

    _sfw.av = _AV()


def crf_do_render():
    """CRF a aplicar neste render, ou None para deixar o padrão do Manim."""
    if os.environ.get("CRF"):
        return os.environ["CRF"]
    if max(config.pixel_width, config.pixel_height) >= 1080:
        return CRF_PADRAO
    return None


def aplicar():
    crf = crf_do_render()
    if crf is not None:
        _trocar_crf(crf)
    return crf
