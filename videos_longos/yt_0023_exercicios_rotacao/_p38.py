s = open('gates_v4.py', encoding='utf-8').read()
a = s[s.index('            anel = ndi.binary_dilation(reg, iterations=7)'):s.index('out.append(f"CONTRASTE {L}')]
b = '''            for ini, fim_, lista in ((2, 4, ev_c), (3, 7, ev_c_ant)):             # v5: anel colado ao halo (2–4 px depois do agrupamento); a definição antiga (3–7 px) fica só como contagem
                anel = ndi.binary_dilation(reg, iterations=fim_) & ~ndi.binary_dilation(reg, iterations=ini)
                if anel.sum() < 20:
                    continue
                viz = np.median(f[anel], axis=0)
                l1, l2 = float(lum(rgb[None, :])[0]), float(lum(viz[None, :])[0])
                cr = (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)
                if cr < 3.0:
                    lista.append((k / 15, nome, area, round(cr, 2)))
'''
s = s.replace(a, b)
s = s.replace('ev_c = []\n', 'ev_c = []\nev_c_ant = []\n', 1)
s = s.replace('agrupamentos lima/magenta com contraste < 3,0")', 'agrupamentos lima/magenta com contraste < 3,0 (anel colado ao halo; definição antiga 3–7 px: {len(ev_c_ant)})")')
open('gates_v4.py', 'w', encoding='utf-8').write(s)
