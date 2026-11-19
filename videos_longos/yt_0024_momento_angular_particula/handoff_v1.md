

<pasted_content id="4eff">
# HANDOFF v1 · yt_0024 "Momento angular de uma partícula" · vídeo inteiro (preview silencioso)

Data: 2026-11-07. Formato: `longo_horizontal`. Unidade nova: `videos_longos/yt_0024_momento_angular_particula/` (`template/config_horizontal.py`).
Este handoff é **autocontido**: a narração v1 está completa no Anexo A e é a fonte do `ancoras.json`; a tabela de conferência numérica está no Anexo B. Física, números e textos de tela foram resolvidos e conferidos (sympy + integração numérica, inclusive a puxada com partida e parada suaves); não redesenhe. Se encontrar inconsistência objetiva, reporte antes de ampliar o escopo.

## 0. O que é esta rodada

- Vídeo de **teoria** da série Rotação de corpos rígidos (Física I; `docs/mapa_curricular.md` 4.11; na página renumerada do mapa, 1.12-T4). Só **uma partícula**: definição L = r × p, dependência do ponto, leitura geométrica (área varrida), τ = dL/dt, círculo de raio fixo, força central e a mesa com furo. **Fora:** corpo rígido geral, L não paralelo a ω, conservação em sistemas, patinadora, giroscópio, pêndulo cônico, exercícios.
- Estrutura: hook (mesa com furo) → abertura → B1 de p a L → B2 a reta → B3 τ = dL/dt → B4 círculo → B5 força central → B6 volta à mesa → síntese e encerramento.
- **Objetivo:** preview do **vídeo inteiro**, 960×540 / 15 fps, **sem voz**. Duração esperada **~14 min** (a fala tem ~2.280 palavras; estimativa, a voz mede; a fala manda, a cena se estica).
- **Prioridade do Kaio nesta unidade: 3D de qualidade** (§4). A mesa é o aparato do vídeo inteiro.
- **Kit:** copiar para a unidade nova, sem alterar outras unidades. Ordem de preferência: `videos_longos/yt_0023_exercicios_rotacao/` (se estiver no checkout: tem as auditorias `CONCÊNTRICO`, `ÁLGEBRA`, `OPACIDADE` e o eixo único) → `videos_longos/yt_0022_torque/` (no Git: `kit.py`, `prob.py`, `prob2.py`, `algebra22.py`, `equacao22.py`, `pecas22.py`, `qa22.py`, `parado22.py`, `classifica_portao.py`, `agrupar_portao.py`, `prancha.py`, `fundo.py`, `fundo_lab.png`, `gerar_ancoras.py`, `montar_preview.py`, `render*.sh`, `threejs/` com `r3d.js`, `b3d.js`, `f22.js`). Para o que faltar (mostrador, auditoria de setas e de cor por operador): `videos_longos/yt_0020_cinematica_angular/`. Se nenhuma estiver no checkout, **pare e avise** antes de recriar o kit do zero.
- **Não comece:** voz, SRT, master, entrega, commit ou push.

## 1. Ficha (`ficha.md` da unidade)

- `formato: longo_horizontal` · `natureza: teoria_visual`
- `disciplina: Física I` · `bloco: Rotação` · `modulo: 4.11 Rotação de corpos rígidos (momento angular de uma partícula)` · `referencia: Kleppner & Kolenkow, An Introduction to Mechanics, 1ª ed., §6.2–6.3 (Ex. 6.1, 6.3, 6.5); Moysés vol. 1, cap. 11; Sears, cap. 10` (só na ficha e na descrição do YouTube, **nunca** na tela nem na fala)
- `Série pública: **MECÂNICA · EP. 5 (ROTAÇÃO DE CORPOS RÍGIDOS)**` (provisório)
- Título: **Momento angular de uma partícula** · pergunta narrativa: **Como algo pode girar mais rápido sem receber torque?**
- `pergunta_central:` o que é o momento angular de uma partícula, o que o muda e por que uma força que aponta para o centro não o muda?
- `pre_requisitos:` momento linear p = mv e F = dp/dt; produto vetorial e torque τ = r × F; Στ = Iα; I de uma partícula; K = ½mv²
- `payoff_principal:` três ideias: (1) momento angular não exige trajetória circular; (2) torque nulo não exige velocidade angular constante; (3) conservar momento angular não é conservar energia cinética
- `duracao_alvo:` ~14 min (sai da fala; teto do Kaio: 15 min)
- `3d_threejs:` `mesa_furo` (H1–H3, A1–A2, B1, B2, B4, B6, S1, EN): mesa de ar com furo, disco, fio, puxador
- `solido_3d:` nenhum do arsenal Blender; geometria própria em Three.js
- Canto: linha 1 `MECÂNICA · MOMENTO ANGULAR DE UMA PARTÍCULA`; linha 2 = bloco da vez (`DE p PARA L` em MathTex nos símbolos, `UMA RETA TAMBÉM GIRA`, `O QUE MUDA L`, `O CÍRCULO`, `FORÇA CENTRAL`, `DE VOLTA À MESA`, `RESUMO`)

## 2. Sistema visual

### 2.1 Cor por família de grandeza (decisões do Kaio para a série; cor por token completa; número substituído herda a cor)

| Família | Elementos | Cor |
|---|---|---|
| Vetor posição e braço | r⃗, r, r⊥, R (raio da trajetória), d (distância do ponto à reta) | laranja queimado `VETC #D2823A` |
| Geometria | áreas varridas (preenchimento), trajetórias, rastros, cotas que não são o vetor posição, linhas de referência | `GEO #B8C4DA` (rastro `RAST #9FB4D6`), em minoria |
| Momento linear | p⃗, p, Δp, impulso dos "chutes" do B5 | magenta `#EA63FF` |
| **Momento angular** | L⃗, L, L_z, dL, ΔL, ⊙/⊗ do L | **magenta-claro `#F19AFF`** (cor nova, decisão do Kaio, 2026-11-07; registrar na tabela "Definidas" do `padrao_video_longo.md` só quando a unidade fechar) |
| Velocidade | v⃗, v, v_θ, v_r, ω | violeta `#9C8CFF` |
| Aceleração | α, a, g | verde `#3FE08B` |
| Massa e inércia | m, I, İ (dI/dt), o disco e a pedra como corpos com massa | rosa `MAS #FF7EB6` |
| Força e torque | F⃗, F, F_t, T (tração), peso mg, τ⃗, τ, τ_z | azul-claro `#5AA2FF` |
| Energia e potência | K, K₀, K_f, ΔK, W, P | ciano `#35D9FF` |
| Ângulo | φ, θ, arcos de ângulo | âmbar `#FFC24D` |
| Tempo e números puros | t, Δt, fatores (×2, ×4, ¼), frações puras | branco |
| Corpos | mesa, puxador, fio | aço PBR (§4); disco com faixa rosa `MAS` no aro |

- **Operadores neutros** (regra do Kaio): `=`, `+`, `−`, `×` do produto vetorial, `·`, `d`, `dt`, `∫`, `√`, barra de fração, parênteses, setas de implicação ficam brancos; só a grandeza leva cor. O subscrito herda a cor da letra (v_θ violeta inteiro, L_z magenta-claro inteiro). Unidades em `\mathrm{}` brancas.
- **L × p:** são da mesma família de propósito (como torque e força). Eles se distinguem pelo desenho: p⃗ sempre no plano, L⃗ sempre perpendicular ao plano (seta inclinada na vista 3/4, ⊙/⊗ na vista de cima).
- **Tração T × período:** não há período neste vídeo; T é sempre a tração (azul).
- MathTex colorido em ≥ 50% dos glifos das grandezas, stroke na cor, rótulos na cor, nada esmaecido parado. Cor por capítulo ≥ 20% (família) em todos os capítulos. A meta de cor nunca obriga a colorir operadores.

### 2.2 Fundo
- `fundo_lab.png` em **todas** as cenas Manim (gradiente `#0B1A3A → #08122B → #0A1030`, vinheta leve, brilho magenta baixo, estrelas). Nunca o `#050816`. No Three.js, o mesmo gradiente procedural (§4.6).
- **Estrelas em movimento contínuo para a esquerda em relógio global** (§3.3).

