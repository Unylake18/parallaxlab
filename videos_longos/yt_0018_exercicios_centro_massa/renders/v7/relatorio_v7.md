# yt_0018 v7 — voz contínua e sincronia no padrão do yt_0010 (preview 960×540, 15 fps)

Vídeo: `renders/preview_yt0018_v7_960x540.mp4` — **14,16 min (849,7 s)**; voz **14,14 min (848,4 s)** em `audio/narracao_v7.wav` (mono, 44,1 kHz, 16 bits). O vídeo termina cerca de 1,5 s depois da última palavra.
Zip: `renders/v7_para_gpt.zip`. Parei antes de 1080p, SRT, capa e entrega.

## Antes (v6) × depois (v7)
| Auditoria | v6 | v7 |
|---|---|---|
| VOZ CONTÍNUA (silêncio < −80 dBFS ≥ 50 ms) | 66 trechos | **0** |
| BORDA ABRUPTA (salto ≥ 35 dB em 10 ms) | 149 | **0** (maior salto 33,5 dB) |
| JUNÇÕES | 47 cortes por âncora, em silêncio digital | **3** (blocos − 1), crossfade 25 ms, 0,34 s de silêncio cada |
| ATRASO dos gatilhos (−0,15 … +0,20 s) | ±0,3 s, medido contra a nominal | **98 gatilhos, 0 fora**; maior atraso **+0,01 s**, maior adiantamento −0,14 s, média −0,075 s |
| CONGELAMENTO (freezedetect n = 0,0005, d = 1,5 s, com fala) | 97 trechos, 235,6 s (26,4%), maior 6,4 s | **0**; 3D: gafanhoto no ar parado 0 |

Medi o v6 com os mesmos scripts (`renders/v7_antes_voz.txt`, `renders/v7_antes_congelamento.txt`). O handoff contou 103 trechos e 248 s com o ffmpeg; os meus números são parecidos.

## Voz
- Texto `narracao_tags_v1_4.md` (as duas trocas do §4). Voz `qw7jgPZWOKrl10GsjQ82`, `eleven_v4`, `/with-timestamps`, **4 blocos** de ≤ 4.500 caracteres cortados em fim de parágrafo, com `previous_text`/`next_text`. Nada foi reaproveitado da v1.1/v1.2/v1.3.
- **Nenhum bloco foi regerado**: gastei 14.754 caracteres de crédito (sobram cerca de 8,5 mil). Eu **não ouvi** os takes: tropeço, tag lida em voz alta e pronúncia ficam para a sua escuta.
- `unir_voz.py`: apara só o silêncio das pontas abaixo de −45 dBFS, crossfade de 25 ms, nivela os blocos (≤ 0,5 dB de ajuste). Sem corte por âncora e sem silêncio inserido.
- **Dois achados sobre a saída do ElevenLabs.** O WAV colado, sem nada meu, já tinha 28 pausas abaixo de −80 dBFS e 32 bordas abruptas: os silêncios do próprio modelo são quase zero. Para zerar as duas auditorias coloquei uma **cama de sala** contínua (ruído rosa a −54 dBFS, estacionário) sob a voz inteira. O piso natural do take era −60 dBFS. Os takes terminavam colados na fala: o silêncio natural nas junções era 0,23 / 0,34 / 0,25 s, e completei até 0,34 s com a mesma cama. É o único conteúdo que não vem da voz.
- **Tempos das palavras.** Conferi 152 inícios de palavra depois de pausa contra a onda: o alinhamento do ElevenLabs chega em média **0,10 s depois** da fala real (mediana −0,10 s, p95 0,25 s, máx. 0,35 s). Corrigi esses 152 inícios pela onda (`audio/voz7_deslocamento.json`). As palavras no meio da frase ficam com o alinhamento original, sem conferência na onda.

## Sincronia (copiado do yt_0010 e adaptado ao kit)
- `plano(A, W, D)` do yt_0010, aplicado **por trecho entre marcas** (início de âncora, gatilho, fração): `SYNC=medir` mede o tempo nominal de animação e de espera de cada trecho (`medicao_<lote>.json`); `SYNC=final` estica cada trecho até a próxima palavra. Âncoras absolutas: cada lote abre e fecha no quadro da voz (o QA confere os 7 lotes: quadros reais = esperado).
- Janela da âncora = do começo da primeira palavra −0,15 s até o da próxima −0,15 s, nos instantes do WAV final. As pausas são só as da voz.
- **LEAD = 0,08 s** nos gatilhos (o yt_0010 usa 0,15 s). Com a quantização de 1/15 s, 0,15 s estourava o −0,15 s: a imagem caía em −0,17 s.
- A abertura de uma âncora atrasou 0,07 s uma vez (X3-4); nenhuma outra.

