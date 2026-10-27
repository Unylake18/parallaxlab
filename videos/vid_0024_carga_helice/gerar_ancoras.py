"""Âncoras: nome -> instante real (s) da voz (alinhamento_palavras.json). Saída: ancoras.json. Âncoras precisam estar em ordem crescente."""
import json, wave
from ancoras_lib import PASTA, PAL, acha

# nome: (frase falada, borda i|f, deslocamento s)
F = [
 ('entra', 'entra num', 'i', 0), ('reta', 'segue reta', 'i', 0), ('circ', 'faz um círculo', 'i', 0), ('hel', 'desenha uma hélice', 'i', 0),
 ('unif', 'num campo uniforme', 'i', 0), ('cons', 'vamos considerar', 'i', 0),
 ('feq', 'essa força é a carga', 'i', 0), ('qpos', 'neste exemplo', 'i', 0), ('perp', 'pela regra do', 'i', 0),
 ('nowork', 'por isso ela não', 'i', 0), ('graf', 'nos gráficos', 'i', 0), ('grafvar', 'as componentes variam', 'i', 0),
 ('grafout', 'não significa', 'i', 0),
 ('dec_head', 'agora separamos', 'i', 0), ('dec_par', 'uma paralela', 'i', 0), ('dec_perp', 'e outra perpendicular', 'i', 0),
 ('dec_sum', 'colocando uma', 'i', 0), ('dec_eq', 'a soma recupera', 'i', 0), ('par_const', 'a paralela permanece', 'i', 0),
 ('perp_gira', 'já a perpendicular', 'i', 0),
 ('front', 'olhando no plano', 'i', 0), ('field', 'e o campo sai', 'i', 0), ('tang', 'a velocidade é tangente', 'i', 0),
 ('centr', 'a força magnética é a própria', 'i', 0), ('igual', 'igualamos os módulos', 'i', 0), ('mult', 'multiplicamos pelo raio', 'i', 0),
 ('canc', 'depois cancelamos', 'i', 0), ('isol', 'e isolamos o raio', 'i', 0), ('rres', 'o raio é massa', 'i', 0),
 ('wi', 'agora a frequência angular', 'i', 0), ('wdiv', 'componente perpendicular dividida', 'i', 0),
 ('wsub', 'substituindo o raio', 'i', 0), ('winv', 'multiplicamos pelo inverso', 'i', 0),
 ('wcanc', 'e a componente perpendicular cancela', 'i', 0), ('tvolta', 'uma volta tem', 'i', 0),
 ('tdiv', 'então dividindo', 'i', 0), ('tsub', 'achamos o período', 'i', 0), ('tres', 'dois pi vezes a massa', 'i', 0),
 ('trep', 'repara que a velocidade', 'i', 0),
 ('jun', 'agora juntamos', 'i', 0), ('vol', 'durante uma volta', 'i', 0), ('avp', 'avança o passo', 'i', 0), ('modp', 'o módulo da componente', 'i', 0),
 ('fix', 'pra fixar', 'i', 0), ('cB', 'com campo magnético mais intenso', 'i', 0), ('cBm', 'raio período e passo', 'i', 0),
 ('cBt', 'e a partícula dá', 'i', 0), ('cvp', 'com mais componente perpendicular', 'i', 0), ('cvpm', 'só o raio aumenta', 'i', 0),
 ('cvz', 'com mais componente paralela', 'i', 0), ('cvzm', 'só o passo aumenta', 'i', 0),
 ('sg', 'e se invertermos', 'i', 0), ('sgf', 'a força inverte', 'i', 0), ('sge', 'mas raio', 'i', 0),
 ('g_head', 'resumindo', 'i', 0), ('g_perp', 'a componente perpendicular gira', 'i', 0), ('g_par', 'a paralela produz', 'i', 0),
 ('g_all', 'e juntas elas formam', 'i', 0), ('g_end', 'sem alterar', 'i', 0),
]
out, pos = [], 0
for nome, frase, borda, off in F:
    k, t = acha(frase, max(0, pos - 2), borda)
    out.append((nome, round(t + off, 3))); pos = k + 1
assert all(b[1] > a[1] for a, b in zip(out, out[1:])), [(a, b) for a, b in zip(out, out[1:]) if b[1] <= a[1]]
with wave.open(str(PASTA / 'audio' / 'narracao_v4b.wav')) as w:
    dur = w.getnframes() / w.getframerate()
fim_fala = PAL[-1]['end']
(PASTA / 'ancoras.json').write_text(json.dumps(dict(A=dict(out), audio_end=round(dur, 3), fim_fala=fim_fala), indent=1), encoding='utf-8')
print(len(out), 'âncoras; fala termina', fim_fala, 'áudio', round(dur, 3))