### 2.3 Layout
- **Teoria com desenho sempre:** desenho/3D à esquerda (~50–55%), CONTA à direita em `Pilha` (centro x ≈ 4,3). Nunca tela só de álgebra.
- Na **vista de cima** da mesa (B2, B4, B6), a mesa ocupa a coluna esquerda inteira; as setas, áreas e rótulos do Manim ficam presos a ela pelo `timeline.json`.
- Faixa de selo única (y 2,55 a 3,15; x 0,6 a 6,7), um selo por vez: `HIPÓTESES`, `CONFERE`, `ATENÇÃO`, `DICA`, `CÂMERA LENTA`, `FORA DE ESCALA`, `ZOOM ×N`.
- **Sem caixas** em volta de equações (decisão do Kaio para este vídeo). O resultado de cada cadeia fica em destaque por **tamanho** (um degrau acima, MathTex L) e por um **sublinhado fino** (stroke 3) na cor da grandeza do lado esquerdo, que entra junto com o último glifo. `PANEL` só para os cartões do resumo (S1), sem borda branca.

## 3. Regras de tela

### 3.1 G1–G34 (todas valendo, como no yt_0020, yt_0022 e yt_0023)
- **G1** selo ≥ 24, frase-chave ≥ 30, rótulo MathTex no desenho ≥ 36, equação na CONTA ≥ 46. **G2** margem 0,45. **G3** objeto principal ocupa 55–75% da coluna dele.
- **G5/G13** trocas por crossfade 0,4–0,6 s; nunca quadro vazio. **G6** nada sobra da cena anterior; texto nunca sobre objeto nem sobre a trajetória dos próximos 2 s (o disco anda: o rótulo foge da órbita). **G7** uma frase-chave por vez. **G8** setas com espessura ≥ 5, comprimento ≥ 0,6, rótulo fora; setas curvas com raio ≥ 0,5. **G10/G12/G24** cor por token completa, inclusive números substituídos. **G14** cópia nunca sobre o original.
- **G19/G23 contas construídas:** todo símbolo existe antes como rótulo no desenho e vai para a CONTA por `TransformFromCopy`; ordem: lei geral → especialização (termos voando do desenho) → passos (linha nova, glyph map) → números (um por vez, do rótulo) → resultado. Nenhuma linha entra pronta.
- **G21** hipóteses em uma linha, com a fala, até a primeira conta. **G25** CONTA em `Pilha`. **G27** rótulos por `rotulo()` com teste de colisão, a ≤ 0,4 do dono; rótulo de objeto que se move acompanha o objeto e fica na horizontal.
- **G28 portão:** zero em `SOBREPOSIÇÃO`, `TEXTO SOBRE OBJETO`, `TEXTO SOBRE CAIXA`, `FORA DA MARGEM`, `SELO DUPLO`, `LINHA ÓRFÃ`, `CALHA`, `TRÂNSITO`, `RÓTULO SOLTO`, `PALCO 3D`, `FUNDO`. Auditoria a cada 3 quadros dentro de cada `play`; Three.js entra pelas silhuetas do `timeline.json`. Prancha humana com os 24 quadros de maior densidade de texto. Exceção só com justificativa escrita no `qa.txt`.
- **G29 ESQUELETO**; **G30 3D × TEXTO**; **G31 DUPLICATA**; **G32 VAZIO**; **G33** estado antes do número.
- **ORDEM:** álgebra escrita da esquerda para a direita, token a token, na ordem da fala (medir o agendamento real).
- **COLUNA VAZIA 0** (metade da tela vazia por mais de 3 s); **PARADO 0** (tela sem informação nova por mais de 3 s fora dos holds do §3.2).
- **OPACIDADE** (escala do yt_0023): linha ativa, rótulo em uso e resultado 1,0; linha anterior ainda citada ≥ 0,85; histórico (no máximo 2 linhas) ≥ 0,6; fantasmas didáticos (trajetória "sem chute" do B5, raio antigo do B6) com preenchimento 0,3–0,5 e contorno 1,0. O que sai, sai inteiro (`FadeOut` até 0 em ≤ 0,4 s). Portão: texto/MathTex com 0,05 < opacidade < 0,6 por mais de 6 quadros, fora da lista declarada de fantasmas.
- **Aliasing:** a 15 fps, o disco anda no máximo ~38° de órbita por quadro (r = 0,30 m, ω = 10 rad/s). Na reprise do B6 usar 0,5× com selo `CÂMERA LENTA`. O rastro é desenhado com subamostragem de 8 posições por quadro (não um polígono de 15 lados).

### 3.2 Pausa útil
Holds de 2–3 s só em: H3 (a pergunta com a seta da tração), B2-5 (três triângulos iguais), B3-5 (gráfico L_z × t com a inclinação), B5-4 (triângulo antes e depois do chute com a mesma área), B6-3 (τ = Iα + İω com a parcela de İω acesa), B6-5 (ω × 4 ao lado de v_θ × 2), B6-8 (balanço de energia). Fora disso, nada parado > 3 s.

### 3.3 Três regras permanentes (Kaio, 2026-11-06)
1. **Fundo de estrelas:** movimento contínuo para a esquerda em relógio global do vídeo (`t_global = T0_lote + clk`, `T0_lote` = `ini` da primeira âncora do lote), velocidade constante por camada, sem balanço vertical, reciclagem só fora da tela (campo ≥ tela + 2 u de cada lado); nunca reinicia por lote, nunca para, nunca volta. Fora da sincronia e do medidor de PARADO. **O fundo do Three.js usa o mesmo relógio e a mesma velocidade aparente**: na emenda Three.js ↔ Manim as estrelas não saltam.
2. **Sem flash:** nenhum texto/fórmula visível (opacidade ≥ 0,15) por menos de 0,7 s e depois removido antes de ser escrito. Destino da `voa` e títulos com opacidade 0 até o primeiro glifo pousar. Classe `FLASH` no portão, em quadros consecutivos, + detector de picos de tinta.
3. **Sólidos 3D com contraste:** nunca tom sobre tom; luminância da superfície ≤ ~85%; arestas e faixas com contraste ≥ 1,6× e ≥ 2 px a 1080p; rótulos e setas fora do sólido; uma só função de desenho por objeto em todas as cenas.

## 4. 3D de qualidade: a cena `mesa_furo` (Three.js)

O Kaio pediu explicitamente **3D de qualidade** nesta unidade. A cena segue o contrato do kit (`setFrame(f)` determinístico, `cenaPronta`, `window.projeta`, `timeline.json` com as coordenadas de tela de tudo que o Manim prende; alinhamento 3D × Manim ≤ 2 px **medido nos quadros gerados**), com o acabamento abaixo. Física dentro da cena: as posições do disco saem de uma tabela gerada em Python (`fisica24.py`, §4.7), nunca de uma animação "a olho".

### 4.1 Geometria (unidade: metro; origem no centro do furo, plano do tampo z = 0, z para cima)
- **Tampo:** quadrado de 1,60 m × 1,60 m × 0,04 m, cantos arredondados (raio 0,03), chanfro de 4 mm na borda superior. Grade de furinhos de ar a cada 4 cm (discos escuros de 2 mm, por textura normal + roughness, não geometria), sem furinho num raio de 6 cm em volta do furo central.
- **Furo central:** bucha de aço polido, raio interno 6 mm, colarinho de 12 mm de raio e 3 mm de altura; a borda interna recebe um anel fino emissivo frio (§4.4) para o furo ser lido de longe.
- **Pés:** quatro pés tubulares de 25 mm, 0,80 m de altura, com travessa; saia de 6 cm abaixo do tampo. Embaixo, a 0,45 m do tampo, o **puxador**: cabo em T de aço (barra de 12 cm, haste de 6 cm) preso ao fio, que desce em linha reta pelo eixo z. O puxador desce exatamente o que o raio encolhe (vínculo do fio inextensível: Δz_puxador = Δr). A mão não é modelada (o Kaio não gosta de bonecos): só o cabo em T, com uma seta azul pequena `PUXA` do Manim na descida.
- **Disco (puck):** cilindro de raio 0,035 m e altura 0,018 m, aço escuro com **aro rosa `MAS`** (faixa de 5 mm) e um botão central de 6 mm onde o fio prende. É pequeno de propósito (partícula). O disco **não gira sobre si mesmo** (orientação fixa: fio preso no centro, sem atrito): nenhuma marca girando nele.
- **Fio:** tubo de raio 1,2 mm (≥ 2 px a 1080p na vista de cima inteira), branco-quente `#F2EEE6` com rugosidade alta; do botão do disco até a bucha, rente ao tampo (z = 0,009), e da bucha até o puxador, vertical. Fio sempre **reto e esticado** quando preso. Nas cenas do B2 o fio é removido e a bucha fica vazia.
- **Marcadores de ponto (B2):** três pequenos pinos de aço com topo esférico (raio 8 mm) cravados no tampo em O₁, O₂, O₃ (§5, B2). O furo é o O do resto do vídeo.

