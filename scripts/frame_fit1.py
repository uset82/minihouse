"""Complete tabletop MiniHouse frame. Dimensions in mm, NOT a steel design.
Run with the project's optional OCCT environment: python scripts/frame_fit1.py
Creates the operation list used inside Fusion, reference STEP, and separate print meshes.
"""
from pathlib import Path
from itertools import combinations
from collections import Counter
from types import SimpleNamespace
import json, math, struct, tempfile, zipfile
import xml.etree.ElementTree as ET
import ocp_step
ocp_step.ocp()
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common, BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeCylinder
from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
from OCP.BRepGProp import BRepGProp
from OCP.BRepCheck import BRepCheck_Analyzer
from OCP.BRepMesh import BRepMesh_IncrementalMesh
from OCP.BRep import BRep_Builder
from OCP.TopoDS import TopoDS_Compound
from OCP.TopAbs import TopAbs_SOLID
from OCP.TopExp import TopExp_Explorer
from OCP.StlAPI import StlAPI_Writer
from OCP.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCP.GProp import GProp_GProps
from OCP.gp import gp_Pnt, gp_Ax2, gp_Dir, gp_Trsf, gp_Vec
from bolted_lap_prototype import write_3mf

OUT = Path(__file__).resolve().parents[1] / 'fase1/prototipo/marco-fit1'
L, D, W, T, FIN, H, PAD = 150., 75., 14., 4., 1.6, 8., 14.6
CROSS = (30., 60., 90., 120.)
NAMES = ('1_left','2_top','3_right','4_bottom') + tuple('cross_'+str(int(c)) for c in CROSS)
CORNERS = [(7,7,4,1),(7,68,1,2),(143,68,2,3),(143,7,3,4)]  # low, high

def ops_for(i):
    ops=[]
    def mp(u,v):
        return [(v,u),(u,D-W+v),(L-W+v,u),(u,v)][i-1]
    def rect(mode,a,b,c,d,z,h):
        p,q=mp(a,b),mp(c,d)
        ops.append(dict(mode=mode,rect=[min(p[0],q[0]),min(p[1],q[1]),max(p[0],q[0]),max(p[1],q[1])],z=z,h=h))
    n = D if i in (1,3) else L
    rect('new',0,0,n,W,0,T)
    lows = (i in (3,4),i in (1,2))
    for (a,c),low in zip(((0,PAD),(n-PAD,n)),lows):
        rect('cut',a,0,c,W,1.8 if low else 0,2.2)
    for a in (0,W-FIN): rect('join',17.,a,n-17.,a+FIN,T,H)
    for u in (7.,n-7.): ops.append(dict(mode='cut',circle=[*mp(u,7),3.3],z=0.,h=T))
    if i in (2,4):
        for u in CROSS:
            # Shelves with side fences locate loose transverse gauges, not engineered fixings.
            v0,v1 = (-4.,0.) if i==2 else (W,W+4.)
            rect('join',u-3.5,v0,u+3.5,v1,0,1.6)
            for a in (u-3.5,u+2.25): rect('join',a,v0,a+1.25,v1,1.6,1.2)
    # Recessed seven-segment rail ID in the channel floor. Rectangles share edges only.
    seg={'a':(0,5,3.6,5.8),'g':(0,2.5,3.6,3.3),'d':(0,0,3.6,.8),
         'b':(2.8,3.3,3.6,5),'c':(2.8,.8,3.6,2.5),'f':(0,3.3,.8,5),'e':(0,.8,.8,2.5)}
    for s in ('bc','abged','abgcd','fgbc')[i-1]:
        a,b,c,d=seg[s]; rect('cut',n/2-1.8+a,4+b,n/2-1.8+c,4+d,3.4,.6)
    return ops

def box(x,y,z,a,b,h): return BRepPrimAPI_MakeBox(gp_Pnt(x,y,z),a,b,h).Shape()
def cyl(x,y,z,r,h): return BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(x,y,z),gp_Dir(0,0,1)),r,h).Shape()
def vol(s):
    p=GProp_GProps(); BRepGProp.VolumeProperties_s(s,p); return abs(p.Mass())
def shift(s,x,y,z):
    tr=gp_Trsf(); tr.SetTranslation(gp_Vec(x,y,z)); return BRepBuilderAPI_Transform(s,tr,True).Shape()
def overlap(a,b): return vol(BRepAlgoAPI_Common(a,b).Shape())
def shape(ops):
    for op in ops:
        z,h=op['z'],op['h']
        if 'rect' in op:
            x,y,a,b=op['rect']; item=box(x,y,z,a-x,b-y,h)
        else:
            x,y,r=op['circle']; item=cyl(x,y,z,r,h)
        if op['mode']=='new': result=item
        else:
            cmd=(BRepAlgoAPI_Fuse if op['mode']=='join' else BRepAlgoAPI_Cut)(result,item)
            cmd.SimplifyResult(); result=cmd.Shape()
    ex=TopExp_Explorer(result,TopAbs_SOLID); assert ex.More(); s=ex.Current(); ex.Next(); assert not ex.More()
    assert BRepCheck_Analyzer(s).IsValid() and vol(s)>0
    return s

def step(path, shapes):
    compound=TopoDS_Compound(); builder=BRep_Builder(); builder.MakeCompound(compound)
    for s in shapes: builder.Add(compound,s)
    writer=STEPControl_Writer(); writer.Transfer(compound,STEPControl_AsIs); assert writer.Write(str(path)).value==1

