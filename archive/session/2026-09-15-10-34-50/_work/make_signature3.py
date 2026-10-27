# Sanitized session source; synthetic fixture values and explicit execution gate.
from document_toolkit.runtime import enter_archive
from document_toolkit.session_runtime import session_path, fixture_value
enter_archive('session/2026-09-15-10-34-50/_work/make_signature3.py')
# -*- coding: utf-8 -*-
fixture_value('texts.e27182eb_1')
import os, random
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
FONTS = session_path('input_4')
NAME = '示例同学'

STYLES = [
    dict(key="行楷", font="STXINGKA.TTF", size=340, slant=-7.0,
         tracking=-0.02, dy=(-6, 6)),
    dict(key="舒体", font="FZSTK.TTF", size=330, slant=-5.5,
         tracking=-0.01, dy=(-5, 5)),
    dict(key="楷体", font="simkai.ttf", size=340, slant=-8.5,
         tracking=0.0, dy=(-4, 4)),
]

INK_BLACK = (20, 20, 24)
INK_BLUE = (26, 46, 112)


def make_signature(style, ink=INK_BLACK, seed=9):
    rnd = random.Random(seed)
    size = style["size"]
    font = ImageFont.truetype(os.path.join(FONTS, style["font"]), size)

    track = style["tracking"] * size
    adv = [font.getlength(c) + track for c in NAME]
    total_w = int(sum(adv))
    pad = size
    big = (total_w + pad * 2, int(size * 2.4))

    tmp = Image.new("RGBA", big, (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    x = pad
    for ch, a in zip(NAME, adv):
        dy = int(rnd.uniform(*style["dy"]))
        d.text((x, pad + dy), ch, font=font, fill=ink + (255,))
        x += a

    shear = style["slant"] / 100.0
    w, h = tmp.size
    shifted = tmp.transform(
        (w + int(abs(shear) * h) + 60, h), Image.AFFINE,
        (1, shear, 30 - min(0.0, shear * h), 0, 1, 0), resample=Image.BICUBIC)

    out = shifted.crop(shifted.getbbox())
    pad2 = int(size * 0.18)
    final = Image.new("RGBA", (out.width + pad2 * 2, out.height + pad2 * 2), (0, 0, 0, 0))
    final.alpha_composite(out, (pad2, pad2))
    return final


if __name__ == "__main__":
    made = []
    for st in STYLES:
        img = make_signature(st, INK_BLACK)
        p = os.path.join(OUT_DIR, '签名_示例同学_%s.png' % st["key"])
        img.save(p)
        made.append((p, img.size))
        if st["key"] == "行楷":
            img2 = make_signature(st, INK_BLUE)
            p2 = os.path.join(OUT_DIR, '签名_示例同学_%s_蓝黑.png' % st["key"])
            img2.save(p2)
            made.append((p2, img2.size))

    prev = os.path.join(OUT_DIR, "sig_preview")
    os.makedirs(prev, exist_ok=True)
    for f in os.listdir(prev):
        os.remove(os.path.join(prev, f))
    for p, sz in made:
        im = Image.open(p)
        bg = Image.new("RGB", im.size, (255, 255, 255))
        bg.paste(im, (0, 0), im)
        bg.save(os.path.join(prev, "白底_" + os.path.basename(p)))
        print(sz, os.path.basename(p))
