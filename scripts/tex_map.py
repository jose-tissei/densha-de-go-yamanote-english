import sys, os, json, shutil
sys.path.insert(0, r'C:\git\densha-ts\work\tr')
from texpatch import *
import cv2
sys.stdout.reconfigure(encoding='utf-8')
SUP = 'Common/Textures/Support'
BAK = f'{W}/texout_bak/Support'
os.makedirs(BAK, exist_ok=True)

PF = {'埼玉': 'Saitama', '千葉': 'Chiba', '東京': 'Tokyo', '神奈川': 'Kanagawa', '茨城': 'Ibaraki', '山梨': 'Yamanashi',
      '福島': 'Fukushima', '新潟': 'Niigata', '富山': 'Toyama', '群馬': 'Gunma', '栃木': 'Tochigi', '石川': 'Ishikawa',
      '長野': 'Nagano', '福井': 'Fukui', '岐阜': 'Gifu', '滋賀': 'Shiga', '静岡': 'Shizuoka', '愛知': 'Aichi', '岐卓': 'Gifu'}

# (box incl. furigana, english)
ST = {
 201: [((616, 124, 714, 184), 'Ikebukuro'), ((820, 128, 892, 190), 'Ueno'), ((586, 230, 678, 290), 'Shinjuku'),
       ((816, 262, 908, 320), 'Tokyo'), ((612, 314, 684, 376), 'Shibuya'), ((766, 376, 840, 436), 'Shinagawa')],
 202: [((394, 252, 466, 312), 'Mitaka'), ((568, 252, 662, 312), 'Shinjuku'), ((738, 155, 878, 218), 'Ochanomizu'),
       ((828, 266, 942, 328), 'Kinshicho'), ((984, 114, 1062, 174), 'Ichikawa'), ((1102, 166, 1182, 224), 'Funabashi'),
       ((1252, 256, 1332, 318), 'Makuhari'), ((1342, 362, 1418, 424), 'Chiba')],
 203: [((726, 12, 800, 76), 'Omiya'), ((582, 126, 722, 184), 'Musashi-Urawa'), ((840, 204, 916, 264), 'Akabane'),
       ((708, 274, 802, 334), 'Ikebukuro'), ((696, 356, 780, 416), 'Shinjuku'), ((740, 450, 832, 512), 'Osaki')],
 204: [((726, 0, 802, 60), 'Kuroiso'), ((688, 74, 780, 128), 'Utsunomiya'), ((594, 108, 668, 164), 'Maebashi'),
       ((520, 166, 592, 226), 'Takasaki'), ((956, 44, 1034, 106), 'Takahagi'), ((908, 176, 976, 232), 'Mito'),
       ((642, 256, 718, 314), 'Omiya'), ((882, 298, 950, 358), 'Narita'), ((762, 340, 852, 396), 'Tokyo'),
       ((718, 402, 792, 460), 'Yokohama'), ((642, 436, 716, 496), 'Ofuna'), ((522, 420, 594, 482), 'Numazu')],
 205: [((624, 12, 698, 72), 'Omiya'), ((782, 42, 852, 100), 'Urawa'), ((720, 146, 788, 202), 'Tabata'),
       ((840, 140, 910, 196), 'Ueno'), ((872, 198, 976, 258), 'Akihabara'), ((856, 262, 942, 318), 'Tokyo'),
       ((726, 290, 802, 348), 'Shinagawa'), ((802, 400, 880, 458), 'Kawasaki'), ((620, 478, 702, 532), 'Yokohama')],
 206: [((776, 6, 852, 66), 'Omiya'), ((598, 126, 672, 184), 'Tachikawa'), ((484, 190, 552, 250), 'Takao'),
       ((704, 214, 790, 274), 'Shinjuku'), ((854, 182, 942, 240), 'Tokyo'), ((828, 266, 898, 322), 'Shinagawa'),
       ((684, 314, 756, 368), 'Yokohama'), ((616, 436, 684, 496), 'Ofuna'), ((1164, 160, 1294, 220), 'Narita Airport')],
}
# manual gray prefecture labels (kanji box only, no furigana)
PFX = {204: [((594, 262, 636, 288), (594, 262, 636, 288), 'Saitama'), ((195, 503, 245, 530), (195, 503, 245, 530), 'Aichi')],
       201: [((350, 228, 438, 294), (352, 250, 436, 292), 'Tokyo')]}

def base(n):
    p = f'{BAK}/term_{n}.png'
    if not os.path.exists(p): shutil.copy(f'{W}/texout/{SUP}/TU_SU_term_{n}.png', p)
    return Image.open(p).convert('RGBA')

