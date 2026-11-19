# yt_0041 · CÁLCULO III · EP. 16 · Coordenadas esféricas na integral tripla · HANDOFF FINAL
**Três correções de tela (R1–R3) + narração final v1.5 + voz + sincronização + legenda `.srt` + render 1080p + master + entrega**

Arquivo único e autocontido. Data: 2026-11-16.

**Base:** o preview v4 (22:12,87, 960×540, 15 fps, sem voz), do zip `yt0041_v4_para_gpt`. O v4 cumpriu o handoff v4:
- D1 a D11 corrigidos (linha órfã do B1-3, rótulo órfão do B2-3, casquinha e painel sem sobreposição, caixinha dentro de x 60..975, S2 sem o CTA, escada do B6-2 em 44, H2 sem painel vazio, B1-1 sem glifo menor, voos retos no B6-1);
- 3D sobre o papel quadriculado com piso, só na metade esquerda, legenda colorida no lugar das hastes, octante, cortes 2D, menores do B2-3;
- QA: R5 = 0, R6 = 0, flash = 0, alinhamento 3D ≤ 0,014 px.

O Kaio perguntou se já dá para seguir com a narração. **Sim.** O que falta é pouco e não muda a matemática:
1. três detalhes de tela (R1–R3);
2. os 12 atrasos de gatilho (> 0,3 s) do v4 acontecem porque a escrita não coube na fala v1.4. **A voz decide o tempo**: a cena passa a seguir o WAV (§6), sem comprimir a caneta.

No zip `yt0041_handoff_final_completo.zip` vão:
- este documento;
- `yt_0041_narracao_v1_5.md` (narração final, a mesma da v4; é a fonte do `gerar_ancoras.py`);
- `regra_narracao_tela_mostra_voz_ensina.md` (regra permanente do Kaio sobre a fala);
- `yt_0041_v3_avaliacao_e_handoff_v4.md` (histórico).

Onde este documento não diverge, continuam valendo os handoffs v2, v3 e v4 e os alvos v3/v2.

---

## 0. Autorização, fases e modo de execução

**Fases abertas pelo Kaio nesta unidade:**
- correções de tela (§3);
- voz (ElevenLabs v4);
- sincronização;
- legenda `.srt`;
- render final 1080p e master;
- entrega em `entregas/`.

**Fases não abertas (não fazer):**
- publicação, capa, `commit`, `push`, `merge`, `branch`, PR;
- qualquer mudança em `template/`, `assets/`, `pyproject.toml`, `uv.lock`, `AGENTS.md`, `docs/` ou em outras unidades.

**O que pode ser alterado:**
- só `videos_longos/yt_0041_coordenadas_esfericas/`;
- `renders/` e `entregas/`, que são saída;
- pode **copiar** (sem alterar a origem) do `videos_longos/yt_0034_regioes_gerais_troca_ordem/` (ou do `yt_0037_coordenadas_polares/`, se já tiver a versão mais nova) para a unidade:
  - `alinhar_voz.py`, o modo tempo real do `gerar_ancoras.py`, `gerar_srt.py`, `capitulos.py`;
  - `render1080.sh`, `render1080_fila.sh`, `montar_final.py`;
  - `qa_canto.py`, `qa_fundo.py`, `qa_sync.py`, `qa_voz.py`, `qa_1080.py`, `prancha_ancoras.py`, `stills_final.py`.

**Modo de execução:**
- Não encerre a vez entre etapas.
- Depois de lançar um render (Manim ou Three.js) ou a voz, espere na mesma vez e siga para a auditoria. Use comando em primeiro plano com timeout de até 10 min por lote, ou um laço `until` sobre o arquivo de saída.
- Mensagem de progresso não é entrega.
- Logs longos vão para arquivo; leia só o fim e os erros.

**Só há duas paradas permitidas:**
1. A variável `ELEVENLABS_API_KEY` não existe na sessão. Peça ao Kaio. **Nunca** grave a chave em arquivo, log ou relatório.
2. O WAV passa de **23:45**. Reporte a duração e pare (estimativa: 4.061 palavras a 3 palavras/s ≈ 22:34; o preview v4 foi cronometrado pela v1.4, em 22:12).

