"""
Sinh script lenh SolidCraft (JSON) dung vo de ban ES3C28P.
Chay:  python make_script.py [standard|xl]
  standard -> es3c28p_case_script.json     (pin toi da 70 x 36 x 8 mm)
  xl       -> es3c28p_case_xl_script.json  (pin 805080: 8 x 50 x 80 mm + mach bao ve)
Roi:   solidcraft-cli run <script>.json --save <ten>.sc

He toa do = he toa do file STEP cua bo mach (mm): PCB x[-52.75,-2.75] y[6,92] z[-1.6,0],
mat kinh LCD huong +Z. Bien dang nem duoc dieu khien boi tham so (TH, WALL, LB, ...),
doi tham so trong SolidCraft (Modify > Change Parameters) se dung lai hinh nem.
"""
import json, math, os, sys
from shapely.geometry import Polygon, box as sbox

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = HERE.replace("\\", "/")

# ---------------- gia tri mac dinh (phai khop voi tham so ben duoi)
VARIANT = sys.argv[1] if len(sys.argv) > 1 else "standard"
assert VARIANT in ("standard", "xl"), VARIANT
TH, WALL, CLR, FIL, ZTB, HDESK, ZS, TONGUE = 18.0, 2.0, 0.4, 3.0, -12.0, -2.7, -1.6, 2.5
BX0, BX1, BY0, BY1, GLASS_Z = -52.75, -2.75, 6.0, 92.0, 4.3
HOLES = [(-6.75, 10.0), (-48.75, 10.0), (-6.75, 88.0), (-48.75, 88.0)]
if VARIANT == "standard":
    EW, LB, LB_RANGE = 0.0, 65.0, "62-70"
    BAT_L, BAT_W, BAT_T = 67.5, 36.0, 8.0    # 67.5: chua cho cot vit D9.2 o 2 lo duoi
    LONG = HOLES                 # 4 vit M3x12 dai: than sau -> PCB -> vau mat truoc
    SHORT = []                   # vit M3x6 bat PCB vao vau mat truoc tu ben trong
else:
    # Ban XL: de dai hon, vo rong them EW moi ben; pin 805080 dai 80 + ~4 mach bao ve.
    # Cot vit o 2 lo duoi cua PCB se xuyen qua pin -> thay bang 2 cot moi o hai ben (ngoai bo mach)
    EW, LB, LB_RANGE = 6.0, 86.0, "82-90"
    BAT_L, BAT_W, BAT_T = 84.0, 50.5, 8.5
    LONG = [(-48.75, 10.0), (-48.75, 88.0)]
    SHORT = [(-6.75, 10.0), (-6.75, 88.0)]
OUT_NAME = {"standard": "es3c28p_case_script.json", "xl": "es3c28p_case_xl_script.json"}[VARIANT]

c, s = math.cos(math.radians(TH)), math.sin(math.radians(TH))
U, B = (-c, s), (-s, -c)
IX0, IY0, IY1 = BX0 - CLR, BY0 - CLR - EW, BY1 + CLR + EW
XT, Y0, Y1 = IX0 - WALL, IY0 - WALL, IY1 + WALL
ZF = GLASS_Z + 0.2 + WALL
XF = (ZF * s - HDESK) / c
FT, FB, BB, TB = (XT, ZF), (XF, ZF), (XF + LB * B[0], ZF + LB * B[1]), (XT, ZTB)
PROFILE = [FT, FB, BB, TB]
YM = (Y0 + Y1) / 2
# cot vit phu o hai ben bo mach (ban XL): sat thanh trong, ngoai chieu dai pin
SIDE = [] if VARIANT == "standard" else [(-6.75, IY0 + 2.3), (-6.75, IY1 - 2.3)]

cmds = []
def cmd(c_, **p):
    cmds.append({"command": c_, "params": p})
