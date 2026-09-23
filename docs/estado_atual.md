# Estado atual — Parallax Lab

**Atualizado em:** 2026-09-23

**Marca:** Parallax Lab · **Instagram aprovado:** @labparallax

**Guia vigente:** `docs/guia_mestre.md`, versão 1.3, com nota de reconciliação de 2026-09-22.

**Fonte operacional:** este arquivo; identidade detalhada em `docs/identidade_visual.md`.

## Ambiente e repositório verificados

- Windows + PyCharm; Python 3.12; Manim Community 0.21.0 e MiKTeX/MathTex já usados em renders. O `uv` existe, mas o vínculo Python da `.venv` e o cache local apresentaram falha no último render; diagnosticar antes do próximo.
- Projeto local: `C:\Users\KaioOrtiz\PycharmProjects\manim-fisica`; branch `main`.
- Remoto `origin` configurado: `https://github.com/Unylake18/parallaxlab.git`.
- A consolidação foi organizada em commits locais na `main`; o push ficou
  pendente enquanto a exclusão de `media/` aguarda aprovação específica.
- A unidade de fechamento do `vid_0001` reúne a configuração visual, a cena, a narração final e a legenda no mesmo commit de produção.
- Preservar o ambiente: não reinstalar, recriar `.venv`, executar `uv init` ou alterar dependências sem diagnóstico concreto. `pyproject.toml` e `uv.lock` não possuem alterações locais.
- MVP: trabalhar em `main`, com commits pequenos; branch/PR para alterações maiores ou arriscadas.

## Identidade: aprovado × implementado

**Aprovado:** marca e @ acima; símbolo de planos geométricos translúcidos deslocados com orbe central; linguagem científica, futurista, cósmica, elegante e limpa. Influência psicodélica leve, sem estética infantil, escolar genérica ou gamer.

**Paleta operacional inicial:** fundo `#050816`, ciano `#35D9FF`, azul `#267BFF`, violeta `#745CFF`, magenta `#EA63FF`, branco `#F5F7FF`. Extração/refinamento pelos assets ainda pendente. Tipografia exata ainda não escolhida/licenciada.

**Assets aprovados e versionados:** os oito PNGs estão presentes na organização prevista abaixo, são rastreados pelo Git e já integram o histórico do repositório. Funções em `docs/identidade_visual.md`; propriedades finais de aplicação ainda dependem do contexto de uso.

```text
assets/branding/
├── master/
│   ├── parallax_lab_logo_master.png
│   ├── parallax_lab_icon_profile.png
│   ├── parallax_lab_icon_transparent.png
│   └── parallax_lab_logo_monochrome.png
├── social/
│   ├── parallax_lab_banner_16x9.png
│   └── parallax_lab_cover_template_9x16.png
└── overlays/
    ├── parallax_lab_watermark.png
    └── parallax_lab_logo_horizontal.png
```

**Implementado e aprovado:** template vertical 9×16, helpers `make_title`/`make_equation`, assets oficiais, paleta, watermark e composição do piloto. Prioridade: legibilidade → compreensão → matemática/física → identidade; logo discreto e faixa inferior livre.

## Unidades de produção concluídas tecnicamente

**vid_0001 / integral_001 — integração por partes**, em `videos/vid_0001_integracao_por_partes/cena.py`, classe `Integral001`.

\[
\int x^2e^x\,dx=e^x(x^2-2x+2)+C.
\]

Cena implementada com duas aplicações explícitas, motivação da escolha de u, distribuição do −2, expansão/fatoração e verificação pela derivada, recuperando x²eˣ. Smoke test preservado como `TemplateSmokeTest`.

- Manim, narração, identidade visual, composição, sincronização e legendas do `vid_0001` estão aprovados. Os sete blocos originais permanecem intactos; `narracao_final.mp3` preserva silêncio limpo de **0,700 s** entre os blocos 3 e 4.
- `legenda.srt` contém 29 cues aprovados, com até duas linhas e notação matemática escrita em Unicode.
- Finais locais em **1080×1920, 30 fps**, duração de **69,500 s**: `renders/vid_0001_integracao_por_partes_final_master_limpo.mp4` e `renders/vid_0001_integracao_por_partes_final_legendado.mp4`.
- QA técnico concluído: H.264 vertical, 2.085 frames, áudio AAC mono a 44,1 kHz completo, legendas presentes, watermark presente, safe area preservada e sem clipping ou sobreposição nos frames inspecionados.
- O QA e a verificação matemática estão consolidados em `videos/vid_0001_integracao_por_partes/revisao.md`; cena, narração, SRT, ficha, roteiro retrospectivo, capa e publicação pendente estão na unidade.
- A conferência visual por frames em 3, 8, 18, 25, 28, 32, 38, 45, 51, 58, 63 e 68 s confirmou equivalência de proporções e posicionamento com o preview aprovado. Reprodução física final em aparelho/plataforma permanece pendente.
- Publicação **não comprovada**; sem link ou data no repositório. Backup externo dos MP4s e reprodução física final em celular não foram verificados.