Qualquer outra dúvida: escolha a leitura mais provável, diga qual e siga.

**Ordem:**
1. §3 correções no código, com stills de conferência (sem voz, tempos do v4 como rascunho);
2. §4 narração e busca dos gatilhos;
3. §5 voz;
4. §6 sincronização;
5. §7 conferência 540p com voz;
6. §8 1080p;
7. §9 QA e entrega;
8. §10 relatório.

Pare só depois do relatório. Guarde este arquivo na unidade como `handoff_final.md`.

---

## 1. Estado de partida

- **Unidade:** `videos_longos/yt_0041_coordenadas_esfericas/` (checkout principal).
- **Código:**
  - `sec_h.py`, `sec_b1.py` … `sec_b7.py`, `sec_s.py`;
  - `k41.py` (inclui `legm()`), `kit.py`;
  - `threejs/cena3d/c41.js`, `threejs/bbox3.py`;
  - `qa3d41.py`, `chk_gat.py`, `sonda3.py`, `run_v3b.sh`;
  - referências: `referencia_v3/` (handoff v3) e `referencia/` (narração v1.4).
- **Não reabrir:**
  - a matemática e os números (Anexo A);
  - as contas do v4, degrau por degrau;
  - a ordem H1 → H2 → A1 → B1-1 … B7 → S1 → S2;
  - o sistema 3D da série (G1–G6: papel sob o 3D, piso em z = 0, 3D até x = 975, legenda colorida, coluna em x = 1020);
  - as cores:

    | Grandeza | Cor |
    |---|---|
    | r | laranja `#FF9440` |
    | φ | violeta `#B48CFF` |
    | θ | verde-água `#2EE6A6` |
    | s | pêssego `#FFC08A` |
    | r² sen φ | lima `#C6F26B` |
    | ρ (densidade) | ciano `#35D9FF` |
    | x | âmbar `#FFC24D` |
    | y | magenta `#EA63FF` |
    | z | azul `#5AA2FF` |

  - nenhum efeito novo: sem pulso, brilho, palco vivo, tracer, partícula ou sombra (`_sem_vivo = True` se o kit tiver palco vivo).
- **Notação (lei de Gauss):** ρ = densidade, r = distância, R = raio fixo, s = r sen φ (sombra), φ a partir de +z em [0, π], θ longitude (lido **téta**), T = a transformação.
- **A cena segue a voz.** Os tempos do v4 não valem mais. Todos os lotes, inclusive os quadros do Three.js, são re-renderizados com a linha do tempo da voz.

---

## 2. Avaliação do v4 (resumo)

O preview v4 foi avaliado pelo Kaio e pelo chat de Produção contra os alvos v3/v2 (folhas de 10 em 10 s e os stills). Resultado: legível, 3D alinhado à grade, sem poluição, sem sobreposição. Restam três detalhes (§3) e o aceite de que **dois pontos do v4 não são mais corrigidos**:
- **B2-2** (7:00–7:50 do v4): a metade direita fica vazia até o painel do chão entrar. Aceito: a fala explica o primeiro painel antes do segundo, e uma caixa vazia seria pior. Não criar painel fantasma.
- **Caneta em andamento** nos stills (um glifo pequeno no meio de uma linha, por exemplo `= r sen²φ co` em 9:30): é a escrita acontecendo, não defeito.

---

## 3. Correções (lista fechada)

### R1 · B2-3: o rótulo `LINHA DE BAIXO: + − +` volta sozinho (9:50 do v4)
- **O que se vê:** a matriz e os menores viram chips (9:30–9:40) e, em 9:50, o rótulo `LINHA DE BAIXO: + − +` reaparece no canto direito, sem a matriz, quando a linha `det = + cos φ · M₃₁ = (−r sen φ) · M₃₂` é escrita.
- **Fazer:** o rótulo só existe junto com a matriz. Para a linha do `det`, usar a mesma legenda **na altura da própria linha do det** (à esquerda do início da linha, cor menta), ou não repetir o rótulo (preferir remover: a linha do `det` já mostra os sinais `+ … ·`).
- **Aceite:** zero quadro com `LINHA DE BAIXO` sem a matriz na tela; tabela de linhas órfãs (varredura a cada 0,5 s) = 0.

