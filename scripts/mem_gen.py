from pathlib import Path

from PIL import Image


WIDTH = 320
HEIGHT = 240
ROOT = Path(__file__).resolve().parents[1]

MARIO_SPRITE = (
    ".....RRRRR......",
    "...RRRRRRRRR....",
    "...BBBSSKSS.....",
    "..BSBSSSKSSS....",
    "..BSBBSSSSSS....",
    "...BSSBBBB......",
    "....RRDRRR......",
    "...RRRDRDRRR....",
    "..RRRRDDDRRRR...",
    "..SSRDDDDDRSS...",
    "..SSSDD.DDSSS...",
    "..BBB.....BBB...",
)
MARIO_PALETTE = {
    ".": 0x3F,  # transparent
    "R": 0x30,  # red
    "S": 0x39,  # skin
    "B": 0x10,  # brown
    "K": 0x00,  # black
    "D": 0x03,  # blue
}


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


def sprite_to_mem(sprite, mem_path):
    assert len(sprite) == 12 and all(len(row) == 16 for row in sprite)
    with open(mem_path, "w") as mem_file:
        for row in sprite:
            for pixel in row:
                mem_file.write(f"{MARIO_PALETTE[pixel]:02X}\n")


image_to_mem(ROOT / "scripts/img/IMG_3729-dithered.png", ROOT / "data/bg1.mem")
image_to_mem(ROOT / "scripts/img/IMG_3728-dithered.png", ROOT / "data/bg2.mem")
image_to_mem(ROOT / "scripts/img/IMG_3727-dithered.png", ROOT / "data/bg3.mem"
)
sprite_to_mem(MARIO_SPRITE, ROOT / "data/mario.mem")
print(f"Wrote three {WIDTH}x{HEIGHT} backgrounds and one 16x12 sprite.")
