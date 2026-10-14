"""Caches locais da V2; reutiliza o asset e os controles editoriais existentes.

Não altera construtor, ficha ou ponte global. Renderiza só 540×960.
"""
import hashlib
import json
import math
import subprocess
import sys
import time
from pathlib import Path

UNIT = Path(__file__).resolve().parent
ROOT = UNIT.parents[1]
sys.path.insert(0, str(UNIT))
sys.path.insert(0, str(ROOT/'experimentos/blender/arsenal'))
import ponte
from configuracao_3d import RES, AMOSTRAS, ALTURA_IMAGEM, CENTRO_IMAGEM

SECAO = dict(estado_visual='geometria', marcadores=0, referencia=0,
             setor=0, grade=0, meridiana=1, **{'lambda': 1.0})
FRAMES = 76


def blender(destino):
    import bpy
    from mathutils import Matrix, Vector
    from bpy_extras.object_utils import world_to_camera_view
    sys.path.insert(0, str(ROOT/'experimentos/blender'))
    import casca_oca as co
    import liquido_rotacao as lr

    ficha = ponte.ler_ficha('liquido_rotacao')
    p = ponte.parametros(ficha, {**SECAO, 'grade': 1}, animado=False)
    co.limpar_cena()
    args = dict(p)
    args['lam'] = args.pop('lambda')
    proxy, _, apos_camera, ctl = lr.liquido_rotacao(**args)
    co.mundo()
    co.luzes()
    cam = co.camera_enquadrada(co.cantos([proxy]), **ficha['enquadramento'], largura=540, altura=960)
    apos_camera(cam)
    pos, rot = cam.location.copy(), cam.rotation_euler.copy()
    alvo = Vector((0, 0, ctl.H/2))

    def tela(xyz):
        q = world_to_camera_view(bpy.context.scene, cam, Vector(xyz))
        return [(q.x-.5)*ALTURA_IMAGEM*540/960 + CENTRO_IMAGEM[0],
                (q.y-.5)*ALTURA_IMAGEM + CENTRO_IMAGEM[1], 0.0]

    R, h0, dh = p['raio'], p['nivel'], p['delta_h']
    a = math.radians(p['fi_meridiana'])
    def xyz(s,z):
        return (s*math.cos(a), s*math.sin(a), z)
    z0 = h0-dh/2
    def dados():
        curva = [tela(pt) for pt in lr._diametro(a,1,R,h0,dh/R**2,.014)]
        return dict(curva=curva,
                    secao=[tela(xyz(-R,0)),tela(xyz(R,0))]+list(reversed(curva)),
                    eixo=[tela(xyz(0,0)),tela(xyz(0,z0+dh+.35))],
                    regiao=[tela(xyz(r*R,z)) for r,z in ((.53,.48),(.64,.48),(.64,.62),(.53,.62))],
                    superficie=[tela((r*R*math.cos(phi),r*R*math.sin(phi),z0+dh*r*r+.016))
                                for r,phi in ((.82,a),(.12,a),(.82,a+math.pi))],
                    aneis=[[tela((r*R*math.cos(phi),r*R*math.sin(phi),z0+dh*r*r+.018))
                            for phi in [2*math.pi*k/120 for k in range(121)]] for r in (.3,.62,.94)],
                    delta=[tela(xyz(R,z)) for z in (z0,z0+dh)])
    inicial = dados()
    tempos = []
    bpy.context.scene.render.film_transparent = True
    bpy.context.scene.render.image_settings.color_mode = 'RGBA'
    destino.mkdir(parents=True, exist_ok=True)
    for i in range(FRAMES):
        f = i/(FRAMES-1)
        # Seção permanece opaca; superfície e grid entram pelos controles já aprovados.
        ctl.estado(lam=1, revela=lr.suave(f/.65), revela_grade=lr.suave((f-.2)/.65))
        giro = Matrix.Rotation(math.radians(4)*lr.suave((f-.35)/.65),3,'Z')
        cam.location = alvo+giro@(pos-alvo)
        cam.rotation_euler = (giro@rot.to_matrix()).to_euler()
        bpy.context.view_layer.update()
        assert not any(o.name.startswith('Tracer') for o in bpy.data.objects)
        t = time.perf_counter()
        arq = destino/f'frame_{i+1:04d}.png'
        if i==0:
            co.render(arq,540,960,AMOSTRAS)
        else:
            bpy.context.scene.render.filepath=str(arq)
            bpy.ops.render.render(write_still=True)
        tempos.append(time.perf_counter()-t)
    (destino/'projecao.json').write_text(json.dumps(dict(inicial=inicial,final=dados()),indent=2),encoding='utf-8')
    (destino/'meta.json').write_text(json.dumps(dict(frames=FRAMES,segundos=sum(tempos),
        bytes=sum(p.stat().st_size for p in destino.glob('frame_*.png')),res=RES,amostras=AMOSTRAS),indent=2),encoding='utf-8')


def main():
    if '--blender' in sys.argv:
        return blender(Path(sys.argv[sys.argv.index('--blender')+1]))
    secao=ponte.sequencia('liquido_rotacao',params=SECAO,animado=False,res=RES,amostras=AMOSTRAS)
    # Hash local inclui código, asset, estilo e configuração; não afeta caches da V1.
    chave=hashlib.sha1(Path(__file__).read_bytes()+ponte._codigo()+
                      (ponte.SOLIDOS/'liquido_rotacao.json').read_bytes()+
                      (ponte.AQUI/'estilo.json').read_bytes()).hexdigest()[:12]
    pasta=ROOT/'renders/vid_0022_v2'/chave
    if not (pasta/'meta.json').exists():
        subprocess.run([ponte.encontrar_blender(),'-b','--python-exit-code','1','-P',str(Path(__file__).resolve()),
                        '--','--blender',str(pasta)],check=True)
    registro=dict(secao=str(secao.pasta),payoff=str(pasta),
                  meta=json.loads((pasta/'meta.json').read_text(encoding='utf-8')))
    (UNIT/'cache_3d_v2.json').write_text(json.dumps(registro,indent=2),encoding='utf-8')
    (UNIT/'projecao_3d_v2.json').write_text((pasta/'projecao.json').read_text(encoding='utf-8'),encoding='utf-8')
    print(json.dumps(registro,indent=2))


if __name__=='__main__':
    main()