def draw(c_, **p):
    """hinh trong sketch kem kich thuoc + vi tri tu goc toa do -> sketch du rang buoc (dof 0)"""
    cmd("sketch.draw.dimensioned", command=c_, params=p, as_drawn=True, locate=True)

# ---------------- tham so (hien trong bang Parameters cua SolidCraft)
params = [
    ("TH", "18 deg", "Goc nga man hinh ve sau. Khoang 15-21 deg"),
    ("WALL", "2 mm", "Do day thanh vo. Khoang 1.6-2.4 mm, nho hon FIL it nhat 0.3 mm"),
    ("CLR", "0.4 mm", "Khe ho bo mach - thanh"),
    ("FIL", "3 mm", "Bo tron canh ngoai. Khoang 2.6-4 mm, lon hon WALL it nhat 0.3 mm"),
    ("LB", f"{LB:g} mm", f"Chieu dai de doc mat ban. Khoang {LB_RANGE} mm"),
    ("ZTB", "-12 mm", "Do sau goc tren-sau (z). Khoang -10 den -15 mm"),
    ("HDESK", "-2.7 mm", "Vi tri mat ban so voi bo mach"),
    ("ZS", "-1.6 mm", "Mat phan chia mat truoc / than sau"),
    ("TONGUE", "2.5 mm", "Chieu cao go dinh vi"),
    ("EW", f"{EW:g} mm", "Phan noi rong vo moi ben (ngoai bo mach)"),
    ("XT", "-52.75 mm - CLR - WALL", "Mat tren ngoai (x)"),
    ("YA", "6 mm - CLR - WALL - EW", "Mat trai ngoai (y)"),
    ("YW", "86 mm + 2 * (CLR + WALL + EW)", "Chieu rong ngoai"),
    ("ZF", "4.3 mm + 0.2 mm + WALL", "Mat truoc ngoai (z)"),
    ("XF", "(ZF * sin(TH) - HDESK) / cos(TH)", "Canh truoc-duoi (x)"),
    ("BBX", "XF - LB * sin(TH)", "Goc sau-duoi (x)"),
    ("BBZ", "ZF - LB * cos(TH)", "Goc sau-duoi (z)"),
]
for n, e, cm in params:
    cmd("parameters.add", name=n, expression=e, comment=cm)
for n in ("TH", "WALL", "FIL", "LB", "ZTB"):
    cmd("parameters.favorite", name=n, favorite=True)

# ---------------- bien dang nem (sketch tren mat XZ: toa do sketch = (x, -z), dun theo +Y)
cmd("sketch.create", plane="XZ", offset="YA", name="Wedge profile")
cmd("sketch.line", points=[["XT", "-ZF"], ["XF", "-ZF"], ["BBX", "-BBZ"], ["XT", "-ZTB"]], closed=True)
cmd("sketch.finish")

def edge_picks():
    pts = [[x, YM, z] for (x, z) in PROFILE]
    for i in range(4):
        (xa, za), (xb, zb) = PROFILE[i], PROFILE[(i + 1) % 4]
        for y in (Y0, Y1):
            pts.append([(xa + xb) / 2, y, (za + zb) / 2])
    return pts

def wedge_body(name):
    cmd("solid.extrude", sketch="Wedge profile", distance="YW", operation="new", body_name=name, name=f"{name} extrude")
    cmd("solid.fillet", body=name, edges=edge_picks(), radius="FIL", name=f"{name} fillet")

wedge_body("Case")
wedge_body("OuterRef")                           # khoi dac dung de cat cot vit theo mat ngoai
cmd("solid.split_body", body="Case", plane={"origin": [0, 0, ZS], "normal": [0, 0, 1]}, name="Split front/rear")
cmd("body.rename", body="Case", name="Front_Bezel")
cmd("body.rename", body="Case (1)", name="Rear_Body")

