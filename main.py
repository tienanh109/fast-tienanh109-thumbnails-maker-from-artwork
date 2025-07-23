# Made by tienanh109 with Python (Pillow)
from PIL import Image, ImageFilter, ImageDraw
import sys
import os

def create_wallpaper(input_path, output_path='output.png',
                     base_size=(1920, 1080), margin_percent=0.1,
                     blur_radius=20, shadow_offset=10):
    try:
        img = Image.open(input_path).convert("RGBA")
    except Exception as e:
        print(f"Cant opening image: {e}")
        return

    input_width, input_height = img.size
    base_width, base_height = base_size

    
    scale = max(base_width / input_width, base_height / input_height)
    bg_img = img.resize((int(input_width * scale), int(input_height * scale)))
    bg_img = bg_img.crop((
        (bg_img.width - base_width) // 2,
        (bg_img.height - base_height) // 2,
        (bg_img.width + base_width) // 2,
        (bg_img.height + base_height) // 2
    ))
    bg_img = bg_img.filter(ImageFilter.GaussianBlur(blur_radius))

  
    fg_margin_w = int(base_width * margin_percent)
    fg_margin_h = int(base_height * margin_percent)
    fg_width = base_width - 2 * fg_margin_w
    fg_height = base_height - 2 * fg_margin_h

    scale_fg = min(fg_width / input_width, fg_height / input_height)
    fg_img = img.resize((int(input_width * scale_fg), int(input_height * scale_fg)))


    shadow = Image.new("RGBA", (fg_img.width + shadow_offset*2, fg_img.height + shadow_offset*2), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rectangle(
        [shadow_offset, shadow_offset, shadow_offset + fg_img.width, shadow_offset + fg_img.height],
        fill=(0, 0, 0, 100)
    )


    background = Image.new("RGBA", base_size)
    background.paste(bg_img, (0, 0))
    center_x = (base_width - fg_img.width) // 2
    center_y = (base_height - fg_img.height) // 2
    background.paste(shadow, (center_x - shadow_offset, center_y - shadow_offset), shadow)
    background.paste(fg_img, (center_x, center_y), fg_img)

    background.convert("RGB").save(output_path)
    print(f"Output saved to {output_path} ({base_width}x{base_height})")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py your_image.jpg/png/webp/...")
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.exists(input_file):
        print("File not found:", input_file)
        sys.exit(1)

    create_wallpaper(input_file)
