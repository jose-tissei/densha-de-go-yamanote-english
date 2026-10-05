use std::env;
use std::fs;
use image_dds::{ImageFormat, Mipmaps, Quality, SurfaceRgba8};
use tegra_swizzle::surface::{deswizzle_surface, swizzle_surface, BlockDim};

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
            BlockDim::block_4x4(),
            None,
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
            BlockDim::block_4x4(),
            None,
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
    }
}
