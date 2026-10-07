# vid_0015 — Duas linhas carregadas em movimento

- formato: curto_vertical
- família: EXERCÍCIO RESOLVIDO
- série pública: EXERCÍCIO RESOLVIDO · EP. 06
- fase: preview com voz recebida e legendas coloridas entregue; V4 silencioso preservado
- cena: `cena.py`, classe `LinhasCarga015`
- briefing: recebido do chat de Produção, aprovado; registro de 2026-10-06

## Enunciado e payoff aprovados

Duas linhas infinitas paralelas, com a mesma densidade linear λ, separadas por d,
movem-se no mesmo sentido com velocidade v. Qual v faz a atração magnética e a
repulsão elétrica terem o mesmo módulo?

Gauss fornece E(d) = |λ|/(2πε₀d), portanto F_E/ℓ = λ²/(2πε₀d).
Ampère fornece B(d) = μ₀|I|/(2πd), portanto F_B/ℓ = μ₀I²/(2πd).
A igualdade exige |I|/|λ| = 1/√(μ₀ε₀) = c.
Somente após voltar ao v do enunciado: |I| = |λ|v, então v = c.
Para partículas massivas, v < c; F_B/F_E = v²/c² < 1, com repulsão líquida.

## Progressão aprovada

Duas linhas com λ, d, v → repulsão elétrica → atração magnética → isolar linha 1
→ cilindro gaussiano → campo radial e vetor área → lateral com fluxo; cada tampa
com fluxo zero → E(d) → F_E/ℓ → corte do cilindro → curva amperiana → B azimutal
→ mão direita → ⊗ na linha inferior → Iℓ × B → F_B/ℓ → forças opostas coexistindo
→ igualar módulos → cancelar fatores comuns → pausa em |I|/|λ| = c
→ voltar ao v → |I| = |λ|v → pausa em v = c → explorar F_B/F_E = v²/c²
no modelo ideal → v < c → repulsão líquida.

## Ajustes finais aprovados

- Headline: “duas linhas carregadas”.
- Retorno: “Mas aqui a corrente é produzida justamente pela própria linha de carga em movimento.”
- Variação de v explicitamente como exploração do modelo ideal, sem sugerir
  acelerar elétrons de um fio real a velocidades relativísticas.

## Critérios físicos de QA

- E radial. Nas tampas, E perpendicular a dA; fluxo zero em cada uma.
- Gauss usa superfície; Ampère usa curva e circulação.
- Linha 1 acima, linha 2 abaixo; velocidades e correntes para a direita (+x).
- Abaixo da linha 1, B entra na tela (−z), com marcador separado e guia ao ponto.
- +x̂ × (−ẑ) = +ŷ: força magnética sobre a linha 2 aponta para cima, para a linha 1.
- Campo da linha 1 avaliado na linha 2; nenhuma força por campo próprio.
- F_E e F_B têm sentidos opostos.
- |I|/|λ| = c precede |I| = |λ|v; v = c somente após retorno ao enunciado.
- Modelo ideal identificado durante toda a exploração de v/c.
- Para v < c, seta magnética nunca ultrapassa a elétrica.

## Limites desta rodada

Sem voz, SRT, master, legendado, capa, render final, arquivos globais ou ações Git.
`qa_estados_v4.json` registra os timestamps da implementação atual; V3 preservada.

## Reconstrução visual aprovada — rodada 2

O preview V1 foi prova de conceito tecnicamente funcional, sem aprovação visual.
O handoff de 2026-10-06 pede segunda implementação: linhas horizontais vivas;
branding de `vid_0014/build_stage` (tag branca 20, opacidade 0,65, canto superior
esquerdo, margem 0,4; watermark 1,8, opacidade 0,35, canto superior direito,
margem 0,28); cilindro coaxial em perspectiva; normais e ângulos de 90° em cada
tampa; transição de superfície a curva; curva de Ampère distinta do campo B;
regra da mão direita por corrente e enrolamento; produto vetorial recalculado;
MF-Tools seletivo nos cancelamentos e reorganizações; gráfico y=(v/c)² revelado
progressivamente, sincronizado a F_E, F_B, resultante e posições fantasma de
afastamento qualitativo. Nenhuma integração dinâmica ou massa suposta.

O tracker fica em 0 ≤ v/c ≤ 0,995. O gráfico indica v=c como fronteira; o rótulo
de modelo ideal permanece no bloco. Faixa y < −5,7 reservada para legendas futuras.
O preview, a cena e o QA V1 foram preservados. A reconstrução não reabre a física,
a ordem dos payoffs ou o texto aprovado de retorno ao enunciado.

## Refinamento aprovado — rodada V3

