# HANDOFF v1 · yt_0025 "Momento angular do corpo rígido" · vídeo inteiro (preview silencioso)

Data: 2026-11-07. Formato: `longo_horizontal`. Unidade nova: `videos_longos/yt_0025_momento_angular_corpo_rigido/` (`template/config_horizontal.py`).
Este handoff é **autocontido**: a narração v1 está completa no Anexo A e é a fonte do `ancoras.json`; a tabela de conferência numérica está no Anexo B. Física, números, sinais e textos de tela foram resolvidos e conferidos (sympy + numpy); não redesenhe. Se encontrar inconsistência objetiva, reporte antes de ampliar o escopo.

## 0. O que é esta rodada

- Vídeo de **teoria** da série Rotação de corpos rígidos (Física I; `docs/mapa_curricular.md` 4.11; na página renumerada do mapa, 1.12-T5). Uma pergunta guia o vídeo inteiro: **como pode existir torque sem aumentar a velocidade angular?** Cada exemplo avança a mesma resposta: pêndulo cônico (um L que só muda de direção) → corpo rígido em eixo fixo (L_z = I_z ω é só a componente axial) → haltere torto (núcleo: as partes transversais se somam) → eixo principal → torque nos mancais → roda desbalanceada.
- **Fora:** matriz de inércia 3×3 na tela, diagonalização, equações de Euler, conservação em sistemas, patinadora, giroscópio, exercícios.
- **Objetivo:** preview do **vídeo inteiro**, 960×540 / 15 fps, **sem voz**. Duração esperada **~14 min** (fala de ~2.200 palavras ≈ 13,6 min a 2,7 palavras/s, mais holds; estimativa, a voz mede; a fala manda, a cena se estica).
- **Prioridade do Kaio nesta unidade: 3D avançado e MF-Tools "usar e abusar"** (§4 e §6). Este é um vídeo 3D de verdade: L⃗ fica no plano (eixo, massa), perpendicular ao fio ou à haste, e esse plano gira no espaço.
- **Kit:** copiar para a unidade nova, sem alterar outras unidades. Ordem de preferência: `videos_longos/yt_0024_momento_angular_particula/` (se estiver no checkout: `threejs/` com o acabamento HDR/PBR/bloom da `mesa_furo`, auditorias e primitiva de escrita) → `videos_longos/yt_0023_exercicios_rotacao/` (auditorias `CONCÊNTRICO`, `ÁLGEBRA`, `OPACIDADE`) → `videos_longos/yt_0022_torque/` (no Git: `kit.py`, `prob.py`, `prob2.py`, `algebra22.py`, `equacao22.py`, `pecas22.py`, `qa22.py`, `parado22.py`, `classifica_portao.py`, `agrupar_portao.py`, `prancha.py`, `fundo.py`, `fundo_lab.png`, `gerar_ancoras.py`, `montar_preview.py`, `render*.sh`, `threejs/` com `r3d.js`, `b3d.js`, `f22.js`). Para o que faltar (mostrador, auditoria de setas e de cor por operador): `videos_longos/yt_0020_cinematica_angular/`. Se nenhuma estiver no checkout, **pare e avise** antes de recriar o kit do zero.
- **Não comece:** voz, SRT, master, entrega, commit ou push.

## 1. Ficha (`ficha.md` da unidade)

- `formato: longo_horizontal` · `natureza: teoria_visual`
- `disciplina: Física I` · `bloco: Rotação` · `modulo: 4.11 Rotação de corpos rígidos (momento angular do corpo rígido)` · `referencia: Kleppner & Kolenkow, An Introduction to Mechanics, 1ª ed., Ex. 6.2 e 6.6, §7.2 e Ex. 7.4–7.6; Moysés vol. 1, cap. 12; Sears, cap. 10` (só na ficha e na descrição do YouTube, **nunca** na tela nem na fala)
- `Série pública: **MECÂNICA · EP. 6 (ROTAÇÃO DE CORPOS RÍGIDOS)**` (provisório)
- Título: **Momento angular do corpo rígido** · pergunta narrativa: **Como pode existir torque sem aumentar a velocidade angular?**
- `pergunta_central:` o que é o momento angular de um corpo rígido em eixo fixo, quando ele não aponta ao longo do eixo e o que é preciso para manter esse eixo no lugar?
- `pre_requisitos:` L⃗ = r⃗ × p⃗ de uma partícula; τ⃗ = dL⃗/dt; I = Σ m ρ²; τ = I α; produto vetorial; força centrípeta
- `payoff_principal:` três ideias: (1) L_z = I_z ω é só a componente ao longo do eixo; (2) um torque pode mudar só a direção de L, com ω constante; (3) no eixo principal, L⃗ = I ω⃗, e a simetria é só um jeito de achar esse eixo
- `duracao_alvo:` ~14 min (sai da fala; teto do Kaio: 15 min)
- `3d_threejs:` `pendulo_conico` (H, A, B1), `corpo_voxel` (B2, B4-3, S2), `haltere_torto` (B3, B4-1, B5, S1), `roda_balanceamento` (B6)
- `solido_3d:` nenhum do arsenal Blender; geometria própria em Three.js
- Canto: linha 1 `MECÂNICA · MOMENTO ANGULAR DO CORPO RÍGIDO`; linha 2 = bloco da vez (`UM L QUE SÓ VIRA` com L em MathTex, `UM CORPO INTEIRO`, `O HALTERE TORTO`, `EIXO PRINCIPAL`, `O QUE OS MANCAIS FAZEM`, `A RODA`, `RESUMO`)

## 2. Sistema visual

### 2.1 Cor por família de grandeza (decisões do Kaio para a série; cor por token completa; número substituído herda a cor)

| Família | Elementos | Cor |
|---|---|---|
| Vetor posição e raio | r⃗, r⃗ᵢ, ρ⃗ᵢ, ρ, R, z, zᵢ, ℓ (quando é o vetor/raio do desenho) | laranja queimado `VETC #D2823A` |
| Geometria | círculos das trajetórias, cone do fio, plano (eixo, haste), cotas de distância (d entre mancais, 0,52 m), eixos principais | `GEO #B8C4DA` (rastro `RAST #9FB4D6`), em minoria |
| Momento linear | p⃗, p, m v⃗ | magenta `#EA63FF` |
| **Momento angular** | L⃗, L⃗ᵢ, L_z, L_h, L⃗_⊥, dL⃗, círculo da ponta de L⃗ | magenta-claro `#F19AFF`; **parte axial cheia, parte transversal tracejada (mesma cor)** |
| Velocidade | v⃗, vᵢ, ω, ω⃗, rotações por segundo | violeta `#9C8CFF` |
| Aceleração | α, g | verde `#3FE08B` |
| Massa e inércia | m, mᵢ, I, I_z, **produtos de inércia** (Σ m x z, Σ m y z), excessos de massa da roda | rosa `MAS #FF7EB6` |
| Força e torque | peso, F⃗_c, F⃗ dos mancais, τ⃗, τ, τ_z, binário | azul-claro `#5AA2FF` |
| Ângulo | θ, α (ângulo da haste), φ, 60°, arcos | âmbar `#FFC24D` (atenção: α ângulo da haste é âmbar; α aceleração angular só aparece em τ_z = I_z α e α = 0, verde) |
| Tempo e números puros | t, dt, fatores (× 9, ÷ 4), 2π | branco |
| Corpos | pórtico, eixo, mancais, haste, bancada, aro | aço PBR (§4); esferas, bolinha e cubinho em destaque com faixa rosa `MAS` |

- **Ambiguidade α:** o ângulo da haste e a aceleração angular usam a mesma letra nos livros. Aqui o ângulo da haste é `α` âmbar e a aceleração angular é `α` verde; eles nunca aparecem na mesma linha exceto em `τ_z = 0 → α = 0` (B5-2), onde só existe o verde. Se a auditoria de cor confundir, renomeie internamente, nunca na tela.
- **Operadores neutros** (regra do Kaio): `=`, `+`, `−`, `×` do produto vetorial, `·`, `d`, `dt`, `Σ`, `√`, barra de fração, parênteses, setas de implicação ficam brancos; só a grandeza leva cor. O subscrito herda a cor da letra (L_z magenta-claro inteiro, I_z rosa inteiro, ρᵢ laranja inteiro). Unidades em `\mathrm{}` brancas. `ẑ` é branco (direção, não grandeza).
- MathTex colorido em ≥ 50% dos glifos das grandezas, stroke na cor, rótulos na cor, nada esmaecido parado. Cor por capítulo ≥ 20% (família) em todos os capítulos.

### 2.2 Fundo
- `fundo_lab.png` em **todas** as cenas Manim (gradiente `#0B1A3A → #08122B → #0A1030`, vinheta leve, brilho magenta baixo, estrelas). Nunca o `#050816`. No Three.js, o mesmo gradiente procedural (§4.6).
- **Estrelas em movimento contínuo para a esquerda em relógio global** (§3.3).

### 2.3 Layout
- **Teoria com desenho sempre:** 3D à esquerda (~50–55%), CONTA à direita em `Pilha` (centro x ≈ 4,3). Nunca tela só de álgebra.
- **Insets:** `VISTA DE CIMA` (B1-5, B5-1) é um quadro 2.5D do Manim no canto inferior direito da coluna 3D (≤ 28% da coluna), com borda GEO fina, mostrando só o círculo da ponta de L⃗ (espaço de L, não espaço físico). Nunca sobre o objeto.
- Faixa de selo única (y 2,55 a 3,15; x 0,6 a 6,7), um selo por vez: `HIPÓTESES`, `CONFERE`, `ATENÇÃO`, `DE OUTRO PONTO`, `REMONTADA`, `CÂMERA LENTA`, `FORA DE ESCALA`, `VISTA EM RAIO X`.
- **Sem caixas** em volta de equações. O resultado de cada cadeia fica em destaque por **tamanho** (um degrau acima, MathTex L) e por um **sublinhado fino** (stroke 3) na cor da grandeza do lado esquerdo, que entra junto com o último glifo. `PANEL` só para os cartões do resumo (S1), sem borda branca.

