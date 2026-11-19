import re,json,sys,glob
A=json.load(open('ancoras.json',encoding='utf-8'))['ancoras']
bad=0;tot=0
for f in sorted(glob.glob('sec_*.py')):
    cur=None
    for i,l in enumerate(open(f,encoding='utf-8'),1):
        for m in re.finditer(r'(?:\.an\(|self\.gat\(|\.gat\()\s*(?:"([^"]*)"|\'([^\']*)\')',l):
            s=m.group(1) or m.group(2)
            if m.group(0).startswith('.an('):
                cur=s;continue
            tot+=1
            fala=A[cur]['fala'].split() if cur in A else []
            al=re.findall(r'\w+',s.lower())
            if not any(fala[k:k+len(al)]==al for k in range(len(fala))):
                bad+=1;print(f,i,cur,repr(s))
print('gat',tot,'sem frase',bad)