### 4.2 Material (aço PBR, como no teste de acabamento do toroide, 2026-11-07)
- Renderer: three.js da unidade (r128 do kit), alvo **HDR half float** com MSAA 4×, cores da marca convertidas sRGB → linear e de volta no fim; tom com ombro suave (até 0,8 linear a cor sai exata; acima comprime para o branco); vinheta de até 18%.
- `MeshPhysicalMaterial` para todo aço: tampo `metalness 0,85 · roughness 0,38 · clearcoat 0,35` (aço escovado escuro, cor base `#5E6878`); bucha, puxador e pés `metalness 0,92 · roughness 0,22 · clearcoat 0,6` (`#7A8696`); disco `metalness 0,9 · roughness 0,3` (`#4E5766`) com aro rosa `MAS` em `metalness 0,2 · roughness 0,45`.
- **Ambiente próprio azul-espacial** via `PMREMGenerator.fromScene` (softbox branca grande em cima, faixa fria ciano à esquerda, reflexo magenta baixo no horizonte), no lugar do `RoomEnvironment` cinza. É ele que dá o reflexo bonito no tampo escovado.
- O tampo **não pode** virar um espelho: o reflexo do disco no tampo fica ≤ 25% de luminância do disco (rugosidade e clearcoat ajustados até passar).

### 4.3 Luz e sombra
- **Luz presa à câmera:** chave em cima à direita (branca, 2,2), contraluz fria `#8CC8FF` por trás (1,2) que desenha um contorno no aro do disco e na borda do tampo; o contraste do disco contra o tampo não muda quando a câmera anda (regra 3.3).
- **Sombra de contato** do disco e do fio no tampo: `DirectionalLight` com `castShadow`, mapa 2048, PCF suave, raio 3; sombra curta e escura sob o disco (o olho lê "desliza sobre o tampo"). Os pés fazem sombra num chão escuro invisível só quando a câmera mostra o vão de baixo.
- **Colchão de ar:** um halo muito fraco (1,5% de luminância, ciano-acinzentado `#A7C4D9`, não o ciano da energia) sob o disco, 4 mm maior que ele, só na vista 3/4. Opcional; se competir com algo, sai.

### 4.4 Brilho seletivo (bloom)
- `UnrealBloomPass` (força **0,40**, raio 0,2, limiar 0,55) numa passada própria em que o aço vira oclusor preto (o fio e o disco da frente tapam o brilho de trás).
- **Só brilham:** o anel interno da bucha (frio, discreto) e a **cabeça do rastro** do disco (os últimos 6 cm passam de 1,0 em HDR na cor `RAST`; a cauda, 0,9 s de trajetória, fica na cor da marca e some linear). Nada mais brilha: setas, áreas e rótulos são do Manim.

### 4.5 Câmeras (escolhidas pela física)
| Nome | Uso | Definição |
|---|---|---|
| `C_34` | H1–H3, A, B1-3, S1, EN | perspectiva 30 mm equivalente, 22° acima do plano do tampo, azimute 35°, distância que enquadra o tampo inteiro e o puxador (o vão de baixo visível pela lateral) |
| `C_TOPO` | B2, B4, B6 (setas, áreas, triângulos, espiral) | **ortográfica** exatamente de cima (eixo da câmera = −z), enquadra 1,30 m × 1,30 m do tampo; comprimentos verdadeiros, ângulos verdadeiros. Toda seta, braço e área do Manim é desenhada nesta vista |
| `C_L` | B1-3 (L saindo do plano), B5-2 (movimento no plano) | perspectiva, 35° acima do plano, para o eixo z ficar legível; o Manim desenha L⃗ entre as projeções de O e de O + L⃗·escala |
- **Transições:** dolly contínuo `C_34 → C_TOPO` em 1,6 s (interpolação da câmera, ortográfica com `zoom` casado no fim; troca perspectiva/ortográfica no quadro em que a diferença de projeção ≤ 1 px) e o inverso. A câmera **para exatamente** no quadro em que o Manim começa a desenhar setas.
- Nada gira na câmera durante uma conta.

### 4.6 Fundo e saída
- Fundo procedural da cena: degradê `#0B1A3A → #08122B → #0A1030`, brilho magenta muito baixo no horizonte e estrelas procedurais que andam para a esquerda **no relógio global** (§3.3). `window.TRANSP = true` sai com alfa quando o Manim já fornece o fundo; escolher um dos dois por lote e declarar no `qa.txt` (nunca dois campos de estrelas sobrepostos).
- Render: 960×540 no preview, 1920×1080 no final. Registrar o custo por quadro nas duas.

### 4.7 Física da cena (`fisica24.py` → `mesa_tab.json`)
- **Hook e B6 (puxada):** m = 0,20 kg; começa em órbita circular r₀ = 0,60 m, v₀ = 1,50 m/s (ω₀ = 2,50 rad/s, anti-horário visto de cima). Puxada: velocidade radial com rampa de cosseno de 0,15 s até −0,30 m/s, constante, e rampa de 0,15 s até zero; termina em r = 0,30 m (duração total 1,15 s). Integrar θ̇ = L/(m r²) com L = 0,180 kg·m²/s (dt ≤ 1e-4 s). Depois, órbita circular em r = 0,30 m, ω = 10,0 rad/s.
- **B2 (reta):** disco livre (sem fio), 1,50 m/s em +x ao longo da reta y = +0,40 m, de x = −0,75 a x = +0,75 m.
- **B4 (círculo acelerado):** em r = 0,60 m, empurrão tangencial F_t = 0,30 N por 1,0 s (α = 2,5 rad/s²): ω de 2,5 a 5,0 rad/s; sem desenhar jato realista (o Manim desenha a seta F_t).
- `mesa_tab.json`: por quadro, posição do disco, r, θ, v_r, v_θ, ω, z do puxador, L, K, T (só onde r̈ = 0), e as projeções de tela (para `C_TOPO` e `C_34`) de: O, disco, ponta de r⃗, ponta de p⃗ (escala 0,5 m por kg·m/s), ponta de v⃗ (0,25 m por m/s), cantos dos triângulos de área.

## 5. Construção por bloco (física para posicionar; textos e falas no Anexo A)

