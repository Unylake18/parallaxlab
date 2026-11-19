"""Preparação local, sem rede e sem tocar outras unidades."""
import json
import re
from pathlib import Path

U = Path(__file__).resolve().parent
texto = (U / 'handoff_v1.md').read_text(encoding='utf-8')
anexo = texto.split('# ANEXO A ·', 1)[1].split('# ANEXO B ·', 1)[0]
(U / 'narracao_v1.md').write_text('# ANEXO A ·' + anexo, encoding='utf-8')
anc, ordem, q = {}, [], 0
for cab, fala in re.findall(r'^### ([^\n]+)\n(.*?)(?=^### |^## |\Z)', anexo, re.M | re.S):
    aid, tela = cab.split(' · tela:', 1)
    aid = aid.split(' ·')[0].strip()
    limpa = re.sub(r'\[[^\]]*\]', '', fala).strip()
    palavras = re.findall(r'\w+', limpa.lower())
    hold = 2 if aid in ('H3', 'B1-6', 'B3-4', 'B5-4') else 0
    n = round((.5 + len(palavras) / 2.7 + hold) * 15)
    anc[aid] = dict(palavras=len(palavras), ini=q/15, fim=(q+n)/15, dur=n/15,
                    nominal=n/15, fala=' '.join(palavras), original=fala.strip(), tela=tela.strip(),
                    hold=hold, t=[round(.15 + k/2.7, 4) for k in range(len(palavras))])
    ordem.append(aid)
    q += n
(U / 'ancoras.json').write_text(json.dumps(dict(origem='Handoff v1; 2,7 palavras/s; tempos estimados, sem voz', ordem=ordem, ancoras=anc), ensure_ascii=False, indent=1), encoding='utf-8')
print(f'{len(ordem)} âncoras; {sum(a["palavras"] for a in anc.values())} palavras; {q/15:.2f} s ({q/900:.2f} min)')
