from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageFilter


WIDTH, HEIGHT = 2048, 1152
OUT = Path(__file__).with_name("ui-flow-1.png")

BG = "#070a12"
PANEL = "#0d1422"
WHITE = "#f7f9ff"
MUTED = "#aebbd0"
MAGENTA = "#ff4fc3"
BLUE = "#16a9ff"
TEAL = "#37d9c2"
LINE = "#d9e2f0"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "segoeuib.ttf" if bold else "segoeui.ttf"
    return ImageFont.truetype(Path("C:/Windows/Fonts") / name, size=size)


canvas = Image.new("RGB", (WIDTH, HEIGHT), BG)
gradient = Image.new("RGB", (WIDTH, HEIGHT), BG)
pixels = gradient.load()
for y in range(HEIGHT):
    shade = int(8 + 10 * (1 - y / HEIGHT))
    for x in range(WIDTH):
        blue = int(17 + 15 * x / WIDTH)
        pixels[x, y] = (shade, shade + 3, blue)
canvas = Image.blend(canvas, gradient, 0.82)
draw = ImageDraw.Draw(canvas)

# Header
draw.text((54, 58), "UI Flow", fill=WHITE, font=font(60, True))
draw.text((308, 58), "— 01", fill=MAGENTA, font=font(60, True))
draw.text((58, 138), "Metadata loading and image-inference paths converge in the search interface.", fill=MUTED, font=font(21))
draw.rounded_rectangle((54, 202, 1994, 1052), radius=20, fill=PANEL, outline="#52627a", width=2)
draw.rounded_rectangle((55, 203, 1993, 250), radius=20, fill="#111c2e")
draw.text((80, 214), "APPLICATION WORKFLOW", fill="#8ba1c3", font=font(15, True))

shadow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
shadow_draw = ImageDraw.Draw(shadow)


def box(x, y, w, h, lines, color):
    shadow_draw.rounded_rectangle((x + 4, y + 7, x + w + 4, y + h + 7), radius=10, fill=(0, 0, 0, 130))
    shadow_blurred = shadow.filter(ImageFilter.GaussianBlur(8))
    canvas.paste(shadow_blurred, (0, 0), shadow_blurred)
    # Reset the temporary layer so prior box shadows are not pasted repeatedly.
    shadow_draw.rectangle((0, 0, WIDTH, HEIGHT), fill=(0, 0, 0, 0))
    draw.rounded_rectangle((x, y, x + w, y + h), radius=10, fill="#0b101b", outline=color, width=3)
    draw.rounded_rectangle((x + 2, y + 2, x + w - 2, y + 7), radius=7, fill=color)
    line_font = font(20, True)
    total = len(lines) * 27
    start = y + (h - total) / 2 - 2
    for i, line in enumerate(lines):
        bounds = draw.textbbox((0, 0), line, font=line_font)
        tx = x + (w - (bounds[2] - bounds[0])) / 2
        draw.text((tx, start + i * 27), line, fill=WHITE, font=line_font)


def arrow(points, label=None, label_xy=None):
    draw.line(points, fill=LINE, width=3, joint="curve")
    x1, y1 = points[-2]
    x2, y2 = points[-1]
    if abs(x2 - x1) >= abs(y2 - y1):
        sign = 1 if x2 > x1 else -1
        triangle = [(x2, y2), (x2 - 11 * sign, y2 - 6), (x2 - 11 * sign, y2 + 6)]
    else:
        sign = 1 if y2 > y1 else -1
        triangle = [(x2, y2), (x2 - 6, y2 - 11 * sign), (x2 + 6, y2 - 11 * sign)]
    draw.polygon(triangle, fill=LINE)
    if label and label_xy:
        draw.rounded_rectangle((label_xy[0] - 7, label_xy[1] - 3, label_xy[0] + 68, label_xy[1] + 25), radius=6, fill=PANEL)
        draw.text(label_xy, label, fill=WHITE, font=font(17, True))


# Nodes
box(78, 550, 134, 82, ["App Launch"], MAGENTA)
box(238, 550, 146, 82, ["Initialize", "Session State"], BLUE)
box(410, 550, 150, 82, ["Main Options", "radio"], MAGENTA)

box(634, 334, 174, 82, ["Metadata Path", "Input"], MAGENTA)
box(838, 334, 174, 82, ["Button : Load", "Metadata"], MAGENTA)
box(1042, 334, 244, 82, ["Save to State :", "Metadata_path"], BLUE)
box(1318, 334, 96, 82, ["Show", "Spinner"], TEAL)
box(1446, 334, 276, 82, ["Save to State : Unique_cls,", "count_options"], BLUE)

box(634, 770, 174, 82, ["Image Directory", "Input"], MAGENTA)
box(838, 770, 174, 82, ["Button : Start", "Inference"], MAGENTA)
box(1042, 770, 244, 82, ["Save to State :", "image_dir, model_path"], BLUE)
box(1318, 770, 96, 82, ["Show", "Spinner"], TEAL)
box(1446, 770, 276, 82, ["Save to State : Unique_cls,", "count_options"], BLUE)

box(1724, 550, 172, 82, ["SEARCH UI", "Section"], MAGENTA)

# Connections
arrow([(212, 591), (238, 591)])
arrow([(384, 591), (410, 591)])
draw.ellipse((581, 577, 607, 603), fill="#111c2e", outline=LINE, width=3)
arrow([(560, 591), (594, 591), (594, 375), (634, 375)], "Load", (574, 445))
arrow([(560, 591), (594, 591), (594, 811), (634, 811)], "Process", (561, 692))

for y in (375, 811):
    arrow([(808, y), (838, y)])
    arrow([(1012, y), (1042, y)])
    arrow([(1286, y), (1318, y)])
    arrow([(1414, y), (1446, y)])

arrow([(1584, 416), (1584, 570), (1724, 570)])
arrow([(1584, 770), (1584, 612), (1724, 612)])

# Small endpoint captions
draw.text((1718, 522), "RESULTS", fill="#8ba1c3", font=font(13, True))
draw.text((78, 981), "OBJECT DETECTION • METADATA SEARCH • SESSION STATE", fill="#7186a8", font=font(14, True))

canvas.save(OUT, "PNG", optimize=True)
print(f"Wrote {OUT}")
