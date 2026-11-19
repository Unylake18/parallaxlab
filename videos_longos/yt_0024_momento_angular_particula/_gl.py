import sys
sys.path.insert(0,'.')
from pecas24 import *
def show(*p, **k):
    m,_=Mx(*p, **k)
    g=m[0]
    print(len(g), [(i, round(float(x.get_center()[0]),2), round(float(x.width),2)) for i,x in enumerate(g)])
show("dA","=",r"\tfrac{1}{2}",r"|\vec r\times\vec v\,dt|")
show(r"\frac{dA}{dt}","=",r"\frac{|\vec r\times\vec p|}{2m}")
show(r"\frac{dA}{dt}","=",r"\frac{|\vec L|}{2m}")
