use std::env;
use std::fs;
use image_dds::{ImageFormat, Mipmaps, Quality, SurfaceRgba8};
use tegra_swizzle::surface::{deswizzle_surface, swizzle_surface, BlockDim};
use tegra_swizzle::BlockHeight;

fn bh_arg(a: Option<&String>) -> Option<BlockHeight> {
    match a.map(|s| s.as_str()) {
        Some("1") => Some(BlockHeight::One),
        Some("2") => Some(BlockHeight::Two),
        Some("4") => Some(BlockHeight::Four),
        Some("8") => Some(BlockHeight::Eight),
        Some("16") => Some(BlockHeight::Sixteen),
        Some("32") => Some(BlockHeight::ThirtyTwo),
        _ => None,
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: tegra_tool <deswizzle|swizzle|png_to_uexp> [args...]");
        return;
    }

    let cmd = &args[1];

    if cmd == "deswizzle" {
        if args.len() < 7 {
            eprintln!("Usage: tegra_tool deswizzle <in_bin> <out_bin> <width> <height> <bytes_per_block>");
            return;
        }
        let in_file = &args[2];
        let out_file = &args[3];
        let width: u32 = args[4].parse().unwrap();
        let height: u32 = args[5].parse().unwrap();
        let bpb: u32 = args[6].parse().unwrap();

        let input_bytes = fs::read(in_file).expect("Failed to read input file");
        let deswizzled = deswizzle_surface(
            width,
            height,
            1,
            &input_bytes,
            if args.get(8).map(|x| x=="1").unwrap_or(false) { BlockDim::uncompressed() } else { BlockDim::block_4x4() },
            bh_arg(args.get(7)),
            bpb,
            1,
            1,
        ).expect("Failed to deswizzle surface");

        fs::write(out_file, deswizzled).expect("Failed to write output file");
        println!("Successfully deswizzled {}x{} (bpb={}) to {}", width, height, bpb, out_file);
    } else if cmd == "swizzle" {
        if args.len() < 7 {
            eprintln!("Usage: tegra_tool swizzle <in_bin> <out_bin> <width> <height> <bytes_per_block>");
            return;
        }
        let in_file = &args[2];
        let out_file = &args[3];
        let width: u32 = args[4].parse().unwrap();
        let height: u32 = args[5].parse().unwrap();
        let bpb: u32 = args[6].parse().unwrap();

        let input_bytes = fs::read(in_file).expect("Failed to read input file");
        let swizzled = swizzle_surface(
            width,
            height,
            1,
            &input_bytes,
            if args.get(8).map(|x| x=="1").unwrap_or(false) { BlockDim::uncompressed() } else { BlockDim::block_4x4() },
            bh_arg(args.get(7)),
            bpb,
            1,
            1,
        ).expect("Failed to swizzle surface");

        fs::write(out_file, swizzled).expect("Failed to write output file");
        println!("Successfully swizzled {}x{} (bpb={}) to {}", width, height, bpb, out_file);
    } else if cmd == "png_to_uexp" {
        if args.len() < 5 {
            eprintln!("Usage: tegra_tool png_to_uexp <in_png> <base_uexp> <out_uexp>");
            return;
        }
        let in_png = &args[2];
        let base_uexp = &args[3];
        let out_uexp = &args[4];

        let img = image::open(in_png).expect("Failed to open input PNG").to_rgba8();
        let (width, height) = (img.width(), img.height());
        println!("Loaded PNG {} ({}x{})", in_png, width, height);

        let surface = SurfaceRgba8::from_image(&img);
        let encoded = surface
            .encode(ImageFormat::BC7RgbaUnorm, Quality::Normal, Mipmaps::Disabled)
            .expect("Failed to encode to BC7");
        println!("Encoded BC7 linear data ({} bytes)", encoded.data.len());

        let swizzled = swizzle_surface(
            width,
            height,
            1,
            &encoded.data,
            BlockDim::block_4x4(),
            None,
            16,
            1,
            1,
        ).expect("Failed to swizzle to Tegra BlockLinear");
        println!("Swizzled Tegra data ({} bytes)", swizzled.len());

        let mut uexp_bytes = fs::read(base_uexp).expect("Failed to read base uexp");
        let data_start = 321usize;
        let data_end = data_start + swizzled.len();
        if uexp_bytes.len() < data_end {
            panic!("Base uexp file is smaller than expected data end");
        }

        uexp_bytes[data_start..data_end].copy_from_slice(&swizzled);
        fs::write(out_uexp, uexp_bytes).expect("Failed to write output uexp");
        println!("Successfully created patched uexp at {}", out_uexp);
    } else if cmd == "encode_bc7" {
        // encode_bc7 <in_png> <out_bin> [block_height]  -> Tegra-swizzled BC7 (mip0 only)
        let img = image::open(&args[2]).expect("Failed to open input PNG").to_rgba8();
        let (width, height) = (img.width(), img.height());
        let surface = SurfaceRgba8::from_image(&img);
        let encoded = surface
            .encode(ImageFormat::BC7RgbaUnorm, Quality::Normal, Mipmaps::Disabled)
            .expect("Failed to encode to BC7");
        let swizzled = swizzle_surface(width, height, 1, &encoded.data, BlockDim::block_4x4(), bh_arg(args.get(4)), 16, 1, 1)
            .expect("Failed to swizzle");
        fs::write(&args[3], &swizzled).expect("write");
        println!("{}x{} -> {} bytes", width, height, swizzled.len());
    } else if cmd == "encode_bgra" {
        // encode_bgra <in_png> <out_bin> [block_height] -> Tegra-swizzled raw BGRA8 (mip0 only)
        let img = image::open(&args[2]).expect("open").to_rgba8();
        let (width, height) = (img.width(), img.height());
        let mut raw = img.into_raw();
        for px in raw.chunks_mut(4) { px.swap(0, 2); }
        let swizzled = swizzle_surface(width, height, 1, &raw, BlockDim::uncompressed(), bh_arg(args.get(4)), 4, 1, 1).expect("swizzle");
        fs::write(&args[3], &swizzled).expect("write");
        println!("{}x{} -> {} bytes", width, height, swizzled.len());
    }
}
