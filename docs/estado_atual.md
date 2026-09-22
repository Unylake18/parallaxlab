# Estado atual — Parallax Lab

**Atualizado em:** 2026-09-22

**Marca:** Parallax Lab · **Instagram aprovado:** @labparallax

**Guia vigente:** `docs/guia_mestre.md`, versão 1.3, com nota de reconciliação de 2026-09-22.

**Fonte operacional:** este arquivo; identidade detalhada em `docs/identidade_visual.md`.

## Ambiente e repositório verificados

- Windows + PyCharm; Python 3.12; uv; Manim Community 0.21.0; MiKTeX/MathTex funcionais; renders MP4 já produzidos.
- Projeto local: `C:\Users\KaioOrtiz\PycharmProjects\manim-fisica`; branch `main`.
- Remoto `origin` configurado: `https://github.com/Unylake18/parallaxlab.git`. Configuração local conferida; estado online não consultado nesta reconciliação.
- HEAD local: `f372c1a` — `feat: adicionar helpers iniciais do template`. Existem alterações não commitadas em documentação, cena e dependências, além de assets e áudios não rastreados. Não confundir arquivos presentes com arquivos já versionados.
- Preservar o ambiente: não reinstalar, recriar `.venv`, executar `uv init` ou alterar dependências sem diagnóstico concreto. Alterações preexistentes em `pyproject.toml`/`uv.lock` foram preservadas nesta etapa.
- MVP: trabalhar em `main`, com commits pequenos; branch/PR para alterações maiores ou arriscadas. Nenhum commit/push nesta consolidação.

## Identidade: aprovado × implementado

**Aprovado:** marca e @ acima; símbolo de planos geométricos translúcidos deslocados com orbe central; linguagem científica, futurista, cósmica, elegante e limpa. Influência psicodélica leve, sem estética infantil, escolar genérica ou gamer.

**Paleta operacional inicial:** fundo `#050816`, ciano `#35D9FF`, azul `#267BFF`, violeta `#745CFF`, magenta `#EA63FF`, branco `#F5F7FF`. Extração/refinamento pelos assets ainda pendente. Tipografia exata ainda não escolhida/licenciada.

**Assets aprovados e presentes localmente:** oito PNGs na organização prevista abaixo. Em 2026-09-22, todos aparecem como untracked (`?? assets/branding/`), nenhum está staged, nenhum é retornado por `git ls-files assets/branding` e, portanto, nenhum está commitado. Funções em `docs/identidade_visual.md`; propriedades de exportação ainda não validadas.

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

**Implementado:** template vertical 9×16 e helpers `make_title`/`make_equation`. **Pendente:** aplicar a identidade aprovada ao template/piloto. A cena ainda usa fundo `#101820` e YELLOW/TEAL/GREEN, sem a integração de branding concluída. Prioridade: legibilidade → compreensão → matemática/física → identidade; logo discreto e faixa inferior livre.

## Vídeo atual e evidências

**vid_0001 / integral_001 — integração por partes**, em `videos/vid_0001_integracao_por_partes/cena.py`, classe `Integral001`.

\[
\int x^2e^x\,dx=e^x(x^2-2x+2)+C.
\]

Cena implementada com duas aplicações explícitas, motivação da escolha de u, distribuição do −2, expansão/fatoração e verificação pela derivada, recuperando x²eˣ. Smoke test preservado como `TemplateSmokeTest`.

- Voz via ElevenLabs, conforme briefing aprovado; sete blocos em `videos/vid_0001_integracao_por_partes/audio/`.
- `narracao_final.mp3`: **68,439 s**, incluindo seis pausas de 0,20 s. Originais preservados; sem mudança de pitch/velocidade.
- Preview mais recente: `media/qa_integral001_com_voz/Integral001_preview_sincronia_fina.mp4`, **68,933 s**, 540×960/15 fps, com **0,494 s** de respiro após o áudio.
- Microajustes guiados pelo texto exato e pelas pausas medidas já implementados. Frames inspecionados; áudio e vídeo copiados sem recodificação na última montagem. Evidências em `media/qa_integral001_com_voz/sincronia_fina/qa.json` e `contact_sheet.jpg`.
- Validação auditiva palavra a palavra e QA físico em celular **pendentes**. Não declarar aprovação audiovisual final.
- Legendas, render final e publicação **pendentes**. O preview já existe; não reiniciar sua produção nem a escolha da voz.

## Comandos e pipeline preservados

```powershell
# Preview já executado com sucesso
uv run python -m manim -p -r 540,960 --fps 15 videos/vid_0001_integracao_por_partes/cena.py Integral001

# Render final previsto, ainda pendente
uv run python -m manim -p -r 1080,1920 --fps 30 videos/vid_0001_integracao_por_partes/cena.py Integral001
```

Resolução explicitamente vertical; `config.frame_width = 9` e `config.frame_height = 16`. O render Manim é silencioso: o MP4 com voz foi montado depois usando as bibliotecas FFmpeg do PyAV existente; o executável `ffmpeg` não foi localizado na sessão anterior. Não instalar dependências por rotina. O piloto de aproximadamente 69 s substitui seu alvo antigo de 45–60 s, mantendo a voz como referência temporal.

## Estratégia e próxima ação

Primeiro ciclo aprovado: **10 vídeos — 6 exercícios, 2 teorias curtas, 2 aplicações**, em **Cálculo + aplicações físicas**. Não é um curso linear. Medir formato, retenção, clareza, interesse, tempo de produção e gargalos; ampliar automação somente após o ciclo e a identificação de um gargalo real.

### Capacidade futura planejada

**Status: PLANEJADA / NÃO IMPLEMENTADA.** O Parallax Lab possui como direção futura aprovada visualizações matemáticas dinâmicas, física animada ampliada, conteúdos de intuição e curiosidades e representações complementares ou sincronizadas de um mesmo fenômeno. Essa expansão não está implementada, não constitui pendência atual e não altera `vid_0001`, os dez primeiros vídeos ou a próxima ação operacional do MVP.

**Próxima ação concreta:** conferir as propriedades dos oito assets locais e definir a tipografia oficial compatível com uso comercial e Windows/Manim; então integrar a identidade ao template em uma unidade técnica própria, preservando a matemática e os timings do piloto.

**Pendências seguintes:** revisar/versionar assets e alterações locais em etapa autorizada; validar sincronização auditiva e legibilidade em celular; concluir legendas/edição, render final e QA; preparar publicação e regras atuais de plataforma. Nenhuma publicação confirmada.
