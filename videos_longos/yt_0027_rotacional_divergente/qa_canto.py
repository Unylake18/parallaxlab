"""[canto] gap entre a caixa da linha 1 e a da linha 2 (>= 10 px) e as duas dentro da placa do canto (y 22–124 px), para todas as seções com canto (1080p; 1 u = 120 px)."""
import re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from kit import *  # noqa
h1 = Base._canto(txt(TITULO, 13.2, color="#C8D6F0", op=0.6), CANTO_Y1)
b1 = (4.5 - h1.get_bottom()[1]) * 120; t1 = (4.5 - h1.get_top()[1]) * 120
tit = set()
for f in Path(__file__).parent.glob("sec_*.py"):
    tit |= set(re.findall(r'secao\("([^"]+)"\)', f.read_text(encoding="utf-8")))
pior = 1e9
for s in sorted(tit):
    h2 = Base._canto(txt(s, 21.6, color="#F5F7FF", bold=True), CANTO_Y2, topo_min=b1 + 10)
    t2, b2 = (4.5 - h2.get_top()[1]) * 120, (4.5 - h2.get_bottom()[1]) * 120
    gap = t2 - b1; pior = min(pior, gap)
    ok = gap >= 10 and t1 >= 22 and b2 <= 124
    print(f"[canto] {s}: linha1 {t1:.0f}–{b1:.0f} px, linha2 {t2:.0f}–{b2:.0f} px, gap {gap:.1f} px {'OK' if ok else 'FALHA'}")
print(f"[canto] pior gap {pior:.1f} px em {len(tit)} títulos")
