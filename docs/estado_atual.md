# Estado atual — Parallax Lab

**Atualizado em:** 2026-09-22

**Marca:** Parallax Lab · **Instagram aprovado:** @labparallax

**Guia vigente:** `docs/guia_mestre.md`, versão 1.3, com nota de reconciliação de 2026-09-22.

**Fonte operacional:** este arquivo; identidade detalhada em `docs/identidade_visual.md`.

## Ambiente e repositório verificados

- Windows + PyCharm; Python 3.12; uv; Manim Community 0.21.0; MiKTeX/MathTex funcionais; renders MP4 já produzidos.
- Projeto local: `C:\Users\KaioOrtiz\PycharmProjects\manim-fisica`; branch `main`.
- Remoto `origin` configurado: `https://github.com/Unylake18/parallaxlab.git`.
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

## Vídeo atual e evidências

**vid_0001 / integral_001 — integração por partes**, em `videos/vid_0001_integracao_por_partes/cena.py`, classe `Integral001`.

\[
\int x^2e^x\,dx=e^x(x^2-2x+2)+C.
\]

Cena implementada com duas aplicações explícitas, motivação da escolha de u, distribuição do −2, expansão/fatoração e verificação pela derivada, recuperando x²eˣ. Smoke test preservado como `TemplateSmokeTest`.

- Manim, narração, identidade visual, composição, sincronização e legendas do `vid_0001` estão aprovados. Os sete blocos originais permanecem intactos; `narracao_final.mp3` preserva silêncio limpo de **0,700 s** entre os blocos 3 e 4.
- `legenda.srt` contém 29 cues aprovados, com até duas linhas e notação matemática escrita em Unicode.
- Master local produzido em **1080×1920, 30 fps**, com duração de **69,500 s**: `renders/vid_0001_integracao_por_partes_final.mp4`.
- QA técnico concluído: H.264 vertical, 2.085 frames, áudio AAC mono a 44,1 kHz completo, legendas presentes, watermark presente, safe area preservada e sem clipping ou sobreposição nos frames inspecionados.
- Evidências do QA: `media/qa_integral001_final/qa_final.json`, `media/qa_integral001_final/master_final_contact_sheet.jpg` e `media/qa_integral001_final/preview_vs_master_contact_sheet.jpg`.
- A conferência visual por frames em 3, 8, 18, 25, 28, 32, 38, 45, 51, 58, 63 e 68 s confirmou equivalência de proporções e posicionamento com o preview aprovado. Reprodução física final em aparelho/plataforma permanece pendente.
- Publicação **pendente**. O vídeo não foi publicado em nenhuma plataforma.

## Comandos e pipeline preservados

```powershell
# Preview já executado com sucesso
uv run python -m manim -p -r 540,960 --fps 15 videos/vid_0001_integracao_por_partes/cena.py Integral001

# Render final operacional
uv run python -m manim -p -r 1080,1920 --fps 30 videos/vid_0001_integracao_por_partes/cena.py Integral001
```

Resolução explicitamente vertical; `config.frame_width = 9` e `config.frame_height = 16`. O render Manim é silencioso: áudio e legendas são aplicados depois com PyAV, preservando timebase de áudio `1/44100`. O executável `ffmpeg` não é necessário para esse fluxo.

Na execução final de 2026-09-22, o comando operacional com `uv run` não iniciou porque o cache local do uv apresentou erro e o executável Python vinculado pela `.venv` não estava disponível. Sem reinstalar ou alterar dependências, o mesmo módulo Manim 0.21.0 foi executado com o runtime Python 3.12 já existente e os pacotes da `.venv`; o master resultante passou no QA. O ambiente uv requer diagnóstico posterior antes do próximo render.

## Estratégia e próxima ação

Primeiro ciclo aprovado: **10 vídeos — 6 exercícios, 2 teorias curtas, 2 aplicações**, em **Cálculo + aplicações físicas**. Não é um curso linear. Medir formato, retenção, clareza, interesse, tempo de produção e gargalos; ampliar automação somente após o ciclo e a identificação de um gargalo real.

### Capacidade futura planejada

**Status: PLANEJADA / NÃO IMPLEMENTADA.** O Parallax Lab possui como direção futura aprovada visualizações matemáticas dinâmicas, física animada ampliada, conteúdos de intuição e curiosidades e representações complementares ou sincronizadas de um mesmo fenômeno. Essa expansão não está implementada, não constitui pendência atual e não altera `vid_0001`, os dez primeiros vídeos ou a próxima ação operacional do MVP.

**Próxima ação concreta:** realizar a reprodução física final em celular e preparar a publicação do master aprovado, sem declarar publicação antes de sua execução.

**Pendências seguintes:** diagnosticar o fluxo local do uv antes de novo render; definir a tipografia oficial; executar QA físico final em celular; preparar publicação e conferir regras atuais da plataforma. Nenhuma publicação confirmada.
