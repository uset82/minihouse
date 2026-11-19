"""Fit2: complete tabletop framing set. Uses unchanged Fit1 base. Run from any cwd.
15-degree gable/openings/printed members are mock-up geometry, not building specifications.
"""
from pathlib import Path
from itertools import combinations
from types import SimpleNamespace
from math import radians, tan, cos, sin, hypot
import json, zipfile, shutil, xml.etree.ElementTree as ET
import frame_fit1 as f
from OCP.BRepBuilderAPI import BRepBuilderAPI_MakePolygon, BRepBuilderAPI_MakeFace
from OCP.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCP.gp import gp_Pnt,gp_Vec
from OCP.STEPControl import STEPControl_Reader

OUT=f.OUT.parent/'marco-fit2'
NAMES=['01_rail_left','02_rail_back','03_rail_right','04_rail_front','05_cross_30','06_cross_60','07_cross_90','08_cross_120','09_wall_front','10_wall_back','11_gable_left','12_gable_right','13_roof_front','14_roof_back']
ANG=radians(15); M=tan(ANG); EAVE=65.; RIDGE=37.5; START=1.9; END=73.1

def box(x0,x1,y0,y1,z0,z1): return f.box(x0,y0,z0,x1-x0,y1-y0,z1-z0)
def prism(poly,vec):
    p=BRepBuilderAPI_MakePolygon()
    for point in poly: p.Add(gp_Pnt(*point))
    p.Close(); return BRepPrimAPI_MakePrism(BRepBuilderAPI_MakeFace(p.Wire()).Face(),gp_Vec(*vec)).Shape()
def yz(x,x1,pts): return prism([(x,y,z) for y,z in pts],(x1-x,0,0))
def xz(y,y1,pts): return prism([(x,y,z) for x,z in pts],(0,y1-y,0))
def op(a,b,fuse):
    w=(f.BRepAlgoAPI_Fuse if fuse else f.BRepAlgoAPI_Cut)(a,b); w.SimplifyResult(); return w.Shape()
def union(items):
    result=items[0]
    for s in items[1:]: result=op(result,s,True)
    return result

def single(s):
    ex=f.TopExp_Explorer(s,f.TopAbs_SOLID); assert ex.More(); a=ex.Current(); ex.Next()
    assert not ex.More() and f.BRepCheck_Analyzer(a).IsValid() and f.vol(a)>5
    return a

def upper_z(y):return EAVE+M*(min(y,75-y)-START)
def roofstrip(x0,x1,a,b,thick):return yz(x0,x1,[(a,upper_z(a)),(b,upper_z(b)),(b,upper_z(b)+thick),(a,upper_z(a)+thick)])

def diag(p,q,width):
    x,y=p; a,b=q; l=hypot(a-x,b-y); dx=-(b-y)*width/(2*l);dy=(a-x)*width/(2*l)
    return [(x+dx,y+dy),(a+dx,b+dy),(a-dx,b-dy),(x-dx,y-dy)]

def side(front):
    y0,y1=(1.9,5.1) if front else (69.9,73.1)
    s=box(1.9,148.1,y0,y1,14.,65.)
    if front: holes=[(5.1,18.,17.,61.8),(21.2,44.5,13.,59.),(47.7,60.5,17.,61.8),(63.7,116.5,29.,58.),(63.7,116.5,17.,25.8),(63.7,116.5,61.2,62.),(119.7,144.9,17.,61.8)]
    else: holes=[(5.1,33.,17.,61.8),(36.2,65.,17.,61.8),(68.2,97.,17.,61.8),(100.2,122.,32.,56.),(100.2,122.,17.,28.8),(100.2,122.,59.2,61.8),(125.2,144.9,17.,61.8)]
    # Small blank above the large front window remains the integral lintel.
    if front: holes=[h for h in holes if h[3]-h[2]>1]
    for x0,x1,z0,z1 in holes: s=op(s,box(x0,x1,y0-1,y1+1,z0,z1),False)
    pieces=[s]
    # Small pitched cap creates a true bearing surface under the roof rather than edge contact.
    a,b=y0,y1
    if front: pts=[(a,65),(b,65),(b,upper_z(b))]
    else: pts=[(a,65),(b,65),(a,upper_z(a))]
    pieces.append(yz(1.9,148.1,pts))
    if not front:
        for p,q in [((4,16),(34.3,63)),((35,63),(66.3,16))]:pieces.append(xz(y0,y1,diag(p,q,2.6)))
    for x in (52.,105.,132.):
        pieces.append(box(x-4,x+4,1.9 if front else 62.9,12.1 if front else 73.1,4.,15.))
    return single(union(pieces))

