"""Reúne os arquivos finais de uma unidade em UMA pasta de entregas, no padrão  «Série - EP NN - Assunto».

Uso, na raiz do repositório:
    uv run python videos/entregar.py vid_0016            # entrega uma unidade (prefixo do nome da pasta basta)
    uv run python videos/entregar.py --todos             # entrega todas as unidades do registro que já têm master
    uv run python videos/entregar.py vid_0016 --dry-run  # só mostra o que seria copiado
    uv run python videos/entregar.py --listar            # mostra o que cada unidade tem pronto

Pasta de destino: entregas/ na raiz (mude com a variável de ambiente PARALLAX_ENTREGAS). Pasta: «Série - EP NN - Assunto - 0016». Em todos os nomes de arquivo o número do vídeo (0001 em diante) vai no fim, antes da
extensão: «master - 0016.mp4». Dentro de cada entrega:
    master - 0016.mp4      versão final limpa, com a voz
    legendado - 0016.mp4   versão final com legendas coloridas
    legenda - 0016.srt     legendas (tempo do vídeo final)
    capa - 0016.png        capa escolhida (quando existir)
    audio/                 voz final (narracao_final - 0016.*, narracao_montagem - 0016.* quando houver)
    texto/                 ficha, roteiro, publicação, revisão e texto da narração
    manifesto - 0016.json  origem de cada arquivo, tamanho, SHA-256 e dados do vídeo (resolução, fps, duração)
Nada é movido nem apagado nas pastas de origem: é sempre cópia. Rodar de novo só copia o que mudou.
Série, episódio e assunto vêm de videos/entregas_registro.json ou, se a unidade não estiver lá, da ficha.md
('Série pública: NOME · EP. N' e o título '# Assunto').
"""
import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = Path(os.environ.get("PARALLAX_ENTREGAS", ROOT / "entregas"))
REGISTRO = json.loads((ROOT / "videos" / "entregas_registro.json").read_text(encoding="utf-8"))
SERIES = {"POR TRÁS DA FÓRMULA": "Por Trás da Fórmula", "DA EQUAÇÃO AO FENÔMENO": "Da Equação ao Fenômeno",
          "EXERCÍCIO RESOLVIDO": "Exercício Resolvido", "ABSURDO CALCULÁVEL": "Absurdo Calculável"}
IMG = {".png", ".jpg", ".jpeg", ".webp"}


def log(*a):
    sys.stdout.buffer.write((" ".join(str(x) for x in a) + "\n").encode("utf-8"))
    sys.stdout.flush()


def unidades():
    return sorted(p for pasta in ("videos", "videos_longos") for p in (ROOT / pasta).glob("*_*") if p.is_dir() and re.match(r"(vid|yt)_\d{4}", p.name))


def achar_unidade(nome):
    res = [p for p in unidades() if p.name == nome or p.name.startswith(nome)]
    if len(res) != 1:
        raise SystemExit(f"Unidade '{nome}' {'não encontrada' if not res else 'ambígua: ' + ', '.join(p.name for p in res)}")
    return res[0]


def limpar(s):
    return re.sub(r'\s+', " ", re.sub(r'[<>:"/\\|?*]', "", s)).strip(" .")


def identidade(un):
    """(série, episódio, assunto, inferido) da unidade."""
    r = REGISTRO.get(un.name)
    if r:
        return r["serie"], int(r["ep"]), r["assunto"], bool(r.get("inferido"))
    ficha = (un / "ficha.md").read_text(encoding="utf-8") if (un / "ficha.md").is_file() else ""
    m = re.search(r"(POR TRÁS DA FÓRMULA|DA EQUAÇÃO AO FENÔMENO|EXERCÍCIO RESOLVIDO|ABSURDO CALCULÁVEL)\s*[·•]\s*EP\.?\s*(\d+)", ficha)
    t = re.search(r"^#\s+(.+)$", ficha, re.M)
    if not (m and t):
        raise SystemExit(f"{un.name}: sem entrada em videos/entregas_registro.json e sem 'Série pública: NOME · EP. N' + '# Assunto' na ficha.md")
    return m.group(1), int(m.group(2)), t.group(1).strip().rstrip("?"), False


def numero(un):
    """Número do vídeo para o fim dos nomes: 0016 (vid_0016...) ou yt0001 (vídeos longos)."""
    m = re.match(r"(vid|yt)_(\d{4})", un.name)
    return m.group(2) if m.group(1) == "vid" else f"yt{m.group(2)}"


def com_numero(rel, un):
    """'capas/capa_01.png' -> 'capas/capa_01 - 0016.png' (o número vai no fim do nome, antes da extensão)."""
    p = Path(rel)
    return (p.parent / f"{p.stem} - {numero(un)}{p.suffix}").as_posix()


def pasta_entrega(un):
    serie, ep, assunto, _ = identidade(un)
    return BASE / limpar(f"{SERIES.get(serie, serie.title())} - EP {ep:02d} - {assunto} - {numero(un)}")


def candidatos(un, tipo):
    """Arquivos finais possíveis (nas pastas da unidade e em renders/ da raiz), do mais novo para o mais antigo."""
    if tipo == "master":
        padroes = ("*postagem_master*.mp4", "*final_master_limpo*.mp4", "*master*.mp4")
    else:
        padroes = ("*postagem_legendado*.mp4", "*final_legendado*.mp4", "*legendado*.mp4")
    achados = {}
    for pasta in (un / "renders", ROOT / "renders"):
        if not pasta.is_dir():
            continue
        for pad in padroes:
            for f in pasta.glob(pad):
                if f.name.startswith(un.name[:8]) and "sem_audio" not in f.name and "preview" not in f.name:
                    achados[f] = f.stat()
    return sorted(achados, key=lambda f: (achados[f].st_mtime_ns, achados[f].st_size), reverse=True)


