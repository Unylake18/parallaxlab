"""Ponte Blender -> Manim, camada 1 (Python puro, sem importar manim nem bpy): cache de sequências PNG com alpha.

Dado um sólido do arsenal e seus parâmetros, devolve a pasta com os quadros RGBA, renderizando no Blender só se a
sequência ainda não existir. A pasta fica em `renders/arsenal3d/<id>/<hash>/` (`renders/` é ignorado pelo Git).
O hash cobre a ficha, o padrão visual (`estilo.json`), o código dos construtores, os parâmetros, a resolução e os
quadros: mudou qualquer um, a sequência é regerada; não mudou, é reaproveitada.

Uso na linha de comando (a partir da raiz do repositório; roda com qualquer Python, não precisa do `.venv`):
    python experimentos/blender/arsenal/ponte.py --lista
    python experimentos/blender/arsenal/ponte.py fio_infinito --res 1920x1080 --frames 60
    python experimentos/blender/arsenal/ponte.py casca_cilindrica_oca --res 1920x1080
    python experimentos/blender/arsenal/ponte.py disco_carregado --set voltas=2 --forcar

A camada 2, `manim_solido3d.py`, usa este módulo dentro de uma cena Manim.
"""

import argparse
import glob
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[2]                       # arsenal -> blender -> experimentos -> raiz do repositório
CACHE = RAIZ / "renders" / "arsenal3d"
SOLIDOS = AQUI / "solidos"
NAO_CODIGO = {"ponte.py", "manim_solido3d.py", "exemplo_manim.py", "gerar_catalogo.py"}


def encontrar_blender():
    """Executável do Blender: variável PARALLAX_BLENDER, `blender` no PATH ou a instalação padrão do Windows."""
    cand = [os.environ.get("PARALLAX_BLENDER"), shutil.which("blender")]
    cand += sorted(glob.glob(r"C:\Program Files\Blender Foundation\Blender *\blender.exe"), reverse=True)
    for c in cand:
        if c and Path(c).exists():
            return str(c)
    raise FileNotFoundError("Blender não encontrado. Instale-o ou aponte PARALLAX_BLENDER para o blender.exe.")


def ler_ficha(solido):
    arq = SOLIDOS / f"{solido}.json"
    if not arq.exists():
        validos = ", ".join(sorted(p.stem for p in SOLIDOS.glob("*.json")))
        raise KeyError(f"Sólido '{solido}' não existe no arsenal. Válidos: {validos}")
    return json.loads(arq.read_text(encoding="utf-8"))


def parametros(ficha, params=None, animado=None):
    """Parâmetros finais = padrões da ficha + `params`; valida os nomes. `animado` liga `cargas_moveis`."""
    p = {k: v["valor"] for k, v in ficha["parametros"].items()}
    extra = dict(params or {})
    if animado is not None:
        if animado and "animacao" not in ficha:
            raise ValueError(f"'{ficha['id']}' não é animável (a ficha não tem bloco 'animacao').")
        if "cargas_moveis" in p:
            extra.setdefault("cargas_moveis", 1 if animado else 0)
    for nome, valor in extra.items():
        if nome not in p:
            raise KeyError(f"Parâmetro '{nome}' não existe em '{ficha['id']}'. Válidos: {', '.join(p)}")
        p[nome] = valor
    return p


def _codigo():
    arquivos = sorted(AQUI.parent.glob("*.py")) + sorted(AQUI.glob("*.py"))
    return b"".join(a.read_bytes() for a in arquivos if a.name not in NAO_CODIGO)


def chave(ficha, p, frames, res, amostras, alpha):
    h = hashlib.sha1()
    h.update(json.dumps(ficha, sort_keys=True, ensure_ascii=False).encode())
    h.update((AQUI / "estilo.json").read_bytes())
    h.update(_codigo())
    h.update(json.dumps([p, frames, res, amostras, alpha], sort_keys=True).encode())
    return h.hexdigest()[:12]


@dataclass
class Sequencia:
    solido: str
    pasta: Path
    frames: int
    animado: bool
    res: str
    alpha: bool

    def quadro(self, i):
        return self.pasta / f"frame_{(i % self.frames) + 1:04d}.png"


def _renderizar(blender, ficha, p, animado, frames, res, amostras, alpha, destino):
    sets = []
    for k, v in p.items():
        sets += ["--set", f"{k}={v}"]
    if animado:
        cmd = [blender, "-b", "-P", str(AQUI / "animar.py"), "--", ficha["id"], "--frames", str(frames),
               "--res", res, "--amostras", str(amostras), "--saida", str(destino), *sets]
    else:
        destino.mkdir(parents=True, exist_ok=True)
        cmd = [blender, "-b", "-P", str(AQUI / "renderizar.py"), "--", ficha["id"], "--res", res,
               "--amostras", str(amostras), "--saida", str(destino / "frame_0001.png"), *sets]
    if alpha:
        cmd.append("--alpha")
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise RuntimeError("Blender falhou (código %d):\n%s" % (r.returncode, "\n".join((r.stdout + r.stderr).splitlines()[-20:])))


