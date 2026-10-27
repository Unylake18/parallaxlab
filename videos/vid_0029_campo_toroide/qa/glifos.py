"""QA de desenvolvimento: índices de glifo das fórmulas do vid_0029 (para os mapas explícitos do TransformByGlyphMap)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3])); sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from kit import E
T = [r'\oint\mathbf B\cdot d\boldsymbol\ell=\mu_0\,I_{\rm enc}', r'\oint B\,d\ell=\mu_0\,I_{\rm enc}', r'B\oint d\ell=\mu_0\,I_{\rm enc}',
     r'B\,(2\pi r)=\mu_0\,I_{\rm enc}', r'B\,(2\pi r)=\mu_0\,N\,I', r'B=\frac{\mu_0\,N\,I}{2\pi r}', r'I_{\rm enc}=24\,I', r'I_{\rm enc}=N\,I',
     r'I_{\rm enc}=N\,I-N\,I', r'I_{\rm enc}=0', r'B\approx\frac{\mu_0\,N\,I}{2\pi R}', r'B\approx\mu_0\left(\frac{N}{2\pi R}\right)I',
     r'B\approx\mu_0\,n\,I', r'\mathbf B\parallel d\boldsymbol\ell']
for t in T:
    m = E(t)
    print(len(m[0]), t, ' '.join(f'{i}:{g.get_center()[0]:+.2f}/{g.get_center()[1]:+.2f}' for i, g in enumerate(m[0])))