def erase(img, box, kind, grow=4):
    a = np.asarray(img).copy(); x0, y0, x1, y1 = box
    sub = a[y0:y1, x0:x1, :3].astype(float); lum = sub.mean(axis=2)
    sat = sub.max(axis=2) - sub.min(axis=2)
    sat_full = np.zeros(a.shape[:2]); sat_full[y0:y1, x0:x1] = sat
    neutral = lum[(lum > 90) & (lum < 140) & (sat < 12)]
    bg = np.median(neutral) if neutral.size > 20 else 112.0
    m = (np.abs(lum - bg) > (20 if kind == 'st' else 16)) & (sat < 30)
    mm = np.zeros(a.shape[:2], np.uint8); mm[y0:y1, x0:x1] = m
    mm = cv2.dilate(mm, np.ones((grow * 2 + 1,) * 2, np.uint8))
    keep = np.zeros_like(mm); keep[y0:y1, x0:x1] = 1; mm *= keep
    out = cv2.inpaint(np.ascontiguousarray(a[..., :3]), mm, 7, cv2.INPAINT_TELEA).astype(float)
    ol = out.mean(axis=2); osat = out.max(axis=2) - out.min(axis=2)
    bad = (mm > 0) & (ol > bg + 18) & (sat_full < 30)
    out[bad] = bg
    a[..., :3] = out.astype(np.uint8)
    return Image.fromarray(a, 'RGBA')

def pf_color(img, box):
    x0, y0, x1, y1 = box
    sub = np.asarray(img)[y0:y1, x0:x1, :3].reshape(-1, 3).astype(float)
    l = sub.mean(axis=1); top = sub[l >= np.percentile(l, 92)]
    return tuple(int(v) for v in np.median(top, axis=0)) + (255,)

def draw_station(img, box, text):
    x0, y0, x1, y1 = box; w = x1 - x0; cx = (x0 + x1) // 2; cy = y1 - 21
    f, size, bb = fit_font(text, 'rodin_eb', int(w * (1.9 if text == 'Narita Airport' else 1.1)), 30, 120)
    d = ImageDraw.Draw(img); tw, th = bb[2] - bb[0], bb[3] - bb[1]
    pos = (cx - tw // 2 - bb[0], cy - th // 2 - bb[1])
    d.text(pos, text, font=f, fill=(255, 255, 255, 255), stroke_width=7, stroke_fill=(255, 255, 255, 255))
    d.text(pos, text, font=f, fill=(0, 0, 0, 255), stroke_width=5, stroke_fill=(0, 0, 0, 255))
    d.text(pos, text, font=f, fill=(255, 255, 255, 255))

def draw_pf(img, box, text, col, kanji_box):
    x0, y0, x1, y1 = kanji_box; w = x1 - x0; h = y1 - y0
    f, size, bb = fit_font(text, 'rodin_eb', int(w * 1.7), int(h * 0.78), 120)
    d = ImageDraw.Draw(img); tw, th = bb[2] - bb[0], bb[3] - bb[1]
    d.text(((x0 + x1) // 2 - tw // 2 - bb[0], (y0 + y1) // 2 - th // 2 - bb[1]), text, font=f, fill=col)

ocr = json.load(open(f'{W}/ocr_terms.json', encoding='utf-8'))
for n in range(201, 207):
    img = base(n)
    k = f'TU_SU_term_{n}'
    # prefectures from OCR
    hits = ocr[k]; kan = []; fur = []
    for h in hits:
        t = h['t'].strip('_ ')
        if t in PF: kan.append((t, h['b']))
        elif all('\u3040' <= c <= '\u309f' for c in t) and h['c'] > 0.5: fur.append(h['b'])
    jobs = []
    for t, b in kan:
        u = list(b)
        for fb in fur:
            if abs((fb[0] + fb[2]) / 2 - (b[0] + b[2]) / 2) < 70 and -30 <= b[1] - fb[3] < 50:
                u = [min(u[0], fb[0]), min(u[1], fb[1]), max(u[2], fb[2]), u[3]]
        jobs.append((tuple(u), b, PF[t]))
    for (u, b, t) in PFX.get(n, []): jobs.append((u, b, t))
    cols = {}
    for u, b, t in jobs:
        cols[u] = pf_color(img, tuple(b))
    for u, b, t in jobs:
        img = erase(img, (max(u[0] - 4, 0), max(u[1] - 4, 0), min(u[2] + 4, img.width), min(u[3] + 4, img.height)), 'pf', 2)
    for u, b, t in jobs:
        draw_pf(img, u, t, cols[u], b if n != 204 or t in ('Saitama', 'Aichi') or True else b)
    for b, t in ST.get(n, []):
        img = erase(img, (b[0] - 2, max(b[1] - 8, 0), b[2] + 2, b[3] + 2), 'st', 4)
    for b, t in ST.get(n, []):
        draw_station(img, b, t)
    write_texture(f'{SUP}/TU_SU_term_{n}', img)
    print('ok', n, len(jobs), len(ST.get(n, [])))
