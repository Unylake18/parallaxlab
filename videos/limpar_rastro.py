"""Apaga o rastro de construção de uma unidade JÁ ENTREGUE em entregas/ (vídeos, quadros, zips, logs, cache do Manim).

Uso, na raiz do repositório:
    uv run python videos/limpar_rastro.py vid_0030             # simulação: mostra o que sairia (padrão)
    uv run python videos/limpar_rastro.py vid_0030 --apagar    # apaga de verdade
    uv run python videos/limpar_rastro.py --todos [--apagar]   # todas as unidades que já têm master em entregas/

Fica: tudo o que está no Git (código, ficha, roteiro, parâmetros), áudio, textos/JSON/SRT soltos e a pasta da entrega
(master, legendado, legenda, capa, audio/, texto/, manifesto). Sai (só arquivos fora do Git, sem seguir junções), em todos os
checkouts do repositório (principal e worktrees):
    - vídeos (.mp4 .mov .webm .mkv .avi), .zip e .log em qualquer lugar da unidade;
    - imagens dentro de pastas de rastro (renders, qa, media*, frames*, q3d, quadros*, preview*, prancha*, capas_*, stills*, public, out);
    - pastas inteiras media*/ (cache do Manim), node_modules/ e __pycache__/;
    - em renders/ da raiz, o que começa com o prefixo da unidade (vid_0030..., yt_0016...);
    - zips dentro da pasta da entrega (quadros para o GPT).
Recusa a unidade se não houver master na entrega ou se algum arquivo dela foi gravado na última hora (render em andamento).
Tudo o que for apagado vai para entregas/limpezas.log; o manifesto da entrega ganha "rastro_limpo_em".
"""
import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

sys.path.insert(0, str(Path(__file__).parent))
from entregar import BASE, ROOT, achar_unidade, log, numero, unidades  # noqa: E402

VIDEO = {".mp4", ".mov", ".webm", ".mkv", ".avi"}
SEMPRE = VIDEO | {".zip", ".log"}
IMG = {".png", ".jpg", ".jpeg", ".webp", ".exr", ".tif", ".tiff", ".bmp", ".gif"}
PASTA_RASTRO = re.compile(r"^(renders?|qa|media.*|frames.*|q3d|quadros.*|previews?.*|pranchas?.*|capas_.*|stills.*|public|out)$", re.I)
PASTA_INTEIRA = re.compile(r"^(media.*|node_modules|__pycache__)$", re.I)
RECENTE_S = 3600


def arquivos(raiz):
    """(caminho, stat) de todo arquivo sob raiz, sem entrar em junções/links."""
    pilha = [raiz]
    while pilha:
        d = pilha.pop()
        try:
            with os.scandir(d) as it:
                for e in it:
                    if e.is_junction() or e.is_symlink():
                        continue
                    if e.is_dir():
                        pilha.append(e.path)
                    else:
                        try:
                            yield Path(e.path), e.stat()
                        except OSError:
                            pass
        except OSError:
            pass


def checkouts():
    saida = subprocess.run(["git", "-C", str(ROOT), "worktree", "list", "--porcelain"], capture_output=True, text=True, encoding="utf-8").stdout
    return [Path(l[9:]) for l in saida.splitlines() if l.startswith("worktree ") and Path(l[9:]).is_dir()]


def rastreados(checkout):
    saida = subprocess.run(["git", "-C", str(checkout), "ls-files", "-z"], capture_output=True, text=True, encoding="utf-8").stdout
    return {s.replace("/", os.sep).lower() for s in saida.split("\0") if s}


def pasta_entrega(un):
    """Pasta em entregas/ que tem «master - NNNN.mp4» desta unidade (curtos e longos)."""
    # O número se repete entre curtos e longos (vid_0027 × yt_0027): vale a pasta cujo manifesto diz "unidade" = esta unidade.
    # Pasta sem manifesto legível só é aceita se for a única candidata; manifesto de outra unidade nunca é aceito.
    alvo = f"master - {numero(un)}.mp4"
    sem_manifesto = []
    for f, st in arquivos(BASE):
        if f.name != alvo or st.st_size == 0:
            continue
        donos = []
        for m in f.parent.glob("manifesto*.json"):
            try:
                donos.append(json.loads(m.read_text(encoding="utf-8")).get("unidade"))
            except (OSError, ValueError):
                pass
        if un.name in donos:
            return f.parent
        if not any(donos):
            sem_manifesto.append(f.parent)
    return sem_manifesto[0] if len(sem_manifesto) == 1 else None


def eh_rastro(rel):
    partes = rel.parts[:-1]
    ext = rel.suffix.lower()
    if ext in SEMPRE or any(PASTA_INTEIRA.match(p) for p in partes):
        return True
    return ext in IMG and any(PASTA_RASTRO.match(p) for p in partes)