# khoang rong ben trong: bien dang offset vao trong WALL, bo tron FIL - WALL, cat khoi 2 nua.
# (khong dung Shell: nhan hinh hoc tu choi Shell o mot so gia tri tham so va de lai khoi dac)
cmd("sketch.create", plane="XZ", offset="YA + WALL", name="Cavity profile")
cmd("sketch.line", points=[["XT", "-ZF"], ["XF", "-ZF"], ["BBX", "-BBZ"], ["XT", "-ZTB"]], closed=True, construction=True)
cmd("sketch.offset", curves=["l1", "l2", "l3", "l4"], distance="WALL", side=[-30.0, 10.0])
cmd("sketch.finish")
cmd("solid.extrude", sketch="Cavity profile", distance="YW - 2 * WALL", operation="new", body_name="Cavity", name="Cavity extrude")
INNER = [tuple(p) for p in list(Polygon(PROFILE).buffer(-WALL, join_style=2).exterior.coords)[:-1]]
cav_picks = [[x, YM, z] for (x, z) in INNER]
for i in range(len(INNER)):
    (xa, za), (xb, zb) = INNER[i], INNER[(i + 1) % len(INNER)]
    for y in (IY0, IY1):
        cav_picks.append([(xa + xb) / 2, y, (za + zb) / 2])
cmd("solid.fillet", body="Cavity", edges=cav_picks, radius="FIL - WALL", name="Cavity fillet")
cmd("solid.combine", target="Front_Bezel", tools=["Cavity"], operation="cut", keep_tools=True, name="Hollow front")
cmd("solid.combine", target="Rear_Body", tools=["Cavity"], operation="cut", keep_tools=True, name="Hollow rear")

# ---------------- mat truoc: cua so kinh + vat mep
WIN = (BX0 + 1.0, BX1 - 1.0, 14.4 + 1.0, 83.6 - 1.0)
cmd("sketch.create", plane="XY", offset=ZF + 1, name="Window")
draw("sketch.rectangle.rounded", p0=[WIN[0], WIN[2]], p1=[WIN[1], WIN[3]], radius=1.0)
cmd("sketch.finish")
cmd("solid.extrude", sketch="Window", distance=4, direction="negative", operation="cut", targets=["Front_Bezel"], name="Window cut")
cmd("solid.chamfer", body="Front_Bezel", edges=[[WIN[0], (WIN[2] + WIN[3]) / 2, ZF]], distance=0.4, name="Window chamfer")

# vau bat vit co lo cay oc nhiet M3 (heat-set insert, ep vao bang mo han tu phia bo mach)
ZPI = ZF - WALL
BOSS_R = 4.4                       # vau D8.8
# lo cay oc nhiet (heat-set insert) M3: nho hon duong kinh ngoai insert (4.2-4.6) de mo han ep vao
INSERT_D, INSERT_DEPTH = 4.0, 4.5  # cho insert dai <= 4 mm, chua 0.5 mm cho nhua chay
HOLE_R = 1.65                      # lo xuyen D3.3
def nut_boss(tag, hx, hy, z0, clip):
    """vau = tru R cat theo mat ngoai vo, bo phan lan vao vung LCD / bo mach (clip), roi gan vao mat truoc"""
    b = f"Boss{tag}"
    cmd("solid.cylinder", radius=BOSS_R, height=ZPI - z0, base=[hx, hy, z0], operation="new", body_name=b, name=f"Boss {tag}")
    cmd("solid.combine", target=b, tools=["OuterRef"], operation="intersect", keep_tools=True, name=f"Trim boss {tag}")
    x0, x1, y0, y1, za, zb = clip
    cmd("solid.box", length=x1 - x0, width=y1 - y0, height=zb - za, corner=[x0, y0, za], operation="cut", targets=[b], name=f"Clip boss {tag}")
    cmd("solid.combine", target="Front_Bezel", tools=[b], operation="join", name=f"Join boss {tag}")
    cmd("solid.cylinder", radius=HOLE_R, height=ZPI - 0.05 - z0 + 1, base=[hx, hy, z0 - 1], operation="cut", targets=["Front_Bezel"], name=f"Screw hole boss {tag}")
    cmd("solid.cylinder", radius=INSERT_D / 2, height=INSERT_DEPTH + 1, base=[hx, hy, z0 - 1], operation="cut",
        targets=["Front_Bezel"], name=f"Insert hole {tag}")

