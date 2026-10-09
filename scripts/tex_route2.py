import sys, json, difflib
sys.path.insert(0, r'C:\git\densha-ts\work\tr')
from texpatch import *
import cv2, easyocr
from scipy.optimize import linear_sum_assignment
from tex_route import EN, CAND, TITLES, BD
sys.stdout.reconfigure(encoding='utf-8')
DRY = len(sys.argv) > 1 and sys.argv[1] == 'dry'
reader = None
MANUAL = {'TU_BD_SKL_RouteName': [
  ((180, 0, 510, 37), (183, 0, 300, 36), 'Ikebukuro'), ((28, 350, 360, 394), (33, 355, 147, 392), 'Shinjuku'),
  ((94, 618, 360, 661), (98, 622, 212, 660), 'Shibuya'), ((142, 706, 462, 749), (146, 710, 322, 748), 'Ebisu'),
  ((452, 980, 732, 1017), (456, 983, 562, 1018), 'Osaki')]}

KANFIX = {('TU_BD_KTL_RouteName', 'Tokyo'): (552, 568, 630, 598), ('TU_BD_UTL_RouteName', 'Tokyo'): (353, 202, 400, 222)}
EXTRA = {'TU_BD_KTL_RouteName': [(548, 562, 632, 599)], 'TU_BD_UTL_RouteName': [(350, 198, 404, 223)]}

def sim(a, b): return difflib.SequenceMatcher(None, a, b).ratio()

