from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).parent
W, H = 2048, 1152
BG, PANEL, WHITE, MUTED = "#080b12", "#101827", "#f8faff", "#aebbd0"
PINK, BLUE, AMBER, LINE = "#ff4fc3", "#16a9ff", "#ffbe3d", "#d9e2f0"


def typeface(size, bold=False):
    return ImageFont.truetype(Path("C:/Windows/Fonts") / ("segoeuib.ttf" if bold else "segoeui.ttf"), size)


def page(number):
    image = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(image)
    draw.text((66, 48), "UI Flow", fill=WHITE, font=typeface(58, True))
    draw.text((320, 48), f"— {number}", fill=PINK, font=typeface(58, True))
    draw.rounded_rectangle((54, 190, W - 54, H - 62), radius=20, fill=PANEL, outline="#55657f", width=2)
    draw.rounded_rectangle((56, 192, W - 56, 236), radius=20, fill="#142037")
    draw.text((80, 203), "APPLICATION WORKFLOW", fill="#91a7cb", font=typeface(15, True))
    return image, draw


def node(draw, x, y, w, h, label, colour=PINK, accent=None):
    draw.rounded_rectangle((x + 5, y + 7, x + w + 5, y + h + 7), radius=10, fill="#05070c")
    draw.rounded_rectangle((x, y, x + w, y + h), radius=10, fill="#0b111d", outline=colour, width=3)
    if accent:
        draw.rounded_rectangle((x + 2, y + 2, x + w - 2, y + 7), radius=7, fill=accent)
    lines = label.split("\n")
    f = typeface(19, True)
    line_h = 25
    top = y + (h - len(lines) * line_h) / 2 - 2
    for i, line in enumerate(lines):
        bb = draw.textbbox((0, 0), line, font=f)
        draw.text((x + (w - (bb[2] - bb[0])) / 2, top + i * line_h), line, fill=WHITE, font=f)


def arrow(draw, points):
    draw.line(points, fill=LINE, width=3, joint="curve")
    x1, y1 = points[-2]
    x2, y2 = points[-1]
    if abs(x2 - x1) >= abs(y2 - y1):
        s = 1 if x2 > x1 else -1
        triangle = [(x2, y2), (x2 - 12 * s, y2 - 7), (x2 - 12 * s, y2 + 7)]
    else:
        s = 1 if y2 > y1 else -1
        triangle = [(x2, y2), (x2 - 7, y2 - 12 * s), (x2 + 7, y2 - 12 * s)]
    draw.polygon(triangle, fill=LINE)


def flow_2():
    image, draw = page(2)
    node(draw, 116, 555, 170, 84, "SEARCH UI\nSection")
    node(draw, 540, 440, 210, 84, "Radio : Search\nMode (OR/AND)")
    node(draw, 796, 440, 248, 84, "Save to State :\nsearch_params.model", BLUE, BLUE)
    node(draw, 1090, 440, 184, 84, "MultiSelect :\nClasses")
    node(draw, 1320, 440, 270, 84, "Save to State :\nsearch_params.select_classes", BLUE, BLUE)
    node(draw, 540, 690, 210, 84, "Threshold\nSelectboxes")
    node(draw, 796, 690, 248, 84, "Save to State :\nsearch_params.thresholds", BLUE, BLUE)
    node(draw, 1090, 690, 184, 84, "Button : Search\nImages")
    node(draw, 1320, 690, 270, 84, "Save to State :\nsearch_params.search_results", BLUE, BLUE)
    node(draw, 1750, 555, 172, 84, "Display\nControls")
    arrow(draw, [(286, 597), (500, 597), (500, 482), (540, 482)])
    arrow(draw, [(750, 482), (796, 482)])
    arrow(draw, [(1044, 482), (1090, 482)])
    arrow(draw, [(1274, 482), (1320, 482)])
    arrow(draw, [(1590, 482), (1642, 482), (1642, 647), (540, 647), (540, 690)])
    arrow(draw, [(750, 732), (796, 732)])
    arrow(draw, [(1044, 732), (1090, 732)])
    arrow(draw, [(1274, 732), (1320, 732)])
    arrow(draw, [(1590, 732), (1670, 732), (1670, 597), (1750, 597)])
    draw.text((115, 982), "SEARCH CONTROLS • FILTERS • RESULT SET", fill="#7186a8", font=typeface(14, True))
    image.save(ROOT / "ui-flow-2.png", "PNG", optimize=True)


def flow_3():
    image, draw = page(3)
    node(draw, 85, 618, 178, 84, "Display Controls")
    node(draw, 398, 472, 250, 84, "Checkbox : Show Boxes\n(Save to State)")
    node(draw, 398, 618, 250, 84, "Slider: Grid Columns\n(Save to State)")
    node(draw, 398, 764, 250, 84, "Checkbox : Highlight Matches\n(Save to State)")
    node(draw, 704, 618, 196, 84, "Render Image Grid")
    node(draw, 958, 618, 170, 84, "For Each Result")
    node(draw, 1380, 392, 230, 84, "Draw Annotations\n(conditional)", PINK, AMBER)
    node(draw, 1380, 580, 330, 126, "", PINK)
    card_font = typeface(17, True)
    for index, line in enumerate(("Display Card", "with", "metadata")):
        bounds = draw.textbbox((0, 0), line, font=card_font)
        draw.text((1452 - (bounds[2] - bounds[0]) / 2, 613 + index * 24), line, fill=WHITE, font=card_font)
    node(draw, 1570, 596, 115, 94, "Convert\nto\nBase64")
    node(draw, 1380, 764, 230, 84, "Export Options")
    node(draw, 1380, 910, 230, 84, "Button : Download JSON")
    arrow(draw, [(263, 660), (360, 660), (360, 514), (398, 514)])
    arrow(draw, [(263, 660), (398, 660)])
    arrow(draw, [(263, 660), (360, 660), (360, 806), (398, 806)])
    arrow(draw, [(648, 514), (674, 514), (674, 660), (704, 660)])
    arrow(draw, [(648, 660), (704, 660)])
    arrow(draw, [(648, 806), (674, 806), (674, 660), (704, 660)])
    arrow(draw, [(900, 660), (958, 660)])
    arrow(draw, [(1128, 660), (1335, 660), (1335, 434), (1380, 434)])
    arrow(draw, [(1545, 476), (1545, 580)])
    arrow(draw, [(1545, 706), (1545, 764)])
    arrow(draw, [(1495, 848), (1495, 910)])
    draw.text((85, 1012), "RESULT PRESENTATION • ANNOTATIONS • EXPORT", fill="#7186a8", font=typeface(14, True))
    image.save(ROOT / "ui-flow-3.png", "PNG", optimize=True)


flow_2()
flow_3()
print("Wrote ui-flow-2.png and ui-flow-3.png")
