# yt_0016 — avaliação do preview v2 e HANDOFF v3 (preview silencioso v3)

Data: 2026-10-28. Base: `preview_yt0016_v2_960x540.mp4` (20:09), 6.047 quadros a 5 fps, 8 stills, código das seções e o relatório do Claude Code.
Documento autocontido para o Claude Code. **A narração não muda** (a v2 da unidade continua valendo, assim como a física do `handoff_v1.md` §3 e as regras de tela
do `handoff_v2.md` §2). Esta rodada é só de **acabamento visual e correções**. Se achar inconsistência objetiva, reporte antes de ampliar o escopo.

(Cópia salva na unidade pelo Claude Code em 2026-10-29, a pedido do `handoff_v4.md` §0.)

---

## Parte 1 — Avaliação do v2

**Salto grande em relação ao v1.** Tempo morto zerado (medição nossa: nenhum trecho ≥ 6 s; 7 entre 4 e 6 s: 12:37, 12:43, 15:04, 15:08, 16:02, 16:19, 20:04); o cavalo 3D,
as esferas com molas, o disco, o manequim e a vela solar funcionam; a abertura nova conta a diferença entre os vídeos; T7 com mola e matriz sincronizada (2:44–4:32)
ficou muito bom; T8 com as contas descendo ao lado do cavalo (6:12–7:00) e T9 com P(t) e P_Terra(t) (10:20–11:08) estão no padrão que o Kaio pediu; nenhuma referência
de livro; números conferem.

**Problemas encontrados quadro a quadro (tempos do v2):**

| # | Tempo | Problema | Gravidade |
|---|---|---|---|
| 1 | 0:05–0:24, 1:44, 5:28–7:24, 19:24 | **Seta −F⃗/−T⃗ no cavalo solta no ar, à frente da cabeça**, longe da corda e (no T8) fora da fronteira do sistema. A força da corda age no arreio (barra branca no peito) e aponta para trás, **ao longo da corda**. | alta (física visual) |
| 2 | 7:08–7:16 | "2.608 N" sobre a cabeça do cavalo e cortado pelo texto da CONTA; "2.800 N" encavalado nos cascos (pendência T8-5 confirmada). | alta |
| 3 | 19:44–19:50 | **Resumo: a terceira ideia ("NÃO CONSERVA? AUMENTE O SISTEMA") nunca aparece**; só o ícone do cavalo, minúsculo, sobre uma faixa de chão que atravessa a tela. | alta |
| 4 | 12:04–12:12 | Texto do T10 diferente do aprovado: "MAIS ENERGIA FICA COM O MAIS LEVE". O aprovado é `QUANTO MAIOR A DIFERENÇA DE MASSAS, MAIOR A FRAÇÃO DA ENERGIA CINÉTICA QUE FICA COM O MAIS LEVE`. | alta (física) |
| 5 | 14:10–14:21 | E7: a **normal do gelo** só pisca ~0,2 s nos pés (14:19); não dá para ver. E o momento da bala a 56° não é decomposto (p_x, p_y), que é o centro do exercício. | alta |
| 6 | 0:58–1:12 | A3: o loop **pisca**: a curva da força e a área somem (1:02, 1:10) e o disco escurece a cada ciclo. | média |
| 7 | 1:20–1:28; 11:32–12:12 | Objetos **saindo do quadro** no loop: disco 2 do A4; blocos do T10 (1 kg cortado na borda esquerda em 11:40 e 12:12; 11:32 os dois somem). | média |
| 8 | 1:28 | Transição A4 → A5: "Δp⃗₁ = −Δp⃗₂ → P⃗ = CONSTANTE" desenhado **por cima do cavalo** que está entrando. | média |
| 9 | 2:44–3:16 | T7 (duas esferas): rótulos F⃗₁₍₂₎, F⃗₁^ext etc. pequenos (~14 px em 960p) e encostados nas setas; em 3:08 a soma `d(p⃗₁+p⃗₂)/dt = …` **passa da borda direita**; em 3:16 "TERCEIRA LEI: IGUAIS E OPOSTAS" encosta no quadro de dP⃗/dt. | média |
| 10 | 7:24–7:56 | Gelo do T8-6: faixa **branca chapada** que atravessa a tela inteira, por baixo da CONTA; "O QUE MUDOU FOI A FORÇA EXTERNA" escrito por cima do gelo, sem contraste. | média |
| 11 | 10:52–11:08 | T9: o eixo de P_Terra(t) sobe para dentro do gráfico de P(t): os rótulos "−1,0" e "+1,0" e "P_Terra" se sobrepõem. | média |
| 12 | 12:20 (e as outras viradas de capítulo) | Dissolve dos **headers**: "COMO A ENERGIA SE DIVIDE" e "EXERCÍCIO 6 · AGARRAR OU REBATER" visíveis ao mesmo tempo, um sobre o outro. | média |
| 13 | 14:36–14:52 | E7: barras de momento e energia desenhadas **sobre o gelo azul** (pouco contraste) e pequenas. | média |
| 14 | 17:52 | E9: traço solto embaixo de "IMPULSO CERTO" (sobra do risco do "v₂ > v₁"). | baixa |
| 15 | 19:08 | Coda: a vela solar entra na zona da CONTA e passa por cima de "O MODELO DO NEWTON CAIU / A CONSERVAÇÃO DO MOMENTO FICOU". | média |
| 16 | 13:12 | E6: coluna da CONTA vazia com texto fantasma por ~3 s entre "rebate" e o balanço de energia. | baixa |