def auto_rows(name, lab, white, leader_mask, gmask):
    global reader
    if reader is None: reader = easyocr.Reader(['ja'], gpu=True, verbose=False)
    kw = 26 if name.startswith('TU_BD_RouteName') else 70
    cl = cv2.dilate(gmask.astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_RECT, (kw, 5)))
    n2, l2, s2, _ = cv2.connectedComponentsWithStats(cl, connectivity=8)
    rows = []
    for i in range(1, n2):
        m = (l2 == i) & gmask
        ys, xs = np.where(m)
        if len(xs) < 40: continue
        rows.append(dict(mask=m, box=(int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)))
    rows.sort(key=lambda r: (r['box'][1], r['box'][0]))
    for r in rows:
        m = r['mask']
        nn, ll, ss, _ = cv2.connectedComponentsWithStats(m.astype(np.uint8), connectivity=8)
        comps = [(ss[k][0], ss[k][1], ss[k][2], ss[k][3], k) for k in range(1, nn)]
        hmax = max(c[3] for c in comps)
        big = sorted([c for c in comps if c[3] >= hmax * 0.6], key=lambda c: c[0])
        grp = [big[0]]
        for c in big[1:]:
            if c[0] - (grp[-1][0] + grp[-1][2]) <= 12: grp.append(c)
            else: break
        gx0 = min(c[0] for c in grp); gx1 = max(c[0] + c[2] for c in grp); gy0 = min(c[1] for c in grp); gy1 = max(c[1] + c[3] for c in grp)
        crop = np.where(np.isin(ll[gy0:gy1, gx0:gx1], [c[4] for c in grp]), 0, 255).astype(np.uint8)
        crop = cv2.resize(crop, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        crop = cv2.copyMakeBorder(crop, 24, 24, 24, 24, cv2.BORDER_CONSTANT, value=255)
        r['ocr'] = ''.join(t for _, t, c in reader.readtext(crop, detail=1))
        r['kan'] = (gx0, gy0, gx1, gy1)
    cands = list(CAND[name])
    S = np.array([[sim(r['ocr'], c) for c in cands] for r in rows])
    if len(rows) <= len(cands):
        ri, ci = linear_sum_assignment(-S)
        for a_, b_ in zip(ri, ci): rows[a_]['jp'] = cands[b_]; rows[a_]['en'] = EN[cands[b_]]
    else:
        for k, r in enumerate(rows): j = S[k].argmax(); r['jp'] = cands[j]; r['en'] = EN[cands[j]]
    return rows

def process(name):
    rel = BD + name
    img = load(rel); A = np.asarray(img).astype(int)
    al = A[..., 3]; rgb = A[..., :3]
    sat = rgb.max(axis=2) - rgb.min(axis=2); lum = rgb.mean(axis=2)
    white = ((al > 70) & (sat < 45) & (lum > 150)).astype(np.uint8)
    n, lab, st, _ = cv2.connectedComponentsWithStats(white, connectivity=8)
    leader_mask = np.isin(lab, [i for i in range(1, n) if st[i][2] >= 45])
    gmask = (white > 0) & ~leader_mask
    if name in MANUAL:
        rows = [dict(box=b, kan=k, en=e, jp=e, ocr='') for b, k, e in MANUAL[name]]
        gmask = np.zeros(white.shape, bool)
        for r in rows: gmask[r['box'][1]:r['box'][3], r['box'][0]:r['box'][2]] = True
        erase = gmask & (al > 0)
    else:
        rows = auto_rows(name, lab, white, leader_mask, gmask)
        erase = cv2.dilate(gmask.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
        erase &= ~cv2.dilate(leader_mask.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool)
    for r in rows:
        if (name, r.get('en')) in KANFIX: r['kan'] = KANFIX[(name, r['en'])]
    for b in EXTRA.get(name, []): erase[b[1]:b[3], b[0]:b[2]] |= al[b[1]:b[3], b[0]:b[2]] > 0
    print(name, 'rows', len(rows))
    for r in rows: print('   ', r['box'], repr(r.get('ocr')), '->', r.get('jp'), r.get('en'))
    if DRY: return
    out = np.asarray(img).copy()
    out[erase] = 0
    # title: every visible pixel that is not white ink (leaders/labels) is title or subtitle
    near_white = cv2.dilate(white, np.ones((9, 9), np.uint8)) > 0
    vis = (al > 6) & ~near_white
    vis[erase] = False
    colorm = cv2.morphologyEx((vis & (al > 25)).astype(np.uint8), cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))
    nc, lc, sc, _ = cv2.connectedComponentsWithStats(colorm, connectivity=8)
    comps = [(k, *sc[k]) for k in range(1, nc) if sc[k][4] > 30]
    title = None
    if comps:
        hmax = max(c[4] for c in comps)
        big_ = [c for c in comps if c[4] >= hmax * 0.6]
        by0 = min(c[2] for c in big_); by1 = max(c[2] + c[4] for c in big_)
        tcomps = [c for c in comps if by0 - 6 <= c[2] + c[4] / 2 <= by1 + 6]
        tm = np.isin(lc, [c[0] for c in tcomps])
        tx0 = min(c[1] for c in tcomps); ty0 = min(c[2] for c in tcomps); tx1 = max(c[1] + c[3] for c in tcomps); ty1 = max(c[2] + c[4] for c in tcomps)
        px = A[tm & (al > 25)]
        col = tuple(int(v) for v in np.median(px[:, :3], axis=0)) + (int(np.median(px[:, 3])),)
        out[vis] = 0
        title = (tx0, ty0, tx1, ty1, col)
        print('   title', [int(v) for v in title[:4]], title[4])
    img2 = Image.fromarray(out, 'RGBA'); d = ImageDraw.Draw(img2)
    for r in rows:
        gx0, gy0, gx1, gy1 = r['kan']; x1 = r['box'][2]
        f, size, bb = fit_font(r['en'], 'rodin_db', max(x1 - gx0, 120), gy1 - gy0, 60)
        ty = (gy0 + gy1) // 2 - (bb[3] - bb[1]) // 2 - bb[1]
        d.text((gx0 - bb[0], ty), r['en'], font=f, fill=(255, 255, 255, 255))
    if title:
        tx0, ty0, tx1, ty1, col = title
        f, size, bb = fit_font(TITLES[name], 'rodin_eb', min(max(int((tx1 - tx0) * 1.0), 260), img.width - 8), int((ty1 - ty0) * 0.95), 90)
        cx = (tx0 + tx1) // 2; cy = (ty0 + ty1) // 2
        tw_ = bb[2] - bb[0]; left = min(max(cx - tw_ // 2, 4), img.width - 4 - tw_)
        d.text((left - bb[0], cy - (bb[3] - bb[1]) // 2 - bb[1]), TITLES[name], font=f, fill=col)
    write_texture(rel, img2); print('ok', name)

for nm in CAND: process(nm)
