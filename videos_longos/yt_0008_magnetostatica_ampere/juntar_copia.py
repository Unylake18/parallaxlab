"""Junta os grupos renderizados SEM recodificar (cópia de pacotes H.264): uv run --no-sync python juntar_copia.py SAIDA.mp4 G1.mp4 G2.mp4 ..."""
import sys
import av

out, parts = sys.argv[1], sys.argv[2:]
o = av.open(out, "w", options={"movflags": "+faststart"})
with av.open(parts[0]) as c0:
    st = o.add_stream_from_template(c0.streams.video[0])
offset, total = 0, 0.0
for p in parts:
    with av.open(p) as c:
        s = c.streams.video[0]
        fim = 0
        for pk in c.demux(s):
            if pk.dts is None:
                continue
            pk.pts, pk.dts = pk.pts + offset, pk.dts + offset
            pk.stream = st
            fim = max(fim, pk.pts + (pk.duration or 0))
            o.mux(pk)
        offset = fim
        total += float(s.duration * s.time_base)
o.close()
print(out, f"{total:.2f} s em {len(parts)} partes")