- **H (H1–H3):** `C_34`. H1: o disco já em órbita de 0,60 m, rastro curto, duas voltas. H2: o puxador desce 0,30 m, o disco espirala e dispara (tempo real); mais duas voltas rápidas a 0,30 m. H3: congela; seta azul da tração no disco apontando para o furo (Manim, presa pela projeção); arco âmbar fino mostrando o sentido do giro; pergunta no topo. Nenhuma fórmula.
- **A (A1–A2):** a mesa continua girando em `C_34`, levemente desfocada (DOF suave no Three.js, não opacidade) atrás do bem-vindos e do título. `NESTE VÍDEO:` com três ícones pequenos (seta reta com ponto ao lado · círculo com seta · espiral) acendendo nas palavras.
- **B1 (B1-1 a B1-5):** `C_34` congelada sobre o tampo, fio removido, disco congelado no meio de um movimento qualquer a 0,50 m do furo, com p⃗ no sentido anti-horário em volta do furo (φ ≈ 65°, para L⃗ apontar para cima). Retomada de F = dp/dt e τ = r × F na CONTA. r⃗ (laranja) do furo ao disco, p⃗ (magenta) no disco, ângulo φ (âmbar) entre eles, paralelogramo GEO translúcido. Em B1-3, dolly para `C_L`: L⃗ magenta-claro sai do furo, perpendicular ao tampo; mão direita como **ícone 2.5D** pequeno ao lado (quatro dedos curvando de r para p, polegar em L), não um modelo 3D de mão. Em B1-4, braço r⊥ (laranja tracejado) do furo até a reta de p⃗, com ângulo reto marcado.
- **B2 (B2-1 a B2-6):** `C_TOPO`. O₁ sobre a reta (x = −0,30, y = +0,40), O₂ = o furo (0, 0), O₃ em (+0,30, +0,80). O disco atravessa; para cada ponto, r⃗ acompanha o disco; ⊗ / ⊙ magenta-claro em O₂ e O₃; "L = 0" em O₁. Triângulos de área com Δt = 0,50 s a partir de O₂ (base 0,75 m, altura 0,40 m, 0,150 m² cada), três seguidos.
- **B3 (B3-1 a B3-5):** desenho 2.5D no Manim (não é mesa): à esquerda, ponto O (pino de aço 2.5D) e uma pedra rosa 2.5D (m = 0,50 kg) solta do repouso numa vertical a d = 0,40 m à direita de O; cota d laranja; queda até 0,60 s (1,76 m, em escala no desenho); r⃗ do ponto à pedra acompanha; seta azul do peso mg. À direita, a CONTA da derivada e depois o gráfico L_z × t (eixo L_z para baixo negativo, reta de 0 a −1,18 kg·m²/s em 0,60 s, inclinação −1,96 N·m indicada por um triângulo de inclinação).
- **B4 (B4-1 a B4-5):** `C_TOPO`, fio de volta, órbita de 0,60 m. r⃗ e v⃗ perpendiculares (marca de ângulo reto). Depois seta F_t azul tangente no disco por 1,0 s, ω violeta crescendo num mostrador pequeno.
- **B5 (B5-1 a B5-5):** Manim 2.5D (sai a mesa). B5-2: plano inclinado em perspectiva no Manim (vista como a `C_L`, GEO) com L⃗ fixo perpendicular e a trajetória presa ao plano. B5-4: construção de Newton: O, ponto A → B em Δt; prolongamento B → c fantasma (sem chute); chute para O em B (seta magenta Δp ao longo de BO); C real; triângulos OAB, OBc (fantasma) e OBC com a mesma cor e a reta paralela a OB tracejada mostrando a mesma altura. B5-5: órbita elíptica (a = 2,6 u, e = 0,6), o "Sol" 2.5D com brilho no foco, 12 setores de **mesmo tempo** (pontos pela equação de Kepler, M = E − e sen E), setores alternando GEO 35% e GEO 20%.
- **B6 (B6-1 a B6-9):** `C_34` → `C_TOPO`. Reprise da puxada em 0,5× (`CÂMERA LENTA`). Mostradores à direita da mesa (não sobre ela): r, I, ω, v_θ, L. Em r = 0,45 m, congela: decomposição v⃗ = v_r (violeta, para o furo) + v_θ (violeta, tangente), ângulo âmbar 8,5° entre v⃗ e a tangente, `ZOOM ×3` num inset no canto da mesa; T⃗ azul para o furo; a componente de T⃗ ao longo de v⃗ acende. Triângulos de área de 0,20 s (0,090 m² cada) ao longo da espiral. Barras ciano K₀ = 0,225 J e K_f = 0,900 J, e a barra W = 0,675 J entrando na diferença.
- **S1/S2:** `C_34` girando devagar (azimute +8° por segundo), disco em órbita de 0,30 m; à direita três linhas (§6, S1) e depois as três ideias em `PANEL`.
- **EN:** encerramento padrão (logo, anéis, `INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS`), pergunta para os comentários, sem "próximo vídeo".

## 6. Álgebra com MF-Tools (lei geral primeiro, nascendo do desenho)

`MathTex` de string única; glyph maps só com o LaTeX estabilizado; linha nova por passo com a anterior legível; sem índices de debug no vídeo. "GM" = `TransformByGlyphMap`; "voo" = `TransformFromCopy` do rótulo do desenho; "→" = um passo, uma linha nova.

| Âncora | Cadeia na CONTA | Movimento obrigatório |
|---|---|---|
| B1-1 | p⃗ = m v⃗ (m voa do aro rosa, v⃗ da seta) · F⃗ = dp⃗/dt · τ⃗ = r⃗ × F⃗ (cartão pequeno de retomada) | voos |
| B1-2 | τ⃗ = r⃗ × F⃗ → L⃗ = r⃗ × p⃗ | **GM**: τ⃗ vira L⃗ e F⃗ vira p⃗ (as duas letras trocam se movendo; r⃗ × fica parado); p⃗ voa da seta |
| B1-4 | \|L⃗\| = r p sen φ (r, p, φ voam do desenho) → = (r sen φ) p → = r⊥ p | GM: sen φ se junta ao r com parênteses; a chave sob r sen φ vira r⊥ e acende o braço tracejado |
| B1-5 | [L] = m · m/s · kg = kg·m²/s | escrita |
| B2-3 | L⃗ = r⃗ × p⃗ → L_z = −m v d (d voa da cota, v da seta, m do aro) → = −0,20 · 1,5 · 0,40 → = −0,12 kg·m²/s | GM da linha geral para a de componente; números um por vez |
| B2-6 | dA = ½ \|r⃗ × v⃗ dt\| (o triângulo pinta enquanto a fórmula escreve) → dA/dt = \|r⃗ × p⃗\| / 2m → dA/dt = \|L⃗\|/2m → = 0,30 m²/s | GM: p⃗ = m v⃗ entra trocando v⃗ por p⃗/m, o m desce para o denominador; r⃗ × p⃗ vira L⃗ |
| B3-1/B3-2 | L⃗ = r⃗ × p⃗ → dL⃗/dt = (dr⃗/dt) × p⃗ + r⃗ × (dp⃗/dt) → = v⃗ × m v⃗ + r⃗ × F⃗ → = 0 + r⃗ × F⃗ | GM: dr⃗/dt vira v⃗ e dp⃗/dt vira F⃗ (cartão do B1-1 acende); v⃗ × m v⃗ ganha um risco e encolhe para 0 com o rótulo pequeno `PARALELOS` |
| B3-3 | dL⃗/dt = r⃗ × F⃗ → τ⃗ = dL⃗/dt (τ⃗ do cartão) | GM: r⃗ × F⃗ atravessa e vira τ⃗; ao lado, F⃗ = dp⃗/dt sobe e as duas leis ficam lado a lado (resultado com sublinhado) |
| B3-5 | L_z = x p_y − y p_x → = d · (−m g t) − y · 0 → L_z = −m g d t · τ_z = −m g d → números: −0,50 · 9,8 · 0,40 = −1,96 N·m | GM; o termo y · 0 cai riscado; o −m g d voa para a inclinação do gráfico |
| B4-1 | \|L⃗\| = r⊥ p (do B1) → r⊥ = R (o braço coincide com o raio) → L = m v R → v = ω R → L = m R² ω | GM em cada passo; v = ωR voa do cartão de cinemática |
| B4-2 | L = (m R²) ω → I = m R² → L = I ω | GM: a chave sob m R² vira I (rosa) |
| B4-4 | τ_z = dL_z/dt → τ_z = d(m R² ω)/dt → R constante: = m R² dω/dt → τ_z = I α | GM: m R² sai da derivada (rótulo `R FIXO` acende); dω/dt vira α |
| B5-1 | τ⃗ = r⃗ × F⃗ → F⃗ ∥ r⃗ → τ⃗ = 0 → dL⃗/dt = 0 → L⃗ constante | GM; o 0 do τ voa para a derivada |
| B6-2 | L = I ω → I = m r² → m r² ω = constante → r ÷ 2 ⇒ I ÷ 4 ⇒ ω × 4 | voos dos mostradores; fatores em branco |
| B6-3 | τ⃗ = dL⃗/dt (a lei do B3 volta, rótulo pequeno `LEI GERAL`) → τ_z = d(I ω)/dt → τ_z = I dω/dt + (dI/dt) ω → τ_z = I α + İ ω · ao lado, apagada a 0,85: τ_z = I α (rótulo `SÓ COM I CONSTANTE`) | GM: a regra do produto separa I e ω, cada um derivando na sua vez; dω/dt vira α e dI/dt vira İ |
| B6-4 | 0 = I α + İ ω → I α = −İ ω → números em r = 0,45 m: I = 0,0405 · ω = 4,44 · İ = −0,054 → α = +5,9 rad/s² | GM: İω atravessa a igualdade com o sinal trocando; números do mostrador |
| B6-5 | v_θ = L/(m r) → r ÷ 2 ⇒ v_θ × 2 · ω = L/(m r²) ⇒ ω × 4 | as duas linhas lado a lado |
| B6-8 | W = ΔK → ΔK = ½ m v_θ,f² − ½ m v_θ,0² → = 0,900 − 0,225 → = 0,675 J · P = T v_r (em r = 0,45: 1,78 · 0,30 = 0,53 W) | barras viram os termos; o selo `ESTADOS COM v_r = 0` acompanha |

