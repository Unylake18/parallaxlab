# Arsenal de sólidos 3D (Blender) — Parallax Lab

Biblioteca de sólidos reutilizáveis, descritos por fichas JSON, que qualquer vídeo pode consultar para decidir se algum
serve **antes** de modelar algo novo. Fase atual: sandbox (`experimentos/blender/arsenal/`), sem uso em vídeo.

## Estrutura

| Caminho | Papel |
|---|---|
| `solidos/<id>.json` | **Fonte única de verdade** de cada sólido: parâmetros, usar/não usar quando, enquadramento, custo, status |
| `catalogo.md` | Índice legível, **gerado** das fichas (não editar à mão) |
| `previews/<id>.png` | Preview 960×540 de cada sólido, gerado pelo próprio arsenal |
| `construtores.py` | id da ficha → função que cria o sólido no Blender |
| `renderizar.py` | Constrói e renderiza qualquer sólido a partir da ficha |
| `gerar_catalogo.py` | Valida as fichas e regera `catalogo.md` (Python puro, sem Blender) |

## Fluxo

Consultar: abrir `catalogo.md`, ler "Usar quando / Não usar quando" dos candidatos, conferir o preview.

Renderizar (a partir da raiz do repositório):

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\renderizar.py -- cilindro_macico_isolante --set n_cargas=60 --res 1920x1080 --alpha
```

Animar (só sólidos com `cargas_moveis` na ficha; `fase` de 0 a 1 percorre um loop que fecha sem emenda):

```powershell
& "C:\Program Files\Blender Foundation\Blender 5.2\blender.exe" -b -P experimentos\blender\arsenal\animar.py -- fio_infinito --frames 60 --res 1920x1080 --alpha --saida caminho\da\pasta
```

Regerar o catálogo depois de editar uma ficha:

```powershell
python experimentos\blender\arsenal\gerar_catalogo.py
```

## Uso no Manim (ponte)

Os sólidos entram numa cena Manim como **sequências PNG com alpha** renderizadas pelo Blender e guardadas em cache
em `renders/arsenal3d/<id>/<hash>/` (`renders/` é ignorado pelo Git). A ponte tem duas camadas:

| Arquivo | Papel |
|---|---|
| `ponte.py` | Python puro (sem Manim nem Blender no import): cache, hash, chamada ao Blender. Também é um CLI. |
| `manim_solido3d.py` | Classe `Solido3D` para a cena: devolve um `ImageMobject` com fundo transparente. |
| `exemplo_manim.py` | Exemplo e teste de integração (sólido animado com Manim atrás e na frente, FadeIn, pausa). |

Em uma cena (a partir da raiz do repositório):

```python
import sys
sys.path.insert(0, "experimentos/blender/arsenal")
from manim_solido3d import Solido3D

class MinhaCena(Scene):
    def construct(self):
        fio = Solido3D("fio_infinito")                              # animado (cargas em loop) se a ficha permitir
        img = fio.mobject(cena=self, altura=5, centro=RIGHT * 3)    # cena=self é obrigatório se animado
        self.play(FadeIn(img)); self.wait(4)                        # 2 loops de 2 s (periodo=2.0)
        img.pausar(); img.retomar(); img.set_fase(0.25)

        self.play(FadeIn(Solido3D("casca_cilindrica_oca").mobject(altura=4)))   # estático: um quadro