LCD_CLIP = (IX0 + 0.05, BX1 + CLR - 0.05, 14.4 - 0.5, 83.6 + 0.5, -0.1, ZPI - 0.01)     # chua 0.5mm quanh LCD
for i, (hx, hy) in enumerate(HOLES):
    nut_boss(str(i + 1), hx, hy, 0.0, LCD_CLIP)
BOARD_CLIP = (IX0 + 0.05, BX1 + CLR - 0.05, BY0 - 0.3, BY1 + 0.3, ZS - 0.1, ZPI - 0.01)  # chua 0.3mm quanh PCB
for i, (hx, hy) in enumerate(SIDE):
    nut_boss(f"S{i + 1}", hx, hy, ZS, BOARD_CLIP)

# khop bac: mat truoc co go = 0.9mm phia trong cua thanh, keo dai TONGUE xuong duoi mat phan chia;
# than sau khoet bac tuong ung (0.9 + 0.15 khe ho). Go la mot phan cua thanh nen lien khoi.
def inset_body(name, d_expr, d_val, fil_expr):
    """khoi dac = bien dang nem lui vao trong d, bo tron fil (de tao vanh mong trong thanh)"""
    sk = name + " profile"
    cmd("sketch.create", plane="XZ", offset=f"YA + {d_expr}", name=sk)
    cmd("sketch.line", points=[["XT", "-ZF"], ["XF", "-ZF"], ["BBX", "-BBZ"], ["XT", "-ZTB"]], closed=True, construction=True)
    cmd("sketch.offset", curves=["l1", "l2", "l3", "l4"], distance=d_expr, side=[-30.0, 10.0])
    cmd("sketch.finish")
    cmd("solid.extrude", sketch=sk, distance=f"YW - 2 * ({d_expr})", operation="new", body_name=name, name=name + " extrude")
    poly = [tuple(p) for p in list(Polygon(PROFILE).buffer(-d_val, join_style=2).exterior.coords)[:-1]]
    picks = [[x, YM, z] for (x, z) in poly]
    for i in range(len(poly)):
        (xa, za), (xb, zb) = poly[i], poly[(i + 1) % len(poly)]
        for y in (Y0 + d_val, Y1 - d_val):
            picks.append([(xa + xb) / 2, y, (za + zb) / 2])
    cmd("solid.fillet", body=name, edges=picks, radius=fil_expr, name=name + " fillet")

LIP_T, LIP_CLR = 0.9, 0.15
inset_body("Lip", "WALL - 0.9 mm", WALL - LIP_T, "FIL - WALL + 0.9 mm")
cmd("solid.combine", target="Lip", tools=["Cavity"], operation="cut", keep_tools=True, name="Lip ring")
cmd("solid.box", length=200, width=200, height=TONGUE, corner=[-120, -50, ZS - TONGUE], operation="new", body_name="LipSlab", name="Lip slab")
cmd("solid.combine", target="Lip", tools=["LipSlab"], operation="intersect", name="Lip band")
cmd("solid.combine", target="Front_Bezel", tools=["Lip"], operation="join", name="Join lip")
inset_body("Rabbet", "WALL - 1.05 mm", WALL - LIP_T - LIP_CLR, "FIL - WALL + 1.05 mm")
cmd("solid.combine", target="Rabbet", tools=["Cavity"], operation="cut", keep_tools=True, name="Rabbet ring")
cmd("solid.box", length=200, width=200, height=TONGUE + 0.2, corner=[-120, -50, ZS - TONGUE - 0.2], operation="new", body_name="RabbetSlab", name="Rabbet slab")
cmd("solid.combine", target="Rabbet", tools=["RabbetSlab"], operation="intersect", name="Rabbet band")
cmd("solid.remove", bodies=["Cavity"], name="Remove cavity helper")