def sequencia(solido, params=None, *, animado=None, frames=None, res="1920x1080", amostras=64, alpha=True,
              render="auto", forcar=False, log=print):
    """Devolve a `Sequencia` (pasta de quadros) do sólido, renderizando no Blender se faltar.

    animado: None = animado se a ficha permitir; True/False força. frames: quadros do loop (padrão: o da ficha, só
    para animado). render: "auto" renderiza se faltar; "nunca" falha com o comando para preparar antes."""
    ficha = ler_ficha(solido)
    if animado is None:
        animado = "animacao" in ficha
    p = parametros(ficha, params, animado=animado)
    n = int(frames or ficha.get("animacao", {}).get("frames_sugeridos", 60)) if animado else 1
    pasta = CACHE / solido / chave(ficha, p, n, res, amostras, alpha)
    seq = Sequencia(solido, pasta, n, bool(animado), res, alpha)

    pronto = (pasta / "meta.json").exists() and len(list(pasta.glob("frame_*.png"))) == n
    if pronto and not forcar:
        return seq
    if render == "nunca":
        raise FileNotFoundError(
            f"Sequência de '{solido}' não está pronta ({pasta}). Prepare antes com:\n  python "
            f"experimentos/blender/arsenal/ponte.py {solido} --res {res}" + (f" --frames {n}" if animado else ""))

    tmp = pasta.with_name(pasta.name + ".tmp")
    shutil.rmtree(tmp, ignore_errors=True)
    shutil.rmtree(pasta, ignore_errors=True)
    log(f"[arsenal3d] renderizando '{solido}' {res} ({n} quadro{'s' if n > 1 else ''}) no Blender...")
    t0 = time.perf_counter()
    _renderizar(encontrar_blender(), ficha, p, animado, n, res, amostras, alpha, tmp)
    meta = {"solido": solido, "params": p, "animado": bool(animado), "frames": n, "res": res, "amostras": amostras,
            "alpha": alpha, "hash": pasta.name, "segundos": round(time.perf_counter() - t0, 1),
            "criado": time.strftime("%Y-%m-%d %H:%M:%S")}
    (tmp / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.rename(pasta)                     # só vira cache quando está completo
    log(f"[arsenal3d] pronto em {meta['segundos']} s: {pasta}")
    return seq


def listar():
    """Sólidos animáveis e sequências já em cache."""
    animaveis = sorted(f.stem for f in SOLIDOS.glob("*.json") if "animacao" in json.loads(f.read_text(encoding="utf-8")))
    print("Animáveis (cargas em movimento):", ", ".join(animaveis))
    print("Em cache:")
    metas = sorted(CACHE.glob("*/*/meta.json")) if CACHE.exists() else []
    for m in metas:
        d = json.loads(m.read_text(encoding="utf-8"))
        print(f"  {d['solido']:<28} {d['res']:<10} {d['frames']:>3} quadro(s)  {d['hash']}  {m.parent}")
    if not metas:
        print("  (vazio)")


def main():
    ap = argparse.ArgumentParser(prog="ponte.py", description="Prepara a sequência PNG de um sólido do arsenal.")
    ap.add_argument("solido", nargs="?")
    ap.add_argument("--lista", action="store_true")
    ap.add_argument("--set", action="append", default=[], dest="overrides", help="nome=valor (repetível)")
    ap.add_argument("--frames", type=int)
    ap.add_argument("--res", default="1920x1080")
    ap.add_argument("--amostras", type=int, default=64)
    ap.add_argument("--estatico", action="store_true", help="um único quadro, sem movimento")
    ap.add_argument("--sem-alpha", action="store_true")
    ap.add_argument("--forcar", action="store_true", help="regera mesmo que já exista em cache")
    a = ap.parse_args()
    if a.lista or not a.solido:
        return listar()
    try:
        ficha = ler_ficha(a.solido)
        ov = {}
        for o in a.overrides:
            k, v = o.split("=", 1)
            tipo = type(ficha["parametros"].get(k, {"valor": ""})["valor"])
            ov[k] = tipo(float(v)) if tipo in (int, float) else v
        seq = sequencia(a.solido, ov, animado=False if a.estatico else None, frames=a.frames, res=a.res,
                        amostras=a.amostras, alpha=not a.sem_alpha, forcar=a.forcar)
    except (KeyError, ValueError, FileNotFoundError, RuntimeError) as e:
        print(f"ERRO: {e.args[0] if e.args else e}", file=sys.stderr)
        return 2
    print(seq.pasta)


if __name__ == "__main__":
    sys.exit(main())