**Auditoria `ÁLGEBRA`** (como no yt_0023): log por `MathTex` com âncora, método (`lei`, `voo`, `GM`, `MatchingTex`, `escrita`) e linha de origem. FALHA se: linha com número aparece antes da linha literal no mesmo bloco; passo marcado GM feito por `FadeIn`; termo com origem visível no desenho entra sem voo. Mínimo: B1 ≥ 3 GM, B2 ≥ 2, B3 ≥ 4, B4 ≥ 4, B6 ≥ 5.

## 7. Auditoria, render, entrega e parada

1. **Portão** G28 + G29–G33 + ORDEM + COLUNA VAZIA + PARADO + FLASH + OPACIDADE + `ÁLGEBRA` zerados + prancha humana + cor por capítulo (≥ 20% família) + COR OPERADOR (ignora `\mathrm{}` e subscritos; barra de fração conta).
2. **Auditorias de física:**
   - `L CONSTANTE` (H2, B6): m r² θ̇ dos quadros do disco = 0,180 ± 0,5% em todos os quadros da puxada e depois dela; ω final = 10,0 ± 0,5%.
   - `VÍNCULO DO FIO` (H2, B6): descida do puxador = r₀ − r (≤ 1 px em `C_34`); fio sempre reto, saindo da bucha.
   - `ÁREAS` (B2, B5-5, B6-6): áreas dos triângulos/setores iguais ± 0,5% (B2: 0,150 m²; B6: 0,090 m²; B5: setores de mesmo tempo).
   - `RETA` (B2): L_z = −0,12 em O₂ e +0,12 em O₃, constante em todos os quadros (±0,5%); 0 em O₁.
   - `QUEDA` (B3): ponto do gráfico = −1,96 t (≤ 1 px) e pedra na altura g t²/2 (≤ 1 px).
   - `ENERGIA` (B6): barras somam (≤ 0,5%); K exibida só nos estados com v_r = 0 (nos quadros da puxada, se houver mostrador de K, ele mostra ½ m (v_r² + v_θ²), nunca só ½ m v_θ²).
   - `SETAS` (B1, B4, B6): r⃗ ⟂ v⃗ no círculo (≤ 0,5°); ângulo v⃗ × tangente = 8,5° ± 0,3° em r = 0,45 m; L⃗ perpendicular ao tampo na `C_L` (≤ 1°, medido pela projeção).
   - `ALINHAMENTO 3D × MANIM`: ≤ 2 px nos pontos do `timeline.json`, medido em 24 quadros espalhados pelos blocos com mesa.
   - `NÚMEROS`: todo valor da tela contra o Anexo B.
   - Fundo (§3.3): deslocamento por quadro sempre para a esquerda, inclusive nas emendas de lote e nas emendas Three.js ↔ Manim.
3. **Prancha de objetos antes dos lotes** (autoconferência, não espera o Kaio): mesa em `C_34`, `C_TOPO` e `C_L` a 1920×1080, com o disco em r = 0,60 e 0,30, fio esticado, puxador nas duas alturas. Conferir: furo legível, fio ≥ 2 px, aro rosa legível, sombra de contato visível, reflexo ≤ 25%, contraste ≥ 1,6× nas arestas. Corrigir até passar.
4. **Render:** vídeo inteiro, 960×540 / 15 fps, sem voz. Lotes: PH (hook + abertura), PB1, PB2, PB3, PB4, PB5, PB6, PS (síntese + encerramento). Ondas de no máximo 3 lotes.
5. **Entregue:** preview; pranchas por lote; `qa.txt` com a duração por âncora (narração × cena) e todas as auditorias; `capitulos_youtube.txt`; quadros de conferência 1920×1080 da prancha de objetos e, no preview, de H2, H3, B1-3, B1-4, B2-3, B2-5, B3-2, B3-5, B4-2, B4-4, B5-4, B5-5, B6-3, B6-4, B6-5, B6-7, B6-8, S1. Zip de QA **sem** o `.mp4`.
6. **Relatório 3D:** cena `mesa_furo` (o que foi copiado de qual unidade), resolução, custo por quadro a 540p e a 1080p, alinhamento medido (px), quanto o acabamento custou a mais e o que faltou.
7. **Pare.** Sem voz, SRT, master, entrega, commit ou push. Relatório: arquivos alterados, verificações com resultado, caminhos e pendências reais. Não chamar falha de portão de aviso menor.

## 8. Decisões já tomadas (não reabrir)
Proposta v2 aprovada pelo Kaio em 2026-11-07: hook da mesa com furo; L em magenta-claro `#F19AFF`; vetor posição em laranja queimado `VETC`; massa e inércia em rosa `MAS`; pêndulo cônico fora (fica para o vídeo do corpo rígido); Three.js para a mesa; sem caixas em volta das equações; o B6 tem tempo protegido (se a narração crescer, sai primeiro a prova de Newton do B5-4); operadores neutros; fundo azul com estrelas contínuas; sem livros na tela ou na fala; sem citar vídeo futuro (só "no módulo de gravitação").

---

# ANEXO A · roteiro com narração v1 (fonte do `ancoras.json`)

Narração **v1**, ~2.280 palavras ≈ 14 min a 2,7 palavras/s (43 âncoras; hook ≈ 35 s; cortáveis: B5-4 ≈ 55 s e B6-9 ≈ 20 s). A duração é estimativa; a voz mede.
Padrão: `padrao_video_longo.md` §5 e `roteiro_voz_elevenlabs_v4.md`. Tom de professor de cursinho, "a gente" e "você", nunca a letra solta (o símbolo é apresentado uma vez, depois só o nome). Números por extenso como serão falados.

**Como ler:** cada `###` é uma âncora (evento visual). A linha `tela:` diz o que aparece; a fala começa ~0,15 s depois e manda: a cena se estica. Tags `[ ]` do ElevenLabs v4 em inglês, uma por trecho; não entram na legenda.

## HOOK

### H1 · tela: `C_34`; mesa de ar de aço escovado, disco com aro rosa girando em círculo de 0,60 m em volta do furo, preso pelo fio que desce pelo furo até o puxador embaixo; rastro curto; duas voltas
[curious] Olha essa mesa de ar. O disco desliza praticamente sem atrito, preso a um fio que passa por um furinho bem no meio da mesa e desce até a mão de alguém, lá embaixo.

### H2 · tela: o puxador desce 0,30 m; o disco espirala para dentro e dispara; mais duas voltas rápidas a 0,30 m (tempo real)
[curious] Agora a pessoa puxa o fio. O raio cai pela metade… e o disco passa a dar quatro voltas no tempo em que antes dava uma.

### H3 · tela: congela; seta azul da tração no disco apontando para o furo; topo: `O FIO SÓ PUXA PARA O CENTRO. QUEM EMPURRA O DISCO PARA O LADO?`; hold de 2 s
[thoughtful] Só que repara numa coisa. O fio só consegue puxar o disco para o furo, ou seja, para o centro. Ele nunca empurra para o lado. Então, se ninguém empurra o disco para o lado, de onde veio esse giro a mais?

## ABERTURA