# ---------------- than sau: cot vit (cat theo mat ngoai), lo xuyen D3.4, lo am dau vit D6.4
SEAT = -8.0
POST_R, CB_R = 4.6, 3.1      # cot D9.2, lo am dau vit D6.2 -> thanh cot >= 1.5 mm (dau M3 luc giac chim D5.5)
cols = []
for i, (hx, hy) in enumerate(LONG + SIDE):
    n = f"Post{i+1}"
    cmd("solid.cylinder", radius=POST_R, height=60 + ZS, base=[hx, hy, -60], operation="new", body_name=n, name=f"Screw post {i+1}")
    cmd("solid.combine", target=n, tools=["OuterRef"], operation="intersect", keep_tools=True, name=f"Trim post {i+1}")
    cols.append(n)
cmd("solid.combine", target="Rear_Body", tools=cols, operation="join", name="Join posts")
cmd("solid.remove", bodies=["OuterRef"], name="Remove helper")

# ---------------- khoang pin: tim vi tri pin sat tuong sau, gan dinh vi
def onfloor(b, u):
    return (FB[0] + B[0] * b + U[0] * u, FB[1] + B[1] * b + U[1] * u)
P = Polygon(PROFILE)
inner = P.buffer(-WALL, join_style=2)
def bat_pts(b0):
    return [onfloor(b0, WALL + 0.05), onfloor(b0 + BAT_W, WALL + 0.05),
            onfloor(b0 + BAT_W, WALL + 0.05 + BAT_T), onfloor(b0, WALL + 0.05 + BAT_T)]
def inside_back(pt, margin):          # khoang cach toi duong mat sau TB->BB (phia trong)
    (xa, za), (xb, zb) = TB, BB
    nx, nz = (zb - za), -(xb - xa); ln = math.hypot(nx, nz); nx, nz = nx / ln, nz / ln
    sg = 1 if ((FT[0] - xa) * nx + (FT[1] - za) * nz) > 0 else -1
    return sg * ((pt[0] - xa) * nx + (pt[1] - za) * nz) >= margin
b0, BAT_B0 = 0.0, None
while b0 < LB:
    if all(inside_back(p, WALL + 0.6) for p in bat_pts(b0)):
        BAT_B0 = b0
    elif BAT_B0 is not None:
        break
    b0 += 0.25
BAT_Y0, BAT_Y1 = (BY0 + BY1) / 2 - BAT_L / 2 - 0.5, (BY0 + BY1) / 2 + BAT_L / 2 + 0.5
embed = P.buffer(-FIL, join_style=2).buffer(FIL - 0.8, join_style=1)   # cach mat ngoai (da bo tron) 0.8mm
def rib(pts, y0, y1, name):
    poly = Polygon(pts).intersection(embed)
    xy = [[round(x, 4), round(-z, 4)] for (x, z) in list(poly.exterior.coords)[:-1]]
    cmd("sketch.create", plane="XZ", offset=y0, name=name)
    cmd("sketch.line", points=xy, closed=True)
    cmd("sketch.constraint.fix", entities=[f"l{i+1}" for i in range(len(xy))])
    cmd("sketch.finish")
    cmd("solid.extrude", sketch=name, distance=y1 - y0, operation="join", targets=["Rear_Body"], name=name + " extrude")
# cac gan deu vat doc <= 41 do so voi phuong dung khi in (mieng than sau up xuong) -> khong can support
side = lambda: [onfloor(BAT_B0 - 9, 0.8), onfloor(LB + 5, 0.8),
                onfloor(LB + 5, WALL + 3.0), onfloor(BAT_B0 + 1, WALL + 3.0), onfloor(BAT_B0 - 9, WALL)]
