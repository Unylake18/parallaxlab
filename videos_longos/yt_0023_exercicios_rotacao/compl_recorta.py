"""Regra do handoff: complemento que leva a fala a >110% da janela perde as últimas frases (nunca a primeira)."""
import json, re
jan = json.load(open('ancoras_v1_nominal.json', encoding='utf-8'))['ancoras']
comp = json.load(open('complemento_v3.json', encoding='utf-8'))
res = json.load(open('audio/compl_resultado.json'))
plano = json.load(open('audio/compl_plano.json'))
fonte = open('narracao_final_fonte_sem_compl.md', encoding='utf-8').read()
paras = {m.group(1): m.group(2) for m in re.finditer(r'^\{([^}]+)\} (.+)$', fonte, flags=re.M)}
W = lambda s: len(re.findall(r'\w+', re.sub(r'\[[^\]]*\]', '', s)))
novo, mudou = [], []
for a, txt in comp:
    if a not in res:
        novo.append([a, txt]); continue
    dur_new = res[a][1] - 0.6
    w_old, w_c = W(paras[a]), W(txt)
    rate = dur_new / (w_old + w_c)
    sents = re.split(r'(?<=[.?!])\s+', txt)
    keep = list(sents)
    while len(keep) > 1 and (w_old + W(' '.join(keep))) * rate > 1.10 * jan[a]['dur']:
        keep.pop()
    t = ' '.join(keep)
    print(f"{a}: {dur_new / jan[a]['dur'] * 100:.0f}% -> {(w_old + W(t)) * rate / jan[a]['dur'] * 100:.0f}% ({len(sents)}->{len(keep)} frases)")
    if t != txt: mudou.append(a)
    novo.append([a, t])
json.dump(novo, open('complemento_v3.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
json.dump(mudou, open('audio/compl_mudou.json', 'w'))
print('mudaram:', mudou)
