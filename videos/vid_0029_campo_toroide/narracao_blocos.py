"""Narração do vid_0029 (fase de voz; V2 da Produção congelada): blocos por beat, na ordem dos eventos do preview v3.

Gera narracao_sugestao.json (blocos, janelas propostas para ~180 s) e texto_narracao_sugestao.txt (texto corrido com as
tags do ElevenLabs v4). O orçamento usa 2,7 palavras/s de fala (briefing) e confere a faixa de 2,5 (medido no vid_0021).
Uso: uv run python videos/vid_0029_campo_toroide/narracao_blocos.py
"""
import json
import re
from pathlib import Path

UNIT = Path(__file__).resolve().parent
RATE, RATE_LOW = 2.7, 2.5
# (beat, janela proposta em s, tag, texto). Janelas propostas para o vídeo de ~180 s, a confirmar com a voz medida.
BLOCOS = [  # Narração V2 (Produção, 2026-10-26): base congelada para a voz. Tags internas ficam no próprio texto.
    ('B01', 12.0, 'curious',
     'Esse anel de fio PRENDE o próprio campo magnético. Liga a corrente... e o campo fica só aqui dentro. '
     'No buraco do meio? Zero. E fora? Zero também. [short pause] Como ele faz isso?'),
    ('B02', 14.0, 'thoughtful',
     'Isso é um toroide: um solenoide dobrado até as pontas se encontrarem. No modelo ideal, as espiras são bem '
     'juntinhas. O número de espiras é o N; a corrente, igual em todas, é o I.'),
    ('B03', 23.0, 'thoughtful',
     'Agora, de cima. O raio médio do anel é o R; o raio do tubo, o a. Desenha um caminho: um círculo em volta do eixo, '
     'com raio r, o raio do caminho. [thoughtful, emphatic] No toroide ideal, a simetria faz o campo acompanhar esse '
     'círculo, com o mesmo módulo em todo ponto. E a gente percorre o caminho no sentido do campo.'),
    ('B04', 25.0, 'thoughtful',
     'Aí entra a Lei de Ampère: a circulação do campo magnético no caminho é mi zero vezes a corrente que atravessa o '
     'disco. Campo e caminho apontam juntos: o produto escalar vira multiplicação simples. E, como o campo vale o mesmo '
     'no círculo todo, ele sai da integral. Sobra o tamanho do caminho... [short pause] desenrola: dois pi vezes o raio '
     'do caminho.'),
    ('B05', 10.0, 'curious',
     'Primeiro teste: o caminho no buraco do anel. Quantos fios atravessam esse disco? [short pause] Nenhum. '
     'Corrente atravessando, zero... então o campo aqui é zero.'),
    ('B06', 31.0, 'thoughtful',
     'Segundo teste: o caminho por dentro do enrolamento. Cada espira fura o disco uma vez, pelo lado de dentro, todas '
     'no mesmo sentido. A corrente que atravessa é o número de espiras vezes a corrente. Passa o dois pi vezes o raio '
     'para o outro lado... [short pause] [excited] e o campo é mi zero vezes o número de espiras vezes a corrente, '
     'dividido por dois pi vezes o raio do caminho. [curious] Repara: o campo não é uniforme. Mais perto do buraco, '
     'mais forte.'),
    ('B07', 18.0, 'curious',
     'E o terceiro: o caminho por fora do anel. Agora cada espira fura o disco DUAS vezes: sobe pelo lado de dentro... '
     'e desce pelo lado de fora. Uma corrente cancela a outra. [short pause] [thoughtful, emphatic] Corrente '
     'atravessando, zero. Campo, zero. É por isso que o campo não escapa.'),
    ('B08', 18.0, 'thoughtful',
     'Agora, o gráfico, aumentando o raio do caminho. No buraco, zero. Entrou no enrolamento, o campo salta. Lá dentro, '
     'cai como um sobre o raio. Saiu, zero de novo. [curious] E na borda de dentro, o campo é quase o DOBRO da borda '
     'de fora.'),
    ('B09', 15.0, 'thoughtful',
     'E dá pra conferir. Se o anel for grande perto do tubo, o raio quase não muda lá dentro. Aí, número de espiras '
     'dividido pela volta do anel vira espiras por metro... [excited] e aparece o campo do solenoide.'),
    ('B10', 14.0, 'calm, satisfied',
     'Resumindo: dentro do enrolamento, o campo cai como um sobre o raio. No buraco e fora, zero, no modelo ideal. '
     'É assim que um solenoide fechado em anel confina o próprio campo. [short pause] Siga o Parallax Lab.'),
]


def falado(texto):
    return re.sub(r'\[[^\]]*\]', ' ', texto)


def main():
    t, rows, linhas = 0.0, [], []
    for beat, janela, tag, texto in BLOCOS:
        n = len(falado(texto).split())
        rows.append({'beat': beat, 'inicio': round(t, 1), 'fim': round(t + janela, 1), 'tag': tag, 'palavras': n,
                     'fala_s': round(n / RATE, 1), 'fala_s_a_2_5': round(n / RATE_LOW, 1),
                     'respiro_s': round(janela - n / RATE, 1), 'texto': texto})
        linhas.append(f'[{tag}] {texto}')
        t += janela
    (UNIT / 'narracao_sugestao.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding='utf-8')
    (UNIT / 'texto_narracao_sugestao.txt').write_text('\n\n'.join(linhas) + '\n', encoding='utf-8')
    total = sum(r['palavras'] for r in rows)
    print(f'total {total} palavras · janela {t:.0f} s · fala {total / RATE:.1f} s a 2,7/s ({total / RATE_LOW:.1f} s a 2,5/s)')
    for r in rows:
        print(f"{r['beat']} {r['inicio']:6.1f}-{r['fim']:6.1f}  {r['palavras']:3d} pal  fala {r['fala_s']:5.1f}s  "
              f"(a 2,5: {r['fala_s_a_2_5']:5.1f}s)  respiro {r['respiro_s']:5.1f}s")


if __name__ == '__main__':
    main()
