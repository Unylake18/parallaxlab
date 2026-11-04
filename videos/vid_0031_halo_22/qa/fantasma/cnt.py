import av,glob,sys
for f in sorted(glob.glob(sys.argv[1]+'/videos/cena/1920p30/partial_movie_files/HaloSol031/*.mov')):
    with av.open(f) as m:
        n=sum(1 for _ in m.decode(video=0)); print(f[-18:],n)