def plano(un):
    """Lista (arquivo, bytes) a apagar, ou levanta SystemExit com o motivo da recusa."""
    entrega = pasta_entrega(un)
    if entrega is None:
        raise SystemExit(f"{un.name}: sem master em entregas/; nada é apagado antes da entrega")
    agora, itens = time.time(), []
    prefixo = re.compile(rf"^{re.escape(un.name[:8] if un.name.startswith('vid') else un.name[:7])}[_.\-]", re.I)
    for co in checkouts():
        dentro = co / un.relative_to(ROOT)
        no_git = rastreados(co)
        if dentro.is_dir():
            for f, st in arquivos(dentro):
                if agora - st.st_mtime < RECENTE_S:
                    raise SystemExit(f"{un.name}: {f} foi gravado há menos de 1 h (render em andamento?); nada apagado")
                rel = f.relative_to(co)
                if str(rel).lower() not in no_git and eh_rastro(f.relative_to(dentro)):
                    itens.append((f, st.st_size))
        renders = co / "renders"
        if renders.is_dir() and not renders.is_junction():
            for e in renders.iterdir():
                if prefixo.match(e.name) and not e.is_junction():
                    itens += [(f, st.st_size) for f, st in arquivos(e)] if e.is_dir() else [(e, e.stat().st_size)]
    itens += [(f, st.st_size) for f, st in arquivos(entrega) if f.suffix.lower() == ".zip"]
    return entrega, itens


def resumo(itens, raiz_unidade):
    grupos = {}
    for f, s in itens:
        try:
            chave = "/".join(f.relative_to(raiz_unidade).parts[:2][:-1] or ["(raiz)"])
        except ValueError:
            chave = str(f.parent)
        grupos[chave] = grupos.get(chave, 0) + s
    return sorted(grupos.items(), key=lambda x: -x[1])


def apagar_vazias(raiz):
    for d, subs, arqs in os.walk(raiz, topdown=False):
        p = Path(d)
        if p != raiz and not p.is_junction() and not any(p.iterdir()):
            p.rmdir()


def limpar(un, apagar=False):
    entrega, itens = plano(un)
    total = sum(s for _, s in itens)
    log(f"{'' if apagar else '(simulação) '}{un.name}: {len(itens)} arquivos, {total / 2**30:.2f} GB  | entrega: {entrega.name}")
    for chave, s in resumo(itens, un)[:12]:
        if s >= 2**20:
            log(f"    {s / 2**30:7.2f} GB  {chave}")
    if not apagar or not itens:
        return total
    feitos = 0
    with open(BASE / "limpezas.log", "a", encoding="utf-8") as fh:
        fh.write(f"\n# {datetime.now().isoformat(timespec='seconds')} {un.name}: {len(itens)} arquivos, {total / 2**30:.2f} GB\n")
        for f, s in itens:
            try:
                if f.stat().st_mode & 0o200 == 0:
                    os.chmod(f, 0o666)
                f.unlink()
                feitos += s
                fh.write(f"{s}\t{f}\n")
            except OSError as e:
                fh.write(f"ERRO\t{f}\t{e}\n")
    for co in checkouts():
        for raiz in (co / un.relative_to(ROOT), co / "renders"):
            if raiz.is_dir() and not raiz.is_junction():
                apagar_vazias(raiz)
    for m in entrega.glob("manifesto*.json"):
        try:
            texto = m.read_text(encoding="utf-8")
        except UnicodeDecodeError:   # manifestos antigos gravados em cp1252: não reescrever
            continue
        dados = json.loads(texto)
        dados["rastro_limpo_em"] = datetime.now().isoformat(timespec="seconds")
        m.write_text(json.dumps(dados, ensure_ascii=False, indent=2 if "\n" in texto else None), encoding="utf-8")
    log(f"    apagado: {feitos / 2**30:.2f} GB (lista em entregas/limpezas.log)")
    return feitos


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("unidade", nargs="?", help="vid_NNNN / yt_NNNN (ou prefixo do nome da pasta)")
    ap.add_argument("--todos", action="store_true", help="todas as unidades que já têm master em entregas/")
    ap.add_argument("--apagar", action="store_true", help="apaga de verdade (sem isto, só simula)")
    a = ap.parse_args()
    if not (a.unidade or a.todos):
        ap.error("informe a unidade (ex.: vid_0030) ou use --todos")
    soma = 0
    for un in (unidades() if a.todos else [achar_unidade(a.unidade)]):
        try:
            soma += limpar(un, a.apagar)
        except SystemExit as e:
            if not a.todos or "sem master" not in str(e):
                log(str(e))
    if a.todos:
        log(f"Total {'apagado' if a.apagar else 'que sairia'}: {soma / 2**30:.2f} GB")


if __name__ == "__main__":
    main()