A V2 confirmou a direção visual, sem estar congelada/aprovada para produção final.
O handoff da V3 exige cadeias matemáticas completas, sem encurtamento para manter
a duração anterior. Toda passagem tem um estado público, em região matemática
estável; referências saem após cumprir sua função. Regiões locais: HEADER, TITLE,
PHYSICS, MATH, SECONDARY e SUBTITLE SAFE. Nenhuma alteração ao template.

Texto de tela: Space Grotesk Medium pelo helper oficial. Expressões: MathTex.
Notas em linguagem natural não entram em MathTex; logo permanece asset.

Gauss mostra lei, carga encerrada, fluxo E A_lat, área 2πdℓ, substituição,
cancelamento de ℓ, estado reduzido e E(d). Elétrica mostra q=λℓ, F_E=qE,
substituição de q e E, produto λ²ℓ e força por comprimento.

A passagem para Ampère marca uma seção transversal no cilindro inteiro, atenua
e remove a superfície, preservando o contorno da seção como curva. Não comprime
o cilindro. Ampère mostra B paralelo a dℓ e constante pela simetria, I_enc=I,
retirada de B da integral, comprimento 2πd e isolamento de B(d).

Magnética inclui produto vetorial, orientação +x×(−z)=+y, seno de 90°, módulo,
substituição de B, produto μ₀I²ℓ e força por comprimento. A comparação usa cópias
das duas expressões; o cancelamento é seguido por λ²=μ₀ε₀I², reorganização,
raiz/módulos, definição de c e primeiro payoff.

O retorno marca um ponto fixo e um trecho vΔt que o atravessa. Mostra Δq=λvΔt,
I=Δq/Δt, substituição e cancelamento de Δt, I=λv, módulos, |I|/|λ|=v,
recuperação do primeiro payoff e v=c. A razão é derivada desde a divisão completa
das forças, com cancelamento, quadrado de |I|/|λ| e μ₀ε₀=1/c², antes do gráfico.

Na exploração, a linha 2 atual desloca-se levemente em relação a uma referência
fantasma fixa por 0,45[1−(v/c)²]. O deslocamento é qualitativo; sem dinâmica ou
tempo físico inferidos. O mesmo tracker controla ponto, curva, forças e valores.
A nota sobre elétrons num fio aparece uma vez. Limite: v/c≤0,995.

A conclusão é separada: o gráfico sai, o sistema se centraliza e aparecem v<c,
F_B/F_E=v²/c²<1, F_B<F_E e finalmente REPULSÃO LÍQUIDA. A cena e o QA V2
também foram preservados, juntamente com seu preview e frames.


## Compressão de ritmo aprovada — rodada V4

Partir da V3, mantendo direção visual, física, tipografia e MF-Tools. Alvo
170–175 s; máximo absoluto 180 s. Não remover etapas matemáticas essenciais.

Fundir campo radial/lateral e as duas tampas; encadear as cadeias algébricas
na mesma região matemática com pausas mínimas; manter transição superfície
→ curva com seção preservada; reduzir permanência dos textos auxiliares.

Os dois payoffs recebem pausa real de 1,5–2 s. Gráfico contínuo de v/c=0
para 0,6, depois 0,95 e 0,995; pausa curta em 0,6 e próximo de 1. Mesmo tracker
para curva, ponto, forças, readouts e deslocamento qualitativo simultâneo.

Conclusão separada, aproximadamente 8 s: v<c, razão<1, F_B<F_E e repulsão
líquida. Sem voz, SRT, master, capa, render final, globais ou ações Git.
V3, seus dados técnicos, preview e frames permanecem preservados.

## Ajustes finos e congelamento da V4 — 2026-10-06

Passagens de 39,73 / 124,70 / 127,03 / 134,33 / 143,77 s limpas com fades
locais sequenciais e MF-Tools nos deslocamentos legíveis. Payoff v=c e caixa
ampliados 22,5%, na mesma posição e com pausa de 1,8 s; primeiro payoff preservado.
No gráfico, F_liq>0 substitui o rótulo quando 1−(v/c)²<0,05, sem sobreposição
e sem alterar a seta proporcional, 0,995 / 0,990 ou o marcador aberto em v=c.
Gauss padronizado para Q_env, carga envolvida; derivação preservada.

Validação: py_compile passou; um único render completo 540×960 / 15 fps passou.
Inspecionados os estados alterados e quadros a 25%, 50% e 75% das cinco passagens.
Duração: 173,1 s (MP4: 173,057 s; cena: 173,067 s), 2.596 quadros, sem áudio.
Os 77 timestamps, pausas, blocos e intervalos de animação são iguais aos da V4.
Preview: `media/videos/cena/960p15/vid_0015_preview_v4_silencioso.mp4`.
Frames atualizados: `frames_producao_v4/`, 18 pranchas; pacote
`vid_0015_v4_frames_producao.zip`. Sem pendências concretas nesta rodada.

