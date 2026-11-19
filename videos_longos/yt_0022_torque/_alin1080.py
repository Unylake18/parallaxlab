import json, numpy as np
from pathlib import Path
U = Path(__file__).resolve().parent
px = lambda m: np.array([(m[0] + 8) / 16 * 1920, (4.5 - m[1]) / 9 * 1080])
casos = [("PH","regua","hook_regua",["dobradica","cm","dois_tercos","ponta","moeda_meio","moeda_ponta"]),
 ("PT1","porta","t1_porta",["dob_meio","perto","macaneta"]),
 ("PT2","porta","t2_porta",["dob_meio","dob_base","dob_topo","macaneta"]),
 ("PT4","regua","t4_regua",["dobradica","cm","dois_tercos","ponta"]),
 ("PS","regua","s2_regua",["dobradica","cm","dois_tercos","ponta"])]
for l,c,ch,ks in casos:
    f = U/"threejs"/"q3d"/f"{l}_1920x1080"/c/"pontos.json"
    o = U/f"qa_overlay_{l}.json"
    if not f.exists() or not o.exists(): print(l,"sem dados"); continue
    pts = json.loads(f.read_text(encoding="utf-8")); reg = json.loads(o.read_text(encoding="utf-8")).get(ch,{})
    err=[]
    for fr,v in reg.items():
        q = pts.get(fr) or pts.get(str(int(fr)))
        if not q: continue
        for k in ks: err.append(float(np.linalg.norm(px(v[k])-np.array(q[k]))))
    print(l,c,len(err),"pontos; médio %.3f px, máx %.3f px"%(np.mean(err),max(err)) if err else "sem pares")
