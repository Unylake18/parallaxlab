"""Especificação dos casos do preview padronizado (Python puro: lida pelo script do Blender e pela cena Manim).

Cada caso tem um parâmetro de varredura `p` (raio da gaussiana ou posição da tampa do pillbox): o Blender gera `frames` quadros com
p = p0 → p1 e o Manim escolhe o quadro pelo mesmo valor, então geometria, texto, gráfico e corte 2D nunca saem de sincronia.
"""

RES = "1120x784"
PASTA_SEQ = "renders/preview_gauss_padronizado"      # relativo à raiz do repositório (ignorado pelo Git)

# id: ordem de aparição; p0/p1: faixa de p; az/el: câmera ortográfica fixa; frames: quadros da sequência
CASOS = {
    "linha":      dict(p0=0.5,  p1=1.9,  frames=36, az=-32, el=18),
    "casca_cil":  dict(p0=0.3,  p1=2.0,  frames=36, az=-32, el=18),
    "macico_cil": dict(p0=0.25, p1=2.0,  frames=36, az=-32, el=18),
    "coax":       dict(p0=0.25, p1=1.95, frames=36, az=-32, el=18),
    "folha":      dict(p0=0.3,  p1=2.0,  frames=30, az=-62, el=16),
    "placa":      dict(p0=0.2,  p1=2.0,  frames=36, az=-62, el=16),
    "duas":       dict(p0=-1.7, p1=1.9,  frames=36, az=-62, el=16),
    "face":       dict(p0=0.2,  p1=1.8,  frames=30, az=-62, el=16),
    "casca_esf":  dict(p0=0.3,  p1=2.0,  frames=36, az=-23, el=17),
    "macico_esf": dict(p0=0.3,  p1=2.0,  frames=36, az=-23, el=17),
    "cap_esf":    dict(p0=0.35, p1=2.05, frames=36, az=-23, el=17),
}
ORDEM = list(CASOS)