def mesh(s,path):
    BRepMesh_IncrementalMesh(s,.04,False,.12,True).Perform()
    w=StlAPI_Writer(); w.ASCIIMode=False; assert w.Write(s,str(path))
    b=path.read_bytes(); v=[]; ids={}; tris=[]; edges=Counter(); total=0.
    for row in struct.iter_unpack('<12fH',b[84:]):
        tri=[]
        for k in (3,6,9):
            key=tuple(round(a,5) for a in row[k:k+3]); j=ids.setdefault(key,len(v)); tri.append(j)
            if j==len(v): v.append(key)
        assert len(set(tri))==3; tris.append(tuple(tri))
        for j in range(3): edges[tri[j],tri[(j+1)%3]]+=1
        a,b1,c=[v[n] for n in tri]; total+=sum(a[j]*(b1[(j+1)%3]*c[(j+2)%3]-b1[(j+2)%3]*c[(j+1)%3]) for j in range(3))/6
    assert all(n==edges[(q,p)]==1 for (p,q),n in edges.items()) and abs(total-vol(s))<vol(s)*.002
    return v,tris

def build():
    OUT.mkdir(exist_ok=True,parents=True)
    ops=[ops_for(i) for i in range(1,5)]+[[dict(mode='new',rect=[u-2.,W+.3,u+2.,D-W-.3],z=1.6,h=2.4)] for u in CROSS]
    parts=[dict(name=n,ops=o) for n,o in zip(NAMES,ops)]
    (OUT/'geometry.json').write_text(json.dumps(dict(parts=parts),indent=2)+'\n')
    shapes=[shape(o) for o in ops]
    for a,b in combinations(shapes,2): assert overlap(a,b)<1e-6
    for x,y,low,high in CORNERS:
        # A closed real shank passes both independently; annulus material exists at each z.
        for idx,z in ((low,.1),(high,2.3)):
            s=shapes[idx-1]; assert overlap(s,cyl(x,y,-1,3,6))<1e-6
            assert overlap(s,cyl(x,y,z,5,1.5))>60
        # Check an above-frame 16 mm OD socket; nuts below are freely accessible before placement on bench.
        assert all(overlap(s,cyl(x,y,4.001,8,9))<1e-6 for s in shapes)
    # Conservative continuous sweep: bound translating rail 4 with five prisms over entire y stroke.
    # At both ends use the proper tongue interval; central channel and four seats bounded to full height.
    covers=[box(0,-15,0,PAD,29,1.8), box(L-PAD,-15,2.2,PAD,29,1.8),box(PAD,-15,0,L-2*PAD,29,12)]
    covers += [box(u-3.5,-1,0,7,19,2.8) for u in CROSS]
    cover=covers[0]
    for s in covers[1:]: cover=BRepAlgoAPI_Fuse(cover,s).Shape()
    assert vol(BRepAlgoAPI_Cut(shapes[3],cover).Shape())<1e-6
    assert all(overlap(cover,s)<1e-6 for s in shapes[:3])
    step(OUT/'MiniHouse_Frame_Fit1.step',shapes)
    # single solid used only for opening a new Fusion document without touching existing designs
    step(Path(__file__).resolve().parents[1]/'.tmp/fit1-seed.step',[box(-5,-5,0,1,1,1)])
    # Base down, fins up, separate objects. Each high tongue starts 2.2 mm above the bed:
    # add build-plate support only there in the slicer, rather than supporting a whole horizontal fin.
    layout=[(12,12),(12,34),(12,61),(12,84),(12,112),(12,124),(12,136),(12,148)]
    packed={}; envelopes=[]
    with tempfile.TemporaryDirectory() as td:
        for j,(s,(x,y)) in enumerate(zip(shapes,layout),1):
            v,t=mesh(s,Path(td)/f'{j}.stl')
            # Proper rotations around Z; no mirrors, bases on plate, fins vertical.
            if j in (2,4): rot=lambda a,b,c:(a,b,c)
            else: rot=lambda a,b,c:(b,-a,c)
            v=[rot(*p) for p in v]; m=list(map(min,zip(*v)))
            v=[(a-m[0]+x,b-m[1]+y,c-m[2]) for a,b,c in v]
            bb=[(min(ax),max(ax)) for ax in zip(*v)]; assert bb[2][0]==0 and min(p[0] for p in bb[:2])>=5 and max(p[1] for p in bb)<=175
            for other in envelopes: assert any(bb[k][0]>=other[k][1]+3 or other[k][0]>=bb[k][1]+3 for k in (0,1))
            envelopes.append(bb); packed[j]=[SimpleNamespace(verts=v,tris=t)]
        path=OUT/'MiniHouse_Frame_Fit1_A1mini.3mf'; write_3mf(path,packed)
        with zipfile.ZipFile(path) as z: data={k:z.read(k) for k in z.namelist()}
        key='3D/3dmodel.model'; txt=data[key].decode();
        for j,n in enumerate(NAMES,1): txt=txt.replace(f'name="ply {j}"',f'name="{n}"')
        data[key]=txt.encode();
        with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
            for k,b in data.items(): z.writestr(k,b)
        with zipfile.ZipFile(path) as z: assert len(ET.fromstring(z.read(key)).findall('.//{*}item'))==8
    print('Checked 8 valid solids; 28 no-overlap pairs; 4 bolt axes/socket zones; continuous bolt-free rail 4 insertion; 8 closed print meshes, separate at z=0. Plate bounds:',envelopes)

if __name__=='__main__': build()
