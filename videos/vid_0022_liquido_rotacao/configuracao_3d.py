"""Estados do asset usados apenas nesta unidade; cache compartilhado pela ponte existente."""
from pathlib import Path

UNIT = Path(__file__).resolve().parent
RES = '540x960'
AMOSTRAS = 24
BASE = dict(estado_visual='fenomeno', marcadores=0, referencia=0, grade=0, meridiana=0, setor=1)
SEQUENCIAS = {
    'plano': dict(params={**BASE, 'lambda':0.0}, frames=96, animado=True),
    # A cena usa somente fases 0..0,5: λ cresce em cosseno e nunca retorna.
    # Offset de rotação igual ao fim do plano; velocidade angular contínua.
    'morph': dict(params={**BASE, 'varrer_lambda':1, 'fase_rotacao':0.25}, frames=128, animado=True),
    'final': dict(params={**BASE, 'lambda':1.0}, frames=96, animado=True),
    'geometria': dict(params=dict(estado_visual='geometria', marcadores=0, referencia=0,
                                setor=0, grade=1, meridiana=1, **{'lambda':1.0}), animado=False),
}

# Mesmo tamanho/centro na cena e no cálculo da correspondência projetada.
ALTURA_IMAGEM = 11.0
CENTRO_IMAGEM = (0.0, 1.2, 0.0)