**As pendências do relatório, uma a uma:**
- *Fontes v1 perdidas* (`sec_abertura`/`sec_cavalo`): sem impacto, a v1 está superada. Daqui em diante, **antes de editar, copie a unidade inteira para `_v2/`** (sem `renders/` nem mídia).
- *T8-5, "2.608 N" na cabeça*: confirmado; corrigir junto com o item 1 (§2.1).
- *E7, recuo exagerado 1,5× com aviso na tela*: **tirar o exagero e o aviso.** A 0,0559 m/s, o caçador anda ~0,5 m em 10 s, o que já se vê com a câmera parada. Velocidade real.
- *Câmera lenta em E6, E7 e T9*: correto manter (os eventos duram frações de segundo), mas **avisar**: chip pequeno `CÂMERA LENTA` (DIM, opacidade 0,85, canto inferior esquerdo do PALCO)
  enquanto estiver lento. Os relógios na tela (t = 0,51 s etc.) continuam em tempo real da física.
- *T8, aceleração em tomadas de 10 s que se repetem*: a 0,32 m/s² por 3 minutos o cavalo chegaria a ~60 m/s, então repetir o trecho é necessário, mas **o salto de 3,5 m/s de volta a
  0,3 m/s na emenda engana**. Solução na §2.4.
- *Disco do A4 saindo do quadro*: corrigir (§2.5), e o mesmo vale para os blocos do T10.
- *Logs e mídia de teste na unidade*: apagar **só** os que você mesmo criou dentro de `videos_longos/yt_0016_sistemas_momento/` (logs, `media/` de teste), listando no relatório. Nada fora da unidade.
- *QA do manequim só no quadril*: estender (§4).

---

## Parte 2 — HANDOFF v3

### 0. Rodada
- Unidade `videos_longos/yt_0016_sistemas_momento/` (preview v2). `git status --short`; copie a unidade para `_v2/` (código, ficha, âncoras; sem renders) antes de editar.
- **Objetivo:** preview silencioso **v3** 960×540 / 15 fps, completo, mais os stills da §5. Re-renderize **só os lotes afetados** (provavelmente: hook/abertura, T7, T8, T9, T10, E6, E7, E9, coda, fim).
- Sem voz, SRT, master, entrega, commit ou push. Não alterar `template/`, `docs/`, `assets/`, `experimentos/threejs/` nem o yt_0015.

### 1. Regra geral nova (vale para o vídeo todo)
- **Nenhum objeto sai do PALCO.** Loops ficam dentro da zona (rebatem, invertem ou recomeçam fora de cena com fade de ≥ 0,5 s **do objeto inteiro**, nunca corte seco nem "piscar").
- **Loops não piscam:** a figura de fundo nunca desaparece por inteiro dentro de um loop; o reinício é um crossfade de ~0,6 s entre o fim e o começo.
- **Headers trocam em sequência** (sai o antigo em 0,25 s, entra o novo em 0,25 s), nunca sobrepostos, inclusive com o dissolve das cenas.
- **Rótulos de vetor e de força:** MathTex no corpo Math S (30–32 em 960p, escala junto em 1080p); `next_to` pelo lado livre com `buff ≥ 0,15`; nunca sobre a seta, o corpo ou outro rótulo.
- Toda equação inteira dentro da zona CONTA (x ≤ 6,6); se não couber, quebrar em duas linhas ou `scale_to_fit_width`.

### 2. Correções por bloco

