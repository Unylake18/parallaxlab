"""Gera a pasta `abrir/`: um atalho .bat por sólido (abre no Blender) + `_escolher.bat` + `abrir/LEIA-ME.md`. Python puro.

    python experimentos/blender/arsenal/gerar_atalhos.py

Rode de novo depois de criar sólidos. O Blender é procurado em %BLENDER_EXE% e, se não existir, em
C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe (a mesma versão validada no projeto).
"""

import json
from pathlib import Path

AQUI = Path(__file__).resolve().parent
PASTA = AQUI / "abrir"

CABECALHO = (
    "@echo off\r\n"
    "setlocal\r\n"
    'set "BLENDER=%BLENDER_EXE%"\r\n'
    'if "%BLENDER%"=="" set "BLENDER=C:\\Program Files\\Blender Foundation\\Blender 5.2\\blender.exe"\r\n'
    'if not exist "%BLENDER%" (\r\n'
    "  echo Blender nao encontrado em %BLENDER%\r\n"
    "  echo Defina a variavel BLENDER_EXE com o caminho do blender.exe\r\n"
    "  pause\r\n"
    "  exit /b 1\r\n"
    ")\r\n"
)


def escrever(caminho, texto):
    with open(caminho, "w", encoding="utf-8", newline="") as f:
        f.write(texto)


def main():
    PASTA.mkdir(exist_ok=True)
    fichas = {f.stem: json.loads(f.read_text(encoding="utf-8")) for f in sorted((AQUI / "solidos").glob("*.json"))}
    for antigo in PASTA.glob("*.bat"):
        antigo.unlink()
    for k in fichas:
        escrever(PASTA / f"{k}.bat", CABECALHO + f'start "" "%BLENDER%" -P "%~dp0..\\abrir_no_blender.py" -- {k}\r\n')
    escrever(PASTA / "_escolher.bat", CABECALHO + "set /p ID=Id do solido (ex.: fio_infinito): \r\n"
             'start "" "%BLENDER%" -P "%~dp0..\\abrir_no_blender.py" -- %ID%\r\n')

    por_area = {}
    for k, f in fichas.items():
        por_area.setdefault(f["area"][0].split("/")[0], []).append((k, f))
    linhas = [
        "# Abrir os sólidos no Blender",
        "",
        "> Arquivo **gerado** por `gerar_atalhos.py` (rode de novo ao criar sólidos). Dê dois cliques no `.bat` do sólido: o Blender abre com ele",
        "> montado, enquadrado e em modo Renderizado; se tem movimento, o loop já toca (espaço pausa, setas andam um quadro).",
        "> `_escolher.bat` pergunta o id. Para mudar parâmetros: `blender.exe -P experimentos/blender/arsenal/abrir_no_blender.py -- <id> --set nome=valor`.",
        "> Os parâmetros e seus valores estão em `solidos/<id>.json`. Blender 5.2; se estiver em outro lugar, defina `BLENDER_EXE`.",
        "",
    ]
    for area in sorted(por_area):
        linhas += [f"## {area}", "", "| Atalho | Sólido | Status | Movimento |", "|---|---|---|---|"]
        for k, f in sorted(por_area[area]):
            anim = f.get("animacao")
            mov = "—" if not anim else ("ciclo único" if anim.get("ciclo") == "unico" else "loop")
            linhas.append(f"| [`{k}.bat`]({k}.bat) | {f['nome']} | {f['status']} | {mov} |")
        linhas.append("")
    escrever(PASTA / "LEIA-ME.md", "\n".join(linhas))
    print(f"OK: {len(fichas)} atalhos + _escolher.bat + LEIA-ME.md em {PASTA}")


if __name__ == "__main__":
    main()