## 3. Regras de tela

### 3.1 G1–G34 (todas valendo, como no yt_0020, yt_0022, yt_0023 e yt_0024)
- **G1** selo ≥ 24, frase-chave ≥ 30, rótulo MathTex no desenho ≥ 36, equação na CONTA ≥ 46. **G2** margem 0,45. **G3** objeto principal ocupa 55–75% da coluna dele.
- **G5/G13** trocas por crossfade 0,4–0,6 s; nunca quadro vazio. **G6** nada sobra da cena anterior; texto nunca sobre objeto nem sobre a trajetória dos próximos 2 s (as massas giram: o rótulo foge do volume varrido). **G7** uma frase-chave por vez. **G8** setas com espessura ≥ 5, comprimento ≥ 0,6, rótulo fora; setas curvas com raio ≥ 0,5. **G10/G12/G24** cor por token completa, inclusive números substituídos. **G14** cópia nunca sobre o original.
- **G19/G23 contas construídas:** todo símbolo existe antes como rótulo no desenho e vai para a CONTA por `TransformFromCopy`; ordem: lei geral → especialização (termos voando do desenho) → passos (linha nova, glyph map) → números (um por vez, do rótulo) → resultado. Nenhuma linha entra pronta.
- **G21** hipóteses em uma linha, com a fala, até a primeira conta. **G25** CONTA em `Pilha`. **G27** rótulos por `rotulo()` com teste de colisão, a ≤ 0,4 do dono; rótulo de objeto que se move acompanha o objeto e fica na horizontal.
- **G28 portão:** zero em `SOBREPOSIÇÃO`, `TEXTO SOBRE OBJETO`, `TEXTO SOBRE CAIXA`, `FORA DA MARGEM`, `SELO DUPLO`, `LINHA ÓRFÃ`, `CALHA`, `TRÂNSITO`, `RÓTULO SOLTO`, `PALCO 3D`, `FUNDO`. Auditoria a cada 3 quadros dentro de cada `play`; Three.js entra pelas silhuetas do `timeline.json`. Prancha humana com os 24 quadros de maior densidade de texto. Exceção só com justificativa escrita no `qa.txt`.
- **G29 ESQUELETO**; **G30 3D × TEXTO**; **G31 DUPLICATA**; **G32 VAZIO**; **G33** estado antes do número.
- **ORDEM:** álgebra escrita da esquerda para a direita, token a token, na ordem da fala (medir o agendamento real).
- **COLUNA VAZIA 0** (metade da tela vazia por mais de 3 s); **PARADO 0** (tela sem informação nova por mais de 3 s fora dos holds do §3.2).
- **OPACIDADE:** linha ativa, rótulo em uso e resultado 1,0; linha anterior ainda citada ≥ 0,85; histórico (no máximo 2 linhas) ≥ 0,6. **Fantasmas declarados** (preenchimento 0,3–0,5, contorno 1,0): o cone do fio, o plano (eixo, haste), os trechos de seta atrás do corpo (§4.8), os L⃗ᵢ das massas depois que se somam no B3-4, o haltere 1 enquanto o haltere 2 entra no B4-1. O que sai, sai inteiro (`FadeOut` até 0 em ≤ 0,4 s). Portão: texto/MathTex com 0,05 < opacidade < 0,6 por mais de 6 quadros, fora da lista.
- **Aliasing (15 fps):** bolinha 12,8° por quadro (ok); haltere a 1 volta/s, 24° por quadro (ok); haltere a 3 voltas/s, 72° por quadro → `CÂMERA LENTA` 1/3; roda a 14,7 voltas/s, 354° por quadro (gira "para trás" no estroboscópio) → **sempre** `CÂMERA LENTA` a 0,75 volta/s com desfoque de movimento (§4.4). Rastros com subamostragem de 8 posições por quadro.

### 3.2 Pausa útil
Holds de 2–3 s só em: H3 (a pergunta com o torque girando), B1-6 (ω² = g/(ℓ cos θ) com os números), B3-4 (os dois L⃗ᵢ somados na origem), B5-4 (binário pelas forças = binário pela geometria). Fora disso, nada parado > 3 s.

### 3.3 Três regras permanentes (Kaio, 2026-11-06)
1. **Fundo de estrelas:** movimento contínuo para a esquerda em relógio global do vídeo (`t_global = T0_lote + clk`, `T0_lote` = `ini` da primeira âncora do lote), velocidade constante por camada, sem balanço vertical, reciclagem só fora da tela (campo ≥ tela + 2 u de cada lado); nunca reinicia por lote, nunca para, nunca volta. Fora da sincronia e do medidor de PARADO. **O fundo do Three.js usa o mesmo relógio e a mesma velocidade aparente**: na emenda Three.js ↔ Manim as estrelas não saltam.
2. **Sem flash:** nenhum texto/fórmula visível (opacidade ≥ 0,15) por menos de 0,7 s e depois removido antes de ser escrito. Destino da `voa` e títulos com opacidade 0 até o primeiro glifo pousar. Classe `FLASH` no portão, em quadros consecutivos, + detector de picos de tinta.
3. **Sólidos 3D com contraste:** nunca tom sobre tom; luminância da superfície ≤ ~85%; arestas e faixas com contraste ≥ 1,6× e ≥ 2 px a 1080p; rótulos e setas fora do sólido; uma só função de desenho por objeto em todas as cenas.

## 4. 3D avançado (Three.js): quatro cenas

Contrato do kit em todas: `setFrame(f)` determinístico, `cenaPronta`, `window.projeta`, `timeline.json` com as coordenadas de tela de tudo que o Manim prende (alinhamento 3D × Manim ≤ 2 px **medido nos quadros gerados**). Posições e ângulos saem de `fisica25.py` (§4.7), nunca "a olho". Um único módulo `cenas25.js` com as quatro cenas, compartilhando renderer, materiais, luz e fundo.

### 4.1 Geometria (unidade: metro; z para cima; rotação anti-horária vista de cima, ω⃗ = +ω ẑ)

- **`pendulo_conico`:** origem no **prego** (olhal de aço, raio 8 mm) no centro da travessa de um pórtico de aço (duas colunas tubulares de 30 mm a ±0,80 m, travessa a z = +0,05, colunas até o piso). Fio: tubo de raio 1,2 mm, branco-quente `#F2EEE6`, comprimento **ℓ = 1,00 m**, **θ = 30°** do eixo vertical. Bolinha: esfera de raio 0,035 m, aço escuro com **faixa rosa `MAS`** no equador. Círculo de raio **R = 0,50 m** no plano z = −0,866. Piso: disco escuro fosco (raio 1,2 m) em z = −1,05, recebendo a sombra suave da bolinha (é ela que dá a profundidade). Eixo de rotação: linha GEO pontilhada do prego ao piso. **Cone do fio:** superfície GEO translúcida (preenchimento 0,08, borda em fresnel), só em H1 e B1-4.
- **`corpo_voxel` (a "batata"):** ~500 cubinhos de 3 cm (`InstancedMesh`, aço escovado), forma = união de 3 elipsoides com semente fixa 25, com 4 mm de folga entre cubos (para ler "feito de pedacinhos"); massa igual por cubo. **Montagem:** o CM fica sobre o eixo vertical da bancada (o mesmo eixo/mancais do haltere). Orientação inicial escolhida em `fisica25.py` para o eixo vertical fazer **35° ± 5° com o eixo principal mais próximo** e L⃗ sair **≥ 20°** do eixo. No B4-3, `REMONTADA`: com a rotação parada, o corpo gira inteiro (slerp de 1,5 s em torno do CM) até o eixo principal de maior I ficar vertical; depois volta a girar. Cubinho em destaque do B2-2: um cubo **acima** do CM, a ~70% do raio máximo, com faixa rosa.
- **`haltere_torto`:** bancada: base circular de aço (raio 0,30 m) em z = −1,05, carcaça cilíndrica do motor, coluna. **Dois mancais de rolamento abaixo do haltere**, em z = −0,45 e z = −0,85 (**d = 0,40 m**): caixa de aço, anel externo, **12 esferas visíveis** e anel interno; a gaiola gira a 0,4 ω (cinemática de rolamento, só visual). Eixo de aço polido (raio 12 mm) de z = −0,95 a z = +0,04. Cubo (raio 30 mm) em z = 0 (**origem = CM**). Haste de raio 8 mm, comprimento total 0,60 m (**ℓ = 0,30 m** de cada lado), a **α = 30°** do eixo. Esferas de raio 0,045 m, aço escuro com faixa rosa. Velocidade: **1 volta/s** (ω = 2π rad/s). **Plano (eixo, haste):** retângulo GEO translúcido (0,10, borda fresnel) preso ao corpo, só em B3-5, B3-7 e B5. **Haltere 2** (B4-1): igual, no mesmo cubo, inclinado a −α (forma um X no plano xz quando φ = 0).
- **`roda_balanceamento`:** roda de carro estilizada **sem marca**: pneu (raio externo 0,30 m, largura 0,205 m, perfil arredondado, banda com sulcos por mapa normal; borracha `#1E2228`, roughness 0,85, metalness 0), aro de liga de 5 raios (raio 0,203 m), cubo com 5 porcas. Eixo **horizontal** (y da cena) sobre dois pedestais de aço com mancais a ±0,25 m do plano médio da roda. **Excessos:** dois blocos rosa `MAS` de 20 g no flange interno do aro (ρ = 0,20 m), em **faces axiais distintas** (y = ±0,10 m) e **diametralmente opostos**; desenhados 2× maiores (`FORA DE ESCALA`). **Contrapesos** (B6-5): blocos de aço claro `#C9D2DE`, cada um na mesma face do seu excesso e diametralmente oposto a ele. Faces marcadas por um anel GEO fino em cada borda do aro.

