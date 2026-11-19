s = open('flash23.py', encoding='utf-8').read()
a = s[s.index('    for j in range(max(0, k - 24), k - 3):'):s.index('out = [f"FLASH POR QUADRO')]
b = '''    estrito = False
    for j in range(max(0, k - 24), k - 3):
        m = fr[j][y0:y1, x0:x1] > 150
        iou = float((m & fim).sum()) / max(1.0, float((m | fim).sum()))
        if iou > 0.5:
            estrito = True                                    # definição anterior (folga de 3 quadros)
            if j >= k - 6:
                continue                                      # v5: a caneta escreve glifo a glifo; até 0,4 s de adiantamento do glifo vizinho no mesmo aglomerado é a própria escrita
            antes = fr[max(0, j - 8)][y0:y1, x0:x1] > 150
            if float((antes & fim).sum()) / max(1.0, float(fim.sum())) >= 0.3:
                continue                                      # glifo estável: já estava ali (mapeado/igual na linha anterior), não apareceu antes da vez
            ruins.append((t0, (x0, y0, x1, y1), iou))
            break
    if estrito:
        n_estrito += 1
'''
s = s.replace(a, b)
s = s.replace('ruins = []\n', 'ruins = []\nn_estrito = 0\n', 1)
s = s.replace('{len(ruins)} com tinta antes da vez"]', '{len(ruins)} com tinta antes da vez (definição estrita antiga, folga de 3 quadros: {n_estrito})"]')
open('flash23.py', 'w', encoding='utf-8').write(s)
