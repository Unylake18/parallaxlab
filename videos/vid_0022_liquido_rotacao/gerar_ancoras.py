"""Âncoras da gravação confirmada (458 palavras), em quatro blocos visuais."""
import json,re
from pathlib import Path
U=Path(__file__).resolve().parent
words=json.loads((U/'alinhamento_palavras.json').read_text(encoding='utf-8'))
norm=lambda x: re.sub(r'[^\w]','',x.lower())
low=[norm(w['word']) for w in words]
pos=0
def find(phrase):
    global pos
    target=[norm(w) for w in phrase.split()]
    for i in range(pos,len(words)-len(target)+1):
        if low[i:i+len(target)]==target:
            pos=i+1
            return words[i]['start']
    raise ValueError(phrase)
def point(visual,phrase):
    return dict(marco=phrase,visual=visual,audio=find(phrase))
first=[dict(marco='inicio',visual=0,audio=0)]
for visual,phrase in [
    (4.2,'a superfície afunda'),(10.2,'Mas por que'),(11,'Depois que o movimento'),
    (12,'Num corte'),(20.2,'um pequeno elemento'),
    (25.2,'Área da face'),(25.6,'espessura dá'),(26.1,'massa é'),
    (28.1,'A velocidade tangencial'),(29.8,'enquanto a aceleração'),
    (32,'A pressão age'),(37,'Cada força'),(38.4,'a resultante radial'),
    (40,'Para um elemento'),(46.267,'As parcelas'),(48.867,'o sinal negativo'),
    (54,'Essa diferença de pressão'),(55,'Pela segunda lei'),
    (59.2,'Cancelamos área'),(61.733,'O resultado mostra'),
    (63.067,'a pressão cresce para fora'),(69,'Na vertical'),
    (71.4,'enquanto a superior'),(73,'Em equilíbrio'),(75.933,'Por isso, ao subir'),
    (78,'Temos então duas tendências'),(80.5,'Agora vem a ligação'),
    (81,'Toda a superfície'),(87,'Ao avançar para fora'),
    (89.5,'ao subir, tende'),(94,'Na superfície'),
    (101,'Substituindo as duas taxas'),(104,'a densidade se cancela'),
    (106.467,'obtemos a inclinação'),(107,'Ela é proporcional'),(110,'quanto mais longe'),
    (119,'Multiplicando essa inclinação'),(124.533,'A integral soma'),
    (125.433,'Tomamos a altura'),(126,'Integrar a distância'),
    (128.467,'É esse crescimento quadrático'),(131,'Espelhando'),
    (134.333,'A partir da altura central'),
]: first.append(point(visual,phrase))
payoff=find('E ao girar essa seção')
first.append(dict(marco='fim_secao',visual=140,audio=payoff))
second=[dict(marco='paraboloide',visual=149.467,audio=payoff),point(154.067,'Usando o raio'),point(154.867,'encontramos o desnível')]
synthesis=find('A cadeia completa')
second.append(dict(marco='fim_desnivel',visual=157,audio=synthesis))
third=[dict(marco='sintese',visual=140,audio=synthesis)]
for visual,phrase in [(141.533,'a pressão cresce para fora'),(142.533,'a superfície sobe'),(145.333,'a inclinação cresce'),(146.133,'a altura cresce')]: third.append(point(visual,phrase))
closing=find('A forma é consequência')
third.append(dict(marco='fim_sintese',visual=149,audio=closing))
cta=find('Siga o Parallax Lab')
fourth=[dict(marco='frase_final',visual=160.8,audio=closing),dict(marco='retirada_cena',visual=164,audio=max(closing+.6,cta-1.5)),dict(marco='logo_no_cta',visual=165.533,audio=cta),dict(marco='fim_logo',visual=168,audio=170.8)]
segments=[first,second,third,fourth]
for group in segments:
    assert all(a['audio']<b['audio'] and a['visual']<b['visual'] for a,b in zip(group,group[1:])),group
assert all(a[-1]['audio']==b[0]['audio'] for a,b in zip(segments,segments[1:]))
data=dict(segments=segments,anchors=[p for g in segments for p in g],texto='Texto confirmado pelo usuário: 458 palavras',metodo='Finais de frases nas pausas RMS; interpolação silábica interna. Montagem: seção, paraboloide/desnível, síntese, fechamento/marca.')
(U/'sync.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(data,ensure_ascii=False,indent=2))
