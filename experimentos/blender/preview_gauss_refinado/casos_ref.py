"""Especificação dos três casos do preview refinado (Python puro: lida pelo Blender e pelo Manim).

`p` é o parâmetro de varredura (raio da gaussiana ou posição da tampa direita do pillbox): o Blender gera `frames` quadros com
p = p0 → p1 e o Manim escolhe o quadro pelo mesmo valor.
"""

RES = "1120x784"
PASTA_SEQ = "renders/preview_gauss_refinado"       # relativo à raiz do repositório (ignorado pelo Git)

CASOS = {
    "coax":   dict(p0=0.25, p1=1.9, frames=40, az=-32, el=18, margem=0.03),
    "duas":   dict(p0=-1.7, p1=1.9, frames=40, az=-62, el=16, margem=0.03),
    "esfera": dict(p0=0.08, p1=1.5, frames=44, az=-23, el=17, margem=0.02),   # r1 = 1,5 R: a esfera ocupa mais o quadro
}
ORDEM = list(CASOS)
