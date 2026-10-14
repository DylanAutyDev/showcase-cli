#!/usr/bin/env python3
"""
ShowcaseCLI - Batch image processor for 1920x1080 showcase presentations
"""

import os
import sys
import re
from pathlib import Path
from colorama import init, Fore, Style
from PIL import Image, ImageFilter, ImageDraw

sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout, 'reconfigure') else None
init(autoreset=True)

LOGO = r"""{cyan}{bold}
 ______     __  __     ______     __     __     ______     ______     ______     ______    
/\  ___\   /\ \_\ \   /\  __ \   /\ \  _ \ \   /\  ___\   /\  __ \   /\  ___\   /\  ___\   
\ \___  \  \ \  __ \  \ \ \/\ \  \ \ \/ ".\ \  \ \ \____  \ \  __ \  \ \___  \  \ \  __\   
 \/\_____\  \ \_\ \_\  \ \_____\  \ \__/".~\_\  \ \_____\  \ \_\ \_\  \/\_____\  \ \_____\ 
  \/_____/   \/_/\/_/   \/_____/   \/_/   \/_/   \/_____/   \/_/\/_/   \/_____/   \/_____/ 
                                                                                           
 ______     __         __                                                                  
/\  ___\   /\ \       /\ \                                                                 
\ \ \____  \ \ \____  \ \ \                                                                
 \ \_____\  \ \_____\  \ \_\                                                               
  \/_____/   \/_____/   \/_/                                                               
{reset}
{yellow}  Image Showcase Generator  v1.1{reset}
{cyan}      1920x1080  -  No Upscale  -  Rounded Corners{reset}
"""


def print_logo():
    print(LOGO.format(
        cyan=Fore.CYAN, yellow=Fore.YELLOW,
        bold=Style.BRIGHT, reset=Style.RESET_ALL
    ))


def heading(text):
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'=' * 56}")
    print(f"  {text}")
    print(f"{'=' * 56}{Style.RESET_ALL}\n")


def prompt(text, default=None):
    if default:
        val = input(f"{Fore.YELLOW}>> {text} {Fore.WHITE}[{default}]{Style.RESET_ALL}: ").strip()
        return val if val else default
    return input(f"{Fore.YELLOW}>> {text}{Style.RESET_ALL}: ").strip()


def confirm(text):
    val = input(f"{Fore.YELLOW}>> {text} {Fore.WHITE}[Y/n]{Style.RESET_ALL}: ").strip().lower()
    return val not in ("n", "no")


def ok(text):
    print(f"  {Fore.GREEN}[OK] {text}{Style.RESET_ALL}")


def info(text):
    print(f"  {Fore.WHITE}[..] {text}{Style.RESET_ALL}")


def warn(text):
    print(f"  {Fore.YELLOW}[!!] {text}{Style.RESET_ALL}")


def err(text):
    print(f"  {Fore.RED}[XX] {text}{Style.RESET_ALL}")


SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".tiff", ".tif", ".webp"}


def get_image_files(directory):
    files = []
    for f in sorted(Path(directory).iterdir()):
        if f.suffix.lower() in SUPPORTED_EXTENSIONS and f.is_file():
            files.append(f)
    return files


def is_valid_color(hex_str):
    return bool(re.match(r"^#?([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$", hex_str.strip()))


def parse_color(hex_str):
    h = hex_str.strip().lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def add_rounded_corners(image, radius):
    mask = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle([(0, 0), (image.width - 1, image.height - 1)], radius=radius, fill=255)
    result = Image.new("RGBA", image.size, (0, 0, 0, 0))
    result.paste(image, (0, 0), mask)
    return result


def process_image(source_path, output_path, background, corner_radius=0):
    img = Image.open(source_path).convert("RGBA")
    w, h = img.size

    if w > 1920:
        scale = 1920.0 / w
        new_w = 1920
        new_h = int(h * scale)
        img = img.resize((new_w, new_h), Image.LANCZOS)
    else:
        new_w, new_h = w, h

    if corner_radius > 0:
        img = add_rounded_corners(img, corner_radius)

    canvas = Image.new("RGBA", (1920, 1080))

    if isinstance(background, tuple):
        canvas.paste(background, (0, 0, 1920, 1080))
    else:
        bg = background.resize((1920, 1080), Image.LANCZOS)
        canvas.paste(bg, (0, 0))
        bg.close()

    paste_x = (1920 - new_w) // 2

    if new_h >= 1080:
        crop_y = (new_h - 1080) // 2
        img = img.crop((0, crop_y, new_w, crop_y + 1080))
        canvas.paste(img, (paste_x, 0), img)
    else:
        paste_y = (1080 - new_h) // 2
        canvas.paste(img, (paste_x, paste_y), img)

    img.close()
    out = canvas.convert("RGB")
    canvas.close()
    out.save(output_path, quality=95)
    out.close()