### R2 · Tamanho real das letras (QA que faltou no v4)
- **O que faltou:** o v4 mediu só o tamanho pedido no código (`sec_b1.py` aparece com `min=0`, medição quebrada) e não a altura real nos quadros.
- **Fazer:** medir no 1080p a **altura do x minúsculo** da fórmula principal de cada bloco e o corpo de todo texto. Se algum texto de coluna ficar < 26 px de corpo ou algum algarismo < 30 px, subir para 36 (legenda 30) sem mudar o layout. A fórmula principal fica em 44–58.
- **Aceite:** tabela `qa/tamanhos_final.txt` por bloco com a altura do x e o menor texto; zero < 26 px.

### R3 · Atrasos de gatilho do v4 (resolvidos pela voz)
- **O que se vê:** `chk_gat.py` no v4 mostra 12 gatilhos > 0,3 s de atraso (maiores: B6-2 +1,5 s, B2-3 +1,1 s, B6-1 +1,1 s, B2-2 +1,0 s, H2 +1,0 s, B7 +1,0 s).
- **Fazer:** nada no código agora. Na §6, a escrita passa a começar na frase do gatilho (meta ≤ 0,2 s). Quando a fala for mais longa que a construção, a espera se divide entre os degraus; quando a construção for mais longa que a fala da âncora, **não acelere a caneta**: use o `[estouro]` da §6.4.
- **Aceite:** `qa/sync.txt` da §6.

Nenhuma outra correção. **Não mexer** em D1–D11 do v4.

---

## 4. Narração final

Arquivo: `yt_0041_narracao_v1_5.md` (no zip). É a fonte do `gerar_ancoras.py`. Tem **4.061 palavras ≈ 22:43** (a v1.4 do preview v4 tinha 3.967; a v1.5 acrescenta 94 palavras em B1-1, B2-2, B2-3 e B5, sem mudar nenhum gatilho). Nada muda no texto nem nos gatilhos (todos verificados contra a fala: `chk_gat.py` do v4 bate).

**Regras já aplicadas na v1.4 e mantidas na v1.5 (não alterar):**
- A tela mostra a conta inteira; a voz conversa como professor (marcação [ensina]/[mecânica] por linha da coluna), sem ler número por número e sem silêncio. Não encurtar.
- Cada letra latina com a **caixa da tela**: "eixo z", r minúsculo para a distância, R maiúsculo só para o raio fixo, s, u, k, c, "d r", "d V"; gregas pelo nome ("fi", "rô", "pi"); θ sempre **téta**.
- A seção `## Leitura dos símbolos` do arquivo traz a tabela de leitura.

**Passos:**
1. Gere `narracao_tags.md` (com a seção `## Texto corrido (para gravação)`) e `narracao_limpa.md` a partir da v1.5, como no yt_0034. Tags de áudio `[ ]` em inglês, uma por frase, base `[thoughtful]`/`[curious]`, `[excited]` só na descoberta; sem tags na legenda.
2. `grep -c '\bteta\b'` = 0 na fala, nos gatilhos e nos arquivos de tags.
3. Rode a busca de gatilhos: `[gatilho-sem-frase]` = 0 antes da voz.

---

## 5. Voz (ElevenLabs v4)

Referência: `docs/roteiro_voz_elevenlabs_v4.md`.

1. Confirme `ELEVENLABS_API_KEY` (primeira parada, §0).
   - Voz `qw7jgPZWOKrl10GsjQ82`, modelo `eleven_v4`.
   - Formato `mp3_44100_192`, decodificado para WAV mono 16 bits 44,1 kHz.
