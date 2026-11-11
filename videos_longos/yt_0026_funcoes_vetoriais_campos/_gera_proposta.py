import json, re, glob
U='.'
anc=json.load(open('ancoras.json',encoding='utf-8')); q=json.load(open('renders/quadros_v8_com_b7.json'))
txt=open('narracao.md',encoding='utf-8').read()
cur={}
for m in re.finditer(r"### (\S+) · tela: ([^\n]*)\n\[([^\]]*)\] ([^\n]+)", txt):
    cur[m.group(1)]=(m.group(2).strip(), m.group(3), m.group(4).strip())
gates={}
for lg in glob.glob('log_P*.txt'):
    for l in open(lg,encoding='utf-8',errors='replace'):
        m=re.match(r"\[gatilho\] (\S+)\s+([0-9.]+)s \(alvo\s+([0-9.]+)s.*?\) (.*)$", l.strip())
        if m: gates.setdefault(m.group(1),[]).append((float(m.group(3)), m.group(4)))
TELA={
 'T0':'uma seta no centro do palco; em "junta infinitas delas" nascem as outras até formar o redemoinho (−y, x); fórmula e "CAMPO VETORIAL"',
 'T1':'colunas finas debaixo de uma superfície (3D); fórmula do volume; "SOMA DE COLUNAS FININHAS"',
 'T2':'campo e curva laranja; setas brancas tangentes em 5 paradas; fórmula do trabalho',
 'T3':'tigela em retalhos com setas atravessando (3D); fórmula do fluxo',
 'T4':'Green: 3×3 células, o par de setas que se cancela, sobra a borda; depois a tabela Green · Stokes · Gauss e "O LOCAL E O GLOBAL ESTÃO CONECTADOS."',
 'T5':'cartão CÁLCULO III com a seta de acento e "DO INFINITAMENTE PEQUENO AO ESPAÇO INTEIRO."',
 'A1':'logo, "BEM-VINDOS AO PARALLAX LAB", título do vídeo e "NESTE VÍDEO: TRANSFORMAÇÃO · IMAGEM · CAMPO VETORIAL"',
 'H1':'malha com a bandeira girando +90°','H2':'a malha volta e o redemoinho cresce em onda (sem pontinhos)','H3':'dois painéis: bandeira girada × redemoinho; "QUAL É O DESENHO CERTO?"',
 'B6-6':'círculos r = 1, 2, 3 acendem, a origem pisca, o disco rígido com um raio girando','B7-2':'domínio A = ℝ³ − {0} (o anel vazado na origem)',
 'S1':'três cartões: TRANSFORMAÇÃO · SUPERFÍCIE · CAMPO, com f : A ⊂ ℝⁿ → ℝᵐ embaixo','S2':'disco das polares e redemoinho lado a lado','CTA':'barquinho no redemoinho e a pergunta; logo, anéis e INSCREVA-SE (hold de ~3 s no fim)'}
