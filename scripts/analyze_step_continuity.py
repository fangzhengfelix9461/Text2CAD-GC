from __future__ import annotations
import argparse, json, math, os
from pathlib import Path
from OCC.Core.STEPControl import STEPControl_Reader
from OCC.Core.IFSelect import IFSelect_RetDone
from OCC.Core.TopExp import topexp
from OCC.Core.TopTools import TopTools_IndexedDataMapOfShapeListOfShape, TopTools_ListIteratorOfListOfShape
from OCC.Core.TopAbs import TopAbs_EDGE, TopAbs_FACE
from OCC.Core.BRep import BRep_Tool
from OCC.Core.LocalAnalysis import LocalAnalysis_SurfaceContinuity
from OCC.Core.GeomAbs import GeomAbs_G2
from OCC.Core.Bnd import Bnd_Box
from OCC.Core.BRepBndLib import brepbndlib

def list_shapes(lst):
    it=TopTools_ListIteratorOfListOfShape(lst); out=[]
    while it.More(): out.append(it.Value()); it.Next()
    return out

def bbox_diag(shape):
    b=Bnd_Box(); brepbndlib.Add(shape,b)
    x0,y0,z0,x1,y1,z1=b.Get()
    return math.dist((x0,y0,z0),(x1,y1,z1))

def analyze(path, samples=7, angle_deg=1.0, curvature_percent=0.01):
    rd=STEPControl_Reader(); status=rd.ReadFile(str(path))
    if status!=IFSelect_RetDone: return {'path':str(path),'read_ok':False,'error':f'ReadFile status={status}'}
    rd.TransferRoots(); shape=rd.OneShape(); diag=bbox_diag(shape)
    em=TopTools_IndexedDataMapOfShapeListOfShape(); topexp.MapShapesAndAncestors(shape,TopAbs_EDGE,TopAbs_FACE,em)
    # STEP files in the audited corpora are not guaranteed to share one declared
    # physical unit after preprocessing.  Report imported model units and scale
    # the positional tolerance by the model diagonal.
    eps_c0=max(1e-12,diag*1e-6); eps_g1=math.radians(angle_deg)
    edges=[]; counts={'G2':0,'G1_only':0,'G0_only':0,'G0_fail':0,'unknown':0,'nonmanifold_or_boundary':0}
    for i in range(1,em.Size()+1):
        edge=em.FindKey(i); faces=list_shapes(em.FindFromIndex(i))
        # duplicate seam ancestors may appear; keep unique by IsSame
        uniq=[]
        for f in faces:
            if not any(f.IsSame(g) for g in uniq): uniq.append(f)
        if len(uniq)!=2:
            counts['nonmanifold_or_boundary']+=1; continue
        try:
            pc1,a1,b1=BRep_Tool.CurveOnSurface(edge,uniq[0]); pc2,a2,b2=BRep_Tool.CurveOnSurface(edge,uniq[1])
            lo=max(a1,a2); hi=min(b1,b2)
            if pc1 is None or pc2 is None or not math.isfinite(lo) or not math.isfinite(hi) or hi<=lo: raise ValueError('missing/incompatible pcurve')
            pts=[]
            for j in range(1,samples+1):
                t=lo+(hi-lo)*j/(samples+1)
                la=LocalAnalysis_SurfaceContinuity(pc1,pc2,t,BRep_Tool.Surface(uniq[0]),BRep_Tool.Surface(uniq[1]),GeomAbs_G2,1e-10,eps_c0,1e-3,1e-3,eps_g1,curvature_percent,10000.0)
                pts.append({'t':t,'done':bool(la.IsDone()),'c0_model_units':float(la.C0Value()) if la.IsDone() else None,'g1_angle_rad':float(la.G1Angle()) if la.IsDone() else None,'g2_curvature_gap':float(la.G2CurvatureGap()) if la.IsDone() else None,'is_c0':bool(la.IsC0()) if la.IsDone() else False,'is_g1':bool(la.IsG1()) if la.IsDone() else False,'is_g2':bool(la.IsG2()) if la.IsDone() else False})
            if all(x['done'] and x['is_g2'] for x in pts): grade='G2'
            elif all(x['done'] and x['is_g1'] for x in pts): grade='G1_only'
            elif all(x['done'] and x['is_c0'] for x in pts): grade='G0_only'
            elif all(x['done'] for x in pts): grade='G0_fail'
            else: grade='unknown'
            counts[grade]+=1
            edges.append({'edge_index':i,'grade':grade,'stored_continuity':int(BRep_Tool.Continuity(edge,uniq[0],uniq[1])) if BRep_Tool.HasContinuity(edge,uniq[0],uniq[1]) else None,'max_c0_model_units':max((x['c0_model_units'] for x in pts if x['c0_model_units'] is not None),default=None),'max_g1_angle_deg':math.degrees(max((x['g1_angle_rad'] for x in pts if x['g1_angle_rad'] is not None),default=float('nan'))),'max_g2_curvature_gap':max((x['g2_curvature_gap'] for x in pts if x['g2_curvature_gap'] is not None),default=None),'samples':pts})
        except Exception as ex:
            counts['unknown']+=1; edges.append({'edge_index':i,'grade':'unknown','error':repr(ex)})
    return {'path':str(path),'read_ok':True,'bbox_diag_model_units':diag,'thresholds':{'c0_model_units':eps_c0,'g1_angle_deg':angle_deg,'g2_relative_percent':curvature_percent},'edge_counts':counts,'manifold_edges_analyzed':len(edges),'edges':edges}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('paths',nargs='+'); ap.add_argument('--out'); a=ap.parse_args()
    expanded=[]
    for p in a.paths:
        q=Path(p)
        if q.is_dir(): expanded.extend(sorted(q.glob('*.step'))+sorted(q.glob('*.stp')))
        else: expanded.append(q)
    rows=[analyze(p) for p in expanded]
    text=json.dumps(rows,ensure_ascii=False,indent=2)
    if a.out: Path(a.out).write_text(text,encoding='utf-8')
    print(json.dumps([{k:v for k,v in r.items() if k!='edges'} for r in rows],ensure_ascii=False,indent=2))
if __name__=='__main__':main()

