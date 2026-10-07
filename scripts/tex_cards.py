import sys
sys.path.insert(0, r'C:\git\densha-ts\work\tr')
from texpatch import *
from PIL import ImageFilter

CAP = {
 '201': "The Yamanote Line officially runs between Shinagawa and Tabata via Shinjuku. Together with the Tohoku Main Line and Tokaido Main Line through Tokyo Station, it forms a loop line connecting the heart of Japan's capital, and is familiar to many with its uguisu-green line color.",
 '202': 'The Sobu Line, officially the "Chuo-Sobu Local Line", runs all-stops service from Chiba Station on the Sobu Line via Ochanomizu to Mitaka Station on the Chuo Line. Its yellow line color is familiar to many.',
 '203': 'The "Saikyo Line" is the popular name for the route linking Omiya Station and Osaki Station via the Tohoku Main Line, the Akabane Line and the Yamanote Freight Line, and is familiar to many.',
 '204': 'The "Ueno-Tokyo Line" is the nickname of the service pattern in which Utsunomiya, Takasaki and Joban line trains, which once terminated at Ueno, run through Tokyo Station onto the Tokaido Line, further enriching the Tokyo-area rail network.',
 '205': 'The "Keihin-Tohoku Line" is the popular name for the route linking Omiya and Yokohama via Tokyo Station. Omiya to Tokyo is part of the Tohoku Main Line, and Tokyo to Yokohama is part of the Tokaido Main Line.',
 '206': 'The "Narita Express" directly links Narita Airport with major stations in the Tokyo area, including Tokyo, Ikebukuro, Shinjuku, Yokohama and Omiya.',
 '221': 'Developed as the standard for the next generation of Tokyo-area commuter trains, aiming for further service and stability improvements. Its keyword is "a train that communicates with passengers and society." The large-windowed front end represents a window of information connecting people to people and to society. It introduces many new technologies, such as more in-car LCD monitors than the E233 series and the "INTEROS" train information management system, successor to "TIMS".',
 '222': 'Developed after the 209 and E217 series, the E231 series introduced the "TIMS" train information management system and, in the commuter type, a wide body to ease crowding. The 500 subseries was introduced for the Yamanote Line, with a new front design and LCD passenger information displays. With the E235 series arriving on the Yamanote Line, it has run on the Sobu Line since 2014 with a changed stripe color.',
 '223': 'A train that inherits the technology cultivated in the E231 series. Main equipment is duplicated for better reliability, and many universal-design features are used, such as lowered luggage racks and hand straps. Air purifiers and expanded passenger information also reflect passengers\' needs.',
 '224': 'A limited express train that inherits the brand image of "N\'EX", synonymous with airport express service, built up by the 253 series that debuted in 1991. It uses universal design to improve comfort and security.',
 '225': 'A suburban train succeeding the 113 series, active on the Yokosuka Line, Sobu Rapid Line, Sobu Main Line and more. Ordinary-car seating is mostly longitudinal to handle crowding, but long-distance use is also considered, and some cars have box seats.',
 '226': 'A limited express train developed in the National Railways era for wide use from limited express to commuter service. It has wide deck areas and two doorways per ordinary car for smooth boarding and alighting.',
 '227': 'A limited express train that debuted as the "Super View Odoriko". Made up of double-decker and high-decker cars, it has large glass panels on the front and sides so passengers can enjoy the view from the windows.',
 '228': 'Developed to ease crowding on the Tokaido Line and debuted in 1992. The first all-double-decker train on conventional lines, a suburban train with greatly increased seating.',
 '229': 'A limited express train based on the 183 series and modified to allow cooperative operation with electric locomotives.',
}

BAND = {'221': 250, '222': 250, '223': 230, '224': 230, '225': 230, '226': 230, '227': 230, '228': 200, '229': 200}

def wrap(text, f, max_w):
    d = ImageDraw.Draw(Image.new('RGBA', (1, 1)))
    lines, cur = [], ''
    for w in text.split(' '):
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=f) <= max_w: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur)
    return lines

def caption_band(img):
    a = np.asarray(img.convert('RGB')).astype(int)
    h, w = a.shape[:2]
    lum = a.min(axis=2)
    rows = (lum > 225).sum(axis=1)
    cand = [y for y in range(int(h * 0.55), h) if rows[y] > w * 0.004]
    y0 = max(int(h * 0.55), (min(cand) if cand else int(h * 0.8)) - 10)
    return y0

def render(img, text, size_max=30, band_h=150):
    w, h = img.size
    y0 = h - band_h
    band = img.crop((0, y0, w, h)).convert('RGBA')
    soft = band.filter(ImageFilter.GaussianBlur(7))
    arr = np.asarray(soft).astype(np.float32)
    bh = h - y0
    t = np.linspace(0, 1, bh); ramp = (0.85 * np.clip(t / 0.35, 0, 1) ** 1.2)[:, None, None]
    arr[..., :3] *= (1 - ramp)
    arr[..., 3] = 255
    band = Image.fromarray(arr.clip(0, 255).astype(np.uint8), 'RGBA')
    pad = 20
    avail_w, avail_h = w - 2 * pad, bh - 12
    size = size_max
    while size > 12:
        f = font('rodin_m', size)
        lines = wrap(text, f, avail_w)
        lh = int(size * 1.28)
        if lh * len(lines) <= avail_h: break
        size -= 1
    d = ImageDraw.Draw(band)
    total = lh * len(lines)
    y = bh - total - 14
    for ln in lines:
        d.text((pad + 1, y + 2), ln, font=f, fill=(0, 0, 0, 255), stroke_width=2, stroke_fill=(0, 0, 0, 255))
        d.text((pad, y), ln, font=f, fill=(255, 255, 255, 255))
        y += lh
    out = img.copy().convert('RGBA'); out.paste(band, (0, y0))
    return out, size, len(lines), y0

def run():
    for k, t in CAP.items():
        rel = f'Common/Textures/Support/TU_SU_term_{k}'
        if rel not in IDX: print('skip', rel); continue
        img = load(rel)
        out, size, nl, y0 = render(img, t, 30, BAND.get(k, 150))
        print(k, img.size, 'band from', y0, 'font', size, 'lines', nl)
        write_texture(rel, out)

if __name__ == '__main__':
    run()