## Telas (o que mudou, conforme o §3)
- **H2/H3:** o replay em câmera lenta vai a **1/23 de velocidade, constante**, de "em câmera lenta" até o fim do H3 (relógio da cena, sem tween): agacha até "escorrega para trás" (a seta de recuo nasce nessa palavra), voa e **pousa com respingo em "e mais cinco problemas"**, o respingo corre até o fim. A pergunta do H3 entra com ele ainda no ar; o ⊕ acompanha o voo. Nenhum quadro parado. O enquadramento do replay passou a mostrar o salto inteiro (cerca de 2 m de largura, câmera a 20°), em vez de 0,6 m.
- **Gafanhoto vivo:** antenas e abdome se mexem em repouso (Three.js, preso ao relógio da cena). No X3-5 o replay é um só e contínuo, até o fim da fala.
- **X1-2:** a diagonal se desenha durante "a diagonal que passa pelo centro…" e o espelhamento vem em "duas metades iguais, espelhadas".
- **X4-4:** os dados entram na palavra deles ("a nave leve sai", "a pesada a um", "três metros por segundo"); as barras crescem durante "dois mil joules para a leve e mil para a pesada". Antes, o dado da pesada entrava 5 s depois da fala.
- **X5-8:** o ⊕ desce e o mostrador cai a 5,0 em "acelera para baixo"; o ⊕ sobe e o mostrador volta a 6,0 em "acelera para cima"; elevador e cavalo acendem em "elevador" e "cavalo".
- **EP1:** o pulso atravessa a caixa em velocidade constante de "sai um pulso" a "na outra parede"; a caixa recua num 2º voo, de "quando ela sai" a "a caixa para". **EP2:** a seta "?" cresce em "o que foi para a direita", a linha do ⊕ pisca em "não podia ter andado", o replay fantasma corre com o relógio. **S2:** cada cartão entra na frase da ferramenta e o anterior apaga para 60%. **EN1:** os cartões do CTA entram na frase de cada um. **EN2:** o foguete anda com o relógio.
- **Movimento que acompanha a fala (geral).** Onde a tela ficaria parada, o termo em foco ganha um **realce translúcido** que pisca. O realce não anima o próprio termo, e a auditoria não o enxerga. Isso zerou o congelamento, mas **é um recurso genérico**: nem todo trecho do §3 ganhou o movimento específico.

## O que **não** fiz do §3
- A2 (itens a cada frase), A4 (lista das três perguntas acesa pela pergunta falada), X2-2/X2-4 (rotação lenta do cubo, esferas dos meios e cota de 24 cm que cresce) e X5-6/X5-7: ficaram com o plano() e o realce genérico, não com o movimento específico. Não girei o cubo porque os rótulos dele estão presos a posições fixas. Isso pede decisão sua.
- 3 `[short pause]` (X3-6, X4-4, X5-6) e as pausas dos seis momentos do v6: não aparecem como pausa na tela, porque a voz nova não tem silêncio colado. Só o X3-5 tem uma pausa de 0,96 s da própria voz.
- O handoff pedia "se um momento precisar de mais tempo do que a fala dá, me reporte": não encontrei um caso em que o evento visual não coubesse na frase.

## Auditorias de tela (v5/v6)
Portão G28 **aberto com 7 justificativas** (`renders/justificativas.json`). Cada uma é **uma só amostra, numa transição** (o item não é flagrado nas amostras vizinhas); olhei quatro delas nos quadros (`renders/v7/_dbg_residuais.png`) e as outras três só pelo log:
TRÂNSITO (PX0 78,5 s; PX2 48,3 s), FORA DA MARGEM (PX3 29,8 s, m g⃗ entrando), PALCO 3D (PX3 155,1 s, contraste 0,067), 3D × TEXTO (PX3 203,3 s), ENCOSTADO (PX5 35,3 s, folga 0,19 contra 0,20), FORA DA ZONA (PX5 123,2 s, selo DICA entrando).
Zerados: TEXTO SOBRE OBJETO/CAIXA, ESQUELETO, DUPLICATA, CALHA, VAZIO, SEM PALCO, FUNDO 0%, BALANÇA (mostrador × N/g ≤ 0,041 kg), alinhamento Three.js × Manim 0,000 px, GAFANHOTO × FÍSICA (0,19 px), exposição < 235, água/lua OK.

## Arquivos
Novos: `gerar_voz_v7.py`, `unir_voz.py`, `auditoria_voz.py`, `verifica_tempos.py`, `congelamento.py`, `conferir_sync.py`, `conferir_lotes.py`, `idle_plano.py`, `pranchas_v7.py`, `medir.sh`, `render_v7.sh`, `narracao_tags_v1_4.md`, `medicao_<lote>.json`.
Alterados: `kit.py` (SYNC, plano, marcas, âncoras absolutas, LEAD), `prob.py`, `prob2.py` (pulsos e realce), `gerar_ancoras.py` (reescrito), `montar_audio.py` (reescrito), `qa.py`, `zip_gpt.py`, `p99.py`, `agua.py`, `sec_hook.py`, `sec_x01.py`, `sec_x3.py`, `sec_x4.py`, `sec_x5.py`, `sec_fim.py`, `threejs/cena3d/lago3d.js`. Do yt_0010 copiei o mecanismo (plano, marcas e checagem), sem alterar a unidade dele.
Não toquei em `template/`, `assets/`, docs globais nem fiz commit.

## Pendências
- Escuta final dos takes (pronúncia, tags, ritmo): é sua.
- Os 7 itens justificados e os trechos do §3 não feitos (acima).
- O alinhamento no meio da frase não foi conferido na onda.