### A1 · tela: logo; `BEM-VINDOS AO PARALLAX LAB`; a mesa girando desfocada atrás
[happy] Fala, pessoal! Bem-vindos ao Parallax Lab.

### A2 · tela: `MOMENTO ANGULAR DE UMA PARTÍCULA`; `NESTE VÍDEO:` e três ícones (reta com ponto ao lado · círculo · espiral) acendendo nas palavras
[thoughtful] Hoje o assunto é o momento angular de uma partícula. A gente vai ver que até um corpo andando em linha reta tem momento angular, descobrir o que faz ele mudar e, no fim, voltar para essa mesa e responder a pergunta.

## B1 · DE p PARA L

### B1-1 · tela: canto linha 2 `DE p PARA L`; `C_34` congelada, fio removido, disco congelado a 0,50 m do furo, a seta magenta p⃗ em sentido anti-horário; CONTA: p⃗ = m v⃗ · F⃗ = dp⃗/dt; cartão pequeno τ⃗ = r⃗ × F⃗
[thoughtful] Vamos começar pelo que a gente já conhece. O momento linear é a massa vezes a velocidade, e a segunda lei de Newton diz que a força resultante é a taxa com que esse momento muda no tempo. E lembrando do torque: para medir o efeito de giro de uma força em torno de um ponto, a gente fazia o produto vetorial do vetor posição com a força.

### B1-2 · tela: r⃗ laranja do furo ao disco; paralelogramo GEO entre r⃗ e p⃗; GM: τ⃗ = r⃗ × F⃗ → L⃗ = r⃗ × p⃗
[thoughtful, emphatic] Então vem a pergunta natural: e se, em vez da força, a gente fizer o mesmo produto com o momento linear? Escolhe um ponto, que aqui vai ser o furo. Desenha o vetor posição, do furo até a partícula, e faz o produto vetorial dele com o momento linear. Isso tem nome: é o momento angular da partícula em relação a esse ponto.

### B1-3 · tela: dolly para `C_L`; L⃗ magenta-claro saindo do furo, perpendicular ao tampo; ícone da mão direita ao lado
[thoughtful] Como todo produto vetorial, o resultado é perpendicular aos dois vetores. O vetor posição e o momento estão no plano da mesa, então o momento angular aponta para fora do plano. O sentido vem da regra da mão direita: os dedos vão do vetor posição para o momento, e o polegar mostra o momento angular. Aqui ele aponta para cima.

### B1-4 · tela: volta a `C_34`; ângulo φ âmbar entre r⃗ e p⃗; braço r⊥ tracejado laranja do furo até a reta de p⃗, ângulo reto; CONTA: |L⃗| = r p sen φ → (r sen φ) p → r⊥ p
[thoughtful] E o tamanho? É a distância ao ponto, vezes o momento, vezes o seno do ângulo entre os dois. Só que repara: a distância vezes o seno é exatamente este segmento aqui, a distância do ponto até a reta por onde o momento passa. É o braço do momento, igualzinho ao braço de alavanca do torque. Ou seja: o momento angular é o momento linear vezes o braço.

### B1-5 · tela: CONTA: [L] = kg·m²/s
[thoughtful] Por isso a unidade é quilograma vezes metro quadrado por segundo. E guarda essa imagem: o que importa não é só quanto momento a partícula tem, mas a que distância do ponto passa a linha do movimento.

## B2 · UMA RETA TAMBÉM GIRA

### B2-1 · tela: canto linha 2 `UMA RETA TAMBÉM GIRA`; dolly para `C_TOPO`; três pinos O₁, O₂ (o furo), O₃; o disco solto atravessa a mesa em linha reta a 1,5 m/s; rótulos m = 0,20 kg, v = 1,5 m/s, d = 0,40 m
[curious] Agora um teste que pega muita gente. Solta o disco do fio e deixa ele atravessar a mesa em linha reta, com velocidade constante. Ninguém faz força nele. Ele tem momento angular?

### B2-2 · tela: em O₁ (sobre a reta), r⃗ sempre ao longo de p⃗; rótulo `L = 0`
[thoughtful] Depende do ponto. Em relação a um ponto em cima da própria reta, o vetor posição e o momento ficam sempre na mesma direção. O braço é zero, então o momento angular é zero.

### B2-3 · tela: em O₂, r⃗ acompanha o disco, braço d constante, ⊗ magenta-claro; CONTA: L_z = −m v d = −0,12 kg·m²/s
[thoughtful] Agora em relação ao furo, que fica a quarenta centímetros da reta. Visto daqui, o disco passa girando no sentido horário em volta do furo. O braço é a distância do furo até a reta, e ele não muda. Então o momento angular vale menos a massa, vezes a velocidade, vezes essa distância: menos zero vírgula doze quilograma metro quadrado por segundo. O sinal negativo é o sentido horário, para dentro da mesa.

### B2-4 · tela: em O₃, do outro lado da reta, ⊙ magenta-claro; `L_z = +0,12`
[thoughtful] E de um ponto do outro lado da reta, o mesmo disco gira no sentido contrário: o momento angular troca de sinal. Ou seja, momento angular não é uma propriedade só da partícula. É da partícula junto com o ponto que você escolheu.

### B2-5 · tela: a partir do furo, três triângulos de Δt = 0,5 s pintados em GEO, mesma base 0,75 m e mesma altura 0,40 m; hold de 2 s
[curious] E tem uma imagem bonita escondida aqui. Liga o furo ao disco e olha a área que esse segmento varre. Em tempos iguais o disco anda distâncias iguais, e a altura até o furo é sempre a mesma. Triângulos com a mesma base e a mesma altura têm a mesma área. O segmento varre áreas iguais em tempos iguais.

### B2-6 · tela: CONTA: dA = ½|r⃗ × v⃗ dt| → dA/dt = |L⃗|/2m = 0,30 m²/s
[thoughtful, emphatic] E isso não é coincidência. A área de cada triângulo fininho é metade do produto vetorial do vetor posição com o deslocamento. Trocando a velocidade pelo momento dividido pela massa, aparece o momento angular: a área varrida por segundo é o momento angular dividido pelo dobro da massa. Momento angular constante, área por segundo constante.

## B3 · O QUE MUDA L

### B3-1 · tela: canto linha 2 `O QUE MUDA L`; sai a mesa; desenho 2.5D: ponto O, pedra rosa; CONTA: L⃗ = r⃗ × p⃗ → dL⃗/dt = (dr⃗/dt) × p⃗ + r⃗ × (dp⃗/dt)
[curious] Então o que faz o momento angular mudar? Vamos derivar a definição no tempo. É a derivada de um produto, então são duas parcelas: a derivada do vetor posição vezes o momento, mais o vetor posição vezes a derivada do momento.

### B3-2 · tela: GM: (dr⃗/dt) vira v⃗ e (dp⃗/dt) vira F⃗; v⃗ × m v⃗ riscado com `PARALELOS` → 0
[thoughtful] A derivada da posição é a velocidade, e a derivada do momento é a força resultante. Só que olha a primeira parcela: velocidade vezes massa vezes velocidade. São dois vetores na mesma direção, e o produto vetorial de vetores paralelos é zero. Ela some.

### B3-3 · tela: GM: r⃗ × F⃗ vira τ⃗ → τ⃗ = dL⃗/dt; F⃗ = dp⃗/dt sobe ao lado; selo `HIPÓTESES: PONTO FIXO · REFERENCIAL INERCIAL · τ E L NO MESMO PONTO`
[thoughtful, emphatic] Sobra o vetor posição vezes a força, que é o torque. Então o torque resultante é a taxa de variação do momento angular. Olha como fica parecido com a segunda lei: a força muda o momento linear, o torque muda o momento angular. Só com um cuidado: o ponto tem que estar parado num referencial inercial, e o torque e o momento angular têm que ser medidos em relação ao mesmo ponto.

### B3-4 · tela: selo `CONFERE`; a pedra de 0,50 kg solta do repouso a d = 0,40 m à direita de O; cota d laranja; seta azul mg; r⃗ acompanha a pedra
[curious] Vamos conferir com algo bem simples: uma pedra de meio quilo solta do repouso, quarenta centímetros à direita de um ponto. Ela cai reto, sem girar nada. Será que ela ganha momento angular em relação a esse ponto?

