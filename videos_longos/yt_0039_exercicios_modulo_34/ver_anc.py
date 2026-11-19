import re,sys,json
a=sys.argv[1]
t=open('narracao.md',encoding='utf-8').read()
for b in re.split(r'^### ',t,flags=re.M)[1:]:
    if b.startswith(a+' '):
        L=b.split('\n'); print([l for l in L if l.startswith('>')][0])
sec=sys.argv[2]
A=json.load(open('ancoras.json',encoding='utf-8'))['ancoras']
cur=None
src=open(sec,encoding='utf-8').read().split('\n')
for i,l in enumerate(src,1):
    m=re.search(r'\.an\("([^"]+)"',l)
    if m: cur=m.group(1)
    m=re.search(r'\.gat\(\s*"([^"]*)"',l)
    if m and cur==a:
        al=re.findall(r'\w+',m.group(1).lower());f=A[cur]['fala'].split()
        ok=any(f[k:k+len(al)]==al for k in range(len(f)))
        ok or print('BAD ',i,m.group(1),'|',src[i][:100].strip() if i<len(src) else '')
