import json,sys
A=json.load(open('ancoras.json',encoding='utf-8'))['ancoras']
for a in sys.argv[1:]:
    w=A[a]['fala'].split();t=A[a]['t'];print(a, A[a]['dur']);print(' '.join(f'{x}@{y:.1f}' for x,y in zip(w,t)))