```

Pontos que importam:

- **Prepare antes do render final**: a primeira chamada de um sólido/resolução renderiza no Blender (de segundos a
  1 min); as seguintes só leem do disco. Comando: `python experimentos/blender/arsenal/ponte.py <id> --res 1920x1080`
  (`--lista` mostra o que existe; `--frames`, `--set nome=valor`, `--estatico`, `--forcar`). Em máquina sem Blender o
  cache não existe (ele não vai para o Git): use `Solido3D(..., render="nunca")` para falhar com o comando certo.
- **Resolução**: por padrão a do render do Manim (preview 960x540 e final 1920x1080 geram sequências separadas, cada
  uma no tamanho certo). O fundo é transparente: o que estiver atrás do sólido aparece.
- **Cache automático**: o hash cobre a ficha, `estilo.json`, o código dos construtores, os parâmetros, a resolução e
  os quadros. Mudou qualquer um, regera; qualquer mudança de código em `experimentos/blender/*.py` invalida todas as
  sequências (é grosseiro de propósito: nunca serve imagem velha).
- **Fase pelo tempo da cena**: o movimento é calculado de `cena.time`, não somando `dt`. Motivo medido: durante um
  `FadeIn`/`FadeOut` aplicado ao próprio mobject o Manim chama o updater duas vezes por quadro, e somar `dt` faria o
  movimento andar em dobro. O loop fecha sem emenda (verificado sem compressão: diferença 0,0 entre quadros de mesma fase).
- **Ciclo único** (`animacao.ciclo = "unico"`, ex.: `colisao_1d`): a fase 1 NÃO repete a fase 0. `animar.py` e a ponte renderizam as fases 0 a 1 incluindo o final, e `Solido3D` congela no último quadro em vez de repetir. Todos os outros movimentos são loops sem emenda.
- **O que o 3D não diz**: sentido da corrente e sinal das cargas. Desenhe seta e rótulo em Manim por cima.
- **Custo e peso**: veja a linha "Animação" de cada sólido no `catalogo.md` (0,5 a 1,3 s por quadro em 1080p; 60 quadros
  pesam de ~36 MB a ~100 MB por sólido, e levam de ~30 s a ~80 s no Blender).
- **Fora do escopo**: nada disto toca `template/`. Usar um sólido num vídeo continua exigindo handoff (ver `AGENTS.md`).

## Status das fichas

- `planejado`: só ideia. Sem construtor.
- `estudo`: funciona e foi renderizado, aparência ainda não aprovada.
- `aprovado`: pode entrar em vídeo.

Aprovados pelo usuário em 2026-10-07: todos os 41 sólidos atuais. Promover um sólido é decisão do usuário; a lista viva está no `catalogo.md`.

## Como adicionar um sólido

1. Escrever o construtor em `construtores.py` e registrá-lo em `CONSTRUTORES`.
2. Criar `solidos/<id>.json` (copiar uma ficha existente; o `id` deve igualar o nome do arquivo).
3. Rodar `renderizar.py -- <id>` para gerar o preview.
4. Rodar `gerar_catalogo.py`: ele recusa fichas incompletas, sem construtor ou sem preview.

## Fila: o que falta de 3D (levantamento de 2026-10-07)

Fonte: leitura integral de `docs/mapa_curricular.md` contra os 41 sólidos existentes. Nada desta lista está construído.
Critério para entrar: o objeto tem de **ganhar** com a terceira dimensão ou com a ponte (movimento sincronizado); o que
é gráfico, equação ou diagrama plano fica no Manim. **Antes de começar os itens marcados com ⚠, decidir a convenção
visual pendente** (ver "Decisões pendentes").

### A. Alto valor (3D essencial; reaproveita o que já existe)

| id sugerido | Capítulo do mapa | O que mostra | Reuso / observação |
|---|---|---|---|
| `onda_eletromagnetica` ⚠ | 6.12, 7.1 | E e B perpendiculares oscilando e a direção de propagação (Poynting) | setas de `vetores3d`, loop por fase; precisa da cor de B |
| `particula_em_campo_magnetico` ⚠ | 6.7 | hélice de uma partícula em B uniforme (raio ciclotrônico, passo) | curva viva + campo ciano; sinal da carga |
| `espira_em_campo_magnetico` ⚠ | 6.7 | torque e momento de dipolo de uma espira girando em B | `anel_carregado` + setas |
| `ima_espira_inducao` ⚠ | 6.10 | ímã atravessando uma espira (fluxo, Lenz) | polos N/S; loop de ida e volta |
| `barra_trilhos_fem_movimento` ⚠ | 6.10 | barra deslizando em trilhos num campo B | `colisao_1d` (trilho) + setas |
| `biot_savart_espira` | 6.8 | dl, r, P no eixo e dB numa espira | `anel_carregado` + setas |
| `equipotenciais` ⚠ | 6.4 | superfícies de potencial (esferas concêntricas; dipolo) em violeta translúcido | construção violeta como as gaussianas; dipolo precisa do sinal |
| `produto_vetorial` | 10.1 | a, b, a×b e o paralelogramo (área) | `vetores3d` |
| `plano_tangente` | 10.3 | superfície, plano tangente e linearização | `superficie_parametrizada` |
| `superficie_quadrica` | 10.1 | elipsoide, hiperboloides, paraboloides e cone | `malha_param` |
| `pontos_criticos` | 10.6 | máximo, mínimo e sela com o plano tangente horizontal | `gradiente_colina` |
| `integral_dupla_colunas` | 10.7 | soma de Riemann 3D (colunas sob a superfície) | novo; refinamento por fase |
| `elemento_volume` | 10.8, 10.9 | elemento dV em cartesianas, cilíndricas e esféricas | novo |
| `orbital_atomico` | 7.11 | nuvens de probabilidade s, p e d | novo: amostragem de pontos |
| `paisagem_potencial` | 4.8 | bola numa pista U(x): poço simples, duplo, barreira | `poco_gravitacional`; liga ao `vid_0013` |
| `giroscopio_precessao` ⚠ | 4.11 | pião girando com precessão e L, torque | vetor de momento angular |
| `cone_de_luz` | 7.6 | cone de luz no espaço-tempo (2+1) | superfície de revolução |

### B. Valor médio (úteis; entram conforme a pauta pedir)

| Capítulo | Candidatos |
|---|---|
| 4.4, 4.5, 4.12 Mecânica | `plano_inclinado` (bloco numa rampa), `rampa_rolamento` (corpos descendo), `trilho_looping` |
| 4.6 | `movimento_circular` (massa num fio), `curva_inclinada` (pista com inclinação) |
| 4.10 | `colisao_2d`, `explosao` (fragmentos e centro de massa) |
| 5.6, 5.7 Fluidos | `tanque_hidrostatico` com empuxo, `prensa_hidraulica`, `tanque_torricelli` (jato) |
| 7.2 a 7.5 Óptica | `espelho_esferico`, `dioptro_plano` (Snell e reflexão interna), `rede_de_difracao` (generalizar a fenda dupla para N fendas), `filme_fino`, `interferometro_michelson`, `polarizador_malus` |
| 6.1, 6.2, 6.5 | `cargas_pontuais` ⚠, `dipolo_eletrico` ⚠, `linhas_de_campo_3d`, `condutor_com_cavidade` |
| 11.2, 11.8 | `integral_de_linha` (trabalho num caminho 3D), `divergencia_local` (cubo elementar), `rotacional_roda_de_pas` |
| 10.6 | `lagrange_restricao` |
| 7.6, 7.11 | `relogio_de_luz`, `atomo_bohr` |
| Futuros (13 a 15) | `transformacao_linear_3d` (cubo → paralelepípedo, determinante), `autovetores_elipsoide`, `membrana_modos` (modos de um tambor) |

### C. Não recomendado em 3D (melhor no Manim)

Cinemática 1D, lançamentos e envoltórias, diagramas de corpo livre, polias, trabalho e potência, circuitos DC, RC, RL e
RLC, diagramas P×V, ciclo de Carnot e entropia, condução térmica (exigiria uma escala de cor de temperatura), limites,
derivadas, integrais e séries, curvas paramétricas e polares planas, EDOs e planos de fase, funções de onda 1D (poço
infinito, tunelamento), Planck e efeito fotoelétrico, decaimento radioativo.

### Decisões pendentes (bloqueiam os itens com ⚠)

1. **Sinal da carga (+ e −)**: o padrão não codifica o sinal em cor. Opções: sinal em geometria (um "+" e um "−"
   esculpidos na esfera), ou só por rótulo no Manim. Afeta dipolo, Coulomb, equipotenciais do dipolo e partícula em B.
2. **Cor do campo magnético B**: o ciano é o campo E. Proposta: B em magenta `#EA63FF` (já na paleta, sem uso 3D) e
   o ciano para E.
3. **Vetores de velocidade, força e momento angular**: proposta de branco neutro `#F5F7FF`, como as tangentes do
   cálculo vetorial, deixando o ciano só para campos.
4. **Polos N e S do ímã**: proposta de duas metades de azuis diferentes, com N e S por rótulo no Manim.


## Registro nos `.md` globais (aplicado em 2026-10-07)

- `AGENTS.md`, em "Consulte conforme necessidade": manda consultar `catalogo.md` antes de modelar um sólido novo
  (só `aprovado` serve) e avisa que usar um sólido num vídeo exige handoff, pois ainda não há helper de integração.
- `docs/formatos.md`, em "Ficha padrão": campo opcional `solido_3d:` (id do arsenal ou `nenhum`, com justificativa),
  nos formatos curto e longo.

Fichas de vídeos já existentes não foram alteradas.