**2.1 Setas da corda no cavalo (hook, A5, T8, S1) — prioridade.**
- Use o ponto do **arreio** (barra branca no peito) e o ponto de amarração **na pedra**, exportados pelo Three.js em `pontos.json` (como já fez com a ponta do rifle), quadro a quadro.
- −F⃗ (hook) / −T⃗ (T8): cauda no arreio, apontando **para trás, paralela à corda**, deslocada ~0,15 acima da corda, fora do corpo. F⃗ / T⃗: cauda na amarração da pedra, apontando para
  a frente, paralela à corda. **Mesmo comprimento na tela** (com a câmera lateral do T8; se a perspectiva encurtar uma delas, use câmera ortográfica nas tomadas com setas).
- No T8, as duas setas da corda ficam **dentro da fronteira** e em cinza apagado (internas). Rótulos de valor (`2.608 N`) junto da seta, acima da corda, com folga ≥ 0,25 da cabeça e do texto
  da CONTA. As setas do chão (2.352 N, 2.800 N) e seus rótulos ficam **abaixo da linha do chão**, sem tocar nos cascos.
- No A5, a seta azul que vira cinza é essa mesma seta do arreio.

**2.2 Resumo (19:12–19:50).** Modo PALCO + CONTA. PALCO: o cavalo 3D **grande** (como no S1, 19:16), andando, com a fronteira. CONTA: as três ideias, uma por vez, cada uma com seu
ícone pequeno à esquerda: (1) dP⃗/dt = F⃗^ext · COMPONENTE POR COMPONENTE (esferas); (2) MOMENTO SE DIVIDE IGUAL; ENERGIA, NÃO (blocos); (3) **NÃO CONSERVA? AUMENTE O SISTEMA**
(blocos + Terra). Quando a ideia 3 entra, a fronteira do cavalo cresce até incluir o chão (com a legenda `+ TERRA`). Sem a faixa de chão atravessando a tela atrás do texto.

**2.3 T10 (12:04–12:12).** Trocar o texto pelo aprovado: `QUANTO MAIOR A DIFERENÇA DE MASSAS, MAIOR A FRAÇÃO DA ENERGIA CINÉTICA QUE FICA COM O MAIS LEVE` (duas linhas na CONTA).
E os blocos do loop sem atrito: limite o deslocamento (eles rebatem em batentes nas bordas do PALCO, ou o loop recomeça com crossfade antes de saírem); nunca cortados.

**2.4 T8, o cavalo acelerando.** Uma única tomada de aceleração **sincronizada com T8-3/T8-4** (de "a = 0,32 m/s²" até a conferência): v de 0,30 a ~3,5 m/s em ~10 s, com a seta da
velocidade (violeta) crescendo e um mostrador pequeno `v = … m/s`. No resto do T8 (T8-1, T8-2, T8-5), o cavalo anda num passo constante, **sem mostrador de velocidade e sem a seta da
aceleração**, com emendas em crossfade. Na variante do gelo (T8-6), a seta da velocidade encolhe (a ≈ −1,26 m/s²) até perto de zero e os cascos escorregam.

**2.5 Abertura.**
- A3 (0:58–1:12): a curva F_res(t) se desenha uma vez e **fica**; a área preenche e fica; no loop, só o disco desliza e a seta p⃗ cresce. Nada de sumir e reaparecer.
- A4 (1:20): os discos colidem e se afastam **dentro** do trilho; no fim do loop, crossfade antes de chegar à borda.
- A4 → A5 (1:28): a conta "Δp⃗₁ = −Δp⃗₂ → P⃗ = CONSTANTE" sai antes de o cavalo entrar (ou vai para a CONTA à direita e fica acima da linha do chão, sem tocar o cavalo).

**2.6 T7 (2:44–3:20).** Rótulos de força no tamanho Math S, pelo lado livre de cada seta; F⃗^ext abaixo das esferas, F⃗₁₍₂₎/F⃗₂₍₁₎ acima da mola. A soma de 3:08 em duas linhas:
`d(p⃗₁ + p⃗₂)/dt =` na primeira, `F⃗₁₍₂₎ + F⃗₂₍₁₎ + F⃗^ext` na segunda (o cancelamento por `TransformByGlyphMap` continua). "TERCEIRA LEI: IGUAIS E OPOSTAS" com folga ≥ 0,25 do quadro.

