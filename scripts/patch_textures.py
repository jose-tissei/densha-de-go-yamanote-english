import os
import shutil
import subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

font_path = r'work\unpacked\pakchunk1\DgocGame\Content\Art\Data_2D\_font\FOT-RodinPro-EB_0_Default.ufont'
tool_exe = r'work\tools\tegra_tool\target\release\tegra_tool.exe'
repak_exe = r'work\tools\repak\repak.exe'

base_tex_dir = r'work\unpacked\pakchunk1\DgocGame\Content\DgocArt\InGame\Common\Textures'
staging_tex_dir = r'work\staging\DgocGame\Content\DgocArt\InGame\Common\Textures'
os.makedirs(staging_tex_dir, exist_ok=True)

out_tmp = r'work\tools\tegra_tool\output'
os.makedirs(out_tmp, exist_ok=True)

def create_base_text(text, width=256, height=128, font_size=88):
    font = ImageFont.truetype(font_path, font_size)
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    dummy = ImageDraw.Draw(img)
    bbox = dummy.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    x = (width - tw) // 2 - bbox[0]
    y = (height - th) // 2 - bbox[1] - 4
    
    # Shadow layer
    shadow = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.text((x, y + 5), text, font=font, fill=(0, 0, 0, 220), stroke_width=6, stroke_fill=(0, 0, 0, 220))
    shadow = shadow.filter(ImageFilter.GaussianBlur(3))
    
    # Outline layer
    outline = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    o_draw = ImageDraw.Draw(outline)
    o_draw.text((x, y), text, font=font, fill=(0, 0, 0, 255), stroke_width=4, stroke_fill=(0, 0, 0, 255))
    outline = outline.filter(ImageFilter.GaussianBlur(1))
    
    # Text layer
    text_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(text_layer)
    t_draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))
    
    out = Image.alpha_composite(shadow, outline)
    out = Image.alpha_composite(out, text_layer)
    return out

def create_glow_text(text, width=256, height=256, font_size=88):
    font = ImageFont.truetype(font_path, font_size)
    dummy = ImageDraw.Draw(Image.new('RGBA', (width, height)))
    bbox = dummy.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    
    x = (width - tw) // 2 - bbox[0]
    y = (height - th) // 2 - bbox[1] - 4
    
    glow_color = (0, 245, 210)
    
    glow_wide = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    g_draw1 = ImageDraw.Draw(glow_wide)
    g_draw1.text((x, y), text, font=font, fill=glow_color + (160,), stroke_width=18, stroke_fill=glow_color + (160,))
    glow_wide = glow_wide.filter(ImageFilter.GaussianBlur(14))
    
    glow_mid = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    g_draw2 = ImageDraw.Draw(glow_mid)
    g_draw2.text((x, y), text, font=font, fill=glow_color + (230,), stroke_width=10, stroke_fill=glow_color + (230,))
    glow_mid = glow_mid.filter(ImageFilter.GaussianBlur(6))
    
    glow_sharp = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    g_draw3 = ImageDraw.Draw(glow_sharp)
    g_draw3.text((x, y), text, font=font, fill=(0, 200, 180, 255), stroke_width=4, stroke_fill=(0, 200, 180, 255))
    glow_sharp = glow_sharp.filter(ImageFilter.GaussianBlur(2))
    
    white_core = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    w_draw = ImageDraw.Draw(white_core)
    w_draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))
    
    out = Image.alpha_composite(glow_wide, glow_mid)
    out = Image.alpha_composite(out, glow_sharp)
    out = Image.alpha_composite(out, white_core)
    return out

print("[1/4] Generating English textures...")
tex_specs = [
    ('TU_PS_4_01', create_base_text('YES', 256, 128, 88)),
    ('TU_PS_4_02', create_glow_text('YES', 256, 256, 88)),
    ('TU_PS_4_03', create_base_text('NO', 256, 128, 92)),
    ('TU_PS_4_04', create_glow_text('NO', 256, 128, 92)),
]

for name, img in tex_specs:
    png_path = os.path.join(out_tmp, f'{name}_en.png')
    img.save(png_path)
    print(f"  Saved {png_path} ({img.size})")

print("\n[2/4] Patching uexp files via tegra_tool...")
for name, _ in tex_specs:
    png_path = os.path.join(out_tmp, f'{name}_en.png')
    base_uexp = os.path.join(base_tex_dir, f'{name}.uexp')
    base_uasset = os.path.join(base_tex_dir, f'{name}.uasset')
    staged_uexp = os.path.join(staging_tex_dir, f'{name}.uexp')
    staged_uasset = os.path.join(staging_tex_dir, f'{name}.uasset')
    
    # Copy original uasset to staging
    shutil.copy(base_uasset, staged_uasset)
    
    # Convert PNG to patched uexp in staging
    cmd = [tool_exe, 'png_to_uexp', png_path, base_uexp, staged_uexp]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"  [!] Error patching {name}: {res.stderr}")
    else:
        print(f"  [+] Successfully patched {name}.uexp into staging")

print("\n[3/4] Repacking pakchunk0-Switch_99_P.pak and pakchunk99-Switch.pak...")
staging_root = r'C:\git\densha-ts\work\staging'
pak_p = r'C:\git\densha-ts\work\pakchunk0-Switch_99_P.pak'
pak_99 = r'C:\git\densha-ts\work\pakchunk99-Switch.pak'

for pak in [pak_p, pak_99]:
    cmd = [repak_exe, "pack", staging_root, pak, "--version", "V8B", "--compression", "Zlib"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode == 0:
        print(f"  [+] Packed {pak} ({os.path.getsize(pak)} bytes)")
    else:
        print(f"  [!] Error packing {pak}: {res.stderr}")

print("\n[4/4] Deploying to LayeredFS, atmosphere, and Ryujinx...")
targets = [
    r'C:\git\densha-ts\work\atmosphere\contents\0100BC501355A000\romfs\DgocGame',
    r'C:\git\densha-ts\work\LayeredFS\0100BC501355A000\romfs\DgocGame',
    r'C:\git\densha-ts\work\tools\ryujinx\publish\portable\mods\contents\0100bc501355a000\EnglishMod\romfs\DgocGame',
    r'C:\git\densha-ts\work\tools\ryujinx\publish\portable\sdcard\atmosphere\contents\0100bc501355a000\romfs\DgocGame',
]

for t in targets:
    paks_dir = os.path.join(t, 'Content', 'Paks')
    os.makedirs(paks_dir, exist_ok=True)
    shutil.copy(pak_p, os.path.join(paks_dir, os.path.basename(pak_p)))
    shutil.copy(pak_99, os.path.join(paks_dir, os.path.basename(pak_99)))
    
    # Also deploy loose texture files for direct override
    loose_tex_dir = os.path.join(t, 'Content', 'DgocArt', 'InGame', 'Common', 'Textures')
    os.makedirs(loose_tex_dir, exist_ok=True)
    for name, _ in tex_specs:
        shutil.copy(os.path.join(staging_tex_dir, f'{name}.uasset'), os.path.join(loose_tex_dir, f'{name}.uasset'))
        shutil.copy(os.path.join(staging_tex_dir, f'{name}.uexp'), os.path.join(loose_tex_dir, f'{name}.uexp'))

print("\n=== All textures patched, repacked, and deployed successfully! ===")