def nwords(s): return len(re.findall(r"\w+", re.sub(r"\[[^\]]*\]","",s)))
P={}
P['A1']=("happy","Fala, pessoal! Bem-vindos ao Parallax Lab. Este é o nosso primeiro vídeo, e a gente começa o Cálculo três, a matéria que leva tudo o que você já sabe para o espaço inteiro. O assunto de hoje é essa seta em cada ponto, e as funções de onde ela vem: funções que recebem um ponto e devolvem um vetor. A gente vai ver o que elas são, por que não dá para desenhar o gráfico delas, e as duas maneiras de enxergar uma: como transformação e como campo vetorial. Para começar, olha só uma coisa curiosa.")
P['S2']=("thoughtful","Essas duas leituras não saem mais de cena. As transformações voltam quando a gente trocar de coordenadas dentro de uma integral; os campos voltam nas integrais de linha, no fluxo e nos grandes teoremas. E o caminho inteiro está desenhado no Atlas Parallax Lab, o nosso mapa: o que vem antes, o que vem depois.")
P['CTA']=("curious","Fica uma pergunta: se você pusesse um barquinho de papel nesse redemoinho, ele só daria voltas em torno do centro… ou também giraria em torno de si mesmo? Deixa a sua resposta nos comentários. No próximo vídeo, a gente aprende a chegar perto de um ponto quando existem infinitos caminhos até ele: limite e continuidade. O Atlas Parallax Lab, com o mapa de tudo isso, está no link da descrição. Se inscreve, e até lá!")
out=[]
out.append("""# yt_0026 · CÁLCULO III · EP. 01 — proposta de narração v1 (foco em tempo)

Proposta para refinar com Projeto, Produção e GPT. **Não é a fala final**: serve para fechar *quanto tempo cada trecho do vídeo tem* e *o que entra em cada um*; o linguajar fica para o refino.

## Como ler
- **Início** = onde a âncora começa no preview v8 (17:23 no total). **Dur.** = tempo da âncora; **Orç.** = palavras que cabem a 2,7 palavras/s (a voz real fica entre 2,5 e 2,8).
- **Gatilhos** = frases em que a animação "acende". Se o refino trocar essas palavras, avisem: o gatilho precisa ser atualizado no código, senão a imagem sai do tempo.
- **Status**: `mantida` (texto atual do `narracao.md`), `NOVA` (proposta aqui), com as palavras e a diferença contra o orçamento.

## O arco (o que a pessoa vai sentir)
1. **0:00–0:59 · gancho.** Uma seta, depois uma em cada ponto: o campo aparece antes de qualquer definição. Três imagens rápidas (volume, trabalho, fluxo) criam a curiosidade e o "o local e o global estão conectados" dá o tema da disciplina.
2. **0:59–1:30 · boas-vindas e promessa (A1, NOVA).** Primeiro vídeo do canal, o que é o Cálculo III, o assunto de hoje, o Atlas Parallax Lab como mapa.
3. **1:30–2:31 · a pergunta aberta (H1–H3).** A mesma fórmula gira o plano *e* desenha um redemoinho. "Qual é o desenho certo?" fica sem resposta de propósito: é o laço que o vídeo só fecha em 16:08.
4. **2:31–16:08 · o caminho didático.** B1 (que função é essa) → B2 (transformação: polares) → B3 (a dobra) → B4 (para o espaço) → B5 (campo) → B6 (o redemoinho, com três perguntas) → B7 (no espaço).
5. **16:08–17:23 · fechamento.** S1 responde a pergunta aberta; S2 liga ao resto da disciplina e ao Atlas; CTA deixa uma pergunta para os comentários e o **gancho do EP. 02** (limite e continuidade; confirmar a ordem no Atlas).

## Impacto no tempo das três âncoras NOVAS
| Âncora | Hoje | Proposta | Diferença | O que fazer com a imagem |
|---|---|---|---|---|
| A1 (boas-vindas) | 31,2 s | ≈ 36 s (97 palavras) | **+4,8 s** | segurar o título e o "NESTE VÍDEO" um pouco mais |
| S2 (liga ao resto e ao Atlas) | 18,3 s | ≈ 20,4 s (55 palavras) | **+2,2 s** | segurar o par disco × redemoinho |
| CTA (pergunta, gancho, Atlas) | 21,2 s + 3 s de hold | ≈ 27,8 s (75 palavras) | **+3,6 s** (já usando o hold) | alongar o logo e o INSCREVA-SE |
Soma: **≈ +10,6 s** (17:23 → ≈ 17:34). Se preferirem não alongar nada, o corte natural é tirar a frase do Atlas do A1 (já está no S2 e no CTA) e a do "link na descrição".

## Linha do tempo
""")
out.append("| Início | Âncora | Dur. | Orç. | Palavras | Status |\n|---|---|---|---|---|---|")
for k in anc['ordem']:
    v=anc['ancoras'][k]; f=q[k]/15
    tag,fala = P[k] if k in P else (cur[k][1],cur[k][2])
    n=nwords(fala); orc=round(v['dur']*2.7)
    out.append(f"| {int(f//60)}:{int(f%60):02d} | {k} | {v['dur']:.1f} s | {orc} | {n} ({n-orc:+d}) | {'**NOVA**' if k in P else 'mantida'} |")
out.append("\n## Fala por âncora\n")
for k in anc['ordem']:
    v=anc['ancoras'][k]; f=q[k]/15
    tag,fala = P[k] if k in P else (cur[k][1],cur[k][2])
    n=nwords(fala); orc=round(v['dur']*2.7)
    out.append(f"### {k} · {int(f//60)}:{int(f%60):02d} · {v['dur']:.1f} s · {n} palavras (orçamento {orc})  {'· **NOVA**' if k in P else ''}")
    out.append(f"**Tela:** {TELA.get(k, cur[k][0] if k in cur else '')}")
    g=sorted(set(x for _,x in gates.get(k,[])))
    if g: out.append("**Gatilhos:** " + " · ".join(f"“{x}”" for x in g))
    out.append(f"\n[{tag}] {fala}\n")
open('narracao_proposta_v1.md','w',encoding='utf-8').write("\n".join(out))
for k in P:
    v=anc['ancoras'][k]; print(k, nwords(P[k][1]), round(v['dur']*2.7))
