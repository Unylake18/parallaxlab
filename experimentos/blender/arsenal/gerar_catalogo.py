"""Gera catalogo.md a partir de solidos/*.json e valida as fichas. Python puro (sem Blender).

    python experimentos/blender/arsenal/gerar_catalogo.py
"""

import json
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
OBRIGATORIOS = ["id", "nome", "status", "area", "descricao", "leitura_visual", "usar_quando",
                "nao_usar_quando", "limitacoes", "construtor", "parametros", "enquadramento",
                "integracao", "preview", "origem"]
STATUS = {"planejado", "estudo", "aprovado"}


def carregar():
    fichas, erros = [], []
    construtores = (AQUI / "construtores.py").read_text(encoding="utf-8")
    for arq in sorted((AQUI / "solidos").glob("*.json")):
        f = json.loads(arq.read_text(encoding="utf-8"))
        falta = [k for k in OBRIGATORIOS if k not in f]
        if falta:
            erros.append(f"{arq.name}: campos ausentes {falta}")
            continue
        if f["id"] != arq.stem:
            erros.append(f"{arq.name}: id '{f['id']}' difere do nome do arquivo")
        if f["status"] not in STATUS:
            erros.append(f"{arq.name}: status inválido '{f['status']}'")
        if not re.search(rf'"{re.escape(f["construtor"])}"\s*:', construtores):
            erros.append(f"{arq.name}: construtor '{f['construtor']}' não está em construtores.py")
        if "animacao" in f:
            for k in ("cargas_moveis", "fase"):
                if k not in f["parametros"]:
                    erros.append(f"{arq.name}: tem 'animacao' mas falta o parâmetro '{k}'")
            for k in ("tipo", "frames_sugeridos"):
                if k not in f["animacao"]:
                    erros.append(f"{arq.name}: 'animacao' sem '{k}'")
        elif "cargas_moveis" in f["parametros"]:
            erros.append(f"{arq.name}: tem o parâmetro cargas_moveis mas não tem o bloco 'animacao'")
        if not (AQUI / f["preview"]).exists():
            erros.append(f"{arq.name}: preview ausente ({f['preview']})")
        fichas.append(f)
    return fichas, erros


CODIGO = ["../casca_oca.py", "../cilindro_macico.py", "../orbita_alpha.py", "construtores.py", "renderizar.py"]


def validar_estilo():
    """Cores referenciadas existem; nenhum hexadecimal solto no código do arsenal."""
    est = json.loads((AQUI / "estilo.json").read_text(encoding="utf-8"))
    erros, cores = [], set(est["cores"])
    refs = [m["cor"] for m in est["materiais"].values() if "cor" in m]
    refs += [m[k] for m in est["materiais"].values() for k in ("cor_perto", "cor_longe") if k in m]
    refs += [l["cor"] for l in est["iluminacao"].values()]
    erros += [f"estilo.json: cor '{c}' não existe em 'cores'" for c in refs if c not in cores]
    for rel in CODIGO:
        for n, linha in enumerate((AQUI / rel).read_text(encoding="utf-8").splitlines(), 1):
            if re.search(r"#[0-9A-Fa-f]{6}\b", linha):
                erros.append(f"{Path(rel).name}:{n}: hexadecimal solto no código (use estilo.json): {linha.strip()}")
    return est, erros


def secao_estilo(est):
    cores = "\n".join(
        f"| `{k}` | `{v['hex']}` | {v['papel']} |" for k, v in est["cores"].items())
    return f"""## Padrão visual

Fonte única: `estilo.json`. {est['fonte']}

| Cor | Hex | Papel |
|---|---|---|
{cores}

**Regras**
{lista(est['regras'])}

**Render:** Eevee, {est['render']['amostras']} amostras, view transform {est['render']['view_transform']}; preview
{est['render']['preview']['largura']}×{est['render']['preview']['altura']} a {est['render']['preview']['fps']} fps; final
{est['render']['final']['largura']}×{est['render']['final']['altura']} a {est['render']['final']['fps']} fps.
"""


def lista(itens):
    return "\n".join(f"- {i}" for i in itens)


def animacao(f):
    a = f.get("animacao")
    if not a:
        return ""
    custo = a.get("custo_1080p_s_por_frame")
    c = f"{custo} s/frame (1080p, com alpha)" if custo is not None else "não medido"
    return (f"\n**Animação (cargas em movimento):** `{a['tipo']}` · loop sem emenda (`fase` de 0 a 1) · "
            f"{a['frames_sugeridos']} quadros sugeridos · custo {c}\n")


def uso_manim(f):
    importa = "from manim_solido3d import Solido3D   # sys.path: experimentos/blender/arsenal"
    if "animacao" in f:
        chamada = f'img = Solido3D("{f["id"]}").mobject(cena=self, altura=5)   # cargas em loop; img.pausar() / img.retomar()'
    else:
        chamada = f'img = Solido3D("{f["id"]}").mobject(altura=5)   # estático: um quadro PNG com alpha'
    return "```python\n" + importa + "\n" + chamada + "\n```\n"


def secao(f):
    params = "\n".join(
        f"| `{k}` | {v['valor']} | {v['unidade']} | {v['descricao']} |" for k, v in f["parametros"].items())
    custo = f["integracao"].get("custo_1080p_s_por_frame")
    custo = f"{custo} s/frame (1080p, Eevee)" if custo is not None else "não medido"
    return f"""### `{f['id']}` — {f['nome']}

**Status:** {f['status']} · {f.get('status_nota', '')}

{f['descricao']}

![{f['nome']}]({f['preview']})

**Como se lê:** {f['leitura_visual']}

**Usar quando**
{lista(f['usar_quando'])}

**Não usar quando**
{lista(f['nao_usar_quando'])}

**Limitações**
{lista(f['limitacoes'])}

| Parâmetro | Padrão | Unid. | Descrição |
|---|---|---|---|
{params}

**Integração:** `{f['integracao']['formato_recomendado']}` · custo {custo}
{animacao(f)}
```powershell
& "C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe" -b -P experimentos\\blender\\arsenal\\renderizar.py -- {f['id']} --res 1920x1080 --alpha
```

**No Manim:**

{uso_manim(f)}
Ficha: `solidos/{f['id']}.json`
"""


def main():
    fichas, erros = carregar()
    est, erros_estilo = validar_estilo()
    erros += erros_estilo
    if erros:
        print("ERROS DE VALIDAÇÃO:")
        print("\n".join(f"  - {e}" for e in erros))
        sys.exit(1)

    por_area = {}
    for f in fichas:
        por_area.setdefault(f["area"][0], []).append(f)

    indice = "\n".join(
        f"| `{f['id']}` | {f['nome']} | {f['status']} | {', '.join(f['area'])} |" for f in fichas)
    corpo = "\n".join(secao(f) for f in fichas)
    texto = f"""# Arsenal de sólidos 3D (Blender)

> Arquivo **gerado** por `gerar_catalogo.py` a partir de `solidos/*.json`. Não edite à mão: edite a ficha e regere.

Cada sólido tem uma ficha com "usar quando / não usar quando". Consulte o índice, abra a ficha do que parecer
servir e confira os critérios antes de decidir. Status: `planejado` (só ideia), `estudo` (funciona, aparência
não aprovada), `aprovado` (pode entrar em vídeo).

| id | Nome | Status | Áreas |
|---|---|---|---|
{indice}

{secao_estilo(est)}
## Sólidos

{corpo}"""
    (AQUI / "catalogo.md").write_text(texto, encoding="utf-8")
    print(f"OK: {len(fichas)} sólidos validados -> catalogo.md")


main()