rib(side(), BAT_Y0 - 1.6, BAT_Y0, "Battery rib L")
rib(side(), BAT_Y1, BAT_Y1 + 1.6, "Battery rib R")
rib([onfloor(BAT_B0 - 7, 0.8), onfloor(BAT_B0, 0.8),
     onfloor(BAT_B0, WALL + 2.5), onfloor(BAT_B0 - 7, WALL)], BAT_Y0 + 6, BAT_Y1 - 6, "Battery front stop")

# khoet bac SAU khi gan cot va gan pin (de chung khong lap vao bac cua khop)
cmd("solid.combine", target="Rear_Body", tools=["Rabbet"], operation="cut", name="Cut rabbet")
# lo vit khoet SAU khi dap gan pin, de gan khong lap vao hoc dau vit
for i, (hx, hy) in enumerate(LONG + SIDE):
    cmd("solid.cylinder", radius=1.7, height=85, base=[hx, hy, -80], operation="cut", targets=["Rear_Body"], name=f"Screw hole {i+1}")
    cmd("solid.cylinder", radius=CB_R, height=80 + SEAT, base=[hx, hy, -80], operation="cut", targets=["Rear_Body"], name=f"Counterbore {i+1}")

# ---------------- khe thoat nhiet tren mat sau
# Huong khoet: lech khoi phuong dung khi in (truc z bo mach) ve phia phap tuyen mat sau, toi da 45 do.
#  -> noc khe nghieng <= 45 do (in khong can support) va mep khe khong bi nhon (khong co thanh mong).
(x1, z1), (x2, z2) = TB, BB
L = math.hypot(x2 - x1, z2 - z1); dx, dz = (x2 - x1) / L, (z2 - z1) / L
nx, nz = dz, -dx                                 # phap tuyen mat sau
if nx * (FT[0] - x1) + nz * (FT[1] - z1) > 0:    # quay ra ngoai
    nx, nz = -nx, -nz
alpha = math.acos(abs(nz)); beta = min(math.radians(45), alpha)
vz = 1.0 if nz > 0 else -1.0                     # truc z cung phia voi phap tuyen
wx = 1.0 if nx > 0 else -1.0                     # huong ngang ve phia phap tuyen
cdx, cdz = wx * math.sin(beta), vz * math.cos(beta)       # huong khoet
ydx, ydz = cdz, -cdx                                       # truc y cua sketch (vuong goc huong khoet)
ox, oz = x1 + dx * 0.4 * L, z1 + dz * 0.4 * L
VENT_W, VENT_PITCH = 1.8, 0.085
cmd("sketch.create", plane={"origin": [round(ox, 4), YM, round(oz, 4)], "x_dir": [0, 1, 0], "y_dir": [round(ydx, 6), 0, round(ydz, 6)]}, name="Vents")
for i in range(6):
    t_ = (0.18 + i * VENT_PITCH) * L
    px, pz = x1 + dx * t_, z1 + dz * t_
    v = (px - ox) * ydx + (pz - oz) * ydz
    draw("sketch.slot.overall", p0=[-23, round(v, 4)], p1=[23, round(v, 4)], width=VENT_W)
cmd("sketch.finish")
cmd("solid.extrude", sketch="Vents", distance=24, direction="symmetric", operation="cut", targets=["Rear_Body"], name="Vent slots")

# ---------------- hoc chan cao su D10 x 1 duoi day
cmd("sketch.create", plane={"origin": [FB[0], 0, FB[1]], "x_dir": [0, 1, 0], "y_dir": [B[0], 0, B[1]]}, name="Feet")
for bb_ in (8.0, LB - 8.0):
    for y in (Y0 + 9, Y1 - 9):
        draw("sketch.circle.center", center=[y, bb_], diameter=10)
cmd("sketch.finish")
cmd("solid.extrude", sketch="Feet", distance=1, operation="cut", targets=["Rear_Body"], name="Feet recesses")

