# HANDOFF v3 · yt_0041 · CÁLCULO III · EP. 16 · Coordenadas esféricas na integral tripla

Data: 2026-11-16. Fase: **preview v3** (540p15, silencioso). Não gere voz, SRT, 1080p nem entrega.

**Base:**
- o preview v2 do Claude Code (`yt_0041_preview_v2_540p15.mp4`, 21:04, silencioso);
- o **handoff v2** (`yt_0041_v1_avaliacao_e_handoff_v2.md`, neste zip). Ele continua valendo em tudo o que este documento não muda, em especial §2 (tamanho), §3 (vistas), §4 (contas A1–A6), §6 (27 correções) e §8 (não mexer).

**Narração vigente:** `yt_0041_narracao_v1_4.md` (≈ 22:12), neste zip.

Notação, cores e conversão px → Manim: iguais ao handoff v2. Resumo:
- ρ densidade, r distância, R raio fixo, s = r sen φ (sombra), φ a partir de +z, θ longitude;
- 120 px por unidade a 1080p: `x_m = (x_px − 960)/120`, `y_m = (540 − y_px)/120`.

---

## 0. Veredito do preview v2

**Ainda não está pronto para a narração.** O que o v2 acertou fica:
- escada do B5 (massa até c) e do B6-2 na tela;
- flash por quadro zerado;
- alinhamento 3D × Manim de 0,014 px.

O resto do handoff v2 quase não entrou. A prancha `comparacao_v2.jpg` comparou com os alvos **v1.1**, não com os v2, e por isso o QA saiu limpo.

O Kaio também pediu, sobre o 3D: **"tudo alinhado na grade, sem poluir demais, bem legível, sem sobreposições"**. Esse pedido vira o sistema da §2, igual ao que a série já adotou no yt_0040 v4.

---

## 1. O que o v2 não aplicou do handoff v2

Os tempos são os do preview v2. Seções medidas pelo `tempos_render_v2.txt`:

| Seção | Tempo no v2 |
|---|---|
| PH | 0:00–1:32 |
| PA | 1:32–1:48 |
| PB1 | 1:48–5:02 |
| PB2 | 5:02–11:28 |
| PB3 | 11:28–13:27 |
| PB4 | 13:27–14:29 |
| PB5 | 14:29–16:18 |
| PB6 | 16:18–19:17 |
| PB7 | 19:17–19:44 |
| PS | 19:44–21:04 |

Os stills de prova estão em `yt_0041_quadros_alvo_v3/prova_preview_v2_stills.jpg`.

| # | Onde (v2) | Problema | O que pede (handoff v2) |
|---|---|---|---|
| P1 | H1, B4, B5, B7 | Cunha de 90° vista de frente (o "coração") | Octante (v2 §3.1), alvos 01, 11, 12 |
| P2 | Vídeo todo | Fórmulas ≈ 14 px a 540p (≈ 28 px a 1080p) | KaTeX 50–54 px principal, 44 secundária, legenda 30, coluna na metade direita (v2 §2) |
| P3 | B1-1, B1-2 (PB1) | Sem as duas vistas 2D | Painéis "PÁGINA (DE LADO)" e "CHÃO (DE CIMA)" (v2 §3.2), alvo 03 |
| P4 | B2-2 (PB2) | Seta entre os painéis continua | Tela cheia sem a seta, alvo 07 |
| P5 | B2-3 (PB2) | Sem os menores M₃₁ e M₃₂ na tela | Escada A1, alvos 08a e 08b, ≥ 6 glyph maps |
| P6 | B2-3, ≈ 2:33 de PB2 (153 s do lote) | 1 s de 2D sem grade | Grade de borda a borda em todo 2D |
| P7 | B2-1 (PB2) | Rótulos nas arestas da caixinha | Legenda colorida (§2, G4) |
| P8 | B3-2 (PB3) | Receita em arame, sem sólido | Sólido opaco, alvo 10b |
| P9 | B6 (PB6) | Placas de texto em cima do 3D | Casquinha pequena + corte meridiano 2D, alvo 13a |
| P10 | S2 (PS) | Lata sem o corte 2D | Corte da página, alvo 14 |
| P11 | Todas as cenas 3D | 3D sobre fundo liso, sem papel nem piso | §2 deste handoff |
| P12 | Vídeo todo | Tempo segue a narração v1.2 (21:04) | Narração v1.4 (≈ 22:12), §3 deste handoff |