2. **Amostras de pronúncia primeiro (curtas, para o Kaio ouvir em paralelo):** gere 6 mp3 em `audio/teste_pronuncia/` com estas frases e siga sem esperar:
   - "O eixo z aponta para cima e o r é a distância até a origem."
   - "O s é igual a r vezes seno de fi."
   - "O volume é d r d fi d téta, vezes r ao quadrado seno de fi."
   - "Em d V, o V é o volume."
   - "Com téta igual a pi sobre três."
   - "Cosseno de fi vezes r, mais r vezes seno de fi."
3. Rode `narracao_tags.md` com `--seco`, depois sem ele:
   ```
   uv run --no-sync python videos/gerar_voz_elevenlabs.py videos_longos/yt_0041_coordenadas_esfericas/narracao_tags.md videos_longos/yt_0041_coordenadas_esfericas/audio/narracao_v1.wav --voz qw7jgPZWOKrl10GsjQ82 --secao "## Texto corrido (para gravação)" --seco
   ```
4. **Uma tomada completa.** Siga com ela. O Kaio ouve em paralelo; se reprovar (inclusive a leitura das letras minúsculas), ele regera e a §6 refaz tudo sozinha. A tomada aprovada vira `audio/narracao_final.wav`.
5. `qa/voz.txt` (`qa_voz.py`):
   - duração;
   - picos e clipping;
   - silêncio > 1,5 s dentro de um parágrafo;
   - tag lida em voz alta;
   - fronteiras sem corte audível;
   - pronúncia de:
     - letras: "eixo z", "r", "s", "u", "k", "c", "d r", "d V", "téta" (nunca "teta"), "fi", "rô", "pi", "T";
     - funções: "seno de fi", "cosseno de fi", "seno ao quadrado", "raiz quarta de um meio";
     - números: "oito sobre três", "três sobre dezesseis", "dois mais raiz de três", "zero vírgula oito quatro";
     - nomes: "Guidorizzi", "Parallax Lab".
6. No relatório: modelo, voz, número de blocos, duração e taxa real (palavras ÷ segundos de fala).

---

## 6. Sincronização (a cena segue a voz)

Regras permanentes dos longos:
- WAV contínuo;
- **nunca** cortar a voz por âncora nem inserir silêncio;
- atraso imagem × fala **≤ 0,2 s** (LEAD 0,15 s);
- quando a fala é mais longa que a construção, a espera se divide entre os gatilhos, nunca tudo no fim da âncora;
- a caneta **não acelera**; nada é escrito em silêncio.

1. `alinhar_voz.py` → `alinhamento_palavras.json`.
2. `ancoras.json` **gerado por script**: `gerar_ancoras.py` no modo tempo real. Cada âncora começa na primeira palavra do seu trecho. Os `self.gat("…")` são buscados no alinhamento.
3. **3D:** a linha do tempo do Three.js sai do mesmo `ancoras.json`.
   - Re-renderize todas as cenas que têm câmera em movimento ou pouso (órbita da bola no H1, caixinha, receita, casquinha, lata, etc.) e as demais que dependem do tempo.
   - Rode `qa3d41.py` (alinhamento ≤ 2 px, 3D dentro de x 60..975 nas cenas de metade esquerda, pousos sem pisca).
4. Rode os lotes 540p e confira:
   - `[gatilho-sem-frase]` = 0;
   - os `[estouro]`, cada um com o motivo. Estouro > 1 s numa âncora: deixe a âncora seguinte começar mais tarde (a voz continua) ou divida a espera entre os degraus. **Nunca** acelere a voz nem a caneta.
   - Os atrasos do v4 (B6-2 +1,5 s, B2-3 +1,1 s, B6-1 +1,1 s, B2-2 +1,0 s, H2 +1,0 s, B7 +1,0 s) entram na meta ≤ 0,2 s.
5. `qa/sync.txt` (`qa_sync.py`): o atraso de cada âncora, de cada degrau das contas (A1–A6 do handoff v2 §4) e de cada gatilho (meta ≤ 0,2 s).
6. **Legenda `.srt`** (`gerar_srt.py`):
   - até 2 linhas × 42 caracteres, de 2 a 5 s por bloco;
   - tempo do WAV = tempo do vídeo;
   - trocas:
     - "eixo z" → eixo z; letras sozinhas ficam como na tela (r, s, u, k, c, R);
     - "fi" → φ, "téta" → θ, "rô" → ρ, "pi" → π;
     - "d r", "d fi", "d téta" → dr, dφ, dθ; "d V" → dV;
     - "Cálculo três" → "Cálculo III".