### B3-5 · tela: CONTA: L_z = x p_y − y p_x → = d(−m g t) → L_z = −m g d t · τ_z = −m g d = −1,96 N·m; gráfico L_z × t, reta de 0 a −1,18 em 0,60 s, triângulo de inclinação; hold de 2 s
[thoughtful] Ganha. O braço continua sendo os quarenta centímetros, mas o momento para baixo cresce com o tempo. Então o momento angular cresce em linha reta: menos a massa, vezes a gravidade, vezes a distância, vezes o tempo. Negativo, porque a pedra passa girando no sentido horário em volta do ponto. E o torque do peso? É menos a massa vezes a gravidade vezes a mesma distância: menos um vírgula noventa e seis newton metro, constante. É exatamente a inclinação dessa reta. Confere.

## B4 · O CÍRCULO

### B4-1 · tela: canto linha 2 `O CÍRCULO`; de volta à mesa em `C_TOPO`, fio preso, órbita de 0,60 m a 1,5 m/s; r⃗ ⟂ v⃗ com ângulo reto; CONTA: |L⃗| = r⊥ p → r⊥ = R → L = m v R → L = m R² ω
[thoughtful] Agora o caso que todo mundo associa ao momento angular: o movimento circular, com o ponto no centro. Aqui o vetor posição é sempre perpendicular à velocidade, então o braço é o próprio raio. O momento angular é a massa, vezes a velocidade, vezes o raio. E como a velocidade é a velocidade angular vezes o raio, fica a massa vezes o raio ao quadrado vezes a velocidade angular.

### B4-2 · tela: GM: m R² vira I → L = I ω; o I rosa acende no aro do disco; números I = 0,072 kg·m² · L = 0,18
[thoughtful] E a massa vezes o raio ao quadrado é o momento de inércia da partícula em relação a esse eixo. Então, no círculo, o momento angular é o momento de inércia vezes a velocidade angular.

### B4-3 · tela: seta azul da tração no disco apontando para o furo; rótulo `τ = 0`; L constante no mostrador
[thoughtful] No movimento circular uniforme, a única força no plano é a tração do fio, e ela aponta para o centro. Força na mesma linha do vetor posição não faz torque. Torque zero, momento angular constante. Faz sentido: velocidade constante, raio constante.

### B4-4 · tela: seta azul F_t tangente ao disco por 1 s; mostrador de ω violeta de 2,5 a 5,0 rad/s; CONTA: τ_z = dL_z/dt → d(m R² ω)/dt → (R FIXO) m R² dω/dt → τ_z = I α
[thoughtful] Agora imagina que alguém dá um empurrão de lado no disco, tangente ao círculo, enquanto o fio segura o raio. Essa força tangencial faz torque, e o momento angular cresce. Escrevendo a lei com o momento angular igual a massa vezes raio ao quadrado vezes velocidade angular, e com o raio fixo, a massa e o raio saem da derivada. Sobra o momento de inércia vezes a aceleração angular. É a segunda lei da rotação, saindo direto de torque igual à variação do momento angular.

### B4-5 · tela: o rótulo `R FIXO` pisca; nota pequena ao lado de τ_z = I α: `SÓ PORQUE R NÃO MUDOU`
[curious] Só que guarda este detalhe, porque ele vai salvar a gente daqui a pouco: o torque igual a momento de inércia vezes aceleração angular só saiu assim porque o raio ficou fixo.

## B5 · FORÇA CENTRAL

### B5-1 · tela: canto linha 2 `FORÇA CENTRAL`; Manim 2.5D: ponto O, partícula, força F⃗ sempre apontando para O; CONTA: τ⃗ = r⃗ × F⃗ → F⃗ ∥ r⃗ → τ⃗ = 0 → dL⃗/dt = 0 → L⃗ constante
[thoughtful, emphatic] Agora a ideia mais poderosa do vídeo. Uma força central é uma força que aponta sempre na linha que liga a partícula a um ponto fixo, para ele ou para longe dele. Como ela fica na mesma direção do vetor posição, o torque em relação a esse ponto é zero. E torque zero significa momento angular constante. Não importa o tamanho da força, nem como ela muda: se ela é central, o momento angular em relação ao centro não muda.

### B5-2 · tela: Manim 2.5D, vista inclinada como a `C_L`: plano GEO, L⃗ fixo perpendicular a ele, a trajetória curva presa ao plano
[thoughtful] Daí saem duas consequências. A primeira: o momento angular é perpendicular ao vetor posição e à velocidade. Se ele não muda de direção, a partícula nunca sai do plano perpendicular a ele. O movimento fica num plano. E se o momento angular for zero, a partícula anda numa reta que passa pelo centro.

### B5-3 · tela: na trajetória, triângulos de mesmo tempo com áreas iguais; dA/dt = |L⃗|/2m acende
[thoughtful] A segunda: lembra que a área varrida por segundo é o momento angular dividido pelo dobro da massa? Se o momento angular é constante, a área por segundo também é. Áreas iguais em tempos iguais, para qualquer força central: um fio, uma mola presa num ponto, a gravidade do Sol.

### B5-4 · tela: construção de Newton: A → B em Δt; prolongamento fantasma B → c (sem chute); chute Δp⃗ magenta em B apontando para O; ponto real C; triângulos OAB, OBc e OBC; reta tracejada paralela a OB passando por c e C; hold de 2 s
[curious] O Newton tinha uma prova geométrica linda disso. Sem força, a partícula iria de A para B e depois para c, com o mesmo passo, e os triângulos teriam a mesma área, como na reta. Agora, no ponto B, ela leva um chute apontando para o centro. Ela vai parar em C, e não em c. Só que o chute foi na direção do centro, então C está numa reta paralela ao segmento até o centro. Mesma base, mesma altura: o triângulo novo tem a mesma área que o antigo. Chute central não muda a área.

### B5-5 · tela: órbita elíptica com o Sol no foco; 12 setores de mesmo tempo alternando tons de GEO; o planeta acelera perto do Sol
[thoughtful] Por isso um planeta anda mais rápido perto do Sol e mais devagar longe dele: perto, o braço é curto, então a velocidade tem que ser maior para varrer a mesma área. O resto das leis dos planetas a gente explora no módulo de gravitação.

## B6 · DE VOLTA À MESA

### B6-1 · tela: canto linha 2 `DE VOLTA À MESA`; `C_34`, a mesa com o disco a 0,60 m; selo `HIPÓTESES: SEM ATRITO · FIO IDEAL · DISCO PEQUENO`; seta azul T⃗ apontando para o furo
[thoughtful] Agora sim, de volta à mesa. O fio passa pelo furo, então a tração aponta sempre para o furo. É uma força central em relação ao furo. Então o momento angular do disco em relação ao furo não muda, mesmo enquanto alguém puxa o fio.

### B6-2 · tela: dolly para `C_TOPO`; reprise da puxada em 0,5× (`CÂMERA LENTA`); mostradores r, I, ω, L; CONTA: L = I ω · I = m r² → m r² ω = constante → r ÷ 2 ⇒ I ÷ 4 ⇒ ω × 4
[thoughtful] No disco, o momento angular é o momento de inércia vezes a velocidade angular, e o momento de inércia é a massa vezes o raio ao quadrado. Quando o raio cai pela metade, o momento de inércia cai para um quarto. Para o produto continuar o mesmo, a velocidade angular tem que quadruplicar: de dois e meio para dez radianos por segundo.

### B6-3 · tela: a puxada congela em r = 0,45 m; CONTA: τ⃗ = dL⃗/dt (`LEI GERAL`) → τ_z = d(I ω)/dt → I dω/dt + (dI/dt) ω → τ_z = I α + İ ω; ao lado, τ_z = I α com `SÓ COM I CONSTANTE`; hold de 2 s
[curious] Mas espera. Torque zero e a velocidade angular aumentando? Isso não contradiz o torque igual a momento de inércia vezes aceleração angular? [short pause] Não contradiz. A lei geral é o torque igual à variação do momento angular. Derivando o momento de inércia vezes a velocidade angular, a regra do produto dá duas parcelas: o momento de inércia vezes a aceleração angular, mais a taxa de variação do momento de inércia vezes a velocidade angular. A versão curta só vale quando o momento de inércia é constante, e lá no círculo ele era. Aqui não é.

