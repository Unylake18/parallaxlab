import av,glob
for f in sorted(glob.glob('media/videos/t3/*/[VW]?.mp4')):
    c=av.open(f); r=[]
    for fr in c.decode(video=0):
        a=fr.to_ndarray(format='gray'); r.append(int((a[300:,:]>128).sum()))
    print(f[-8:], r[:20])
