# VID20 · POR TRÁS DA FÓRMULA · EP.07 — entrega final

Arquivo para postagem: `final_legendado.mp4` — 1080×1920, 30 fps constantes, 5.154 quadros, 171,80 s, 26,42 MiB. Vídeo H.264 High, yuv420p, CRF 15; áudio AAC a 44,1 kHz, alvo de 320 kb/s (média medida de 229 kb/s). MP4 com faststart.

## Correção de fluidez

O preview sincronizado partia de um MP4 a 15 fps e esticava seus trechos. A entrega final foi renderizada diretamente da geometria e das equações em Full HD a 30 fps. Não usa os quadros do preview.

Os 43 marcos da narração distribuem o tempo entre 144 operações da cena. As transformações algébricas duram no máximo 37 quadros, ou 1,233 s. Tempo adicional fica nas pausas de leitura, após a limpeza dos objetos transitórios, em vez de prolongar o movimento. Pausas acompanhando explicações continuam presentes, inclusive durante a explicação da posição constante do corte.

As legendas coloridas são compostas antes da codificação dos quadros nativos. A montagem com o áudio copia o vídeo sem recodificá-lo. O ajuste final de timestamps elimina apenas o arredondamento do concat de clipes e mantém todos os quadros.

## Conferência executada

- Compilação dos quatro scripts locais; planejamento e validação matemática da cena original.
- Prova curta em 1080×1920/30 fps. Na separação dos termos, todos os 36 pares entre os 37 quadros apresentaram movimento.
- Render completo nativo e decodificação integral do MP4 entregue: resolução, 5.154 quadros, intervalos constantes de 1/30 s, perfil H.264 e duração de 171,80 s confirmados.
- Os 43 marcos conferem com a programação do áudio, com precisão de um quadro.
- Os 21 movimentos por mapa de glifos da parte algébrica tiveram mudança em todos os pares de quadros analisados na faixa das equações. Nenhum trecho de pouca mudança acima de 0,3 s foi detectado nesses movimentos.
- Inspeção visual de 55 estados ao longo de toda a unidade: base, altura e volume da coluna, refinamentos até 64×64, limite, cortes, integrações, primitivas, limites, sinais, resultado e encerramento. Legendas e fórmulas permanecem separadas.
- Os 72 blocos do SRT conservam o texto aprovado, sem sobreposição temporal, com largura segura na resolução final.
- WAV idêntico ao arquivo recebido, verificado por SHA-256. Áudio completo de 171,36 s; encerramento visual adicional de 0,44 s. A velocidade da gravação foi preservada.
- Payload H.264 idêntico antes e depois da montagem, confirmado por hash. Nenhum quadro foi reamostrado ou recodificado nessa etapa.
- `cena.py` original e previews anteriores preservados; fonte conferida por SHA-256.

## Arquivos desta etapa

Criados na unidade: `cena_final.py`, `planejar_final.py`, `timing_final.json`, `legenda_final.py`, `manim_final.cfg`, `montar_final.py`, `final_legendado.mp4` e este relatório. Atualizado: `ficha.md`, somente o estado e as referências da entrega final.

Artefatos de planejamento, prova, render, logs, métricas e imagens: `media/vid_0020_final/`. Relatório técnico: `media/vid_0020_final/qa_final.json`. Ficha anterior preservada nessa pasta.

As legendas mantêm o alinhamento aprovado por frases e pausas; os tempos internos das palavras seguem a estimativa silábica da etapa anterior. A análise de movimento distingue transformações das pausas intencionais de leitura. Não houve mudança de matemática, template global, dependências, commit ou push.
