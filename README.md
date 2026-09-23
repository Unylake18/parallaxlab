# Parallax Lab — Manim Física & Matemática

Repositório técnico para produção de vídeos educacionais de Física e Matemática com Manim.

## Ambiente validado

- Windows
- Python 3.12
- uv
- Manim Community 0.21.0
- MiKTeX / MathTex
- PyCharm

O Manim/MathTex já gerou os dois vídeos finais. O executável Python vinculado
à `.venv` e o cache local do `uv` apresentaram falha no último render;
diagnosticar antes de novo uso, sem reinstalação por rotina.

Não executar `uv init`, recriar `.venv` ou alterar dependências sem uma causa técnica diagnosticada.

## Estrutura

- `docs/` — documentação e estado operacional
- `template/` — configuração e componentes reutilizáveis do Manim
- `videos/` — fontes e documentos de cada vídeo; montagem de áudio/legenda
- `renders/` — MP4s finais locais, ignorados pelo Git; backup externo pendente

## Fonte operacional

Antes de alterar a infraestrutura, ler:

- `START_HERE.md`
- `docs/estado_atual.md`
- `docs/guia_mestre.md`
- `docs/identidade_visual.md`

`docs/estado_atual.md` registra o estado operacional após conferência do
filesystem e Git. `docs/padroes_producao.md` compara as duas unidades reais.

## Preview e final

Executar na raiz do projeto:

```powershell
uv run python -m manim -p -r 540,960 --fps 15 videos/vid_0001_integracao_por_partes/cena.py Integral001
```

Para o segundo vídeo, use
`videos/vid_0002_integral_substituicao/cena.py` e a classe `Integral002`.
O render final usa `-r 1080,1920 --fps 30`.
O render Manim é silencioso; `videos/montar_master.py` combina a cena e a
narração, e `videos/montar_legendado.py` aplica o SRT no master limpo.
Os dois finais de cada unidade ficam em `renders/` com sufixos
`_final_master_limpo.mp4` e `_final_legendado.mp4`.

## Git

Nos primeiros dez vídeos, trabalhar normalmente em `main` com commits pequenos e coerentes.

Branch/PR fica reservado para mudanças maiores, como dependências, refatoração relevante do template ou automações.
