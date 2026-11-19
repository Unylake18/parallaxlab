import re,json,glob,sys
A=json.load(open('ancoras.json',encoding='utf-8'))['ancoras']
M={'xis':'x','ípsilon':'y','erre':'r','bê':'b','cá':'k','dáblio':'w','vê':'v','á':'a'}
conv=lambda s:' '.join(M.get(w,w) for w in s.split())
apply='--apply' in sys.argv
bad=tot=ok2=0
for f in sorted(glob.glob('sec_*.py')):
    cur=None;src=open(f,encoding='utf-8').read().split('\n');ch=False
    for i,l in enumerate(src):
        m=re.search(r'\.an\("([^"]+)"',l)
        if m: cur=m.group(1)
        m=re.search(r'(\.gat\(\s*)"([^"]*)"',l)
        if not m or cur not in A: continue
        tot+=1
        f_=A[cur]['fala'].split()
        def has(s):
            al=re.findall(r'\w+',s.lower());return any(f_[k:k+len(al)]==al for k in range(len(f_)))
        s=m.group(2)
        if has(s): continue
        c=conv(s)
        if has(c):
            ok2+=1
            if apply: src[i]=l.replace('"'+s+'"','"'+c+'"',1);ch=True
        else:
            bad+=1
    if apply and ch: open(f,'w',encoding='utf-8').write('\n'.join(src))
print('total',tot,'convertidos',ok2,'ainda sem frase',bad)
