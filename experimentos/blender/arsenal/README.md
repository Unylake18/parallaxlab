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
| `gerar_cobertura.py` | Gera `cobertura.md`: o que existe e o que falta por capítulo do mapa curricular |
| `abrir/<id>.bat` | Atalho de dois cliques: abre o sólido já montado na janela do Blender (loop tocando, se animado); índice em `abrir/LEIA-ME.md` |
| `abrir_no_blender.py` | Script que os atalhos chamam (monta o sólido na interface, câmera + modo Renderizado) |
| `gerar_atalhos.py` | Gera `abrir/*.bat` e `abrir/LEIA-ME.md` a partir das fichas (rode de novo ao criar sólidos) |

## Abrir no Blender para ver

Dois cliques em `abrir/<id>.bat` (ou `abrir/_escolher.bat`, que pergunta o id): o Blender abre com o sólido montado, na câmera do
enquadramento da ficha, em modo Renderizado, e o loop já toca (espaço pausa, setas ← → andam um quadro). Vale o estado do preview
(`preview_set`); para outro estado: `blender.exe -P experimentos/blender/arsenal/abrir_no_blender.py -- <id> --set nome=valor`. Se o
Blender não estiver em `C:\Program Files\Blender Foundation\Blender 5.2`, defina a variável de ambiente `BLENDER_EXE`. Nada é
salvo: para guardar a cena, use Arquivo → Salvar (os `.blend` ficam fora do Git).

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

## O que falta de 3D e a cobertura por capítulo

A lista completa, por capítulo do mapa curricular, com o status de cada sólido, o que falta, o assunto e a limitação, está
em **`cobertura.md`** (gerado por `gerar_cobertura.py`: o status vem das fichas, as lacunas ficam no script).

A fila A do levantamento de 2026-10-07 (17 sólidos de alto valor) foi construída e aprovada em 2026-10-07 (o `ima_espira_inducao` foi ajustado depois e aprovado). A **fila B** (30 sólidos: mecânica, fluidos, eletricidade, óptica, física moderna, cálculo,
álgebra linear e EDP) foi construída e aprovada no mesmo dia. Sobram só duas lacunas 3D (centro de massa e campos
conservativos): veja `cobertura.md`, seção 2a.

### Convenções visuais decididas pelo usuário (2026-10-07)

1. **Sinal da carga**: esculpido na geometria (um "+" ou "−" em relevo na esfera, virado para a câmera): `carga_sinal` em
   `vetores3d.py`. Sólidos com cargas de sinal chamam `orientar_glifos` no gancho `apos_camera`.
2. **Campo magnético B = magenta `#EA63FF`**; o ciano segue só para o campo elétrico E.
3. **Velocidade, força, torque e momento angular = branco neutro** `#F5F7FF`.
4. **Polos do ímã**: N = azul, S = magenta (o nome N/S vai por rótulo no Manim). Atenção: o magenta serve ao B e ao polo S;
   no `ima_espira_inducao` não há linhas de B justamente para não confundir as duas leituras.


## Registro nos `.md` globais (aplicado em 2026-10-07)

- `AGENTS.md`, em "Consulte conforme necessidade": manda consultar `catalogo.md` antes de modelar um sólido novo
  (só `aprovado` serve) e avisa que usar um sólido num vídeo exige handoff, pois ainda não há helper de integração.
- `docs/formatos.md`, em "Ficha padrão": campo opcional `solido_3d:` (id do arsenal ou `nenhum`, com justificativa),
  nos formatos curto e longo.

Fichas de vídeos já existentes não foram alteradas.