### 4.2 Material (aço PBR, como no acabamento do toroide e da `mesa_furo`)
- Renderer: three.js do kit (r128), alvo **HDR half float** com MSAA 4×, cores da marca sRGB → linear e de volta no fim; tom com ombro suave (até 0,8 linear a cor sai exata; acima comprime para o branco); vinheta de até 18%.
- `MeshPhysicalMaterial`: aço estrutural (pórtico, bancada, pedestais) `metalness 0,85 · roughness 0,38 · clearcoat 0,35` (`#5E6878`); eixo, haste, mancais, prego `metalness 0,92 · roughness 0,22 · clearcoat 0,6` (`#7A8696`); esferas, bolinha e cubinhos `metalness 0,9 · roughness 0,3` (`#4E5766`); faixas rosa `MAS` `metalness 0,2 · roughness 0,45`; aro de liga `metalness 0,95 · roughness 0,18` (`#AEB7C4`).
- **Ambiente próprio azul-espacial** via `PMREMGenerator.fromScene` (softbox branca grande em cima, faixa fria ciano à esquerda, reflexo magenta baixo no horizonte), no lugar do `RoomEnvironment` cinza.
- **Oclusão de ambiente nos cubinhos** (`corpo_voxel`): AO assada por instância (fração de vizinhos ocupados, escurecendo até 35%), para a batata não virar uma mancha prateada.

### 4.3 Luz e sombra
- **Luz presa à câmera:** chave em cima à direita (branca, 2,2), contraluz fria `#8CC8FF` por trás (1,2) que desenha contorno nas esferas, na haste e no pneu.
- **Sombras suaves** (`DirectionalLight`, mapa 2048, PCF, raio 3): bolinha no piso, haltere e batata na base, roda no chão da bancada.

### 4.4 Efeitos
- **Bloom seletivo** (`UnrealBloomPass`, força 0,40, raio 0,2, limiar 0,55) numa passada própria com o aço como oclusor preto. **Só brilham:** a cabeça do rastro da bolinha e das esferas (últimos 6 cm passam de 1,0 em HDR na cor `RAST`; cauda de 0,8 s some linear). Nada mais brilha.
- **Desfoque de profundidade** (DOF suave, bokeh pequeno) só em A1–A2, atrás do título.
- **Desfoque de movimento por acumulação** na roda: 8 subquadros por quadro, só nos raios e no pneu (os excessos e contrapesos ficam nítidos para serem lidos).
- **Raio X** (B6-2, B6-5): o pneu desce para 25% de opacidade com borda fresnel 1,0 (selo `VISTA EM RAIO X`), para os dois excessos ficarem visíveis nas duas faces ao mesmo tempo.
- **Câmera orbitando** só em S1 (azimute +8°/s), nunca durante uma conta.

### 4.5 Câmeras (escolhidas pela física)

| Nome | Uso | Definição |
|---|---|---|
| `P_34` | H, A, B1 | perspectiva 35 mm equivalente, 18° acima do plano do círculo, azimute 35°, enquadra prego, cone e piso; o L⃗ (escala 1,6 m por kg·m²/s, ~0,54 m) cabe acima e ao lado do prego |
| `V_34` | B2, B4-3, S2 | perspectiva, 22° de elevação, azimute 30°, batata a ~60% da coluna |
| `H_34` | B3, B4-1, B4-2, B5, S1 | perspectiva, 20° de elevação, azimute 35°, haltere e os dois mancais visíveis; L⃗ na escala 1,8 m por kg·m²/s |
| `H_LADO` | B3-5 (ângulo reto entre L⃗ e a haste, 60° do eixo) | **ortográfica**, olhando ao longo de −y, com a rotação congelada em φ = 0 (haste no plano xz, massa de cima em +x): ângulos verdadeiros |
| `R_34` | B6 | perspectiva, 25° de elevação, azimute 55° (banda e face externa visíveis; face interna pelos raios ou pelo raio X) |

- Dolly contínuo entre câmeras em 1,4–1,6 s; troca perspectiva/ortográfica no quadro em que a diferença de projeção ≤ 1 px. A câmera **para exatamente** no quadro em que o Manim começa a desenhar setas. Nada gira na câmera durante uma conta.
- **Escolha de azimute pela leitura:** nos quadros congelados em que L⃗, τ⃗ e as partes axial/transversal são desenhadas, o azimute é escolhido para nenhuma dessas setas cair atrás do corpo nem ficar com menos de 60% do comprimento verdadeiro na tela.

### 4.6 Fundo e saída
- Fundo procedural: degradê `#0B1A3A → #08122B → #0A1030`, brilho magenta muito baixo no horizonte, estrelas andando para a esquerda **no relógio global** (§3.3). `window.TRANSP = true` sai com alfa quando o Manim já fornece o fundo; um dos dois por lote, declarado no `qa.txt`.
- Render: 960×540 no preview, 1920×1080 no final. Registrar o custo por quadro de cada cena nas duas.

### 4.7 Física da cena (`fisica25.py` → `tab25.json`)
- **Pêndulo:** g = 9,8 m/s²; ω = √(g/(ℓ cos θ)) = 3,364 rad/s; φ(t) = ω t, bolinha em ℓ(sen θ cos φ, sen θ sen φ, −cos θ). L⃗ (origem no prego) = m ℓ² ω (sen θ cos θ cos φ, sen θ cos θ sen φ, sen²θ); τ⃗ = r⃗ × (−m g ẑ).
- **Batata:** posições dos cubos, tensor de inércia em relação ao CM (só interno, **nunca na tela**), autovalores/autovetores, a orientação inicial e a final; L⃗ = I·ω⃗ por quadro; ângulo entre L⃗ e o eixo nos dois estados. Cubo destacado: ρ⃗ᵢ, zᵢ, v⃗ᵢ, partes axial (mᵢ ρᵢ² ω) e transversal (−mᵢ ω zᵢ ρ⃗ᵢ) do seu L⃗ᵢ.
- **Haltere:** r⃗₁ = ℓ(sen α cos φ, sen α sen φ, cos α), r⃗₂ = −r⃗₁, φ = 2π t. L⃗ = 2 m ℓ² ω (−sen α cos α cos φ, −sen α cos α sen φ, sen²α); τ⃗ = ω⃗ × L⃗; F⃗_c de cada massa; forças dos mancais ±(τ/d) na direção que faz o binário τ⃗.
- **Roda:** em câmera lenta a 0,75 volta/s; os números da fala são os de 100 km/h (Anexo B), nunca os da câmera lenta. Forças nos excessos desenhadas com comprimento fixo de leitura (não em escala com a câmera lenta).
- `tab25.json`: por quadro e por câmera, as projeções de tela de: prego/origem, bolinha/massas/cubo destacado/excessos, pontas de r⃗, ρ⃗, zᵢ ẑ, p⃗, v⃗, L⃗ e suas partes, dL⃗, τ⃗, F⃗_c, forças dos mancais, pontos do círculo da ponta de L⃗ (48 pontos), **profundidade** de cada ponto e **fator de perspectiva** (para a espessura e a ponta das setas do Manim).

### 4.8 Setas 3D do Manim (oclusão e perspectiva)
- Setas desenhadas pelo Manim entre pontos projetados; espessura e tamanho da ponta multiplicados pelo fator de perspectiva da ponta (setas que vão para longe afinam um pouco, como no 3D).
- **Oclusão:** o Three.js exporta por quadro uma máscara de silhueta do corpo (PNG 1 bit, mesma resolução). O trecho de uma seta que passa atrás do corpo (profundidade maior que a do corpo na máscara) é desenhado tracejado a 0,35 (fantasma declarado). Auditoria `OCLUSÃO`: nenhuma seta desenhada por cima de um corpo que está na frente dela.

## 5. Construção por bloco (física para posicionar; textos e falas no Anexo A)

**Convenção de sinais para o storyboard (conferida no sympy):** L⃗ é sempre perpendicular ao fio ou à haste e se inclina **para o lado da massa que está abaixo da origem**. O torque é horizontal, perpendicular ao plano (eixo, massa) e **90° à frente** da parte horizontal de L⃗, no sentido da rotação; ele aponta ao longo da velocidade da massa de baixo.
- Pêndulo com a bolinha em +x: L_h aponta para +x (para a bolinha); τ⃗ aponta para +y (a velocidade da bolinha).
- Haltere com a massa de cima em +x: L⃗_⊥ aponta para −x (para o lado da massa de baixo); τ⃗ aponta para −y (a velocidade da massa de baixo).
- Cubinho acima da origem: parte transversal de L⃗ᵢ aponta para o eixo (−ρ̂ᵢ); abaixo, para fora.

