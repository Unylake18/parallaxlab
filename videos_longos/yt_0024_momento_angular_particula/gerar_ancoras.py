"""yt_0024: extrai, sem reescrever, a narração v1 (narracao_v1.md = Anexo A do handoff v1) → ancoras.json. Tempos NOMINAIS (2,7 palavras/s), sem voz."""
import json
import re
from pathlib import Path
U = Path(__file__).resolve().parent
anexo = (U / 'narracao_v1.md').read_text(encoding='utf-8')
anc, ordem, q = {}, [], 0
for cab, fala in re.findall(r'^### ([^\n]+)\n(.*?)(?=^### |^## |\Z)', anexo, re.M | re.S):
    aid, tela = cab.split(' · tela:', 1)
    aid = aid.strip()
    limpa = re.sub(r'\[[^\]]*\]', '', fala).strip()
    palavras = re.findall(r'\w+', limpa.lower())
    dur = round((0.15 + len(palavras) / 2.7 + 0.35) * 15)
    anc[aid] = dict(palavras=len(palavras), ini=q / 15, fim=(q + dur) / 15, dur=dur / 15, nominal=dur / 15, fala=' '.join(palavras),
                    original=fala.strip(), tela=tela.strip(), t=[round(.15 + k / 2.7, 4) for k in range(len(palavras))])
    ordem.append(aid)
    q += dur
(U / 'ancoras.json').write_text(json.dumps(dict(origem='narração v1 (handoff v1, 2026-11-07); estimativa 2,7 palavras/s; sem áudio', ordem=ordem, ancoras=anc),
                                       ensure_ascii=False, indent=1), encoding='utf-8')
print(f'{len(ordem)} âncoras, {sum(a["palavras"] for a in anc.values())} palavras, {q / 900:.2f} min nominais')
for a in ordem:
    print(a, anc[a]['palavras'], round(anc[a]['dur'], 1))
