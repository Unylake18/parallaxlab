"""Pacote de revisão da repaginação; preserva o ZIP da primeira versão."""
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

PASTA = Path(__file__).resolve().parent


def empacotar():
    video = PASTA / 'media_repagina/preview_repagina_0007_960x540_15fps.mp4'
    tecnico = json.loads((PASTA / 'qa_repagina/tecnico.json').read_text(encoding='utf-8'))
    assert tecnico['blocos'] == 18 and tecnico['faixas_audio'] == 0
    arquivos = [(video, 'video/preview_repagina_0007.mp4')]
    for f in sorted((PASTA / 'qa_repagina').glob('N*.png')):
        arquivos.append((f, 'quadros/' + f.name))
    for f in sorted((PASTA / 'qa_repagina').glob('prancha_*.jpg')):
        arquivos.append((f, 'pranchas/' + f.name))
    for f in sorted((PASTA / 'qa_repagina/movimento').glob('*')):
        if f.is_file(): arquivos.append((f, 'movimento/' + f.name))
    for nome in ('qa_repagina.md', 'timing_repagina.json', 'validacao_repagina.json',
                 'proposta_repagina_aprovada.md', 'ficha.md'):
        arquivos.append((PASTA / nome, 'documentacao/' + nome))
    arquivos.append((PASTA / 'qa_repagina/tecnico.json', 'documentacao/tecnico.json'))
    manifesto = [dict(arquivo=nome, bytes=f.stat().st_size,
                     sha256=hashlib.sha256(f.read_bytes()).hexdigest()) for f, nome in arquivos]
    saida = PASTA / 'avaliacao_repagina_visual_0007.zip'
    with ZipFile(saida, 'w', ZIP_DEFLATED, compresslevel=6) as z:
        for f, nome in arquivos: z.write(f, nome)
        z.writestr('manifesto.json', json.dumps(manifesto, indent=2, ensure_ascii=False))
        z.writestr('LEIA-ME.txt',
            'LONGO 0007 — REPAGINAÇÃO N01–N18\n'
            'Comece pelo MP4 completo em video/ e pelo relatório em documentacao/.\n'
            'quadros/: todos os quadros de avaliação extraídos (marcos + finais).\n'
            'movimento/: 12 amostras por bloco e suas pranchas temporais.\n'
            'Estas seleções não são cada um dos frames de 15 fps do MP4.\n'
            'Preview silencioso; aprovação artística e narração ainda posteriores.\n')
    with ZipFile(saida) as z: assert z.testzip() is None
    print(json.dumps(dict(zip=str(saida), bytes=saida.stat().st_size,
                          arquivos=len(arquivos)+2), ensure_ascii=False, indent=2))


if __name__ == '__main__': empacotar()
