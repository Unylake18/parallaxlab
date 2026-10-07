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

Regerar o catálogo depois de editar uma ficha:

```powershell
python experimentos\blender\arsenal\gerar_catalogo.py
```

## Status das fichas

- `planejado`: só ideia. Sem construtor.
- `estudo`: funciona e foi renderizado, aparência ainda não aprovada.
- `aprovado`: pode entrar em vídeo.

Aprovados (2026-10-07): `casca_cilindrica_oca`, `cilindro_macico_isolante`, `casca_esferica_oca`, `esfera_macica_isolante`, `placa_infinita_carregada`, `cilindro_coaxial`, `gaussiana_esferica`, `gaussiana_cilindrica`, `gaussiana_caixa`, `anel_carregado`, `disco_carregado` e `haste_carregada`. Promover um sólido é decisão do usuário.

## Como adicionar um sólido

1. Escrever o construtor em `construtores.py` e registrá-lo em `CONSTRUTORES`.
2. Criar `solidos/<id>.json` (copiar uma ficha existente; o `id` deve igualar o nome do arquivo).
3. Rodar `renderizar.py -- <id>` para gerar o preview.
4. Rodar `gerar_catalogo.py`: ele recusa fichas incompletas, sem construtor ou sem preview.

## Fila sugerida (nada disto existe ainda)

Derivada de `docs/mapa_curricular.md`. Ordem de prioridade é decisão sua.

| Área | Candidatos |
|---|---|
| Lei de Gauss | esfera maciça isolante, casca esférica oca, placa/plano infinito, cilindro coaxial, superfícies gaussianas (esférica, cilíndrica, caixa) |
| Campo elétrico | anel carregado, disco carregado, haste carregada |
| Ampère | fio infinito, solenoide, toroide |
| Mecânica | aro, disco, haste (momento de inércia); esfera/cilindro/aro rolando |
| Cálculo | sólido de revolução (discos/anéis; cascas cilíndricas) |

## Registro nos `.md` globais (aplicado em 2026-10-07)

- `AGENTS.md`, em "Consulte conforme necessidade": manda consultar `catalogo.md` antes de modelar um sólido novo
  (só `aprovado` serve) e avisa que usar um sólido num vídeo exige handoff, pois ainda não há helper de integração.
- `docs/formatos.md`, em "Ficha padrão": campo opcional `solido_3d:` (id do arsenal ou `nenhum`, com justificativa),
  nos formatos curto e longo.

Fichas de vídeos já existentes não foram alteradas.
