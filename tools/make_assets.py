from PIL import Image, ImageDraw, ImageFont

PAPER = (0xED, 0xF1, 0xF6)
GRID = (0xDC, 0xE4, 0xEE)
INK = (0x16, 0x23, 0x3D)
SLATE = (0x5A, 0x6B, 0x87)
MEASURE = (0x0E, 0x7C, 0x7C)
STONE = (0xB8, 0xC4, 0xD4)

MED = "plex/IBMPlexMono-Medium.ttf"
SEMI = "plex/IBMPlexMono-SemiBold.ttf"
REG = "plex/IBMPlexMono-Regular.ttf"


def ellipse(base, cx, cy, rx, ry, fill, rot, ss=4):
    """Rotated ellipse drawn on a supersampled scratch layer."""
    w, h = int(rx * 2 * ss) + 8 * ss, int(ry * 2 * ss) + 8 * ss
    lay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.ellipse([4 * ss, 4 * ss, w - 4 * ss, h - 4 * ss], fill=fill)
    lay = lay.rotate(-rot, resample=Image.BICUBIC, expand=True)
    lay = lay.resize((lay.width // ss, lay.height // ss), Image.LANCZOS)
    base.alpha_composite(lay, (int(cx - lay.width / 2), int(cy - lay.height / 2)))


def cairn(size, palette, ss=4):
    """The stacked-stone mark, drawn to a transparent square of `size`."""
    S = size * ss
    img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    u = S / 64.0
    specs = [
        (31, 52, 29, 9.5, palette[0], -3),
        (34, 40, 22.5, 8.5, palette[1], 4),
        (30, 30, 16.5, 7.5, palette[2], -5),
        (32, 21, 10.5, 5.5, palette[3], 3),
    ]
    for cx, cy, rx, ry, fill, rot in specs:
        ellipse(img, cx * u, cy * u, rx * u, ry * u, fill, rot, ss=2)
    return img.resize((size, size), Image.LANCZOS)


def rounded_icon(size, radius_ratio=0.2237):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, size - 1, size - 1], radius=int(size * radius_ratio), fill=INK + (255,))
    mark = cairn(size, [(0x56, 0x64, 0x82, 255), (0x6C, 0x7C, 0x9C, 255),
                        (0xE2, 0xEC, 0xF4, 255), (0x86, 0xD6, 0xD6, 255)])
    # nudge the stack down slightly so it sits optically centred in the tile
    img.alpha_composite(mark, (0, int(size * 0.02)))
    return img


# ---------- apple-touch-icon ----------
rounded_icon(180).convert("RGB").save("site/apple-touch-icon.png", optimize=True)
rounded_icon(512).convert("RGB").save("site/icon-512.png", optimize=True)

# ---------- open graph card ----------
W, H = 1200, 630
og = Image.new("RGBA", (W, H), PAPER + (255,))
d = ImageDraw.Draw(og)

# survey grid, same 32px pitch as the site
for x in range(0, W, 32):
    d.line([(x, 0), (x, H)], fill=GRID, width=1)
for y in range(0, H, 32):
    d.line([(0, y), (W, y)], fill=GRID, width=1)

M = 80  # gutter

# masthead: mark + wordmark
mark = cairn(38, [(0x56, 0x64, 0x82, 255), (0x6C, 0x7C, 0x9C, 255),
                  (0xC3, 0xD0, 0xDE, 255), (0x0E, 0x7C, 0x7C, 255)])
og.alpha_composite(mark, (M, 74))

f_word = ImageFont.truetype(SEMI, 21)
word = "RAMIREZ LABS"
x = M + 52
for ch in word:  # manual tracking, .16em
    d.text((x, 84), ch, font=f_word, fill=INK)
    x += d.textlength(ch, font=f_word) + 3.4

# headline
f_h1 = ImageFont.truetype(MED, 62)
lines = [("Apps that keep your data", INK), ("on your device.", MEASURE)]
y = 236
for text, colour in lines:
    d.text((M, y), text, font=f_h1, fill=colour)
    y += 78

# survey-rod rule with ticks
ry = 452
d.line([(M, ry), (W - M, ry)], fill=INK, width=2)
for tx in range(M, W - M, 32):
    d.line([(tx, ry), (tx, ry + 9)], fill=STONE, width=1)

# subline
f_sub = ImageFont.truetype(REG, 25)
d.text((M, ry + 34), "iPhone  ·  Mac  ·  Vision Pro", font=f_sub, fill=SLATE)

f_foot = ImageFont.truetype(REG, 21)
foot = "RAMIREZLABS.APP"
x = M
for ch in foot:
    d.text((x, H - 76), ch, font=f_foot, fill=SLATE)
    x += d.textlength(ch, font=f_foot) + 2.6

og.convert("RGB").save("site/og.png", optimize=True, quality=92)
print("wrote apple-touch-icon.png, icon-512.png, og.png")