def escolher(un, tipo):
    fixo = REGISTRO.get(un.name, {}).get(tipo)
    cands = candidatos(un, tipo)
    if fixo:
        return ROOT / fixo, [c for c in cands if c != ROOT / fixo]
    return (cands[0], cands[1:]) if cands else (None, [])


def sha256(f):
    h = hashlib.sha256()
    with open(f, "rb") as fh:
        for bloco in iter(lambda: fh.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def info_video(f):
    try:
        import av
        with av.open(str(f)) as c:
            v = c.streams.video[0]
            return {"largura": v.width, "altura": v.height, "fps": round(float(v.average_rate), 3), "duracao_s": round(float(c.duration) / 1e6, 2),
                    "audio": bool(c.streams.audio)}
    except Exception as e:  # noqa: BLE001
        return {"erro": str(e)}


def copiar(origem, destino, dry):
    """Copia só se faltar ou tiver mudado (tamanho/data). Devolve True se copiou."""
    if destino.exists() and destino.stat().st_size == origem.stat().st_size and destino.stat().st_mtime_ns >= origem.stat().st_mtime_ns:
        return False
    if not dry:
        destino.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(origem, destino)
    return True


def entregar(un, dry=False):
    master, alt_m = escolher(un, "master")
    leg, alt_l = escolher(un, "legendado")
    if master is None and leg is None:
        log(f"{un.name}: sem master nem legendado finais; nada a entregar")
        return None
    serie, ep, assunto, inferido = identidade(un)
    dest = pasta_entrega(un)
    plano = []          # (origem, destino relativo, categoria)
    if master:
        plano.append((master, "master.mp4", "video"))
    if leg:
        plano.append((leg, "legendado.mp4", "video"))
    if (un / "legenda.srt").is_file():
        plano.append((un / "legenda.srt", "legenda.srt", "legenda"))
    capa_fixa = REGISTRO.get(un.name, {}).get("capa")
    capa = (ROOT / capa_fixa) if capa_fixa else next((p for p in sorted(un.glob("capa_instagram*.png"))), None)
    if capa and capa.is_file():
        plano.append((capa, "capa.png", "capa"))
    # só a capa escolhida entra na entrega; propostas e alternativas ficam fora
    for f in sorted((un / "audio").glob("narracao_final.*")) + sorted((un / "audio").glob("narracao_montagem.*")):
        plano.append((f, f"audio/{f.name}", "audio"))
    for nome in ("ficha.md", "roteiro.md", "publicacao.md", "revisao.md", "texto_narracao.txt", "narracao_sugestao.md"):
        if (un / nome).is_file():
            plano.append((un / nome, f"texto/{nome}", "texto"))
    copiados, itens = 0, []
    for origem, rel, cat in plano:
        rel = com_numero(rel, un)
        copiou = copiar(origem, dest / rel, dry)
        copiados += copiou
        item = {"arquivo": rel, "origem": origem.relative_to(ROOT).as_posix(), "bytes": origem.stat().st_size, "categoria": cat}
        if cat in ("video", "legenda", "audio"):
            item["sha256"] = sha256(origem)
        if cat == "video":
            item.update(info_video(origem))
        itens.append(item)
    manifesto = {"unidade": un.name, "serie": SERIES.get(serie, serie), "ep": ep, "assunto": assunto, "serie_inferida": inferido,
                 "gerado_em": datetime.now().isoformat(timespec="seconds"), "arquivos": itens,
                 "versoes_finais_nao_copiadas": [f.relative_to(ROOT).as_posix() for f in alt_m + alt_l],
                 "observacao": "Cópia; as origens não foram alteradas. Rodar videos/entregar.py de novo atualiza só o que mudou."}
    if not dry:
        dest.mkdir(parents=True, exist_ok=True)
        (dest / com_numero("manifesto.json", un)).write_text(json.dumps(manifesto, ensure_ascii=False, indent=2), encoding="utf-8")
    aviso = " [série/EP inferidos: confirmar]" if inferido else ""
    outras = f" | outras versões finais não copiadas: {len(alt_m) + len(alt_l)}" if (alt_m or alt_l) else ""
    log(f"{'(simulação) ' if dry else ''}{dest.relative_to(BASE.parent) if BASE.parent in dest.parents else dest}: {len(plano)} arquivos, {copiados} copiados{aviso}{outras}")
    return manifesto


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("unidade", nargs="?", help="vid_NNNN (ou prefixo do nome da pasta)")
    ap.add_argument("--todos", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--listar", action="store_true")
    a = ap.parse_args()
    if a.listar:
        for un in unidades():
            m, _ = escolher(un, "master")
            l, _ = escolher(un, "legendado")
            try:
                nome = pasta_entrega(un).name
            except SystemExit:
                nome = "(sem identidade)"
            log(f"{un.name:48s} master={'sim' if m else 'não':3s} legendado={'sim' if l else 'não':3s} -> {nome}")
        return
    if a.todos:
        for un in unidades():
            try:
                entregar(un, a.dry_run)
            except SystemExit as e:
                log(f"{un.name}: {e}")
        return
    if not a.unidade:
        ap.error("informe a unidade (ex.: vid_0016) ou use --todos / --listar")
    entregar(achar_unidade(a.unidade), a.dry_run)


if __name__ == "__main__":
    main()
