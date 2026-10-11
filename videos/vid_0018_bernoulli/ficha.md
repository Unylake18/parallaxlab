# Bernoulli

Série pública: **POR TRÁS DA FÓRMULA · EP. 06**

formato: curto_vertical
solido_3d: nenhum — briefing V4 preserva o universo 2D da V3 para geometria e álgebra
estado: final 1080p com voz recebida e legendas coloridas — QA concluído, pronto para postagem

## Briefing mínimo

Construir Bernoulli a partir do trabalho líquido das pressões sobre o mesmo
volume transferido: pressão → força → deslocamento → trabalho. Explicitar
`A₁ Δx₁ = A₂ Δx₂ = ΔV`, o trabalho positivo na entrada e negativo na saída.
Construir massa, variações de energia, balanço, cancelamento e reorganização.
Interpretar os três termos por unidade de volume. No estreitamento horizontal,
separar continuidade (velocidade) de Bernoulli (pressão). Fechar com as hipóteses.

V5 aprovado: 540×960, 15 fps, silencioso, duração de 162,93 s (2min43s).
Proposta inicial preservada em `texto_narracao_proposto.txt` (559 palavras).
Decisão anterior de Produção: manter a estrutura da V5 e enxugar a narração.
Texto anterior de 320 palavras preservado em `texto_narracao_320.txt`.
Handoff atual: áudio novo fornecido pelo usuário, sincronização, legendas
coloridas nas cores das variáveis e vídeo pronto para postagem em 1080p.
Texto recebido em `texto_narracao.txt`: 447 palavras. WAV recebido com 167,52 s,
44.100 Hz, estéreo, PCM de 16 bits, copiado para `audio/narracao_final.wav`.
Montagem em `cena_final.py`, sem cortar ou acelerar a voz. Duração final:
168,80 s (2min48,8s), 1080×1920, 30 fps. `sync.json` registra 166 ações
e 40 âncoras visuais; `legenda.srt` contém 66 entradas com o texto completo.
Tempos das legendas estimados por pausas do WAV e pesos silábicos, sem ASR.
Master e legendado: H.264 CRF 14, yuv420p, áudio AAC; 5.064 quadros cada.
QA: decodificação integral dos dois MP4s, 120 amostras visuais conferidas,
texto integral no SRT e pacotes AAC idênticos entre render e entregas.
Relatório em `revisao.md`; evidências em `qa_final/relatorio.json`.
Entrega: `entregas/Por Trás da Fórmula - EP 06 - Bernoulli - 0018/`.
V5 silenciosa preservada em sua mídia original. Capa não solicitada nesta rodada.
Todo o episódio em 2D, inclusive hook e exemplo horizontal final. Arsenal intacto.

Tubo e rótulos maiores; um único pacote ΔV conserva volume durante o percurso.
Derivar → guardar → reutilizar: W₁, W₂, Wₚ, m, ΔK e ΔUg alimentam as etapas
seguintes. MF-Tools seletivo em substituições, fatoração, cancelamento e
reorganização por estado. Cabeçalho do vid_0014, EP. 06; paleta aprovada.
V1, V2 e V3 preservadas. Hipóteses com mais respiro e CTA final discreto
“Segue o Parallax Lab / @labparallax” na V5 silenciosa. Na montagem com voz,
o CTA acompanha o áudio recebido: “Siga o Parallax Lab”.
Teste do arsenal: retirado da V3 e mantido fora da V4 por direção explícita;
o esquema 2D comunica melhor áreas, pressão, deslocamentos, velocidade e altura.