def run():
    print_logo()

    heading("STEP 1: Source Directory")
    src_dir = prompt("Enter source directory of images")
    src_path = Path(src_dir).resolve()

    if not src_path.is_dir():
        err(f"Directory not found: {src_path}")
        sys.exit(1)

    images = get_image_files(src_path)
    if not images:
        err(f"No supported images found in {src_path}")
        sys.exit(1)

    ok(f"Found {len(images)} image(s) to process")
    for img in images:
        info(f"  - {img.name}")

    if not confirm("Proceed with these images?"):
        info("Aborted by user.")
        sys.exit(0)

    heading("STEP 2: Background Type")
    bg_type = prompt("Background type (0=color / 1=image)", "0").lower()

    background = None
    bg_image_path = None
    blur_radius = 0
    darken_pct = 0

    if bg_type in ("1", "image"):
        bg_path = prompt("Enter path to background image")
        bg_file = Path(bg_path).resolve()
        if not bg_file.is_file():
            err(f"File not found: {bg_file}")
            sys.exit(1)
        bg_image_path = bg_file

        blur_input = prompt("Blur radius (0 = no blur)", "60")
        try:
            blur_radius = int(blur_input)
            if blur_radius < 0:
                raise ValueError
        except ValueError:
            err("Invalid blur radius, using 60")
            blur_radius = 60

        darken_input = prompt("Darken background % (0 = none)", "40")
        try:
            darken_pct = int(darken_input)
            if darken_pct < 0 or darken_pct > 100:
                raise ValueError
        except ValueError:
            err("Invalid percentage, using 40")
            darken_pct = 40

        heading("STEP 3: Confirm Background")
        print(f"  {Fore.WHITE}Background image: {bg_file.name}")
        print(f"  {Fore.WHITE}Blur radius:      {blur_radius}px{Style.RESET_ALL}")
        print(f"  {Fore.WHITE}Darken:           {darken_pct}%{Style.RESET_ALL}")

        if not confirm("Use this background?"):
            info("Aborted.")
            sys.exit(0)

        bg_img = Image.open(bg_image_path).convert("RGBA")
        if blur_radius > 0:
            ok(f"Applying blur (radius={blur_radius})...")
            bg_img = bg_img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
        if darken_pct > 0:
            ok(f"Darkening by {darken_pct}%...")
            overlay = Image.new("RGBA", bg_img.size, (0, 0, 0, int(255 * darken_pct / 100)))
            bg_img = Image.alpha_composite(bg_img, overlay)
        background = bg_img
    else:
        hex_color = prompt("Background hex color", "#1a1a2e")
        if not is_valid_color(hex_color):
            warn(f"Invalid color '{hex_color}', using #1a1a2e")
            hex_color = "#1a1a2e"
        background = parse_color(hex_color)

        heading("STEP 3: Confirm Background")
        r, g, b = background
        print(f"  {Fore.WHITE}Background color: #{r:02x}{g:02x}{b:02x}{Style.RESET_ALL}")

        if not confirm("Use this color?"):
            info("Aborted.")
            sys.exit(0)

    heading("STEP 4: Rounded Corners")
    corner_input = prompt("Corner radius in px (0 = sharp)", "12")
    try:
        corner_radius = int(corner_input)
        if corner_radius < 0:
            raise ValueError
    except ValueError:
        warn("Invalid radius, using 12")
        corner_radius = 12

    heading("STEP 5: Processing")
    out_dir = src_path / "showcase"
    out_dir.mkdir(exist_ok=True)
    ok(f"Output directory: {out_dir}")

    if not confirm("Start processing?"):
        info("Aborted.")
        sys.exit(0)

    success = 0
    failed = 0
    total = len(images)

    for i, img_path in enumerate(images, 1):
        out_name = f"{img_path.stem}_showcase{img_path.suffix}"
        out_file = out_dir / out_name
        try:
            process_image(img_path, out_file, background, corner_radius)
            ok(f"[{i}/{total}] {img_path.name} -> {out_name}")
            success += 1
        except Exception as e:
            err(f"[{i}/{total}] {img_path.name} FAILED: {e}")
            failed += 1

    heading("Done!")
    print(f"  {Fore.GREEN}{Style.BRIGHT}Successfully processed: {success}{Style.RESET_ALL}")
    if failed:
        print(f"  {Fore.RED}{Style.BRIGHT}Failed:                 {failed}{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}Output folder:          {out_dir}{Style.RESET_ALL}")

    if isinstance(background, Image.Image):
        background.close()

    print()


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}\nInterrupted by user.{Style.RESET_ALL}")
        sys.exit(0)