- **H (H1–H3):** `P_34`. H1: duas voltas com rastro e cone. H2: congela com a bolinha em +x; peso azul na bolinha; r⃗ laranja do prego à bolinha; τ⃗ azul saindo do prego para +y; arco âmbar fino do giro. H3: volta a girar; τ⃗ gira junto (sempre ao longo da velocidade da bolinha); pergunta no topo. Nenhuma fórmula.
- **A (A1–A2):** pêndulo girando desfocado (DOF) atrás do título; três ícones 2.5D pequenos (cone, haltere torto, roda).
- **B1 (B1-1 a B1-8):** `P_34`. B1-1 congelado com a bolinha em +x. B1-2: L⃗ nasce do prego (cresce do pé à ponta em 0,8 s), com ângulo reto ao fio; plano (eixo, fio) translúcido; mão direita como ícone 2.5D. B1-3: L⃗ se decompõe em L_z cheia (vertical) e L_h tracejada (horizontal); θ âmbar. B1-4: gira; ponta de L⃗ deixa o círculo fino magenta-claro (os 48 pontos do `tab25.json`). B1-5: congela; inset `VISTA DE CIMA` com L_h em dois instantes separados por ω dt (ângulo âmbar), dL⃗ tangente; τ⃗ do prego desliza (translação pura) até a ponta de L⃗ e **coincide** com dL⃗ (auditoria ≤ 1°). B1-7: v⃗ violeta em três posições do círculo, iguais; L⃗ em três posições, iguais. B1-8 `[CORTÁVEL]`: origem desce para o centro do círculo; L⃗ vertical; τ do peso e τ do fio (azuis) opostos.
- **B2 (B2-1 a B2-6):** `V_34`, batata girando a 0,5 volta/s. B2-2: cubinho destacado, círculo GEO, r⃗ᵢ abrindo em ρ⃗ᵢ + zᵢ ẑ (GM no desenho e na CONTA ao mesmo tempo). B2-3: as duas partes de L⃗ᵢ saem do cubinho. B2-4: onda de dentro para fora, cada cubo empilha uma fatia (bloquinho magenta-claro) na seta vertical L_z na origem, crescendo até o valor de I_z ω. B2-6: as partes transversais de ~40 cubos piscam por 1 s (setinhas tracejadas curtas), em direções variadas.
- **B3 (B3-1 a B3-7):** `H_34`. B3-1 girando. B3-2: congela em φ = 0; massa de cima acende; seu círculo; r⃗₁ abre em ρ⃗₁ + z₁ ẑ; L⃗₁ sai da massa (parte axial cheia e transversal tracejada para −x). B3-3: massa de baixo; a GM dos dois sinais de menos acontece na CONTA **e** no desenho (ρ⃗₂ e z₂ piscam juntos); L⃗₂ sai da massa de baixo com a transversal também para −x. B3-4: **a transformação-chave**: L⃗₁ e L⃗₂ deslizam por translação pura até a origem e se encaixam ponta com cauda (axial sobre axial, transversal sobre transversal); nasce o L⃗ total (cheio, magenta-claro); os L⃗ᵢ ficam como fantasmas a 0,4. B3-5: dolly para `H_LADO`; ângulo reto entre L⃗ e a haste, 60° âmbar entre L⃗ e o eixo. B3-6: os "retângulos" massa × altura × raio das duas massas acendem (rosa translúcido, cada um com lados z e ρ) e são **iguais**. B3-7: volta a `H_34` girando; plano translúcido gira com o corpo; L⃗ sempre dentro dele; círculo da ponta.
- **B4 (B4-1 a B4-3):** `H_34`. B4-1: haltere 2 entra (cresce do cubo); a transversal do haltere 2 aponta para +x quando a do haltere 1 aponta para −x; somam zero (as duas tracejadas encolhem juntas e somem); o L⃗ total encolhe para vertical. B4-2: ícones 2.5D. B4-3: `V_34`, batata girando no eixo de antes com L⃗ inclinado girando; `REMONTADA`; para; slerp; gira; L⃗ alinhado; os três eixos principais (GEO, linhas finas pelo CM) acendem 1 s.
- **B5 (B5-1 a B5-5):** `H_34`, haltere girando a 1 volta/s. Inset `VISTA DE CIMA` com L⃗_⊥ e dL⃗. τ⃗ azul na origem (horizontal, 90° à frente de L⃗_⊥). B5-3: os mancais acendem (anel externo com borda azul fina); setas F⃗ horizontais e opostas nos dois, girando com o corpo; cota GEO d = 0,40 m. B5-4: setas F⃗_c nas duas massas (horizontais, para o eixo), cota GEO vertical de 0,52 m entre as linhas delas. B5-5: rotação vai para 3 voltas/s mostrada em `CÂMERA LENTA` 1/3; τ⃗ e F⃗ crescem até ×9 (comprimento de leitura limitado a 1,6× o inicial, com o número dizendo ×9).
- **B6 (B6-1 a B6-5):** `R_34`. B6-1: a roda parada em três ângulos (0°, 120°, 250°), cada um por 1 s, sem tender a girar. B6-2: gira em `CÂMERA LENTA`; raio X; círculos dos dois excessos; L⃗_⊥ do par (tracejada) girando. B6-3: setas F⃗ nos excessos e nos apoios. B6-4: gráfico pequeno à direita da roda (força horizontal num apoio × tempo, senoide; eixo do tempo marcado em "1/15 s"). B6-5: contrapesos entram (voam de fora para a posição); a transversal encolhe a zero; as setas dos apoios somem; rótulo `EIXO PRINCIPAL` no eixo.
- **S1/S2:** `H_34` orbitando devagar; à direita três linhas e depois três cartões `PANEL`. S2: a batata, menor, girando, com os cubinhos se afastando e se aproximando do CM (só geometria; nenhuma seta, nenhuma afirmação física na tela).
- **EN:** encerramento padrão (logo, anéis violeta, `INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS`), pergunta para os comentários, sem "próximo vídeo".

## 6. Álgebra com MF-Tools (usar e abusar; lei geral primeiro, nascendo do desenho)

`MathTex` de string única; glyph maps só com o LaTeX estabilizado; linha nova por passo com a anterior legível; sem índices de debug no vídeo. "GM" = `TransformByGlyphMap`; "voo" = `TransformFromCopy` do rótulo do desenho; "→" = um passo, uma linha nova. Prefira `auto_fade`; não use `keep_orientation()`.

| Âncora | Cadeia na CONTA | Movimento obrigatório |
|---|---|---|
| B1-1 | L⃗ = r⃗ × p⃗ → \|L⃗\| = r p (r ⟂ p) → = ℓ m v | voos de r⃗ e p⃗ do desenho; **GM**: r vira ℓ, p vira m v (m voa da faixa rosa) |
| B1-3 | R = ℓ sen θ · v = ω R → \|L⃗\| = m ω ℓ² sen θ → L_z = \|L⃗\| sen θ → = m (ℓ sen θ)² ω → = m R² ω · L_h = \|L⃗\| cos θ → = m ω ℓ² sen θ cos θ | **GM**: o sen θ de fora entra no parênteses com o ℓ; a chave sob ℓ sen θ vira R; L_z e L_h voam das duas setas do desenho |
| B1-5 | \|dL⃗\| = L_h · ω dt → \|dL⃗/dt\| = ω L_h · τ = m g R → = m g ℓ sen θ | L_h voa da seta tracejada; ω dt voa do ângulo âmbar do inset; **GM**: dt atravessa e vira denominador; R abre em ℓ sen θ |
| B1-6 | τ⃗ = dL⃗/dt (lei, rótulo `LEI GERAL`) → m g ℓ sen θ = ω · m ω ℓ² sen θ cos θ → g = ω² ℓ cos θ → ω² = g/(ℓ cos θ) → ω = √(9,8/(1,00 · cos 30°)) → = 3,36 rad/s · período = 2π/ω = 1,87 s | os dois lados voam das linhas do B1-5; **GM de cancelamento**: m, um ℓ e sen θ dos dois lados riscam juntos em pares (risco branco, encolhem e somem); ω · ω vira ω²; ℓ cos θ desce para o denominador; números um por vez |
| B1-8 | (cortável) τ⃗_peso + τ⃗_fio = 0 → L⃗ constante | escrita |
| B2-1 | L⃗ = Σ r⃗ᵢ × p⃗ᵢ → dL⃗/dt = Σ r⃗ᵢ × F⃗ᵢ → = Σ τ⃗_ext | `TransformMatchingTex`; F⃗ᵢ abre em F⃗_ext + F⃗_int e o termo interno risca com o selo de hipótese |
| B2-2/B2-3 | r⃗ᵢ = ρ⃗ᵢ + zᵢ ẑ → L⃗ᵢ = r⃗ᵢ × mᵢ v⃗ᵢ → = (ρ⃗ᵢ + zᵢ ẑ) × mᵢ v⃗ᵢ → = ρ⃗ᵢ × mᵢ v⃗ᵢ + zᵢ ẑ × mᵢ v⃗ᵢ | **GM**: r⃗ᵢ abre em (ρ⃗ᵢ + zᵢ ẑ) no mesmo instante em que a seta do desenho se abre; distributiva com o × mᵢ v⃗ᵢ **copiado** para os dois termos (cópia deliberada); cada termo acende junto com a sua seta no desenho |
| B2-4 | mᵢ ρᵢ vᵢ → vᵢ = ω ρᵢ → mᵢ ρᵢ² ω → L_z = Σ mᵢ ρᵢ² ω → = (Σ mᵢ ρᵢ²) ω → L_z = I_z ω | **GM**: vᵢ vira ω ρᵢ e os dois ρᵢ viram ρᵢ²; ω sai da soma (desliza para fora do parênteses); a chave sob Σ mᵢ ρᵢ² vira I_z (rosa) |
| B2-5 | τ⃗ = dL⃗/dt → τ_z = dL_z/dt → = d(I_z ω)/dt → (I_z constante) = I_z dω/dt → τ_z = I_z α | **GM**: I_z sai da derivada (rótulo `RÍGIDO` acende); dω/dt vira α (verde) |
| B2-6 | L_z = I_z ω · L⃗_⊥ = ? | escrita (o "?" branco) |
| B3-3 | ρ⃗₂ = −ρ⃗₁ · z₂ = −z₁ → z₂ ρ⃗₂ = (−z₁)(−ρ⃗₁) → z₂ ρ⃗₂ = z₁ ρ⃗₁ | voos de ρ⃗₂, z₂ do desenho; **GM-chave**: os dois "−" deslizam um para o outro, viram um "+" por 0,3 s e somem; o resto se reorganiza |
| B3-5 | L_z = 2 m (ℓ sen α)² ω → = 2 · 0,40 · (0,30 · 0,5)² · 2π → = 0,113 kg·m²/s · L_⊥ = 2 m ℓ² ω sen α cos α → = 0,196 kg·m²/s | voos dos rótulos; números um por vez |
| B3-6 | L⃗_⊥ = −ω Σ mᵢ zᵢ ρ⃗ᵢ → componentes: Σ m x z · Σ m y z → `PRODUTOS DE INÉRCIA` | **GM**: ρ⃗ᵢ abre em (xᵢ, yᵢ); o rótulo rosa nasce por baixo das duas somas |
| B4-1/B4-2 | parceiro: z ρ⃗ + z(−ρ⃗) = 0 → L⃗_⊥ = 0 → L⃗ = I ω⃗ | **GM**: os dois termos opostos deslizam um sobre o outro e cancelam; L_z = I_z ω da memória vira L⃗ = I ω⃗ (os índices z somem, aparecem as setinhas) |
| B5-1 | dL⃗/dt = ω⃗ × L⃗ → \|dL⃗/dt\| = ω L_⊥ → τ = ω · 2 m ℓ² ω sen α cos α → τ = 2 m ℓ² ω² sen α cos α | a linha do B1-5 volta (voo) e o L_h vira L_⊥ (GM); ω · ω vira ω² |
| B5-2 | ω = 2π rad/s · L_⊥ = 0,196 → τ = 1,23 N·m · τ_z = 0 → α = 0 | números voam do B3-5; α verde |
| B5-3 | τ = F d → F = τ/d → = 1,23 / 0,40 → F = 3,1 N | **GM**: d atravessa e vira denominador; d voa da cota |
| B5-4 | F_c = m ω² ρ → = 0,40 · (2π)² · 0,15 → = 2,37 N → binário = F_c · 2 ℓ cos α → = 2,37 · 0,52 → = 1,23 N·m | voos; o 1,23 do B5-2 acende ao lado com selo `CONFERE` |
| B5-5 | τ ∝ ω² → ω × 3 ⇒ τ × 9 → τ = 11,1 N·m · F = 27,7 N | escrita; fatores brancos |
| B6-2 | Σ m x z ≠ 0 | voo do rótulo do B3-6 |
| B6-3 | ω = v/R → = 27,8 / 0,30 → = 92,6 rad/s (≈ 15 voltas/s) → F = m ω² ρ → = 0,020 · 92,6² · 0,20 → ≈ 34 N → binário = F · 0,20 → ≈ 6,9 N·m | km/h → m/s numa linha só (100/3,6); números um por vez |
| B6-4 | 50 km/h: ω ÷ 2 ⇒ binário ÷ 4 | escrita |
| S1 | L_z = I_z ω · τ⃗ = dL⃗/dt · Eixo principal: L⃗ = I ω⃗ | voos das linhas sublinhadas do B2-4, B1-6 e B4-2 |