---

## 2. Sistema 3D da série (G1–G6), aplicado ao yt_0041

É o mesmo sistema do yt_0040 v4 (referência visual em `ref_yt0040/ref_3d_piso_b41.jpg` e `ref_3d_piso_b71.jpg`, neste zip). Ele **substitui** a linha do handoff v2 "3D e CTA ficam lisos".

### G1 · Papel sob o 3D
- O papel quadriculado (60 px a 1080p, o mesmo do 2D) fica **em toda a tela**, também atrás do 3D.
- O PNG do Three.js tem fundo transparente e é composto por cima do papel.
- Só o CTA final fica liso.

### G2 · Piso quadriculado em z = 0
- Grade de passo 0,5 u no plano z = 0, cor `#4A5080`, tubo de raio 0,0032 (× escala da cena), desenhada em z = −0,004 para não brigar com as arestas.
- Extensão por cena:
  - bola, cebola, casquinha e lata: [−1,5; 1,5]²;
  - receita: [−1; 1]²;
  - ponto: [−0,5; 2,5]².
- O piso substitui a "grade polar" antiga do ponto.
- Função de referência: `piso()` em `c3d41.html` (alvos v3).

### G3 · Câmera da série
- Uma câmera para todas as cenas da bola (H1, B4, B5, B7): mesma posição, mesmo alvo e mesma escala, com a origem no mesmo ponto da tela.
- O 3D ocupa a metade esquerda: **nada do 3D passa de x = 975 px**. O piso é cortado nessa borda, como no alvo; nenhuma linha do piso entra na coluna de fórmulas.

### G4 · Sem hastes; legenda alinhada ao papel
- Os rótulos de superfície saem do desenho e vão para uma **legenda colorida** (quadradinho na cor + texto 30 px):
  - o texto começa em x = 120 e fica na linha y = 1020 do papel;
  - se houver dois itens, o segundo começa em x = 540.
- No máximo 2 hastes por quadro, cada uma ≤ 90 px, e nunca cruzando texto.
- Os rótulos dos eixos x, y e z ficam a ≤ 30 px da ponta da seta, sem tocar nela. O B4 e o B5 precisam dos rótulos de x e y, que faltavam.

Legendas dos alvos:

| Cena | Legenda |
|---|---|
| H1 | `■ LEVE NO CENTRO: ρ = 0` (`#5FA8C8`) e `■ PESADA NA CASCA: ρ = 1` (`#35D9FF`) |
| B4 | `■ CASCA DE RAIO r, ESPESSURA dr` (`#FF9440`) |
| B5 | `■ r = 0,84: METADE DA MASSA DE CADA LADO` (`#FF9440`) |

### G5 · Geometria opaca e limpa
- Superfícies opacas com sombreamento suave (estilo da bola do alvo 01), sem arame denso: no máximo 8 meridianos e 4 paralelos.
- Na receita (B3-2), **sai a esfera fantasma em arame**. Fica só o sólido, o eixo z a partir da origem, a sonda e o piso.

### G6 · Tudo começa numa linha do papel
- Todo texto e toda fórmula começam num múltiplo de 60 px: coluna em **x = 1020** (não 1010) e linhas de base nos múltiplos de 60.
- O espaço entre o 3D e a coluna é ≥ 60 px.
- Nos painéis 2D dentro de cena 3D (B1-1, B6-1, S2), o painel é opaco, com grade própria, e as bordas caem em linhas do papel.
- No S2, a lata fica pequena no alto à esquerda, o painel do corte vai de x = 60 a 700, o texto começa em x = 780 e nada da lata entra no painel.

---

## 3. Tempo pela narração v1.4

