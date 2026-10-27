import json,re,sys
A=json.load(open('asr_v3_1/transcricao_asr.json',encoding='utf-8'))
W=[(re.sub(r'[^\wáéíóúâêôãõàçü]','',w['word'].lower()),w['start'],w['end']) for s in A['segmentos'] for w in s['words']]
def q(frase,n=1):
    t=[re.sub(r'[^\wáéíóúâêôãõàçü]','',x.lower()) for x in frase.split()]
    out=[]
    for i in range(len(W)-len(t)+1):
        if [w[0] for w in W[i:i+len(t)]]==t: out.append((round(W[i][1],2),round(W[i+len(t)-1][2],2)))
    return out
for f in sys.argv[1:]: print(f,'->',q(f))