**Auditoria `ÁLGEBRA`:** log por `MathTex` com âncora, método (`lei`, `voo`, `GM`, `MatchingTex`, `escrita`) e linha de origem. FALHA se: linha com número aparece antes da linha literal no mesmo bloco; passo marcado GM feito por `FadeIn`; termo com origem visível no desenho entra sem voo. **Mínimo de GM:** B1 ≥ 6, B2 ≥ 5, B3 ≥ 3 (incluindo a dos dois sinais), B4 ≥ 2, B5 ≥ 3, B6 ≥ 1.

## 7. Auditoria, render, entrega e parada

1. **Portão** G28 + G29–G33 + ORDEM + COLUNA VAZIA + PARADO + FLASH + OPACIDADE + `ÁLGEBRA` + `OCLUSÃO` zerados + prancha humana + cor por capítulo (≥ 20% família) + COR OPERADOR (ignora `\mathrm{}` e subscritos; barra de fração conta).
2. **Auditorias de física:**
   - `PÊNDULO`: ω = 3,364 rad/s ± 0,5%; θ = 30° ± 0,2°; \|L⃗\| = 0,336 constante ± 0,5%; L⃗ ⟂ fio (≤ 1°); ponta de L⃗ num círculo horizontal (altura constante ≤ 1 px); τ⃗ ∥ dL⃗ e τ⃗ ∥ v⃗ da bolinha (≤ 1°).
   - `HALTERE`: na `H_LADO`, L⃗ ⟂ haste (≤ 1°) e 60° ± 0,5° do eixo; L_z = 0,113, L_⊥ = 0,196 (± 0,5%); τ⃗ ⟂ plano (eixo, haste), 90° ± 1° à frente de L⃗_⊥; forças dos mancais opostas, horizontais, girando em fase com τ⃗.
   - `SINAIS`: L⃗_⊥ do lado da massa de baixo; τ⃗ ao longo da velocidade da massa de baixo; parte transversal do cubinho de cima apontando para o eixo.
   - `X`: L⃗_⊥ total = 0 (≤ 1% de L_z) com os dois halteres.
   - `VOXEL`: L⃗ desenhado = I·ω⃗ do `tab25.json` (≤ 1°); ângulo L⃗ × eixo ≥ 20° antes e ≤ 0,5° depois da remontagem; CM no eixo (≤ 1 mm).
   - `RODA`: CM no eixo (excessos simétricos em relação ao centro); com contrapesos, Σ m x z = Σ m y z = 0; velocidade aparente na tela ≤ 30° por quadro (câmera lenta) e selo `CÂMERA LENTA` presente em todo quadro com a roda girando.
   - `ALINHAMENTO 3D × MANIM`: ≤ 2 px nos pontos do `timeline.json`, medido em 24 quadros espalhados pelas quatro cenas.
   - `NÚMEROS`: todo valor da tela contra o Anexo B.
   - Fundo (§3.3): deslocamento por quadro sempre para a esquerda, inclusive nas emendas de lote e Three.js ↔ Manim.
3. **Prancha de objetos antes dos lotes** (autoconferência): as quatro cenas a 1920×1080 nas câmeras do §4.5 (pêndulo em φ = 0; batata nas duas orientações; haltere em φ = 0 nas duas câmeras e com o X; roda parada com e sem raio X, com e sem contrapesos). Conferir: fio ≥ 2 px, faixas rosa legíveis, esferas dos rolamentos visíveis, cubinhos separados (AO funcionando), sombras visíveis, contraste ≥ 1,6× nas arestas, roda sem nenhuma marca comercial. Corrigir até passar.
4. **Render:** vídeo inteiro, 960×540 / 15 fps, sem voz. Lotes: PH (hook + abertura), PB1, PB2, PB3, PB4, PB5, PB6, PS (síntese + encerramento). Ondas de no máximo 3 lotes.
5. **Entregue:** preview; pranchas por lote; `qa.txt` com a duração por âncora (narração × cena) e todas as auditorias; `capitulos_youtube.txt`; quadros 1920×1080 da prancha de objetos e, no preview, de H2, H3, B1-2, B1-3, B1-5, B1-6, B2-3, B2-4, B3-3, B3-4, B3-5, B3-7, B4-1, B4-3, B5-2, B5-3, B5-4, B6-2, B6-5, S1. Zip de QA **sem** o `.mp4`.
6. **Relatório 3D:** as quatro cenas (o que foi copiado de qual unidade), resolução, custo por quadro a 540p e a 1080p de cada cena, quanto cada efeito do §4.4 custou, alinhamento medido (px) e o que faltou.
7. **Pare.** Sem voz, SRT, master, entrega, commit ou push. Relatório: arquivos alterados, verificações com resultado, caminhos e pendências reais. Não chamar falha de portão de aviso menor.

## 8. Decisões já tomadas (não reabrir)
Proposta v2 aprovada pelo Kaio em 2026-11-07: pergunta guia "como pode existir torque sem aumentar a velocidade angular?"; pêndulo → haltere → roda, cada exemplo avançando a mesma resposta; a condição é **eixo principal**, não simetria (síntese "Eixo principal: L⃗ = I ω⃗"); "a rapidez é constante; a velocidade muda de direção"; "cada massa descreve um círculo horizontal, como a bolinha" (não "é um pêndulo cônico"); o haltere é o núcleo e o passo das partes transversais se somando é protegido; **matriz 3×3 fora** da tela; conferência pelas forças centrípetas dentro; os 3,1 N são só a parte do binário; frases da roda ("não apresenta posição preferida", "binário girante", "pode provocar vibração"); contrapesos "neste caso", não como regra de toda roda. Mantidos da série: L em magenta-claro `#F19AFF`, vetor posição laranja queimado `VETC`, massa e inércia rosa `MAS`, Three.js com acabamento HDR/PBR, sem caixas nas equações, operadores neutros, fundo azul com estrelas contínuas, sem livros na tela ou na fala, sem citar vídeo futuro. **Cortes, nesta ordem, se a fala crescer:** B1-8 (troca de origem), B5-5 (3 voltas/s), a frase dos 50 km/h do B6-4. B3 inteiro e B5-4 nunca saem.

---
# ANEXO A · roteiro com narração v1 (fonte do `ancoras.json`)

Narração **v1**, ~2.200 palavras ≈ 13,6 min a 2,7 palavras/s (42 âncoras; hook ≈ 33 s; cortáveis: B1-8 ≈ 20 s, B5-5 ≈ 15 s). A duração é estimativa; a voz mede.
Padrão: `padrao_video_longo.md` §5 e `roteiro_voz_elevenlabs_v4.md`. Tom de professor de cursinho, "a gente" e "você", nunca a letra solta (o símbolo é apresentado uma vez, depois só o nome). Números por extenso como serão falados.