- O preview v3 é cronometrado pela `yt_0041_narracao_v1_4.md`: 3.967 palavras a 3 palavras/s, ≈ 22:12.
- Use as durações por âncora da tabela do arquivo.
- A **caneta não acelera**. Cada degrau se escreve enquanto a voz conversa sobre ele (âncoras `[mecânica]`). Nada é escrito em silêncio e não há silêncio inserido.
- Se uma escada não couber na fala da âncora, **não comprima a escrita**: liste no relatório (âncora, degraus, segundos que faltam) para a narração ser ajustada aqui.

---

## 4. Quadros-alvo v3 (pasta `yt_0041_quadros_alvo_v3/`)

| Alvo | Cena | O que mostra |
|---|---|---|
| 01_H1_bola_octante_v3 | H1 | Papel + piso + octante + legenda de dois itens, coluna em 1020 |
| 03_B1-1_endereco_duas_vistas_v3 | B1-1 | Piso sob o ponto, duas vistas, coluna em 1020 |
| 10b_B3-2_receita_v3 | B3-2 | Receita sólida sem esfera fantasma, piso [−1; 1]² |
| 11_B4_cebola_octante_v3 | B4 | Casca laranja, legenda, rótulos x, y, z |
| 12_B5_massa_ate_c_v3 | B5 | Casca em 0,84, legenda, escada completa |
| 13a_B6-1_casquinha_corte_v3 | B6-1 | Casquinha pequena sobre o piso + corte meridiano |
| 14_S2_lata_corte_v3 | S2 | Lata pequena, corte 60–700, texto em 780, cartão do próximo vídeo |

- Folha de contato: `00_folha_contato_v3.jpg`.
- As cenas sem alvo v3 seguem os **alvos v2** (`yt_0041_quadros_alvo_v2/`: 07, 08a, 08b, 13b) com G1–G6 aplicados: papel sob o 3D, piso e legenda.
- Isso vale também para a caixa/bolagrade (B1-3, B2-4, B3-1) e a caixinha (B2-1).
- Fontes dos alvos: `sb41.html` (compositor canvas + KaTeX, `?k=<chave>`) e `c3d41.html` (Three.js r128, `?k=<chave>`), renderizados por `r3d.js` e `shot2.js`. Os alvos são referência de composição; não é para copiar o pipeline.

---

## 5. QA do preview v3 (relatório obrigatório)

Vale a lista do handoff v2 §7, com estas mudanças:

1. **Comparação:** prancha lado a lado com os alvos **v3** (7) e **v2** (07, 08a, 08b, 13b). Comparar com v1.1 invalida o relatório.
2. **Prancha 3D:** para cada cena 3D, uma prancha 2×3 com um quadro a cada 1/6 da cena, mostrando papel, piso, legenda e coluna.
3. **G1–G6 por cena 3D** (OK/NÃO):
   - papel sob o 3D;
   - piso;
   - nada do 3D além de x = 975;
   - número de hastes (≤ 2, ≤ 90 px);
   - distância rótulo–ponta de cada eixo (≤ 30 px);
   - meridianos/paralelos;
   - x de início da coluna (1020).
4. **P1–P12 da §1:** um por linha, com OK/NÃO e o tempo no v3.
5. **Tempo:** duração total e, por âncora, duração da fala v1.4 × duração da cena. Lista das escadas que não couberam (§3).
6. **2D sem grade:** zero segundos.
7. Sem pulso, brilho, palco vivo, tracer ou qualquer efeito novo. Tela parada não é portão automático.

---

## 6. O que NÃO mexer

- Tudo da §8 do handoff v2: matemática, resultados, cores, notação, caneta, ordem dos blocos e kit de QA.
- O que o v2 já acertou: as escadas do B5 e do B6-2, flash zero e o alinhamento 3D.
- Documentos globais, template, assets e outras unidades.

## 7. Entrega desta fase
- Preview 540p15 silencioso.
- Relatório da §5.
- Pranchas de comparação (alvos v3/v2) e pranchas 3D.
- Pare, sem voz, sem 1080p e sem entrega.