def gable(left):
    x0,x1=(1.9,6.7) if left else (143.3,148.1)
    a,b=5.45,69.55
    s=yz(x0,x1,[(a,14),(b,14),(b,upper_z(b)),(RIDGE,upper_z(RIDGE)),(a,upper_z(a))]);
    holes=([(8.65,19.,17.,61.),(22.2,52.8,27.,59.),(22.2,52.8,17.,23.8),(56.,66.35,17.,61.)] if left else [(8.65,35.9,17.,61.),(39.1,66.35,17.,61.)]);
    for y0,y1,z0,z1 in holes:s=op(s,box(x0-1,x1+1,y0,y1,z0,z1),False)
    for p,q in [(11.8,35.9),(39.1,63.2)]:
        h=64.2; s=op(s,yz(x0-1,x1+1,[(p,h),(q,h),(q,upper_z(q)-3.),(p,upper_z(p)-3.)]),False)
    bits=[s];
    if not left: bits.append(yz(x0,x1,diag((8,16),(36.7,62),2.6)))
    for y in (23.,52.):bits.append(box(1.9 if left else 137.9,12.1 if left else 148.1,y-4,y+4,4.,15.))
    cx=(x0+x1)/2
    for y in (18.,57.):bits.append(box(cx-1,cx+1,y-1,y+1,upper_z(y)-1.,upper_z(y)+2.4))
    return single(union(bits))

def roof(front):
    a,b=(START,37.3) if front else (37.7,END)
    s=roofstrip(1.9,148.1,a,b,2.8)
    # Frame cutouts leave integral rafters and eave, ridge and mid-slope purlins.
    xs=[(6.9,28.5),(31.5,58.5),(61.5,88.5),(91.5,118.5),(121.5,143.1)]
    mid=(a+b)/2
    for x0,x1 in xs:
        for y0,y1 in ((a+3.,mid-1.1),(mid+1.1,b-3.)):
            s=op(s,box(x0,x1,y0,y1,60,90),False)
    for x in (4.3,145.7):
        y=18. if front else 57.; s=op(s,box(x-1.3,x+1.3,y-1.3,y+1.3,60,90),False)
    return single(s)

def plate(file,items,meshes):
    objs={}; bb_list=[]
    for i,x,y,rot in items:
        verts,tris=meshes[i]; vv=[rot(*p) for p in verts]; mn=list(map(min,zip(*vv)))
        vv=[(a-mn[0]+x,b-mn[1]+y,c-mn[2]) for a,b,c in vv]; bb=[(min(ax),max(ax)) for ax in zip(*vv)]
        assert min(lo for lo,hi in bb[:2])>=5 and max(hi for lo,hi in bb)<=175 and abs(bb[2][0])<1e-6
        for other in bb_list: assert any(bb[k][0]>=other[k][1]+3 or other[k][0]>=bb[k][1]+3 for k in (0,1))
        bb_list.append(bb);objs[i+1]=[SimpleNamespace(verts=vv,tris=tris)]
    path=OUT/file; f.write_3mf(path,objs)
    with zipfile.ZipFile(path) as z: data={k:z.read(k) for k in z.namelist()}
    key='3D/3dmodel.model'; txt=data[key].decode()
    for j in objs:txt=txt.replace(f'name="ply {j}"',f'name="{NAMES[j-1]}"')
    data[key]=txt.encode()
    with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED) as z:
        for k,b in data.items():z.writestr(k,b)
    return bb_list

