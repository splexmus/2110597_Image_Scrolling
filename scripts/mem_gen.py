from pathlib import Path

from PIL import Image


WIDTH = 320
HEIGHT = 240
ROOT = Path(__file__).resolve().parents[1]


def image_to_mem(image_path, mem_path):
    """Resize an image and write one 6-bit RGB222 pixel per line."""
    with Image.open(image_path) as source:
        image = source.convert("RGB").resize(
            (WIDTH, HEIGHT), Image.Resampling.LANCZOS
        )
    pixels = image.load()

    with open(mem_path, "w") as mem_file:
        for y in range(HEIGHT):
            for x in range(WIDTH):
                red, green, blue = pixels[x, y]
                rgb222 = ((red >> 6) << 4) | ((green >> 6) << 2) | (blue >> 6)
                mem_file.write(f"{rgb222:02X}\n")


image_to_mem(ROOT / "scripts/img/IMG_3729-dithered.png", ROOT / "data/bg1.mem")
image_to_mem(ROOT / "scripts/img/IMG_3728-dithered.png", ROOT / "data/bg2.mem")
image_to_mem(ROOT / "scripts/img/IMG_3727-dithered.png", ROOT / "data/bg3.mem"
)
print(f"Wrote three {WIDTH}x{HEIGHT} 6-bit RGB222 memory files.")