### B6-4 · tela: CONTA: 0 = I α + İ ω → I α = −İ ω → I = 0,0405 · ω = 4,44 · İ = −0,054 → α = +5,9 rad/s²
[thoughtful] Com torque zero, a primeira parcela tem que cancelar a segunda. Como o raio está diminuindo, o momento de inércia está caindo, e a aceleração angular sai positiva. No meio da puxada, a quarenta e cinco centímetros do furo, ela dá quase seis radianos por segundo ao quadrado, sem torque nenhum.

### B6-5 · tela: mostradores lado a lado: ω 2,5 → 10 (× 4) e v_θ 1,5 → 3,0 (× 2); CONTA: v_θ = L/(m r) · ω = L/(m r²); hold de 2 s
[thoughtful] E repara numa diferença que obriga a pensar no raio. A velocidade angular quadruplicou, mas a velocidade do disco ao longo da volta só dobrou: de um e meio para três metros por segundo. A velocidade angular depende do raio ao quadrado, a velocidade tangencial depende só do raio.

### B6-6 · tela: triângulos de 0,20 s ao longo da espiral, todos com 0,090 m²; cada um mais baixo e mais largo que o anterior
[thoughtful] E as áreas? Continuam iguais em tempos iguais, durante a puxada inteira. Com o raio menor, o triângulo fica mais baixo, então tem que ficar mais largo: o disco percorre mais arco a cada instante. É a mesma imagem da reta e do planeta.

### B6-7 · tela: congela em r = 0,45 m; inset `ZOOM ×3`: v⃗ = v_r (para o furo) + v_θ (tangente), ângulo âmbar 8,5°; T⃗ para o furo; a componente de T⃗ ao longo de v⃗ acende
[curious] Falta uma pergunta: e a energia? Quem deu energia para o disco correr mais? Olha a velocidade durante a puxada. A trajetória é uma espiral, então a velocidade tem uma parte ao longo da volta e uma parte apontando para o furo. A tração também aponta para o furo. Então a tração tem uma componente na direção do movimento, e faz trabalho positivo. Força central não faz torque, mas pode fazer trabalho.

### B6-8 · tela: barras ciano: K₀ = 0,225 J, K_f = 0,900 J, W = 0,675 J entrando na diferença; selo `ESTADOS COM v_r = 0`; CONTA: W = ΔK = 0,900 − 0,225 = 0,675 J · P = T v_r (0,53 W em r = 0,45 m); hold de 2 s
[thoughtful] A energia cinética vai de zero vírgula duzentos e vinte e cinco para zero vírgula novecentos joule, quatro vezes mais, comparando os dois estados em que o disco não está se aproximando do furo. Os zero vírgula seiscentos e setenta e cinco joule de diferença são o trabalho da mão, entregue pelo fio. Ou seja: o momento angular se conservou, e a energia cinética não.

### B6-9 · tela: selo `ATENÇÃO`; gráfico T × r de 0,75 N em 0,60 m a 6,0 N em 0,30 m, com a nota `PUXADA SEM ACELERAÇÃO RADIAL`
[thoughtful] E por isso fica cada vez mais difícil puxar. Com a puxada sem acelerar o disco para dentro, a tração cresce com o inverso do cubo do raio: de zero vírgula setenta e cinco newton para seis newton quando o raio cai pela metade. [Cortável inteira se a narração passar do tempo.]

## SÍNTESE E ENCERRAMENTO

### S1 · tela: canto linha 2 `RESUMO`; `C_34` girando devagar, disco a 0,30 m; à direita, escritas uma a uma: L⃗ = r⃗ × p⃗ · τ⃗ = dL⃗/dt · τ⃗ = 0 ⇒ L⃗ constante; depois três cartões `PANEL`: `NÃO PRECISA DE CÍRCULO` · `TORQUE ZERO, ω PODE MUDAR` · `L CONSERVA, K NÃO`
[calm, satisfied] A pergunta inicial está respondida. Ninguém empurrou o disco para o lado. A tração é central, então não faz torque, e o momento angular em relação ao furo ficou constante. Com o raio menor, a única forma de manter esse momento angular é girar mais rápido. E a energia extra veio da mão, que fez trabalho pelo fio. Resumindo em três ideias: momento angular não precisa de círculo; torque zero não quer dizer velocidade angular constante; e conservar momento angular não é conservar energia.

### S2 · tela: a mesa fica menor à esquerda; à direita, uma nuvem de partículas girando juntas em volta de um eixo, cada uma com o seu r⃗ × p⃗ pequeno
[curious] E fica uma pergunta para você: e se, em vez de uma partícula, for um corpo inteiro girando, feito de milhões delas? Como somar todos esses momentos angulares?

### EN · tela: encerramento padrão (logo, anéis violeta, `INSCREVA-SE PARA ACOMPANHAR OS PRÓXIMOS VÍDEOS`); pergunta para os comentários: `UMA PEDRA CAINDO RETO TEM MOMENTO ANGULAR? EM RELAÇÃO A QUAL PONTO?`
[happy] Se essas conexões ajudaram você, se inscreve no Parallax Lab para acompanhar os próximos vídeos. E deixa nos comentários: em relação a qual ponto uma pedra caindo reto tem momento angular zero? Até a próxima!

---

# ANEXO B · conferência numérica (fonte única dos números da tela)

Conferido em `pautas/verificacao/verifica_l_particula_sympy.py` (sympy: identidades vetoriais; numpy: integração da puxada com rampas de 0,15 s). g = 9,8 m/s².

| Onde | Grandeza | Valor |
|---|---|---|
| B2 | L_z em O₂ (furo), reta y = +0,40 m, v = +1,5 m/s, m = 0,20 kg | −0,12 kg·m²/s (horário); em O₃ +0,12; em O₁ 0 |
| B2 | área por Δt = 0,50 s · dA/dt | 0,150 m² · 0,30 m²/s |
| B3 | pedra 0,50 kg a d = 0,40 m: τ_z · L_z(t) · L_z(0,60 s) · queda em 0,60 s | −1,96 N·m · −1,96 t · −1,18 kg·m²/s · 1,76 m |
| B4 | órbita R = 0,60 m, v = 1,50 m/s: ω · I · L | 2,50 rad/s · 0,072 kg·m² · 0,180 kg·m²/s |
| B4 | F_t = 0,30 N por 1,0 s: τ · α · ω(1 s) · L(1 s) | 0,18 N·m · 2,5 rad/s² · 5,0 rad/s · 0,36 kg·m²/s |
| H/B6 | r 0,60 → 0,30 m; v_θ · ω · I | 1,50 → 3,00 m/s · 2,50 → 10,0 rad/s · 0,072 → 0,018 kg·m² |
| H/B6 | L · dA/dt (constantes) | 0,180 kg·m²/s · 0,450 m²/s |
| H/B6 | K₀ · K_f · ΔK = W (estados com v_r = 0, qualquer perfil de puxada) | 0,225 J · 0,900 J · 0,675 J |
| H/B6 | puxada: rampa 0,15 s · 0,30 m/s constante · rampa 0,15 s | 1,15 s no total; ≈ 0,8 volta durante a puxada |
| B6-3/4 | em r = 0,45 m (fase de v_r constante): I · ω · v_θ · İ · İω · α | 0,0405 kg·m² · 4,44 rad/s · 2,00 m/s · −0,054 kg·m²/s · −0,240 · +5,93 rad/s² |
| B6-6 | área por 0,20 s | 0,090 m² |
| B6-7 | ângulo entre v⃗ e a tangente em r = 0,45 m (v_r = 0,30 m/s) | 8,5° |
| B6-8 | T e P em r = 0,45 m (r̈ = 0) | 1,78 N · 0,53 W |
| B6-9 | T = L²/(m r³) com r̈ = 0 | 0,75 N (0,60 m) → 6,0 N (0,30 m) |
| geral | aliasing máximo do disco a 15 fps | 38° de órbita por quadro (r = 0,30 m); reprise em 0,5× |
</pasted_content id="4eff">