**Como ler:** cada `###` é uma âncora (evento visual). A linha `tela:` diz o que aparece; a fala começa ~0,15 s depois e manda: a cena se estica. Tags `[ ]` do ElevenLabs v4 em inglês, uma por trecho; não entram na legenda. `[CORTÁVEL]` marca o que sai primeiro se passar do tempo.

## HOOK

### H1 · tela: `P_34`; pêndulo cônico no pórtico de aço, bolinha com faixa rosa girando num círculo horizontal, rastro GEO, o fio varrendo um cone translúcido; duas voltas
[curious] Olha esse pêndulo. Em vez de ir e voltar, a bolinha anda num círculo deitado, sempre na mesma altura, sempre com a mesma rapidez. Volta depois de volta, a velocidade angular não muda nada.

### H2 · tela: congela; seta azul do peso na bolinha; vetor posição laranja do prego até a bolinha; seta azul do torque do peso saindo do prego, horizontal; topo: `O PESO FAZ TORQUE EM RELAÇÃO AO PREGO`
[thoughtful] Só que repara numa coisa. Em relação ao prego lá em cima, o peso da bolinha tem braço. Ele faz torque, e esse torque não é zero. E a gente sabe que torque muda o momento angular.

### H3 · tela: volta a girar; a seta do torque gira junto com a bolinha; topo troca para `COMO EXISTE TORQUE SEM ω AUMENTAR?`; hold de 2 s
[curious] Então como pode existir torque sem a velocidade angular aumentar? O que é que esse torque está mudando?

## ABERTURA

### A1 · tela: logo; `BEM-VINDOS AO PARALLAX LAB`; o pêndulo girando desfocado atrás
[happy] Fala, pessoal! Bem-vindos ao Parallax Lab.

### A2 · tela: `MOMENTO ANGULAR DO CORPO RÍGIDO`; `NESTE VÍDEO:` e três ícones (cone · haltere torto · roda) acendendo nas palavras
[thoughtful] Hoje o assunto é o momento angular de um corpo rígido. E a gente vai responder essa pergunta em três passos: primeiro esse pêndulo, depois um haltere torto girando num eixo, e no fim a roda de um carro. Os três contam a mesma história.

## B1 · UM L QUE SÓ VIRA

### B1-1 · tela: canto linha 2 `UM L QUE SÓ VIRA`; `P_34` congelada, bolinha em φ = 0; r⃗ laranja do prego à bolinha, p⃗ magenta tangente, marca de ângulo reto; CONTA: L⃗ = r⃗ × p⃗ → |L⃗| = r p → = ℓ m v
[thoughtful] Antes de somar muitas partículas, vamos entender uma só. O momento angular da bolinha em relação ao prego é o produto vetorial do vetor posição com o momento linear. O vetor posição vai do prego até a bolinha, ao longo do fio. O momento linear é tangente ao círculo, na horizontal. Os dois são perpendiculares, então o tamanho do momento angular é o comprimento do fio vezes o momento linear.

### B1-2 · tela: L⃗ magenta-claro sai do prego, perpendicular ao fio, inclinado para fora, do lado da bolinha; o plano (eixo, fio) aparece translúcido; ícone 2.5D da mão direita
[thoughtful] E a direção? Perpendicular ao fio e perpendicular ao momento linear. Pela regra da mão direita, ele aponta para cima e para fora, inclinado para o lado da bolinha. Repara: ele não aponta ao longo do eixo de rotação.

### B1-3 · tela: L⃗ se decompõe em L_z (vertical, cheia) e L_h (horizontal, tracejada); ângulo θ âmbar entre o fio e o eixo; CONTA: R = ℓ sen θ · v = ω R → L_z = \|L⃗\| sen θ → = m R² ω · L_h = \|L⃗\| cos θ → = m ω ℓ² sen θ cos θ
[thoughtful] Vale separar esse vetor em duas partes: uma vertical, ao longo do eixo, e uma horizontal. O raio do círculo é o comprimento do fio vezes o seno do ângulo. Fazendo a conta, a parte vertical fica a massa vezes o raio ao quadrado vezes a velocidade angular. Ou seja, momento de inércia vezes velocidade angular, igualzinho ao círculo de sempre. A parte horizontal é a novidade.

### B1-4 · tela: volta a girar; L⃗ gira junto; L_z parada; a ponta de L⃗ desenha um círculo horizontal fino magenta-claro; mostrador de \|L⃗\| constante
[curious] Agora deixa o pêndulo girar. A parte vertical fica parada. Mas a parte horizontal acompanha a bolinha, e a ponta do momento angular desenha um círculo. O tamanho não muda… a direção muda o tempo todo. E um vetor que muda de direção está mudando.

### B1-5 · tela: congela; inset `VISTA DE CIMA` do círculo da ponta: L_h girando de um ângulo ω dt; dL⃗ tangente; a seta do torque do peso desliza do prego até a ponta e coincide com dL⃗; CONTA: \|dL⃗\| = L_h ω dt → \|dL⃗/dt\| = ω L_h · τ = m g R → = m g ℓ sen θ
[thoughtful] Num intervalo de tempo pequeno, a parte horizontal gira de um ângulo igual à velocidade angular vezes esse tempo. Então a variação do momento angular é a parte horizontal vezes a velocidade angular vezes o tempo, e aponta na tangente desse círculo. Agora olha o torque do peso: o braço é o raio do círculo, e ele aponta exatamente na mesma direção. O torque não está acelerando o giro. Ele está virando o momento angular.

### B1-6 · tela: CONTA: τ⃗ = dL⃗/dt → m g ℓ sen θ = ω · m ω ℓ² sen θ cos θ → (m, ℓ e sen θ cancelam) → g = ω² ℓ cos θ → ω² = g/(ℓ cos θ) → ℓ = 1,00 m, θ = 30° → ω = 3,36 rad/s · período 1,87 s; hold de 2 s
[thoughtful, emphatic] E isso já dá física de verdade. Iguala o torque à taxa de variação do momento angular. A massa cancela, um comprimento cancela, o seno cancela, e sobra: a velocidade angular ao quadrado é a gravidade dividida pelo comprimento do fio vezes o cosseno do ângulo. Com um metro de fio a trinta graus, dá três vírgula três seis radianos por segundo, uma volta a cada um vírgula oito sete segundo. É a única velocidade angular em que esse pêndulo gira nesse ângulo.

### B1-7 · tela: frase-chave `RAPIDEZ CONSTANTE · VELOCIDADE MUDA DE DIREÇÃO`; v⃗ violeta da bolinha em três posições, mesmo comprimento; ao lado, L⃗ em três posições, mesmo comprimento
[thoughtful] Só um cuidado com as palavras. A rapidez da bolinha é constante, mas a velocidade dela muda de direção, e por isso existe aceleração centrípeta. Com o momento angular é a mesma coisa: o tamanho é constante, mas o vetor muda.

### B1-8 · `[CORTÁVEL]` · tela: selo `DE OUTRO PONTO`; a origem desce do prego para o centro do círculo; L⃗ fica vertical e parado; τ do peso e τ do fio, opostos, somam zero
[thoughtful] Um detalhe: se você medir tudo em relação ao centro do círculo, em vez do prego, o momento angular fica vertical e constante, e o torque do peso cancela o torque do fio. As duas contas estão certas: o momento angular depende do ponto.

## B2 · UM CORPO INTEIRO

### B2-1 · tela: canto linha 2 `UM CORPO INTEIRO`; `V_34`: a batata de cubinhos de aço presa ao eixo vertical da bancada, girando; selo `HIPÓTESES: FORÇAS INTERNAS AOS PARES, NA MESMA LINHA`; CONTA: L⃗ = Σ r⃗ᵢ × p⃗ᵢ → dL⃗/dt = Σ τ⃗_ext
[thoughtful] Agora, um corpo inteiro. Um corpo rígido é um monte de pedacinhos, cada um com o seu momento angular em relação a uma origem fixa. O momento angular do corpo é a soma de todos eles. E, quando a gente deriva essa soma, as forças internas aparecem aos pares, iguais, opostas e na mesma linha, então os torques delas se cancelam. Sobra: o torque externo total é a taxa de variação do momento angular do corpo.

### B2-2 · tela: um cubinho acende (rosa); seu círculo horizontal GEO; origem O no eixo, na altura do centro de massa; r⃗ᵢ laranja de O ao cubinho; r⃗ᵢ se abre em ρ⃗ᵢ (horizontal) + zᵢ ẑ (vertical, tracejado); v⃗ᵢ violeta tangente; CONTA: r⃗ᵢ = ρ⃗ᵢ + zᵢ ẑ
[thoughtful] Pega um pedacinho só. Com o eixo fixo, ele anda num círculo horizontal. A gente coloca a origem num ponto fixo do eixo e quebra o vetor posição em duas partes: uma horizontal, que é o raio do círculo desse pedacinho, e uma vertical, que é a altura dele em relação à origem.

### B2-3 · tela: CONTA: L⃗ᵢ = r⃗ᵢ × mᵢ v⃗ᵢ → = ρ⃗ᵢ × mᵢ v⃗ᵢ + zᵢ ẑ × mᵢ v⃗ᵢ; no desenho, dois vetores magenta-claro saem do cubinho: um vertical (do ρ⃗ᵢ) e um horizontal (do zᵢ), apontando para o eixo
[thoughtful] Aí o momento angular desse pedacinho também se quebra em dois. A parte do raio dá um vetor vertical, ao longo do eixo. A parte da altura dá um vetor horizontal. Exatamente como no pêndulo.

