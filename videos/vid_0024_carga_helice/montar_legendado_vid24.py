"""Queima legenda.srt no master do vid_0024 com cores por grandeza, usando o montador padrão (videos/montar_legendado.py)
com UMA diferença: a caixa da legenda fica na faixa inferior reservada pela cena (y >= 855 px em 960), e não sobre as
equações e notas. Uso: python montar_legendado_vid24.py MASTER.mp4 LEGENDA.srt SAIDA.mp4"""
import sys
from pathlib import Path

PASTA = Path(__file__).resolve().parent
ORIGEM = PASTA.parent / 'montar_legendado.py'
fonte = ORIGEM.read_text(encoding='utf-8')
alvo = 'bottom = round((821 if pilot else 855) * scale)'
assert alvo in fonte
fonte = fonte.replace(alvo, 'bottom = round((821 if pilot else 935) * scale)')
ns = {'__name__': 'montar_legendado_vid24', '__file__': str(ORIGEM)}
exec(compile(fonte, str(ORIGEM), 'exec'), ns)
sys.argv = ['montar_legendado.py', *sys.argv[1:], '--color-module', str(PASTA / 'cores_legenda.py')]
ns['main']()