def main():
    OUT.mkdir(exist_ok=True);d=OUT/'assembled_meshes';d.mkdir(exist_ok=True);steps=OUT/'step_parts';steps.mkdir(exist_ok=True)
    base=json.loads((f.OUT/'geometry.json').read_text())['parts'];s=[f.shape(part['ops']) for part in base]+[side(True),side(False),gable(True),gable(False),roof(True),roof(False)]
    for (i,a),(j,b) in combinations(enumerate(s),2):assert f.overlap(a,b)<1e-5,(NAMES[i],NAMES[j])
    # Positive seating area: each foot enters an unchanged Fit1 channel, roof touches walls/gables.
    for i,j in [(8,3),(9,1),(10,0),(11,2),(12,8),(13,9),(12,10),(12,11),(13,10),(13,11)]:assert f.overlap(f.shift(s[i],0,0,-.1),s[j])>.1,(i,j)
    meta=[]; meshes=[]
    for i,(n,b) in enumerate(zip(NAMES,s)):
        props=f.GProp_GProps();f.BRepGProp.VolumeProperties_s(b,props);meta.append(dict(name=n,volume_mm3=props.Mass(),center_mm=list(props.CentreOfMass().Coord())))
        meshes.append(f.mesh(b,d/(n+'.stl'))); f.step(steps/(n+'.step'),[b])
    (OUT/'parts.json').write_text(json.dumps(meta,indent=2)+'\n'); f.ocp_step.write_step(OUT/'MiniHouse_Frames_Fit2.step',[SimpleNamespace(name=n) for n in NAMES],exact_shapes=s,product_name='MiniHouse Frames Fit2')
    reader=STEPControl_Reader();assert reader.ReadFile(str(OUT/'MiniHouse_Frames_Fit2.step')).value==1;reader.TransferRoots(); it=f.TopExp_Explorer(reader.OneShape(),f.TopAbs_SOLID);vs=[]
    while it.More():vs.append(f.vol(it.Current()));it.Next()
    assert len(vs)==14 and all(abs(a-b)<.01 for a,b in zip(sorted(vs),sorted(f.vol(b) for b in s)))
    # Proper rigid rotations: flatten outside faces on the bed; feet, locating pegs and ribs stay attached.
    plate('02_Long_walls.3mf',[(8,12,10,lambda x,y,z:(-x,z,y)),(9,12,85,lambda x,y,z:(x,z,-y))],meshes)
    plate('03_Gable_frames.3mf',[(10,12,15,lambda x,y,z:(y,z,x)),(11,92,15,lambda x,y,z:(-y,z,-x))],meshes)
    def tilt(t):return lambda x,y,z:(x,cos(t)*y+sin(t)*z,-sin(t)*y+cos(t)*z)
    plate('04_Roof_frames.3mf',[(12,12,20,tilt(ANG)),(13,12,85,tilt(-ANG))],meshes)
    shutil.copyfile(f.OUT/'MiniHouse_Frame_Fit1_A1mini.3mf',OUT/'01_Numbered_base.3mf')
    count=0
    for file in sorted(OUT.glob('0*.3mf')):
        with zipfile.ZipFile(file) as z:
            tree=ET.fromstring(z.read('3D/3dmodel.model')); count+=len(tree.findall('.//{*}item'))
    assert count==14
    print('Fit2 checked: 14 connected solids, 91 clear part pairs; 10 seating checks, STEP roundtrip, 14 print objects on four plates. Width x depth x height:',150,75,upper_z(37.3)+2.8)

if __name__=='__main__':main()
