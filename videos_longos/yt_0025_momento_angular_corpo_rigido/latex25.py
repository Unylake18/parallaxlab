"""Conversão local com cwd explícito: evita caminhos extensos no dvisvgm/Windows."""
import subprocess
from pathlib import Path
import manim.utils.tex_file_writing as texwrite

def svg_local(dvi_file,extension,page=1):
    p=Path(dvi_file).resolve();out=p.with_suffix('.svg')
    if not out.exists():
        args=['dvisvgm',*(['--pdf'] if extension=='.pdf' else []),f'--page={page}','--no-fonts','--verbosity=3',f'--output={out.name}',p.name]
        r=subprocess.run(args,cwd=p.parent,capture_output=True,text=True)
        if r.returncode or not out.exists():
            raise RuntimeError(f'dvisvgm {r.returncode}: {r.stdout} {r.stderr}')
    return out

texwrite.convert_to_svg=svg_local
