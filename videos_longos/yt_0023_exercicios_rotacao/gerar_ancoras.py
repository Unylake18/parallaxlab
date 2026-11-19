"""Extrai, sem reescrever, a narração aprovada do Anexo A. Tempos NOMINAIS, sem voz."""
import json
import re
from pathlib import Path
U = Path(__file__).resolve().parent
texto = (U / 'handoff_v2.md').read_text(encoding='utf-8')
anexo = texto.split('# ANEXO A ·', 1)[1]
(U / 'narracao_sugestao.md').write_text('# ANEXO A ·' + anexo, encoding='utf-8')
anc, ordem, q = {}, [], 0
for cab, fala in re.findall(r'^### ([^\n]+)\n(.*?)(?=^### |^## |\Z)', anexo.split('## Conferência numérica')[0], re.M | re.S):
    aid, tela = cab.split(' · tela:', 1)
    limpa = re.sub(r'\[[^\]]*\]', '', fala).strip()
    palavras = re.findall(r'\w+', limpa.lower())
    dur = round((0.15 + len(palavras) / 2.7 + 0.35) * 15)
    anc[aid] = dict(palavras=len(palavras), ini=q/15, fim=(q+dur)/15, dur=dur/15,
                    nominal=dur/15, fala=' '.join(palavras), original=fala.strip(), tela=tela.strip(),
                    t=[round(.15+k/2.7, 4) for k in range(len(palavras))])
    ordem.append(aid)
    q += dur
(U / 'ancoras.json').write_text(json.dumps(dict(origem='Anexo A v1.1; estimativa 2,7 palavras/s; sem áudio', ordem=ordem, ancoras=anc), ensure_ascii=False, indent=2), encoding='utf-8')
print(f'{len(ordem)} âncoras, {sum(a["palavras"] for a in anc.values())} palavras, {q/900:.2f} min nominais')