### B2-4 · tela: CONTA: mᵢ ρᵢ vᵢ → mᵢ ρᵢ² ω → L_z = Σ mᵢ ρᵢ² ω → = (Σ mᵢ ρᵢ²) ω → L_z = I_z ω; os cubinhos acendem em onda, de dentro para fora, e cada um empilha uma fatia na seta vertical
[thoughtful] Soma as partes verticais. Cada uma é a massa vezes o raio vezes a velocidade, e a velocidade é a velocidade angular vezes o raio. Então cada pedacinho dá massa vezes raio ao quadrado vezes velocidade angular. A velocidade angular é a mesma para todos e sai da soma, e o que sobra dentro é o momento de inércia em relação ao eixo. A componente do momento angular ao longo do eixo é o momento de inércia vezes a velocidade angular. Sempre, para qualquer corpo rígido girando em torno de um eixo fixo.

### B2-5 · tela: CONTA: τ⃗ = dL⃗/dt → τ_z = dL_z/dt → (I_z constante) → τ_z = I_z α
[thoughtful] E, como o corpo é rígido, o momento de inércia não muda. Pegando só a componente da lei do torque ao longo do eixo, sai o torque igual a momento de inércia vezes aceleração angular. Aquela equação que a gente já usava é só uma componente da lei geral.

### B2-6 · tela: as setas horizontais de muitos cubinhos piscam, apontando para lados diferentes; na CONTA, abaixo de L_z = I_z ω: L⃗_⊥ = ?
[curious] Mas repara no que essa igualdade não diz. Ela fala só da componente ao longo do eixo. E as partes horizontais de cada pedacinho? Elas se cancelam ou se somam? Para ver, vamos para o caso mais simples possível.

## B3 · O HALTERE TORTO

### B3-1 · tela: canto linha 2 `O HALTERE TORTO`; `H_34`: bancada com motor, coluna com dois mancais abaixo, eixo vertical, haste a 30° do eixo com duas esferas de faixa rosa; gira a 1 volta/s; selo `HIPÓTESES: HASTE SEM MASSA · MASSAS PONTUAIS · ω CONSTANTE`; rótulos m = 0,40 kg, ℓ = 0,30 m, α = 30°
[thoughtful] Um haltere torto: duas massas iguais, de quatrocentos gramas, nas pontas de uma haste. A haste está presa ao eixo pelo meio, mas inclinada, a trinta graus do eixo, com cada massa a trinta centímetros do centro. O centro de massa fica bem no eixo, e um motor mantém a rotação em uma volta por segundo.

### B3-2 · tela: congela com a haste no plano xz; a massa de cima acende; seu círculo GEO; r⃗₁ = ρ⃗₁ + z₁ ẑ; L⃗₁ sai da massa: parte vertical e parte horizontal apontando para dentro, para o lado oposto ao dela
[thoughtful] Cada massa descreve um círculo horizontal, como a bolinha do exemplo anterior. Pega a massa de cima. A altura dela é positiva, então a parte horizontal do momento angular dela aponta para dentro, para o lado oposto ao dela.

### B3-3 · tela: a massa de baixo acende; CONTA: ρ⃗₂ = −ρ⃗₁ · z₂ = −z₁ → z₂ ρ⃗₂ = (−z₁)(−ρ⃗₁) → z₂ ρ⃗₂ = z₁ ρ⃗₁ (os dois sinais de menos se encontram e somem); no desenho, L⃗₂ sai da massa de baixo com a parte horizontal apontando para o mesmo lado da de L⃗₁
[curious] Agora a massa de baixo. Ela está do outro lado do eixo, então o raio dela aponta para o lado oposto. Mas a altura também trocou de sinal, porque ela está abaixo da origem. Duas trocas de sinal juntas… e o produto não troca. A parte horizontal da massa de baixo aponta para o mesmo lado que a da massa de cima.

### B3-4 · tela: os dois L⃗ᵢ, cada um nascendo na sua massa, deslizam para a origem e se somam ponta com cauda: vertical com vertical, horizontal com horizontal; nasce o L⃗ total, inclinado; hold de 2 s
[thoughtful, emphatic] Leva os dois para a mesma origem e soma. As partes verticais se somam, claro. Mas as partes horizontais também se somam, mesmo com as massas em lados opostos. O resultado é um momento angular inclinado, que não aponta ao longo do eixo.

### B3-5 · tela: dolly para `H_LADO` (ortográfica, perpendicular ao plano eixo–haste); marca de ângulo reto entre L⃗ e a haste; ângulo de 60° âmbar entre L⃗ e o eixo; CONTA: L_z = 2 m (ℓ sen α)² ω → = 0,113 kg·m²/s · L_⊥ = 2 m ℓ² ω sen α cos α → = 0,196 kg·m²/s
[thoughtful] De lado, dá para ver a geometria inteira. O momento angular fica perpendicular à haste, a sessenta graus do eixo. A parte ao longo do eixo continua sendo o momento de inércia vezes a velocidade angular: zero vírgula cento e treze. Mas a parte transversal é ainda maior: zero vírgula cento e noventa e seis.

### B3-6 · tela: CONTA: L⃗_⊥ = −ω Σ mᵢ zᵢ ρ⃗ᵢ → componentes: Σ m x z · Σ m y z → rótulo rosa `PRODUTOS DE INÉRCIA`; no desenho, os dois retângulos "massa × altura × raio" das duas massas acendem iguais
[thoughtful] A parte transversal vem da soma da massa vezes a altura vezes o raio de cada pedacinho. Em coordenadas, são as somas da massa vezes x vezes z, e da massa vezes y vezes z. Essas somas têm nome: produtos de inércia. Elas medem o quanto a massa está distribuída de um jeito torto em relação ao eixo.

### B3-7 · tela: volta a `H_34` e a girar; L⃗ inteiro gira junto, sempre no plano translúcido (eixo, haste); a ponta desenha um círculo; L_z parada
[curious] E agora, com o haltere girando, o que acontece com esse vetor? A parte transversal está presa ao haltere, então gira junto com ele. A ponta do momento angular desenha um círculo, como no pêndulo. O tamanho fica, a direção muda.

## B4 · EIXO PRINCIPAL

### B4-1 · tela: canto linha 2 `EIXO PRINCIPAL`; um segundo haltere, inclinado para o outro lado, entra no mesmo cubo formando um X; as partes transversais dos dois apontam em sentidos opostos e somam zero; o L⃗ total fica vertical
[thoughtful] Então que distribuição de massa faria essa parte transversal sumir? Um jeito simples: para cada pedacinho, um parceiro igual, na mesma altura, do outro lado do eixo. Aí os produtos de inércia zeram. Por exemplo: um segundo haltere, inclinado para o outro lado, formando um xis. As partes transversais se cancelam, e o momento angular volta a apontar ao longo do eixo.

### B4-2 · tela: CONTA: L⃗_⊥ = 0 → L⃗ = I ω⃗; rótulo `EIXO PRINCIPAL`; três ícones 2.5D pequenos: disco, roda, haltere perpendicular ao eixo
[thoughtful] Quando isso acontece, o momento angular é o momento de inércia vezes o vetor velocidade angular, inteirinho, paralelo ao eixo. Um eixo assim se chama eixo principal de inércia. Um disco girando pelo centro, uma roda bem feita, um haltere perpendicular ao eixo: todos giram em torno de um eixo principal.

### B4-3 · tela: `V_34`: a batata volta, girando no eixo de antes, com L⃗ inclinado girando; selo `REMONTADA`; ela para, gira inteira devagar até um eixo principal (calculado) ficar vertical, e volta a girar; L⃗ alinha com o eixo; os três eixos principais acendem por 1 s em GEO
[curious] E aqui tem um detalhe importante: simetria ajuda, mas não é obrigatória. Essa batata não tem simetria nenhuma. Girando num eixo qualquer, o momento angular sai torto. Mas existem três direções perpendiculares, só dela, em que ele fica alinhado. Girando em torno de qualquer uma delas, não sobra parte transversal. A simetria é só um jeito fácil de achar esses eixos.

## B5 · O QUE OS MANCAIS FAZEM

### B5-1 · tela: canto linha 2 `O QUE OS MANCAIS FAZEM`; `H_34`, haltere torto girando; inset `VISTA DE CIMA` com L⃗_⊥ girando e dL⃗ tangente; CONTA: dL⃗/dt = ω⃗ × L⃗ → \|dL⃗/dt\| = ω L_⊥ → τ = 2 m ℓ² ω² sen α cos α
[thoughtful] De volta ao haltere torto. A velocidade angular é constante, mas a parte transversal do momento angular está mudando de direção. Pela mesma conta do pêndulo, a taxa de variação é a velocidade angular vezes a parte transversal. Pela lei geral, isso precisa de um torque externo desse tamanho.

### B5-2 · tela: CONTA: ω = 2π rad/s · L_⊥ = 0,196 → τ = 1,23 N·m · τ_z = 0 → α = 0; no desenho, τ⃗ azul na origem, horizontal, perpendicular ao plano (eixo, haste), girando junto, sempre 90° à frente de L⃗_⊥
[thoughtful] Com uma volta por segundo, dá um vírgula vinte e três newton metro. E repara na direção: o torque é horizontal, perpendicular ao eixo. Ele não tem componente ao longo do eixo, por isso não muda a velocidade angular. Ele só vira o momento angular. É a resposta da pergunta do começo, agora num corpo rígido.

### B5-3 · tela: os dois mancais (abaixo do haltere, a 0,40 m um do outro) acendem; setas azuis F⃗ horizontais e opostas nos dois, girando; cota GEO d = 0,40 m; CONTA: τ = F d → F = τ/d → = 1,23/0,40 → F = 3,1 N; selo `ATENÇÃO: SÓ A PARTE DO BINÁRIO`
[thoughtful] Quem dá esse torque? O eixo, pelos dois mancais. Eles empurram em sentidos opostos, formando um binário, e esse par de forças gira junto com o haltere. Com os mancais a quarenta centímetros um do outro, cada um empurra com uns três newtons. [short pause] Atenção: essa é só a parte das forças que mantém a rotação imposta. A força total no apoio também inclui segurar o peso.