---

## 7. Conferência 540p com voz (antes do 1080p)

Render de **todos os lotes** em 540p/15 fps com os tempos da voz, e preview com voz. Feche o que falhar antes do 1080p.

**Portões:**
- `FLASH POR QUADRO` = 0;
- sem pulso nem palco vivo (efeito não pedido) e sem tracer;
- **GRADE** de tela inteira em todo quadro 2D e papel sob o 3D;
- **CAIXA VAZIA por quadro** = 0;
- **LINHA ÓRFÃ** = 0 (varredura a cada 0,5 s);
- R5 = 0 a cada 0,2 s (texto × texto, texto × linha/polígono, texto × aresta 3D), também durante os voos; R5V listado com o motivo;
- R6 (margens) = 0;
- 3D: nada fora de x 60..975 nas cenas de metade esquerda e nenhum pixel do 3D sob painel;
- rótulo de eixo a ≤ 30 px da ponta da seta;
- canto: troca no primeiro play de cada bloco;
- tamanhos (R2): corpo ≥ 26 px, algarismo ≥ 30 px, fórmula principal 44–58;
- alinhamento 3D ≤ 2 px; pousos sem pisca;
- palco vazio ≤ 0,5 s;
- `[gatilho-sem-frase]` = 0;
- tabela CONTAS com cada degrau, o tempo e a frase que o dispara (A1–A6);
- `qa_canto.py` e `qa_fundo.py`;
- logo em todos os quadros do A1;
- S2 sem sobreposição com o CTA; cartão do S2 ≥ 8 s;
- SYNC e VOZ.

**Pranchas:**
- `correcoes_final.jpg`: R1 (antes/depois), R2 (tabela) e R3 (atrasos antes/depois);
- uma prancha com **um quadro de cada âncora no instante da primeira palavra** (19 quadros);
- lado a lado com os alvos v3 (01, 03, 10b, 11, 12, 13a, 14) e v2 (07, 08a, 08b, 13b);
- pranchas 3D 2×3 por lote (`qa3d41.py`).

---

## 8. Render final 1080p

1. **Three.js em 1080p** (todas as cenas), com a mesma câmera e a linha do tempo da voz, e QA 3D de novo sobre o 1080p.
2. **Manim em 1080p30** pelo fluxo normal, com `template/config_horizontal.py`.
   - Não configure CRF: o `template/qualidade.py` já usa **14** em renders ≥ 1080p.
   - Não recodifique. Sem teto de tempo de render.
3. **Emenda** com `montar_final.py` (remux, sem reencodar), na ordem dos lotes.
4. **Master:**
   ```
   uv run python videos/montar_master.py <sem_audio_1080p30.mp4> audio/narracao_final.wav renders/yt_0041_master_final_1080p30.mp4
   ```
   Confira:
   - 1920×1080, 30 fps;
   - duração do master = WAV (+ a cauda do CTA, se a montagem a mantiver);
   - `crf=14.0`, com o comando do AGENTS.md.
5. Se o disco apertar, apague só PNGs e renders 540p **desta** unidade já auditados.

---

## 9. QA final e entrega

**QA completo no vídeo final (`qa_1080.py`):**
- os portões do §7 sobre o 1080p (amostragem por lote);
- A/V contínuo;
- `crf=14.0`;
- `.srt` conferido em 6 pontos:
  - início;
  - `r² sen φ` do B2-3 (o det);
  - `4πR³/3` do B2-4;
  - `r = 0,84` do B5;
  - `V = π` do B6-2;
  - fim.
- `renders/capitulos_final.txt` com os tempos da voz:

| Âncora | Título |
|---|---|
| H1 | `A BOLA PESADA NA CASCA` |
| A1 | `BEM-VINDOS` |
| B1-1 | `O ENDEREÇO ESFÉRICO` |
| B1-2 | `UM PONTO DE EXEMPLO` |
| B1-3 | `A CAIXA VIRA A BOLA` |
| B2-1 | `A CAIXINHA CURVA` |
| B2-2 | `DUAS POLARES EM SEQUÊNCIA` |
| B2-3 | `O DETERMINANTE` |
| B2-4 | `O TESTE DA BOLA` |
| B3-1 | `O TEOREMA, METADE POR METADE` |
| B3-2 | `A RECEITA E A SONDA` |
| B4 | `A BOLA É UMA CEBOLA` |
| B5 | `DE VOLTA À BOLA` |
| B6-1 | `A CASQUINHA: AS SUPERFÍCIES` |
| B6-2 | `A CASQUINHA: A CONTA` |
| B7 | `QUANDO USAR` |
| S1 | `RESUMINDO` |
| S2 | `E UMA LATA?` |

**Entrega:** `uv run python videos/entregar.py yt_0041` (cópia).
- O destino tem de ser o `entregas/` do checkout principal.
- A pasta leva:
  - `master`;
  - `legenda` (`.srt`);
  - `audio/`;
  - `texto/`: ficha, `narracao_tags.md`, `narracao_limpa.md`, este handoff e os capítulos;
  - `manifesto`.
- O número `0041` vai no fim de cada nome. Não há capa.
- Série, EP e assunto vêm da `ficha.md`: `CÁLCULO III · EP. 16`, `# Coordenadas esféricas na integral tripla`.
- **Na ficha:** a duração real e `duracao_alvo` da v1.5.

Não rode `entregar.py` se um portão do §7 estiver aberto. Pare e reporte.

---

## 10. Relatório de entrega (obrigatório, e depois pare)

1. Arquivos alterados e criados.
2. R1–R3, cada um com o caminho do still que prova, e a prancha `correcoes_final.jpg`.
3. Todos os portões do §7 com números reais, a tabela CONTAS, a sincronização das 19 âncoras e o QA de voz.
4. Caminhos: WAV, amostras de pronúncia, preview 540p com voz, master 1080p, `.srt`, capítulos e a pasta em `entregas/`.
5. Three.js: cenas, resolução, custo por quadro no 1080p, alinhamento medido (px).
6. Duração final e taxa real da voz, comparadas com 3 palavras/s.
7. Pendências reais.

Depois do relatório: **pare**. Não faça publicação, capa, commit, merge nem push.

---

## Anexo A · Números congelados

- Hook: ρ = √(x² + y² + z²) numa bola de raio 1; em cartesianas aparece ∫ √(k² + z²) dz com raiz e logaritmo (trava).
- Endereço: (r, φ, θ) = (2, π/6, π/3) → z = √3, s = 1, x = 1/2, y = √3/2; confere x² + y² + z² = 4.
- Fator: r² sen φ; células do polo ≈ 0,020 e do equador ≈ 0,075, razão 2 + √3 ≈ 3,7.
- Determinante: M₃₁ = r² sen φ cos φ, M₃₂ = r sen²φ; det = r² sen φ.
- Teste da bola: V = 4πR³/3; erros mostrados: 4πR (sem o fator) e 2π²R³/3 ≈ 6,6 R³; ≈ 4,19 R³ (bola unitária).
- Cebola: área 4πr²; d/dR(4πR³/3) = 4πR².
- Bola pesada (ρ = r): M = π, média M/V = 3/4, c⁴ = 1/2, c = ⁴√(1/2) ≈ 0,84.
- Casquinha: cone z = √(x² + y²) (φ = π/4) e esfera x² + y² + z² = 2z (r = 2 cos φ, centro (0, 0, 1)); V = π, conferido por π/3 + 2π/3.
- Lata: x² + y² ≤ 1, 0 ≤ z ≤ 1; r = 1/cos φ ou 1/sen φ; racha em φ = π/4. Gancho: "No próximo vídeo: coordenadas cilíndricas".
