# Rotacional e divergente

- **ID:** `yt_0027`
- **formato:** `longo_horizontal`
- **natureza:** `teoria_visual`
- **Série pública:** **CÁLCULO III · EP. 02**
- **disciplina:** `Cálculo III`
- **bloco:** `Funções de várias variáveis a valores vetoriais`
- **modulo:** `3.1-T2 Rotacional e divergente (no docs/mapa_curricular.md atual: 11.1)`
- **referencia:** `Guidorizzi, Um Curso de Cálculo, vol. 3, 6ª ed., §1.3 (Ex. 1, 3, 4, 5, 6; Exerc. 3, 4, 5) e §1.4 (Ex. 1, 2, 3, 5, 6, 7)` — só na ficha e na descrição do YouTube; nunca na tela nem na fala.
- **título:** Rotacional e divergente
- **pergunta narrativa:** Duas rodinhas passam pelas mesmas setas; por que só uma gira?
- **pergunta_central:** o que um campo faz com um pedacinho de fluido num ponto: quanto ele gira e quanto ele se expande?
- **pre_requisitos:** campo vetorial lido como velocidade; derivadas parciais; gradiente
- **payoff_principal:** rot e div são medidas locais (dependem de como as setas mudam em volta do ponto); as duas fórmulas nascem da rodinha (média dos giros de dois braços) e da caixa fixa (saldo do que sai por unidade de área); o desenho de longe engana (vórtice sem giro, rio reto com giro, falsa fonte); na física, os furos são fios (Gauss e Ampère)
- **hipoteses:** campo = velocidade de um fluido em escoamento estacionário, de classe C¹; rodinha = sonda ideal, pequena e rígida, gira a ½ rot; divergente positivo = o pedacinho se expande (não há criação de matéria)
- **duracao_alvo:** 20:22 de voz real (`audio/narracao_final.wav`, 1221,8 s; narração v6, 3.843 palavras, 3,15 palavras/s); o vídeo segura +3 s no CTA
- **3d_threejs:** `cubo` (B6-1, v3 = `cubo3` do `referencia_v3/c3d27.html`: chapa a 32 %, uma seta por parede, molduras por eixo que acendem com a parcela, material chapado), `roda` (B6-2/3) — confirmados no final (cubo no B6-1; roda no B6-2 e B6-3) — `threejs/cena3d/f27.js` (base `b3d.js`), sem sombra, névoa nem chão, composto sobre o milimetrado
- **solido_3d:** nenhum do arsenal Blender; geometria de `rotacional_roda_de_pas` (cruz de pás) e `divergencia_local` (caixa com setas pelas faces) usada como referência e portada para Three.js
- **fundo:** (final, 11/11, pedido do Kaio) violeta liso #18143A → #0F0C26 como imagem da câmera + grade de quadradinhos #2B2558 (traço 1,2) que nasce dos eixos de cada cena (`papel27.py`, cópia do papel v2): grade padrão 1 u (= V do palco); grade por painel/cartão nos layouts de dois painéis e cartões; liso no 3D (B6-1 a B6-3) e no gráfico do calor (B7-4); placas lisas atrás do canto e do logo; 3D composto sobre o violeta
- **canto:** a partir do bloco A. Linha 1 `CÁLCULO III · ROTACIONAL E DIVERGENTE`; linha 2: `UM PEDACINHO DE FLUIDO`, `ROTACIONAL`, `DOIS ENGANOS`, `DIVERGENTE`, `A FALSA FONTE`, `NO ESPAÇO`, `NA FÍSICA`, `LAPLACIANO`, `RESUMO`
- **ordem:** H → A → B1 → B2 → B3 → B4 → B5 → B6 → F → B7 → S (v4: B1 abre com B1-1a, nomes das peças P e Q; B6 abre com B6-0, em qualquer dimensão)
- **Status:** FINAL (handoff final, 11/11): ajustes §2 (13 itens), voz ElevenLabs v4, sincronia pelo alinhamento forçado, `legenda.srt`, render 1080p30 CRF 14, master e entrega. Quadros-alvo em `referencia_v2/`–`referencia_v4/` e `referencia_v5/` (alvos 18–21). Pá marcada da rodinha inteira azul-clara no 2D e no 3D (decisão do Kaio, 11/11)

## Arquivos
- `narracao.md` — Anexo A do handoff v1 (fonte do `ancoras.json`); `gerar_ancoras.py` → `ancoras.json`, `duracoes_estimadas.json`
- `kit.py` — kit copiado do yt_0026 (relógio por quadro, âncoras, canto, caneta, contorno, chapas, auditorias, Fundo3D)
- `v27.py` — helpers do `v7.py` do yt_0026 (copiados) + peças do `sb27.html`: campo comprimido, rodinha, fita, objetos materiais, fluxos exatos (Anexo C), QA [fluxo] e [colisão]
- `comparar.py` — lado a lado (render × quadro-alvo): os 24 do v2; com `RODADA=v3`, os 11 do v3 + os v2 das cenas corrigidas
- `qa_sobrepos_rel.py` — relatório R5 (`renders/v3/qa/sobreposicoes_v3.txt`) a partir dos logs do render com `QA_SOBREPOS=1`
- `sec_*.py` — um lote por seção; `cena.py` registra os lotes
- `render.sh` / `render3d.sh` / `render_todos.sh`, `montar_preview.py`, `folha_contato.py`, `zip_claude.py`, `qa_*.py`