Comandos executados na raiz do projeto:
```powershell
uv run --no-sync python -m py_compile videos/vid_0015_linhas_carga_movimento/cena.py
uv run --no-sync python -m manim -r 540,960 --fps 15 --media_dir videos/vid_0015_linhas_carga_movimento/media -o vid_0015_preview_v4_silencioso videos/vid_0015_linhas_carga_movimento/cena.py LinhasCarga015
uv run --no-sync python videos/vid_0015_linhas_carga_movimento/inspecionar_preview.py
```

## Narração aprovada para geração de voz — 2026-10-06

Estrutura congelada após as cinco trocas aprovadas: módulos no primeiro payoff,
cancelamento exato no segundo payoff e no veredito, parâmetro do modelo perto
do limite e módulo constante como justificativa para retirar o campo da integral.
Sem outras alterações de roteiro ou preview antes de ouvir o áudio real.

`narracao_sugestao.md` atualizado; `texto_narracao.txt` contém somente a fala,
em 19 parágrafos. Contagem conferida por espaços: 473 palavras; média na janela
de 173,1 s: 2,73 palavras/s, aproximadamente 164 palavras/min. Os trechos mais
densos ficam registrados na tabela; duração de voz ainda não medida.

O usuário fará a geração manual no ElevenLabs, com leitura natural e sem forçar
os timestamps. Áudio pendente; medir e ouvir antes de decidir cortes ou respiros.
Nesta rodada: nenhum áudio gerado, nenhuma sincronização ou alteração de cena.

## Voz recebida e preview legendado — 2026-10-06

WAV recebido do usuário: `ElevenLabs_Untitled_project (6).wav`, 178,64 s.
Cópia idêntica preservada em `audio/narracao_final.wav`. O usuário confirmou
a pergunta “Qual velocidade das cargas igualaria os módulos dessas forças?”
e o restante do texto aprovado. Texto atualizado: 477 palavras, 19 parágrafos.

Preview entregue: `renders/vid_0015_preview_sync_legendado.mp4`, 540×960,
15 fps, 178,667 s, 2.680 quadros, com a voz completa. Também disponível a
versão com voz sem legendas: `renders/vid_0015_preview_sync_master.mp4`.
A sincronização remapeia os quadros da V4 conforme as pausas da voz; preserva
a sequência e os estados visuais. `cena.py` e a V4 silenciosa não foram alterados.

`legenda.srt`: 72 legendas, texto normalizado sem grafia fonética, até duas
linhas. Arial Bold 29, contorno e caixa escura, conforme a referência do vídeo
0014; posicionamento na faixa segura inferior. Cores alinhadas à cena: carga
e força elétrica em ciano, corrente e força magnética em magenta, velocidade
em azul e velocidade da luz em violeta. Cores mantidas entre linhas e legendas.

Verificações: py_compile dos três helpers passou; texto integral do SRT coincide
com as 477 palavras confirmadas; largura máxima 438 px, até 20,98 caracteres/s.
Os dois MP4 foram decodificados integralmente, sem erros. Conferidos Gauss e
tampas, superfície→curva, campo entrando na tela, os dois payoffs, exemplo
0,600/0,360, aproximação 0,995/0,990, marcador aberto e conclusão repulsiva.
As 18 pranchas em `frames_preview_legendado/avaliacao_*.jpg` cobrem as 72 legendas.

Limitação: os tempos das palavras são estimados por pausas do WAV e pesos
silábicos, como no vídeo 0014, sem transcrição automática. A conferência realizada
foi textual, técnica e visual; a revisão auditiva fina permanece pendente.
Nenhum arquivo global, dependência ou ação Git foi alterado/executado.

Arquivos da rodada: `texto_narracao.txt`, `narracao_sugestao.md`, esta ficha,
`gerar_sync.py`, `montar_preview_sync.py`, `legendas_cores.py`, `sync.json`,
`native.json`, `palavras_tempos.json`, `legenda.srt`, áudio recebido/derivado,
renders, frames, logs e `qa_legendado.json`.

Comandos executados na raiz do projeto:
```powershell
uv run --no-sync python videos/vid_0015_linhas_carga_movimento/gerar_sync.py
uv run --no-sync python videos/vid_0015_linhas_carga_movimento/montar_preview_sync.py
uv run --no-sync python -m py_compile videos/vid_0015_linhas_carga_movimento/gerar_sync.py videos/vid_0015_linhas_carga_movimento/montar_preview_sync.py videos/vid_0015_linhas_carga_movimento/legendas_cores.py
```
