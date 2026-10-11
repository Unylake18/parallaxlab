# Revisão final — vid_0018_bernoulli

## Resultado

Montagem final da V5 com o WAV novo fornecido pelo usuário, sem corte,
aceleração ou síntese de voz. 1080×1920 nativo, 30 fps, 168,80 s
(2min48,8s), 5.064 quadros. Master com voz e versão com legendas incorporadas:
H.264, CRF 14, yuv420p, AAC estéreo. Render intermediário sem perdas,
H.264 qp=0/yuv444p. V5 silenciosa preservada.

Áudio recebido: `K:/Downloads/ElevenLabs_Untitled_project (19).wav`.
Cópia em `audio/narracao_final.wav`: 167,52 s, 44.100 Hz, estéreo, PCM16.
SHA-256: `ef4e1c54d97f386150557902099e0225da6aa822e7c9169f8789d647ebc90573`.
Entrada do WAV em 0,40 s; priming AAC medido de 0,021333 s compensado no SRT.
Pico da fonte −3,86 dBFS; nenhuma amostra saturada.

Texto recebido: 447 palavras. Legenda com 66 entradas, até duas linhas,
sem omissões ou alterações no texto. Cores: pressão/força/trabalho em
ciano #35D9FF; velocidade/energia cinética em violeta #745CFF;
altura/energia gravitacional em magenta #EA63FF; área em azul #267BFF.
Demais palavras brancas. CTA acompanha a voz: “Siga o Parallax Lab”.

## Arquivos desta rodada

- `cena_final.py`: montagem derivada da V5, tempos guiados pela voz,
  CTA recebido, interpretação de pressão após as unidades e render sem perdas.
- `cena.py`: permite selecionar o nome do JSON de tempos; a montagem final
  não sobrescreve o histórico da V5 silenciosa.
- `gerar_sync.py`, `preparar_montagem.py`: alinhamento, SRT, 166 ações,
  40 âncoras visuais, durações quantizadas sem acúmulo de quadros.
- `legendas_cores.py`, `montar_final.py`: cores e exportação das duas entregas.
- `verificar_final.py`: QA integral de vídeo, áudio, texto e amostras visuais.
- `texto_narracao.txt`, `audio/narracao_final.wav`: material recebido.
  Texto anterior preservado em `texto_narracao_320.txt`.
- `ficha.md`, este relatório, JSONs de sincronização/execução e evidências de QA.

Nenhum arquivo global, dependência ou ambiente foi alterado.

## Verificações executadas

- `py_compile` dos scripts da montagem: passou.
- `git diff --check`: passou; somente aviso local de conversão LF/CRLF.
- Medição da cena e preview 540×960/15 fps sincronizado: concluídos.
- Render final `BernoulliFinal` em 1080×1920/30 fps: concluído.
- Agenda final contra execução: 166 ações coincidem, erro máximo menor
  que 0,001 s; duração real de 168,80 s.
- Decodificação integral dos dois MP4s: 5.064 quadros cada, sem erros.
- Verificação de codec, resolução, taxa de quadros, formato de pixel e CRF: passou.
- WAV da unidade conserva o SHA-256 da fonte. Voz integral, velocidade 1,0.
  Correlação da envoltória do áudio: 0,999916.
- Pacotes AAC idênticos entre render nativo, master e legendado.
- SRT reproduz as 447 palavras; até duas linhas e largura segura.
- 120 amostras finais inspecionadas: meio de cada uma das 66 legendas,
  estados prontos e meios das 21 transformações por glifos. Fórmulas,
  cores, sinais, estreitamento, hipóteses e CTA conferidos. Ajustada a
  distância entre unidades e explicação adicional de pressão.
- Preview: faixa reservada às legendas livre de conteúdo da cena.

Evidências: `qa_final/relatorio.json`, `qa_final/*.png` e 20 folhas de contato;
logs `render_final.log`, `montar_final.log`, `qa_final.log`.

## Entrega

Pasta: `entregas/Por Trás da Fórmula - EP 06 - Bernoulli - 0018/`.
`master - 0018.mp4`, `legendado - 0018.mp4`, `legenda - 0018.srt`,
`audio/`, `texto/` e manifesto com hashes. Empacotamento por
`uv run --no-sync --offline python videos/entregar.py vid_0018`.

## Limitações e escopo

O alinhamento das legendas usa pausas medidas e pesos silábicos, sem
reconhecimento automático de fala; os tempos de palavras são estimativas,
não uma transcrição fonética. As âncoras visuais seguem o áudio recebido.
Não há pendência de render, exportação ou integridade dos arquivos.
Capa não solicitada nesta rodada; nenhuma publicação executada.

Teste do arsenal: nenhum sólido 3D, conforme direção explícita da V5.
Geometria 2D mantida; resolução final 1080×1920. Sem custo ou peso de
sequências Blender; áreas, forças, deslocamentos e alturas permaneceram
legíveis no esquema aprovado. Nenhuma lacuna do arsenal identificada nesta unidade.
