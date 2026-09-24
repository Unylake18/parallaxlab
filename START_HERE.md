# START HERE — Parallax Lab

Manual curto para abrir antes de trabalhar. O guia completo está em `docs/guia_mestre.md`; a verdade operacional está em `docs/estado_atual.md`.

**Reconciliação de 2026-09-23:** `vid_0001` e `vid_0002` têm cena, narração,
SRT, capa e MP4s finais locais. Ambos passaram por QA técnico; reprodução
física em celular, backup externo dos MP4s e publicação não estão comprovados.
Veja os nomes exatos em `docs/estado_atual.md`. `vid_0003` está em revisão de
preview: teoria curta — de onde vem a fórmula da integração por partes?
## Setup já validado

- Windows + PyCharm
- Python 3.12
- `uv` e Python 3.12.4 da `.venv` validados; `uv run python -m manim --version` funciona
- Manim Community 0.21.0
- MiKTeX/`MathTex` funcionando
- primeiro MP4 já renderizado

Não reinstale, recrie o projeto ou rode `uv init` por rotina. Primeiro leia `docs/estado_atual.md` e preserve o que funciona.

## Primeiro ciclo

O `vid_0001` resolve:

\[
\int x^2e^x\,dx
\]

Ensinar integração por partes duas vezes e terminar conferindo pela derivada:

\[
\int x^2e^x\,dx=e^x(x^2-2x+2)+C.
\]

O piloto e o `vid_0002` são as duas primeiras unidades técnicas concluídas.
`vid_0002` resolve ∫2x cos(x²) dx = sin(x²) + C por substituição e regra da
cadeia concreta. Ambos permanecem sem publicação comprovada.

## Ciclo diário

`escolher questão → resolver → verificar → roteiro → Manim → voz → edição → QA → publicar → métricas`

Uma única regra: **não pule a verificação**. Para uma primitiva, derive o resultado. Em física, confira unidades, hipóteses, sinais e plausibilidade.

## Comandos principais

Na raiz do repositório:

```powershell
uv run python -m manim --version

# Preview vertical rápido
uv run python -m manim -p -r 540,960 --fps 15 videos/vid_0001_integracao_por_partes/cena.py Integral001

# Preview atual: origem da integração por partes, com coda
uv run python -m manim -r 540,960 --fps 15 videos/vid_0003_origem_integracao_por_partes/cena.py Integral003

# Render vertical final
uv run python -m manim -p -r 1080,1920 --fps 30 videos/vid_0001_integracao_por_partes/cena.py Integral001

git status
git add <arquivos>
git commit -m "tipo: resumo claro"
# Somente com autorização explícita
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
├── montar_master.py
├── montar_legendado.py
├── vid_0001_integracao_por_partes/
│   ├── cena.py
│   ├── ficha.md
│   ├── roteiro.md
│   ├── revisao.md
│   ├── legenda.srt
│   ├── capa_instagram.png
│   └── publicacao.md
└── vid_0002_integral_substituicao/  # mesmos documentos; áudio de montagem reproduzível

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
- [x] Versionar identidade, cena, narração e legendas do piloto; concluir QA técnico.
- [x] Produzir e conferir tecnicamente o segundo vídeo.
- [ ] Conferir ambos em tela física de celular e confirmar backup dos MP4s.
- [ ] Preparar textos por plataforma e publicar sem marca d’água cruzada.
- [ ] Registrar link/data, tempo de produção e métricas disponíveis.
- [ ] Atualizar `docs/estado_atual.md` e fazer commit/push.

## Primeiros dez vídeos

Mini-temporada inicial: **Cálculo + aplicações físicas**.

1. Exercício — \(\int x^2e^x\,dx\): integração por partes duas vezes.
2. Exercício — integral por substituição simples.
3. Teoria curta — de onde vem a fórmula da integração por partes?
4. Exercício — trabalhar explicitamente como escolher \(u\) em integração por partes.
5. Aplicação — derivada como velocidade instantânea.
6. Exercício — limite simples com interpretação visual.
7. Exercício — outra integração por partes, com estrutura diferente.
8. Teoria curta — o que uma integral realmente acumula.
9. Aplicação — de \(v(t)\) ao deslocamento usando integral.
10. Exercício — derivada ou integral aplicada a um problema curto de movimento.

Distribuição: **6 exercícios + 2 teorias curtas + 2 aplicações**.

Atualização editorial de 2026-09-23: a família de exercício do vídeo 4 é
preservada; seu enunciado ainda precisa ser definido. A antiga pauta
“derivada pela regra da cadeia” ficou **sem posição decidida**. Esta é uma
inconsistência editorial pendente, não uma exclusão definitiva nem autorização
para realocá-la. Vídeos 1, 2 e 5–10 e distribuição permanecem preservados.

Depois do vídeo 10: compare formatos, retenção e tempo de produção. Automatize apenas o gargalo que os dados mostrarem.

## Próxima ação

1. Confirmar QA físico em celular e backup externo dos finais dos vídeos 1 e 2.
2. Revisar o preview visual de `vid_0003`, incluindo a coda removível de 9 s;
   consultar `videos/vid_0003_origem_integracao_por_partes/revisao.md`.
   Não avançar para publicação. `vid_0004` deve trabalhar a escolha de u.
