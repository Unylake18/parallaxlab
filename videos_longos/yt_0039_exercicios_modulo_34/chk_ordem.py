import re,json,glob
A=json.load(open('ancoras.json',encoding='utf-8'))['ancoras']
for f in sorted(glob.glob('sec_*.py')):
    cur=None;pos=-1;prev=''
    for i,l in enumerate(open(f,encoding='utf-8'),1):
        m=re.search(r'\.an\("([^"]+)"',l)
        if m: cur=m.group(1);pos=-1;continue
        m=re.search(r'\.gat\(\s*"([^"]*)"',l)
        if m and cur in A:
            f_=A[cur]['fala'].split();al=re.findall(r'\w+',m.group(1).lower())
            k=next((k for k in range(len(f_)) if f_[k:k+len(al)]==al),None)
            if k is not None:
                if k<pos: print('VOLTA',f,i,cur,repr(m.group(1)),'antes de',repr(prev),k,pos)
                pos=max(pos,k);prev=m.group(1)
