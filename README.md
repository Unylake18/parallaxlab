# Parallax Lab — Manim Física & Matemática

Repositório técnico para produção de vídeos educacionais de Física e Matemática com Manim.

## Ambiente validado

- Windows
- Python 3.12
- uv
- Manim Community 0.21.0
- MiKTeX / MathTex
- PyCharm

O ambiente já está funcionando.

Não executar `uv init`, recriar `.venv` ou alterar dependências sem uma causa técnica diagnosticada.

## Estrutura

- `docs/` — documentação e estado operacional
- `template/` — configuração e componentes reutilizáveis do Manim
- `videos/` — arquivos de cada vídeo
- `renders/` — previews e renders exportados

## Fonte operacional

Antes de alterar a infraestrutura, ler:

- `START_HERE.md`
- `docs/estado_atual.md`
- `docs/guia_mestre.md`

`docs/estado_atual.md` prevalece quando houver divergência sobre o estado atual do projeto.

## Preview

Executar na raiz do projeto:

```powershell
uv run python -m manim -p -r 540,960 --fps 15 videos/vid_0001_integracao_por_partes/cena.py Integral001
```

## Render final

```powershell
uv run python -m manim -p -r 1080,1920 --fps 30 videos/vid_0001_integracao_por_partes/cena.py Integral001
```

## Git

Nos primeiros dez vídeos, trabalhar normalmente em `main` com commits pequenos e coerentes.

Branch/PR fica reservado para mudanças maiores, como dependências, refatoração relevante do template ou automações.
