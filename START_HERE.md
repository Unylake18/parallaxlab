# START HERE — Parallax Lab

Manual curto para abrir antes de trabalhar. O guia completo está em `docs/guia_mestre.md`; a verdade operacional está em `docs/estado_atual.md`.

**Reconciliação de 2026-09-22:** marca Parallax Lab, Instagram @labparallax. Identidade aprovada em `docs/identidade_visual.md`; oito assets presentes localmente, todos untracked, não staged e ainda não commitados. Template básico e piloto com voz já existem; aplicação do branding ao Manim ainda pendente. O preview mais recente tem 68,933 s; a voz aprovada substitui o alvo antigo de 45–60 s. Validação auditiva palavra a palavra e QA físico em celular continuam pendentes.
## Setup já validado

- Windows + PyCharm
- Python 3.12
- `uv` funcionando
- Manim Community 0.21.0
- MiKTeX/`MathTex` funcionando
- primeiro MP4 já renderizado

Não reinstale, recrie o projeto ou rode `uv init` por rotina. Primeiro leia `docs/estado_atual.md` e preserve o que funciona.

## Missão atual

Publicar `vid_0001` / `integral_001`:

\[
\int x^2e^x\,dx
\]

Ensinar integração por partes duas vezes e terminar conferindo pela derivada:

\[
\int x^2e^x\,dx=e^x(x^2-2x+2)+C.
\]

O piloto serve para validar **didática, ritmo, legibilidade, template, narração e pipeline**.

## Ciclo diário

`escolher questão → resolver → verificar → roteiro → Manim → voz → edição → QA → publicar → métricas`

Uma única regra: **não pule a verificação**. Para uma primitiva, derive o resultado. Em física, confira unidades, hipóteses, sinais e plausibilidade.

## Comandos principais

Na raiz do repositório:

```powershell
uv run python -m manim --version

# Preview vertical rápido
uv run python -m manim -p -r 540,960 --fps 15 videos/vid_0001_integracao_por_partes/cena.py Integral001

# Render vertical final
uv run python -m manim -p -r 1080,1920 --fps 30 videos/vid_0001_integracao_por_partes/cena.py Integral001

git status
git add <arquivos>
git commit -m "tipo: resumo claro"
git push origin main
```

Use 540×960/15 fps para iterar rápido. Só faça o render final em 1080×1920/30 fps quando o preview estiver aprovado.

No template/base scene, mantenha a área lógica vertical:

```python
from manim import config

config.frame_width = 9
config.frame_height = 16
```

## Estrutura mínima

```text
docs/
├── estado_atual.md       # o que é verdade agora
├── decisoes.md           # decisões estáveis
└── plataformas_AAAA-MM.md

template/
├── __init__.py
├── config.py
└── helpers.py            # layout e animações reutilizáveis

videos/
└── vid_0001_integracao_por_partes/
    ├── cena.py
    ├── ficha.md
    ├── roteiro.md
    ├── revisao.md
    ├── legenda.srt
    └── publicacao.md

renders/                  # arquivos pesados; backup externo
```

Nos primeiros dez vídeos, trabalhe diretamente em `main` com commits pequenos. Branch/PR só para template, dependências, automação ou mudança arriscada.

## Checklist do piloto

- [x] Resolver \(\int x^2e^x\,dx\) por partes duas vezes.
- [x] Derivar \(e^x(x^2-2x+2)+C\) e recuperar \(x^2e^x\).
- [x] Receber sete blocos de narração aprovados; piloto de aproximadamente 69 segundos.
- [x] Justificar a escolha de \(u=x^2\) pela redução do grau.
- [x] Animar passagens com `TransformMatchingTex` e `FadeOut`/`FadeIn` conforme a relação matemática.
- [x] Renderizar preview vertical com voz.
- [ ] Aplicar a identidade aprovada ao template e conferir em tela de celular.
- [ ] Validar sincronização auditiva e produzir/revisar legendas.
- [ ] Conferir matemática, áudio, legibilidade, resolução e começo/fim.
- [ ] Preparar textos por plataforma e publicar sem marca d’água cruzada.
- [ ] Registrar link/data, tempo de produção e métricas disponíveis.
- [ ] Atualizar `docs/estado_atual.md` e fazer commit/push.

## Primeiros dez vídeos

Mini-temporada inicial: **Cálculo + aplicações físicas**.

1. Exercício — \(\int x^2e^x\,dx\): integração por partes duas vezes.
2. Exercício — integral por substituição simples.
3. Teoria curta — como escolher \(u\) em integração por partes.
4. Exercício — derivada pela regra da cadeia.
5. Aplicação — derivada como velocidade instantânea.
6. Exercício — limite simples com interpretação visual.
7. Exercício — outra integração por partes, com estrutura diferente.
8. Teoria curta — o que uma integral realmente acumula.
9. Aplicação — de \(v(t)\) ao deslocamento usando integral.
10. Exercício — derivada ou integral aplicada a um problema curto de movimento.

Distribuição: **6 exercícios + 2 teorias curtas + 2 aplicações**.

Depois do vídeo 10: compare formatos, retenção e tempo de produção. Automatize apenas o gargalo que os dados mostrarem.

## Próxima ação

1. Conferir assets locais e definir tipografia comercial compatível com Windows/Manim.
2. Integrar a identidade aprovada ao template, preservando matemática e timings do piloto.
3. Validar sincronização auditiva e QA físico em celular.
4. Concluir legendas/edição, render final e QA antes de publicar.
