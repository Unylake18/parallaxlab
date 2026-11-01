# vid_0025 — relatório de entrega final (legendado embutido + master)

Data: 25/10/2026. Sem commit/push. Capa não aberta.

## Entrega

Pasta: `entregas/Da Equação ao Fenômeno - EP 07 - Por que o arco-íris tem 42° - 0025/`

| Arquivo | Conteúdo |
|---|---|
| `master - 0025.mp4` | 1080×1920, 30 fps, H.264 CRF **14,0** + AAC, 150,84 s (2:30,8), 20,4 MB |
| `legendado - 0025.mp4` | idem, com legenda colorida embutida (CRF 14), 150,84 s, 14,8 MB |
| `legenda - 0025.srt` | 69 blocos, tempo do vídeo |
| `audio/narracao_final - 0025.wav` | voz v5 original (146,2 s) |
| `audio/narracao_montagem - 0025.wav` | voz + 9 pausas (150,84 s) = áudio do master |
| `texto/` | ficha, texto da narração (v5), `narracao_sugestao` antiga (texto congelado do briefing, **não** é a v5) |
| `manifesto - 0025.json` | origem, tamanho, SHA-256 |

Também em `renders/`: `vid_0025_arco_iris_final_master_limpo.mp4`, `..._final_legendado.mp4`, `conferencia_legendado.png`, `vid_0025_final_frames_e_video.zip` (4.525 quadros em JPEG 540×960 + legendado + cena.py + srt; temporário, não versionar).

## Verificações

- **Render:** 1080×1920/30 fps, CRF 14,0 gravado no stream; 4.525 quadros = relógio da cena = renderer = plano de sincronia.
- **Sincronia (re-medida a 30 fps):** 70 âncoras; atraso máximo **−0,007 s**, mínimo −0,115 s, média −0,099 s (a imagem sempre começa antes da palavra; limite pedido 0,2 s de atraso). O plano a 30 fps difere do aprovado a 15 fps em no máximo 0,144 s.
- **Duração:** 150,84 s (2:30,8), limite 2:59.
- **Auditor de sobreposição (texto×texto, texto×traço, quadro e faixa da legenda), em todos os estados de leitura e no fim de cada trecho:** zero avisos.
- **Conferência visual do legendado** (`conferencia_legendado.png`): cores, posição e ausência de sobreposição nos pontos críticos (C07, C09, C10, CTA de C11).

## Legenda colorida (mesma cor da grandeza na tela)

| Cor | Termos |
|---|---|
| violeta `#745CFF` (i) | incidência · cinquenta e nove graus |
| magenta `#EA63FF` (r) | refração · refrata · "quarenta" de "refração de quarenta..." |
| ciano `#35D9FF` (θ, 42°) | quarenta e dois graus · máximo |
| vermelho `#FF4B4B` | vermelho · quarenta e dois vírgula quatro graus |
| violeta do arco `#9B5CFF` | violeta · quarenta vírgula seis |
| âmbar `#FFC857` | Sol · antissolar |

Frases coloridas com mais de uma palavra nunca quebram entre linhas (o SRT é gerado com isso em conta); `cores_legenda.py` alimenta `montar_legendado.py --color-module`.

## O que mudou depois da aprovação do preview

- Faixa da legenda: o estilo padrão ocupa y de −6,3 a −4,9; o auditor usava −5,65. Corrigido para −4,85 e o vídeo foi reajustado: gráfico e blocos de C07 (para cima), gráfico de zoom, mini-arco e frase de ordem das cores em C09, linha "TOPO DO ARCO…" e legendas de apoio de C10, ícones e CTA de C11. Mudança só de posição; tempos e sincronia idênticos.
- Render e plano de sincronia refeitos a 30 fps (relógio da cena passou a ler o fps do Manim).

## Pendências e avisos

- **`videos/entregar.py` não roda como está:** `videos/` é uma junção para o disco K: e o script resolve a raiz pelo caminho real (`K:\C_movidos`), onde não existe `videos/entregas_registro.json`. Rodei uma cópia temporária com a raiz fixada (script compartilhado não alterado). Vale corrigir `ROOT` (usar `.absolute()`) numa tarefa à parte.
- A voz não foi ouvida por mim; a legenda colorida foi conferida em quadros, não em reprodução contínua.
- `texto/narracao_sugestao - 0025.md` é o texto congelado antigo; a narração real é `texto_narracao - 0025.txt` (v5).
- Capa, texto de publicação e publicação continuam fechados.

Teste do arsenal: não se aplica (solido_3d: nenhum).
