# Estado atual do canal

**Atualizado em:** 2026-09-21  
**Guia vigente:** 1.2  
**START_HERE vigente:** 1.1

## Objetivo atual

Construir e publicar o primeiro piloto do canal faceless de Física & Matemática usando Manim:

\[
\int x^2e^x\,dx
\]

O vídeo deve ensinar integração por partes duas vezes, justificar a escolha de \(u=x^2\) e conferir a primitiva pela derivada.

**ID do piloto:** `vid_0001`  
**Nome de trabalho:** `integral_001`  
**Pasta planejada:** `videos/vid_0001_integracao_por_partes/`  
**Status:** ambiente e template vertical validados; preview técnico renderizado com sucesso; implementação do `vid_0001` ainda pendente.
## Ambiente validado

- Sistema operacional: Windows
- IDE: PyCharm
- Python: 3.12
- Gerenciador de projeto/dependências: `uv`
- `uv`: funcionando
- Manim Community: 0.21.0
- MiKTeX: instalado e funcional
- `MathTex`: funcionando
- Primeiro MP4 de teste: renderizado com sucesso
- Galaxy Tab S6 Lite: disponível para estudo, rascunho ou trechos manuscritos
- ChatGPT Plus: disponível
- Claude Pro: disponível
- Gemini Pro: disponível

### Observação

O primeiro MP4 validou o pipeline técnico básico `Python → Manim → LaTeX/MathTex → MP4`. Ele **não é ainda o piloto editorial completo**.

Não reinstalar Python, Manim, MiKTeX, recriar `.venv` ou rodar `uv init` sem um problema diagnosticado.

## Repositório

- Nome/local do projeto: `manim-fisica`
- Caminho local conhecido no Windows: `C:\Users\KaioOrtiz\PycharmProjects\manim-fisica`
- Git local: inicializado
- GitHub remoto: `origin`
- URL do repositório: `https://github.com/Unylake18/parallaxlab.git`
- Branch atual: `main`
- Primeiro commit da estrutura: `acd47bf` — `chore: organizar estrutura inicial do Parallax Lab`
- Último commit relevante: `6f467c2` — `docs: registrar repositório GitHub`
- Estratégia MVP: trabalhar em `main` com commits pequenos; usar branch/PR apenas para alterações maiores, arriscadas ou estruturais.

## Configuração de vídeo aprovada

Formato alvo:

- orientação: vertical 9:16
- preview: 540×960, 15 fps
- final: 1080×1920, 30 fps
- fundo: escuro
- alto contraste
- fórmulas grandes
- espaço inferior reservado para legenda/interface das plataformas

Configuração lógica no Manim:

```python
from manim import config

config.frame_width = 9
config.frame_height = 16
```

Comandos padrão planejados:

```powershell
# Preview vertical
uv run python -m manim -p -r 540,960 --fps 15 videos/vid_0001_integracao_por_partes/cena.py Integral001

# Render vertical final
uv run python -m manim -p -r 1080,1920 --fps 30 videos/vid_0001_integracao_por_partes/cena.py Integral001
```

## Solução-fonte do piloto

Primeira integração por partes:

\[
u=x^2,
\qquad
dv=e^x\,dx
\]

\[
du=2x\,dx,
\qquad
v=e^x
\]

Logo,

\[
I=\int x^2e^x\,dx
=x^2e^x-2\int xe^x\,dx.
\]

Segunda integração por partes:

\[
\int xe^x\,dx
=xe^x-\int e^x\,dx
=xe^x-e^x.
\]

Substituindo:

\[
I=x^2e^x-2(xe^x-e^x)+C
\]

\[
\boxed{I=e^x(x^2-2x+2)+C}.
\]

Verificação:

\[
\frac{d}{dx}\left[e^x(x^2-2x+2)\right]
=e^x(x^2-2x+2)+e^x(2x-2)
=x^2e^x.
\]

## Decisões vigentes

1. Canal faceless em português brasileiro.
2. Conteúdo curto, direto e objetivo.
3. Uma ideia central por vídeo.
4. Exercícios são a espinha dorsal; teoria curta e aplicações complementam.
5. O canal deve ajudar o responsável a estudar Física e Matemática enquanto produz conteúdo.
6. IA pode resolver, revisar, roteirizar e ajudar na animação, mas a matemática/física deve ter verificação objetiva.
7. O primeiro ciclo terá 10 vídeos: **6 exercícios + 2 teorias curtas + 2 aplicações**.
8. A primeira mini-temporada será coerente em torno de **Cálculo + aplicações físicas**.
9. O piloto será produzido primeiro com Manim; o Galaxy Tab pode entrar depois quando melhorar a didática.
10. `TransformMatchingTex` deve ser preferido quando termos matemáticos correspondentes precisam permanecer visualmente reconhecíveis.
11. Não automatizar publicação nem julgamento matemático/didático no MVP.
12. Só automatizar gargalos depois de dez vídeos comparáveis.

## Documentos vigentes

- `docs/decisoes.md` ← criado
- `START_HERE.md` ← usar conteúdo da versão `START_HERE_v1.1.md`
- `docs/estado_atual.md` ← este arquivo
- `docs/decisoes.md` ← ainda precisa ser criado/confirmado
- `docs/plataformas_AAAA-MM.md` ← criar quando começar a preparar publicação e monetização

## Próxima ação concreta

1. Validar o template vertical mínimo.
2. Adaptar o código de teste existente sem apagar a versão funcional.
3. Criar `cena.py` do piloto.
4. Renderizar preview vertical em 540×960/15 fps.
5. Conferir a cena em tela de celular.
6. Só depois avançar para narração, legendas, edição e render final.

## Pendências reais

- [x] Confirmar/inicializar Git no projeto local.
- [x] Criar repositório remoto no GitHub.
- [x] Registrar URL do GitHub.
- [x] Confirmar branch principal.
- [x] Fazer primeiro commit da estrutura/documentação.
- [x] Criar template vertical reutilizável.
- [ ] Criar helpers iniciais.
- [ ] Produzir preview do `vid_0001`.
- [ ] Aprovar roteiro de 45–60 segundos.
- [ ] Definir voz do piloto.
- [ ] Definir editor de vídeo do MVP.
- [ ] Criar regras atuais de publicação em `docs/plataformas_AAAA-MM.md`.
- [ ] Publicar o primeiro vídeo.

## Regra para próxima sessão

Antes de sugerir reinstalações, mudanças estruturais ou automações, leia este arquivo.  
Se alguma informação acima deixar de ser verdadeira, atualize este documento no mesmo ciclo de trabalho.
