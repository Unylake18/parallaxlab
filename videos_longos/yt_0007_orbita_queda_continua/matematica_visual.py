"""Semântica declarada em LaTeX, independente do desenho dos glifos."""
import re
from manim import MathTex, config

BLUE='#267BFF'; CYAN='#35D9FF'; VIOLET='#745CFF'; MAGENTA='#EA63FF'; WHITE='#F5F7FF'
CORES={'M':BLUE,'F_g':CYAN,'g':CYAN,'a_c':CYAN,r'\vec a':CYAN,
       'r':VIOLET,'R':VIOLET,'R_T':VIOLET,'r_b':VIOLET,'s':VIOLET,'a':VIOLET,
       't':MAGENTA,'T':MAGENTA}
PADRAO=re.compile(r'\\(?:mathrm|text|operatorname)(?:\{[^{}]*\}|\s+[A-Za-z])|\\vec\s+[A-Za-z]|F_g|a_c|R_T|r_b|\\[A-Za-z]+|[A-Za-z]')


def semantizar_tex(tex):
    def cor(m):
        token=m.group(0)
        c=CORES.get(token)
        return r'\textcolor[HTML]{'+c[1:]+'}{'+token+'}' if c else token
    return PADRAO.sub(cor,tex)


def formula(tex,size=43,maxw=12):
    # String única: os mapas de MF-Tools operam sobre o conjunto de glifos [0].
    template=config.tex_template.copy()
    template.add_to_preamble(r'\usepackage{xcolor}')
    m=MathTex(semantizar_tex(tex),font_size=size,color=WHITE,tex_template=template)
    m.tex_original=tex
    if m.width>maxw: m.scale_to_fit_width(maxw)
    return m.set_z_index(100)


def valor_tempo(m,valor):
    m.set_value(valor)
    if hasattr(m,'unit_sign'): m.unit_sign.set_color(WHITE)
    return m


def medida(valor,unidade,size=32):
    template=config.tex_template.copy(); template.add_to_preamble(r'\usepackage{xcolor}')
    tex=r'\textcolor[HTML]{745CFF}{'+valor+r'}\,\mathrm{'+unidade+'}'
    return MathTex(tex,font_size=size,color=WHITE,tex_template=template).set_z_index(100)