# ---------------- cong tac gat mini SS12D00 (ngat pin) tren thanh ben trai, sau cong USB
# Than 8.6 x 3.6 x 3.5 mm nam trong khung giu o mat trong thanh, can gat thong qua khe 4.5 x 2.2.
# Thanh vo tai cho cong tac mong con 1.2 mm de can gat (G3: 3 mm) nho ra ~1.8 mm. Co dinh bang keo.
SW_XC = -27.75                     # cung do cao voi tam cong USB-C
SW_ZC = -13.0 if VARIANT == "standard" else -24.0   # phia sau cong USB (XL: duoi hoc lom USB)
SW_L, SW_W = 9.0, 4.0              # hoc than cong tac: dai theo x (song song lo USB), rong theo z
SW_RECESS, SW_FRAME_T, SW_FRAME_H = 0.8, 1.2, 3.0
def sbox(x0, x1, y0, y1, z0, z1, op, nm):
    cmd("solid.box", length=x1 - x0, width=y1 - y0, height=z1 - z0, corner=[x0, y0, z0],
        operation=op, targets=["Rear_Body"], name=nm)
fx0, fx1 = SW_XC - SW_L / 2 - SW_FRAME_T, SW_XC + SW_L / 2 + SW_FRAME_T
fz0, fz1 = SW_ZC - SW_W / 2 - SW_FRAME_T, SW_ZC + SW_W / 2
sbox(fx0, fx1, IY0 - 0.5, IY0 + SW_FRAME_H, fz0, fz1, "join", "Switch frame")
# canh khung phia +z (huong man hinh) vat 45 do -> khi in up mieng xuong khong bi treo
wz = [[IY0 - 0.5, fz1], [IY0 + SW_FRAME_H, fz1], [IY0 - 0.5, fz1 + SW_FRAME_H + 0.5]]
cmd("sketch.create", plane="YZ", offset=fx0, name="Switch frame wedge")
cmd("sketch.line", points=[[round(y, 4), round(z, 4)] for y, z in wz], closed=True)
cmd("sketch.constraint.fix", entities=["l1", "l2", "l3"])
cmd("sketch.finish")
cmd("solid.extrude", sketch="Switch frame wedge", distance=fx1 - fx0, operation="join", targets=["Rear_Body"], name="Switch frame wedge extrude")
sbox(SW_XC - SW_L / 2, SW_XC + SW_L / 2, IY0 - SW_RECESS, IY0 + SW_FRAME_H + 1, SW_ZC - SW_W / 2, SW_ZC + SW_W / 2, "cut", "Switch pocket")
cmd("sketch.create", plane="XZ", offset=Y0 - 1.0, name="Switch lever slot")
draw("sketch.slot.overall", p0=[SW_XC - 2.25, -SW_ZC], p1=[SW_XC + 2.25, -SW_ZC], width=2.2)
cmd("sketch.finish")
cmd("solid.extrude", sketch="Switch lever slot", distance=(IY0 - SW_RECESS + 0.05) - (Y0 - 1.0), operation="cut",
    targets=["Rear_Body"], name="Switch lever slot cut")

