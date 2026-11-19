"""Do do day thanh tren file STL: tu moi tam tam giac ban tia vao trong (nguoc phap tuyen),
khoang cach toi mat gap dau tien = do day cuc bo. Bao cac vung mong hon nguong (mac dinh 0.8 mm,
~2 duong dun 0.4 mm) - slicer thuong bo qua thanh mong hon 1 duong dun.
Dung: python wall_thickness.py file.stl [nguong_mm]"""
import sys, numpy as np, trimesh

path = sys.argv[1]
thr = float(sys.argv[2]) if len(sys.argv) > 2 else 0.8
m = trimesh.load(path)
m.merge_vertices()
c, n, a = m.triangles_center, m.face_normals, m.area_faces
origins = c - n * 1e-3
locs, ray_idx, tri_idx = m.ray.intersects_location(origins, -n, multiple_hits=True)
d = np.full(len(c), np.inf)
dist = np.linalg.norm(locs - origins[ray_idx], axis=1)
ok = (tri_idx != ray_idx) & (dist > 1e-3)
np.minimum.at(d, ray_idx[ok], dist[ok])
thin = d < thr
print(f"{path}: {len(c)} mat, mong < {thr} mm: {a[thin].sum():.1f} mm2 / {a.sum():.0f} mm2, mong nhat {d.min():.2f} mm")
if thin.any():
    sub = m.submesh([np.where(thin)[0]], append=True)
    for q in sorted(sub.split(only_watertight=False), key=lambda q: -q.area)[:8]:
        b = q.bounds
        sel = thin & np.all((c >= b[0] - 1e-6) & (c <= b[1] + 1e-6), axis=1)
        print("   %.1f mm2  min %.2f mm  tai x %.1f..%.1f y %.1f..%.1f z %.1f..%.1f"
              % (q.area, d[sel].min(), b[0, 0], b[1, 0], b[0, 1], b[1, 1], b[0, 2], b[1, 2]))
