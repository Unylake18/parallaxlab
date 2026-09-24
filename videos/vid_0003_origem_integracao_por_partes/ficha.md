# vid_0003 — De onde vem a fórmula da integração por partes?

- Família: teoria curta; terceiro vídeo do primeiro ciclo.
- Mensagem: regra do produto reorganizada e integrada.
- Fonte editorial: briefing e storyboard do handoff aprovado em 2026-09-23.
- Pré-requisito: regra do produto e relação entre derivada e integral.
- Cena: `cena.py`, classe `Integral003`; alternativa `Integral003SemCoda`.
- Formato: área lógica 9×16, preview 540×960/15 fps.
- Planejamento visual: principal de 56 s; coda de 9 s; total de 65 s.
- Esta etapa: preview visual silencioso. Sem voz aprovada, SRT sincronizado,
  capa ou exportação final. Não há publicação autorizada.
- Template, ambiente e dependências existentes preservados.
- Comandos e evidências de QA: `revisao.md`; sequência implementada: `roteiro.md`.

## Solução-fonte e verificação

Para funções u(x) e v(x) continuamente diferenciáveis no intervalo considerado:

\[
(uv)'=u'v+uv',\qquad (uv)'dx=u'v\,dx+uv'\,dx.
\]

Converter termo a termo: (uv)'dx → d(uv); u'v dx = v u'dx → v du;
u v'dx → u dv. Portanto:

\[
d(uv)=v\,du+u\,dv,
\qquad u\,dv=d(uv)-v\,du,
\]
\[
\int u\,dv=\int d(uv)-\int v\,du,
\qquad \boxed{\int u\,dv=uv-\int v\,du}.
\]

Primitivas são entendidas até uma constante aditiva, como indicado discretamente
na tela. A fórmula aprovada é preservada. A derivada do lado direito é
u'v + uv' − vu' = uv', o integrando de u dv em relação a x. Os termos u'v
e vu' se cancelam pela comutatividade da multiplicação.

## Coda complementar e removível

Plano (u,v), U,V positivos, arco crescente contínuo da origem a (U,V),
sem equação atribuída na tela. A curva é desenhada por uma Bézier com controles
crescentes nas duas coordenadas. A região inferior corresponde à acumulação
∫v du; a região à esquerda do arco, complementar no retângulo, a ∫u dv.
As duas usam o mesmo contorno amostrado. A síntese UV = ∫v du + ∫u dv se
refere somente às acumulações desde a origem ao longo desse arco. Não são
integrais indefinidas arbitrárias nessa interpretação.

Não é apresentada como prova geral: título, hipótese visual e legenda de
escopo acompanham o desenho. Não há aula de áreas, exemplos adicionais ou
fórmula para a curva. Remover a coda não altera os primeiros 56 s.