# ---------------- hoc lom quanh cong USB-C (chi ban XL: thanh ben cach bo mach EW mm)
# Dap mot khoi "thanh cong" ben trong roi khoet hoc tu ngoai vao, de lai thanh 2 mm sat cong USB
# giong ban tieu chuan. Noc hoc vat 45 do -> van in khong can support.
USB_CX, USB_CZ = -27.75, (-1.6 + -4.85) / 2
if EW > 0:
    PW_IN = BY0 - CLR                 # mat trong thanh cong (y)
    PW_OUT = PW_IN - WALL             # day hoc lom (y)
    RX0, RX1, RZ_TOP, RZ_ROOF = USB_CX - 12, USB_CX + 12, 3.0, -9.0
    BX_0, BX_1 = RX0 - 2, RX1 + 2
    def pbox(x0, x1, y0, y1, z0, z1, target, nm):
        cmd("solid.box", length=x1 - x0, width=y1 - y0, height=z1 - z0, corner=[x0, y0, z0],
            operation="join", targets=[target], name=nm)
    pbox(BX_0, BX_1, IY0 - 0.5, PW_IN, ZS, ZPI, "Front_Bezel", "Port wall front")
    pbox(BX_0, BX_1, IY0 - 0.5, PW_IN, -15.0, ZS - TONGUE - 0.2, "Rear_Body", "Port wall rear")
    pbox(BX_0, BX_1, IY0 + 0.15, PW_IN, ZS - TONGUE - 0.2, ZS, "Rear_Body", "Port wall rear (lip zone)")
    yo = Y0 - 1.0
    pts = [[yo, RZ_TOP], [PW_OUT, RZ_TOP], [PW_OUT, RZ_ROOF], [yo, RZ_ROOF - (PW_OUT - yo)]]   # noc doc 45 do
    cmd("sketch.create", plane="YZ", offset=RX0, name="USB-C recess")
    cmd("sketch.line", points=[[round(y, 4), round(z, 4)] for y, z in pts], closed=True)
    cmd("sketch.constraint.fix", entities=["l1", "l2", "l3", "l4"])
    cmd("sketch.finish")
    cmd("solid.extrude", sketch="USB-C recess", distance=RX1 - RX0, operation="cut",
        targets=["Front_Bezel", "Rear_Body"], name="USB-C recess cut")

# ---------------- lo USB-C (canh trai, y-min)
cmd("sketch.create", plane="XZ", offset=BY0 - CLR + 0.02, name="USB-C opening")
draw("sketch.rectangle.rounded", p0=[USB_CX - 6.4, -USB_CZ - 3.6], p1=[USB_CX + 6.4, -USB_CZ + 3.6], radius=3.0)
cmd("sketch.finish")
cmd("solid.extrude", sketch="USB-C opening", distance=20, direction="negative", operation="cut",
    targets=["Front_Bezel", "Rear_Body"], name="USB-C cut")

# (khe the microSD: bo theo yeu cau - the nho chi lap/thao khi mo vo)

# ---------------- cho tranh linh kien (tu kiem tra va cham ban CadQuery)
comps = json.load(open(os.path.join(HERE, "..", "comps.json")))
def comp_box(sub):
    for cc in comps:
        if sub in cc["path"]:
            x0, x1, y0, y1, z0, z1 = cc["bb"]
            return (x0 - 0.3, x1 + 0.3, y0 - 0.3, y1 + 0.3, z0 - 0.3, min(z1, -1.6))
KEEP = [
    ("Front_Bezel", comp_box("MOLEX1.25-WS-4P#181"), "Clear MX1.25 4P (top)"),
    ("Front_Bezel", comp_box("USB-TYPE-C20"), "Clear USB-C body"),
    ("Front_Bezel", comp_box("6246087344/1/Extruded"), "Clear antenna area"),
    ("Rear_Body", (-8.0, -2.9, 37.6, 47.2, -11.0, -1.6), "Clear speaker plug"),
]
for tgt, (x0, x1, y0, y1, z0, z1), nm in KEEP:
    cmd("solid.box", length=x1 - x0, width=y1 - y0, height=z1 - z0, corner=[x0, y0, z0],
        operation="cut", targets=[tgt], name=nm)

# ---------------- mau + mat dat khi in + xuat file
cmd("appearance.assign", bodies=["Front_Bezel"], color="#e8e6df")
cmd("appearance.assign", bodies=["Rear_Body"], color="#3a3f47")

json.dump({"commands": cmds}, open(os.path.join(HERE, OUT_NAME), "w"), indent=1)
print(VARIANT, len(cmds), "commands; battery bay start", BAT_B0, "y", BAT_Y0, BAT_Y1, "width", Y1 - Y0)