**2.7 T8-6, gelo (7:24–7:56).** Gelo só **sob as patas**, dentro do PALCO: placa translúcida azulada (`#9CC7FF` a ~35%, com reflexo leve), nunca branco chapado nem atravessando a CONTA.
A frase final vai na CONTA, abaixo da conta de 588 N, em fundo escuro.

**2.8 T9 (10:52–11:08).** Dois gráficos empilhados **com espaço**: P(t) em cima (eixo y de −1,2 a +0,2), P_Terra(t) embaixo (de −0,2 a +1,2), separados por ≥ 0,4; rótulos dos eixos à
esquerda de cada eixo, sem invadir o outro gráfico. O gráfico da soma (= 0) continua na CONTA.

**2.9 E6 (13:12).** Sem coluna vazia: o balanço de energia começa a entrar enquanto a última linha do "rebate" ainda está na tela (a anterior apaga para 40%).

**2.10 E7 (13:36–14:52).**
- **Recuo em velocidade real** (0,0559 m/s e 0,0313 m/s), sem o aviso "RECUO EXAGERADO NA TELA".
- **Tiro a 56° em câmera lenta** (chip `CÂMERA LENTA`): durante o disparo, a **normal do gelo** aparece como seta azul-claro grande nos pés, crescendo e voltando ao normal, e **fica marcada**
  (opacidade 0,5) até o fim do bloco; ao lado, rótulo `N⃗ (EXTERNA, IMPULSIVA)`.
- **Decomposição do momento da bala:** seta magenta p⃗_bala ao longo do cano (ponto do cano em `pontos.json`), com p_x e p_y tracejadas; p_y ganha um "X" quando aparece `P_y NÃO SE CONSERVA`
  e p_x se liga à seta do recuo quando aparece `P_x SE CONSERVA`. Variáveis saindo do desenho para a conta (`TransformFromCopy`).
- Barras (14:36–14:52) na zona CONTA, em fundo escuro (painel `PANEL`), maiores (altura ≥ 2,2), fora do gelo.

**2.11 E9 (17:52).** Remover o traço solto embaixo de "IMPULSO CERTO". O tanque 3D fica de fora (o 2D de componentes está claro; não precisa refazer).

**2.12 Coda (19:00–19:10).** A vela fica no PALCO; se ela se afastar, a câmera acompanha ou ela sai pela esquerda. O texto final só na CONTA, sem nada 3D por cima.

**2.13 Pausas de 4–6 s** (12:37, 12:43, 15:04, 15:08, 16:02, 16:19): em cada uma, um realce do termo citado no desenho e na conta, ou o próximo objeto entrando mais cedo. Meta: nenhuma ≥ 4 s,
exceto o cartão final.

### 3. O que não muda
Narração v2, âncoras, capítulos (11, mesmos títulos), cores, números da física, 3D já aprovado (cavalo, esferas, disco, manequim, vela), grade PALCO/CONTA, selos de ligação, DICAs.

### 4. QA
- Medição de quadros parados (lista ≥ 4 s).
- Auditoria de sobreposição em todo o vídeo, incluindo **rótulo × objeto 3D** (projete as caixas do cavalo, do manequim e da vela com os pontos exportados do Three.js e cheque colisão com
  todo texto/MathTex) e **objetos fora do PALCO** (qualquer bounding box que cruze a borda do quadro ou da zona).
- Alinhamento 3D × Manim ≤ 2 px, agora também para: arreio e amarração da pedra (setas da corda), mãos × bola (E6), ponta do cano × seta p⃗_bala (E7).
- Conferir que "QUANTO MAIOR A DIFERENÇA…" está com o texto exato da §2.3 e que a ideia 3 do resumo aparece.
- Nenhuma referência de livro; nenhum header sobreposto em viradas de capítulo.

### 5. Stills 1920×1080
H1 (setas no arreio e na pedra) · T8-4 (conta + 2.608 N fora da cabeça) · T8-6 (gelo) · T9-6 (gráficos empilhados) · T10 fim (texto aprovado + blocos dentro do PALCO) · E7-4 (normal + p_x/p_y) ·
E7-5 (barras na CONTA) · RESUMO com as três ideias.

### 6. Parada e relatório
Pare com o preview v3 completo. Relatório (AGENTS.md): arquivos alterados; lotes re-renderizados; renders e caminhos; pausas ≥ 4 s; resultado das auditorias (sobreposição, 3D × texto, fora do PALCO);
alinhamento (incluindo os pontos novos); arquivos de teste apagados (lista); pendências. Zip para avaliação como no v3. Sem commit nem push.
