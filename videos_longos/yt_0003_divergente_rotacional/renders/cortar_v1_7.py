"""Cortes A–F e exemplo K do preview completo V1.6 por cópia de pacotes (sem recompressão)."""
import av
from pathlib import Path
d = Path(__file__).parent / 'videos/cena/540p15'
src = d / 'preview_v1_7.mp4'
cortes = {'A': (0, 63.67), 'B': (63.67, 224.93), 'C': (224.93, 327.87), 'K': (327.87, 351.8),
          'D': (351.8, 525.93), 'E': (525.93, 664.33), 'F': (664.33, 1e9)}
for nome, (t0, t1) in cortes.items():
    out = d / f'trecho_{nome}_v1_7_do_completo.mp4'
    with av.open(str(src)) as i, av.open(str(out), 'w') as o:
        si = i.streams.video[0]; so = o.add_stream_from_template(si)
        i.seek(int(t0/si.time_base), stream=si, backward=True, any_frame=False)
        base = None; n = 0; started = False
        for p in i.demux(si):
            if p.dts is None: continue
            t = float(p.pts*si.time_base)
            if not started:
                if t + 1e-6 < t0 and not p.is_keyframe: continue
                if not p.is_keyframe: continue
                started = True
            if t >= t1: break
            if base is None: base = p.dts
            p.dts -= base; p.pts -= base; p.stream = so; o.mux(p); n += 1
    print(nome, n, 'pacotes', out.stat().st_size)