## Comandos e pipeline preservados

```powershell
# Preview já executado com sucesso
uv run python -m manim -p -r 540,960 --fps 15 videos/vid_0001_integracao_por_partes/cena.py Integral001

# Render final operacional
uv run python -m manim -p -r 1080,1920 --fps 30 videos/vid_0001_integracao_por_partes/cena.py Integral001
```

Resolução explicitamente vertical; `config.frame_width = 9` e `config.frame_height = 16`. O render Manim é silencioso: `videos/montar_master.py` e `videos/montar_legendado.py` documentam a montagem posterior com PyAV/Pillow. O executável `ffmpeg` não é necessário para esse fluxo.

Na execução final de 2026-09-22, o comando operacional com `uv run` não iniciou porque o cache local do uv apresentou erro e o executável Python vinculado pela `.venv` não estava disponível. Sem reinstalar ou alterar dependências, o mesmo módulo Manim 0.21.0 foi executado com o runtime Python 3.12 já existente e os pacotes da `.venv`; o master resultante passou no QA. O ambiente uv requer diagnóstico posterior antes do próximo render.

## vid_0002 — integral por substituição

Implementado em `videos/vid_0002_integral_substituicao/cena.py`, classe
`Integral002`: ∫ 2x cos(x²) dx = sin(x²) + C, com substituição explícita,
regra da cadeia no caso concreto, verificação aplicada, síntese derivada/integral
e coda sincronizada F/F′ removível. `Integral002SemCoda` encerra após a síntese.

Os finais locais são `renders/vid_0002_integral_substituicao_final_master_limpo.mp4`
e `renders/vid_0002_integral_substituicao_final_legendado.mp4`: **1080×1920,
30 fps, 2.083 frames e ~69,433 s**. O SRT final tem 25 entradas; áudio AAC de
**69,224 s**. A fonte original `audio/narracao_final.wav` (**71,024 s**) fica
intacta; `preparar_audio.py` reproduz byte a byte a versão final de montagem
`audio/narracao_montagem.wav`, com corte de 1,8 s de silêncio inicial e ajuste
de +1,2 dB somente entre 26,12–29,44 s. A matemática, CTA, coda e QA final
estão em `videos/vid_0002_integral_substituicao/revisao.md`; a publicação
permanece sem evidência. Capa e demais fontes estão na pasta da unidade.

Os dois vídeos são tecnicamente finalizados, mas a revisão física em celular,
o backup externo dos MP4s e a publicação não estão confirmados. Os MP4s ficam
em `renders/`, ignorado pelo Git; cenas, áudio, SRT, capas e documentação
ficam nas pastas versionadas. O template Manim não foi expandido nesta
consolidação. Aprendizados comparados em `docs/padroes_producao.md`.

Na limpeza local, previews/logs de `renders/` e duas cópias WAV intermediárias
foram removidos após auditoria. `media/` ainda guarda caches e QA históricos:
a revisão automática bloqueou a exclusão recursiva desses 920 arquivos.
O inventário por caminho, tamanho e classe está em
`renders/auditoria_limpeza_2026-09-23.csv`; nenhuma fonte ou MP4 final depende
desse diretório, mas a exclusão aguarda aprovação específica.

## Estratégia e próxima ação

Primeiro ciclo aprovado: **10 vídeos — 6 exercícios, 2 teorias curtas, 2 aplicações**, em **Cálculo + aplicações físicas**. Não é um curso linear. Medir formato, retenção, clareza, interesse, tempo de produção e gargalos; ampliar automação somente após o ciclo e a identificação de um gargalo real.

### Capacidade futura planejada

**Status: PLANEJADA / NÃO IMPLEMENTADA.** O Parallax Lab possui como direção futura aprovada visualizações matemáticas dinâmicas, física animada ampliada, conteúdos de intuição e curiosidades e representações complementares ou sincronizadas de um mesmo fenômeno. Essa expansão não está implementada, não constitui pendência atual e não altera `vid_0001`, os dez primeiros vídeos ou a próxima ação operacional do MVP.

**Próxima produção:** `vid_0003`, teoria curta sobre a escolha de `u` em integração por partes. Nenhuma cena, pasta, voz ou roteiro foi iniciado nesta consolidação. Antes de publicar os vídeos 1 e 2, fazer QA físico em celular e confirmar backup externo dos MP4s.

**Pendências seguintes:** diagnosticar o fluxo local do uv antes de novo render; definir a tipografia oficial; confirmar backup dos MP4s e QA físico em celular; preparar publicação e conferir regras atuais da plataforma. Nenhuma publicação confirmada no repositório.