### B5-4 · tela: selo `CONFERE`; setas azuis F⃗_c nas duas massas, horizontais, para o eixo, opostas, em alturas diferentes; cota vertical de 0,52 m; CONTA: F_c = m ω² ρ → = 0,40 · (2π)² · 0,15 → = 2,37 N → binário = F_c · 2ℓ cos α → = 2,37 · 0,52 → = 1,23 N·m; hold de 2 s
[curious] Dá para conferir por outro caminho, só com forças. Cada massa anda num círculo, então precisa de uma força centrípeta apontando para o eixo: dois vírgula trinta e sete newtons. As duas forças são opostas, mas estão em alturas diferentes, separadas por cinquenta e dois centímetros. Forças opostas em linhas diferentes formam um binário… e dá de novo um vírgula vinte e três newton metro. A geometria do momento angular e as forças contam a mesma coisa.

### B5-5 · tela: mostrador de rotação 1 → 3 voltas/s (a 3 voltas/s, 72° por quadro: mostrar em `CÂMERA LENTA` 1/3); τ e F crescem; CONTA: τ ∝ ω² → × 9 → τ = 11,1 N·m · F = 27,7 N
[thoughtful] E esse torque cresce com o quadrado da velocidade angular. Com três voltas por segundo, ele fica nove vezes maior: quase vinte e oito newtons em cada mancal. Por isso essa história importa tanto para coisas que giram rápido.

## B6 · A RODA

### B6-1 · tela: canto linha 2 `A RODA`; `R_34`: roda de carro (pneu, aro de liga) num eixo horizontal com dois apoios; dois excessos rosa diametralmente opostos, um em cada face (selo `FORA DE ESCALA` no tamanho dos blocos); a roda é posta em três posições e fica parada em cada uma; selo `HIPÓTESES: EIXO HORIZONTAL · ATRITO DESPREZÍVEL`
[thoughtful] Agora uma roda de carro com dois excessos de massa de vinte gramas, em lados opostos e em faces opostas da roda. O centro de massa continua no eixo. Com o eixo horizontal e atrito desprezível, a roda não tem uma posição preferida por causa do peso: deixa ela em qualquer posição, e ela fica. Parada, ela parece balanceada.

### B6-2 · tela: a roda gira (`CÂMERA LENTA`); cada excesso descreve seu círculo; a parte transversal do L do par aparece, como no haltere, e gira; CONTA: Σ m x z ≠ 0
[thoughtful] Mas, girando, é exatamente o haltere torto: duas massas em lados opostos do eixo e em posições diferentes ao longo dele. O produto de inércia não é zero, e o momento angular sai inclinado. O centro de massa pode estar no eixo e ainda existir um binário girante.

### B6-3 · tela: CONTA: v = 100 km/h · R = 0,30 m → ω = v/R → = 92,6 rad/s (≈ 15 voltas/s) → F = m ω² ρ → ≈ 34 N → binário ≈ 7 N·m; setas azuis nos excessos e nos apoios, girando
[thoughtful] A cem quilômetros por hora, uma roda de trinta centímetros de raio dá quase quinze voltas por segundo. Cada excesso de vinte gramas precisa de uma força centrípeta de uns trinta e quatro newtons, mais ou menos o peso de três quilos e meio. E os dois juntos formam um binário de quase sete newton metro, girando quinze vezes por segundo.

### B6-4 · tela: as setas dos apoios alternando; ao lado, gráfico pequeno da força horizontal num apoio × tempo, senoide de ~15 por segundo; CONTA: 50 km/h → binário ÷ 4
[thoughtful] Esse binário transmite esforços periódicos aos apoios e pode provocar vibração. E, como ele cresce com o quadrado da velocidade, a cinquenta quilômetros por hora fica quatro vezes menor. Por isso o efeito costuma aparecer mais em velocidade alta.

### B6-5 · tela: dois contrapesos de aço claro entram, um em cada face, do lado oposto a cada excesso; a parte transversal de L encolhe até zero; L⃗ alinha com o eixo; as setas dos apoios somem; rótulo `EIXO PRINCIPAL`
[thoughtful] O balanceamento dinâmico corrige a distribuição de massa. Neste caso, um contrapeso em cada face, do lado oposto a cada excesso, zera o produto de inércia. Numa roda real, a máquina mede onde e quanto colocar. O eixo da roda volta a ser um eixo principal, o momento angular fica alinhado com ele, e os apoios não precisam mais fazer esse binário.

## SÍNTESE E ENCERRAMENTO

### S1 · tela: canto linha 2 `RESUMO`; `H_34` girando devagar à esquerda com L⃗ girando; à direita, escritas uma a uma: L_z = I_z ω · τ⃗ = dL⃗/dt · Eixo principal: L⃗ = I ω⃗; depois três cartões `PANEL`: `L_z = Iω NÃO É O VETOR INTEIRO` · `L GIRANDO PEDE TORQUE` · `EIXO PRINCIPAL: L ∥ ω`
[calm, satisfied] Então, como pode existir torque sem a velocidade angular aumentar? Quando o torque é perpendicular ao eixo, ele não muda a rapidez do giro: ele muda a direção do momento angular. No pêndulo, isso aconteceu com uma partícula só. No haltere torto e na roda, aconteceu porque a massa estava distribuída torta em relação ao eixo. Resumindo: a componente ao longo do eixo é sempre o momento de inércia vezes a velocidade angular. Mas o vetor inteiro só fica paralelo ao eixo quando o eixo é principal. Fora disso, ele gira com o corpo, e manter o eixo no lugar custa torque.

### S2 · tela: o haltere fica menor à esquerda; à direita, a batata de cubinhos girando se abre e se fecha devagar, sem nada tocando nela
[curious] E fica uma pergunta para você: e se nenhum torque externo agir sobre um corpo que muda de forma enquanto gira? O que acontece com a rotação dele?

### EN · tela: encerramento padrão (logo, anéis violeta, `INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS`); pergunta para os comentários: `E SE A RODA TIVESSE UM EXCESSO SÓ, NUMA FACE SÓ?`
[happy] Se essas conexões ajudaram você, se inscreve no Parallax Lab para acompanhar os próximos vídeos. E deixa nos comentários: se a roda tivesse um excesso de massa só, numa face só, os apoios sentiriam só um binário, ou alguma coisa a mais? Até a próxima!

# ANEXO B · conferência numérica (fonte única dos números da tela)

Conferido em `pautas/verificacao/verifica_l_corpo_rigido_sympy.py` (sympy: identidades vetoriais, sinais, ω² = g/(ℓ cos θ), τ⃗ = ω⃗ × L⃗ = Σ r⃗ᵢ × F⃗ᵢ, partes transversais somando; numpy: números e eixos principais). g = 9,8 m/s². Convenção: z para cima, rotação anti-horária vista de cima.

| Onde | Grandeza | Valor |
|---|---|---|
| H/B1 | pêndulo: m · ℓ · θ · R | 0,20 kg · 1,00 m · 30° · 0,50 m |
| H/B1 | ω · período · rapidez da bolinha | 3,36 rad/s · 1,87 s · 1,68 m/s |
| B1 | \|L⃗\| (prego) · L_z · L_h · I = m R² | 0,336 · 0,168 · 0,291 kg·m²/s · 0,050 kg·m² |
| B1 | τ do peso (prego) = m g R · ω L_h | 0,98 N·m · 0,98 N·m |
| B1-8 | L⃗ em relação ao centro do círculo | 0,168 kg·m²/s, vertical, constante |
| B3 | haltere: m · ℓ · α · ρ = ℓ sen α · z = ℓ cos α · ω | 0,40 kg (cada) · 0,30 m · 30° · 0,15 m · ±0,260 m · 2π = 6,28 rad/s (1 volta/s) |
| B3 | I_z · L_z · L_⊥ · \|L⃗\| · ângulo L⃗ × eixo | 0,018 kg·m² · 0,113 · 0,196 · 0,226 kg·m²/s · 60° (L⃗ ⟂ haste) |
| B5 | τ = ω L_⊥ · F por mancal (d = 0,40 m, só a parte do binário) | 1,23 N·m · 3,1 N |
| B5-4 | F_c por massa = m ω² ρ · separação vertical 2ℓ cos α · binário | 2,37 N · 0,52 m · 1,23 N·m |
| B5-5 | 3 voltas/s: τ · F por mancal | 11,1 N·m · 27,7 N |
| B6 | roda: v · R · ω · voltas/s | 100 km/h = 27,8 m/s · 0,30 m · 92,6 rad/s · 14,7 (≈ 15) |
| B6 | excesso: m · ρ · posição axial · F_c (≈ peso de 3,5 kg) | 20 g · 0,20 m · ±0,10 m (faces opostas, diametralmente opostos) · 34,3 N (fala: "uns trinta e quatro") |
| B6 | Σ m x z · binário a 100 km/h · a 50 km/h | 8,0 × 10⁻⁴ kg·m² · 6,86 N·m (fala: "quase sete") · 1,71 N·m (÷ 4) |
| B4-3 | batata: ângulo L⃗ × eixo antes / depois da remontagem | valor do `tab25.json` (≥ 20°) / 0° |
| geral | aliasing a 15 fps | bolinha 12,8°/quadro · haltere 24°/quadro (1 volta/s), 72° (3 voltas/s → câmera lenta 1/3) · roda 354°/quadro → câmera lenta 0,75 volta/s |
| geral | energia (não aparece na tela; conferência) | K = ½ ω⃗·L⃗ = ½ I_z ω²: haltere 0,355 J; a parte transversal de L⃗ não entra na energia |
