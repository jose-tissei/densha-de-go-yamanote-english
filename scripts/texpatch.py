import os, sys, json, subprocess, tempfile, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, r'C:\git\densha-ts\work\tr')
from texinfo import parse

W = r'C:\git\densha-ts\work'
TOOL = f'{W}/tools/tegra_tool/target/release/tegra_tool.exe'
STAGE = f'{W}/staging/DgocGame/Content/DgocArt'
FONTDIR = f'{W}/unpacked/pakchunk1/DgocGame/Content/Art/Data_2D/_font'
IDX = json.load(open(f'{W}/texdump_index.json'))

FONTS = {
    'regular': f'{W}/unpacked/pakchunk0/Engine/Content/Slate/Fonts/Roboto-Regular.ttf',
    'bold': f'{W}/unpacked/pakchunk0/Engine/Content/Slate/Fonts/Roboto-Bold.ttf',
    'rodin_m': f'{FONTDIR}/FOT-RodinPro-M_0_Default.ufont',
    'rodin_db': f'{FONTDIR}/FOT-RodinPro-DB_0_Default.ufont',
    'rodin_eb': f'{FONTDIR}/FOT-RodinPro-EB_0_Default.ufont',
    'georgia_b': r'C:\Windows\Fonts\georgiab.ttf',
    'times_b': r'C:\Windows\Fonts\timesbd.ttf',
}
_fc = {}
def font(name, size):
    k = (name, size)
    if k not in _fc: _fc[k] = ImageFont.truetype(FONTS[name], size)
    return _fc[k]

def load(rel):
    return Image.open(f'{W}/texdump/{rel}.png').convert('RGBA')

def fit_font(text, name, max_w, max_h, start=200):
    size = start
    while size > 6:
        f = font(name, size)
        bb = ImageDraw.Draw(Image.new('RGBA', (1, 1))).multiline_textbbox((0, 0), text, font=f, spacing=int(size * 0.2))
        if bb[2] - bb[0] <= max_w and bb[3] - bb[1] <= max_h: return f, size, bb
        size -= 1
    return font(name, 6), 6, (0, 0, 6, 6)

def clear(img, box, rgb=(255, 255, 255)):
    a = np.asarray(img).copy()
    x0, y0, x1, y1 = box
    a[y0:y1, x0:x1, :3] = rgb
    a[y0:y1, x0:x1, 3] = 0
    return Image.fromarray(a, 'RGBA')

def scrim(img, box, strength=0.78, bottom_bias=True):
    a = np.asarray(img).astype(np.float32).copy()
    x0, y0, x1, y1 = box
    h = y1 - y0
    ramp = np.linspace(0.55, 1.0, h)[:, None] if bottom_bias else np.ones((h, 1))
    k = (strength * ramp)[..., None]
    a[y0:y1, x0:x1, :3] = a[y0:y1, x0:x1, :3] * (1 - k)
    return Image.fromarray(a.clip(0, 255).astype(np.uint8), 'RGBA')

def draw_text(img, box, text, fontname='regular', color=(255, 255, 255, 255), align='center', valign='middle',
              max_size=200, shadow=None, spacing=0.2, stroke=0):
    x0, y0, x1, y1 = box
    f, size, bb = fit_font(text, fontname, x1 - x0, y1 - y0, max_size)
    d = ImageDraw.Draw(img)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    x = x0 + {'left': 0, 'center': (x1 - x0 - tw) // 2, 'right': x1 - x0 - tw}[align] - bb[0]
    y = y0 + {'top': 0, 'middle': (y1 - y0 - th) // 2, 'bottom': y1 - y0 - th}[valign] - bb[1]
    if shadow:
        d.multiline_text((x + 2, y + 2), text, font=f, fill=shadow, align=align, spacing=int(size * spacing))
    d.multiline_text((x, y), text, font=f, fill=color, align=align, spacing=int(size * spacing), stroke_width=stroke,
                     stroke_fill=(0, 0, 0, 255))
    return img, size

def text_bbox_alpha(img, thr=40):
    al = np.asarray(img)[..., 3]
    ys, xs = np.where(al > thr)
    return xs.min(), ys.min(), xs.max() + 1, ys.max() + 1

def write_texture(rel, img):
    v = IDX[rel]
    fp = f"{W}/unpacked/pakchunk{v['chunk']}/DgocGame/Content/DgocArt/{rel}.uexp"
    r = parse(fp)
    m = r['mips'][0]
    assert (m['w'], m['h']) == (v['w'], v['h']) and img.size == (v['w'], v['h']), (rel, img.size, (v['w'], v['h']))
    pad = Image.new('RGBA', (v['wp'], v['h']), (0, 0, 0, 0))
    pad.paste(img, (0, 0))
    tmp = tempfile.mktemp(suffix='.png'); tmpb = tmp + '.bin'
    try:
        pad.save(tmp)
        p = subprocess.run([TOOL, 'encode_bgra' if v.get('fmt') == 'PF_B8G8R8A8' else 'encode_bc7', tmp, tmpb, str(v['bh'])], capture_output=True, text=True)
        if p.returncode != 0: raise RuntimeError(p.stderr[-300:])
        data = open(tmpb, 'rb').read()
    finally:
        for t in (tmp, tmpb):
            try: os.remove(t)
            except: pass
    if len(data) != m['cnt']: raise RuntimeError(f'{rel}: size {len(data)} != {m["cnt"]}')
    raw = bytearray(r['raw']); raw[m['off']:m['off'] + m['cnt']] = data
    out = f'{STAGE}/{rel}.uexp'
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, 'wb').write(raw)
    shutil.copy(fp[:-5] + '.uasset', f'{STAGE}/{rel}.uasset')
    os.makedirs(f'{W}/texout', exist_ok=True)
    pr = f'{W}/texout/{rel}.png'; os.makedirs(os.path.dirname(pr), exist_ok=True); img.save(pr)
