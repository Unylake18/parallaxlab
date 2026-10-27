"""QA da sincronia: início real de cada evento do Manim × instante da palavra que o nomeia.

Lê timeline.json (ancoras = palavra − 0,1 s) e <midia>/estados.json (gravado pelo render). Para cada âncora esperada na
palavra (sem antecipação de preparo), atraso = início do evento − início da palavra. Critério: atraso ≤ 0,2 s.
Os eventos do 3D (liga, campo, contagens, câmera, varredura) saem direto do timeline: atraso 0 por construção.
Uso: uv run python videos/vid_0029_campo_toroide/qa/conferir_sync.py [media_preview|media_final]
"""
import json
import sys
from pathlib import Path

UNIT = Path(__file__).resolve().parents[1]
LEAD = 0.1


def main():
    midia = sys.argv[1] if len(sys.argv) > 1 else 'media_preview'
    X = json.loads((UNIT / 'timeline.json').read_text(encoding='utf-8'))['ancoras']
    sync = json.loads((UNIT / midia / 'estados.json').read_text(encoding='utf-8'))['ancoras']
    rows, worst = [], 0.
    for s in sync:
        lead = round(X[s['ancora']] - s['alvo_s'], 3)
        if lead > 1e-3:        # preparo antecipado de propósito (ex.: tirar o chip antes da próxima frase)
            continue
        palavra = X[s['ancora']] + LEAD
        atraso = round(s['inicio_s'] - palavra, 3)
        worst = max(worst, atraso)
        rows.append((s['ancora'], palavra, s['inicio_s'], atraso))
    for name, p, i, d in rows:
        flag = '  <-- ACIMA DE 0,2 s' if d > .2 else ''
        print(f'{name:24s} palavra {p:7.2f}  evento {i:7.2f}  atraso {d:+.2f}s{flag}')
    print(f'\n{len(rows)} eventos ancorados na fala - pior atraso {worst:+.3f} s - '
          f"{'OK (<= 0,2 s)' if worst <= .2 else 'REPROVADO'}")


if __name__ == '__main__':
    main()
