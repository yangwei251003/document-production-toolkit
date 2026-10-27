# Sanitized session source; synthetic fixture values and explicit execution gate.
from document_toolkit.runtime import enter_archive
from document_toolkit.session_runtime import session_path, fixture_value
enter_archive('session/2026-09-15-10-34-50/_work/make_flowchart.py')
# -*- coding: utf-8 -*-
fixture_value('texts.a0288840_1')
import os
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "flowchart.png")

W = 1650
SCALE = 1  # 直接高分辨率绘制

FONT_DIR = session_path('input_3')
F_BOLD = os.path.join(FONT_DIR, "msyhbd.ttc")
F_REG = os.path.join(FONT_DIR, "msyh.ttc")

def font(path, size):
    return ImageFont.truetype(path, size)

# ---------- 颜色 ----------
C_BG        = (255, 255, 255)
C_TITLE     = (24, 62, 108)
C_SUB       = (96, 116, 140)
C_NODE_FILL = (231, 242, 252)
C_NODE_EDGE = (41, 106, 168)
C_NODE_TEXT = (22, 74, 128)
C_NUM_FILL  = (41, 106, 168)
C_NOTE_FILL = (249, 251, 253)
C_NOTE_EDGE = (196, 210, 226)
C_NOTE_TEXT = (48, 56, 66)
C_WARN      = (192, 57, 43)
C_ARROW     = (41, 106, 168)
C_START_F   = (255, 249, 235)
C_START_E   = (223, 168, 60)
C_END_F     = (233, 246, 236)
C_END_E     = (56, 142, 88)

# ---------- 内容 ----------
TITLE = "触电急救流程图"
SUBTITLE = fixture_value('texts.a0288840_2')

START_LABEL = "触电事故发生"
END_LABEL   = "伤者恢复心跳呼吸 / 移交医护人员"

STEPS = [
    {
        "no": "1", "title": "迅速脱离电源", "sub": '合成示例段落：用于验证文档布局与内容转换流程',
        "note": [
            ("拉", '：合成示例段落：用于验证文档布局与内容转换流程'),
            ("切", "：用绝缘工具切断电源线"),
            ("挑", "：用干燥木棒、竹竿挑开电线"),
            ("拽", "：站在干燥绝缘物上拽拉衣服"),
            ("垫", "：垫绝缘板使触电者与地隔离"),
            ("!", '合成示例段落：用于验证文档布局与内容转换流程'),
        ],
    },
    {
        "no": "2", "title": "判断伤情（10 秒内）", "sub": "意识 · 呼吸 · 脉搏",
        "note": [
            ("意", '：合成示例段落：用于验证文档布局与内容转换流程'),
            ("呼", '：合成示例段落：用于验证文档布局与内容转换流程'),
            ("脉", '：合成示例段落：用于验证文档布局与内容转换流程'),
        ],
    },
    {
        "no": "3", "title": "呼救并拨打 120", "sub": "边施救 边呼救",
        "note": [
            ("救", '：合成示例段落：用于验证文档布局与内容转换流程'),
            ("报", "：讲清地点、伤情、联系电话"),
            ("续", '：合成示例段落：用于验证文档布局与内容转换流程'),
        ],
    },
    {
        "no": "4", "title": "心肺复苏（CPR）", "sub": "按压 : 通气 = 30 : 2",
        "note": [
            ("位", '：合成示例段落：用于验证文档布局与内容转换流程'),
            ("置", '：合成示例段落：用于验证文档布局与内容转换流程/3）'),
            ("深", "：按压深度 5～6 cm"),
            ("频", '：合成示例段落：用于验证文档布局与内容转换流程/分'),
            ("比", "：按压 : 人工呼吸 = 30 : 2"),
        ],
    },
    {
        "no": "5", "title": "持续施救、移交医护", "sub": "直至医护到场接替",
        "note": [
            ("续", '：合成示例段落：用于验证文档布局与内容转换流程'),
            ("送", '：合成示例段落：用于验证文档布局与内容转换流程'),
            ("记", '：合成示例段落：用于验证文档布局与内容转换流程'),
        ],
    },
]

# ---------- 度量 ----------
PAD_X = 56
TITLE_Y = 46
TITLE_SIZE = 66
SUB_SIZE = 30
NODE_TITLE_SIZE = 38
NODE_NO_SIZE = 40
NOTE_TITLE_SIZE = 26
NOTE_TEXT_SIZE = 30
SMALL_SIZE = 27

f_title = font(F_BOLD, TITLE_SIZE)
f_sub = font(F_REG, SUB_SIZE)
f_ntitle = font(F_BOLD, NODE_TITLE_SIZE)
f_nno = font(F_BOLD, NODE_NO_SIZE)
f_note_key = font(F_BOLD, NOTE_TEXT_SIZE)
f_note = font(F_REG, NOTE_TEXT_SIZE)
f_small = font(F_BOLD, SMALL_SIZE)
SUB2_SIZE = 27
f_sub2 = font(F_REG, SUB2_SIZE)

MAIN_X0 = PAD_X
MAIN_W = 560
NOTE_X0 = MAIN_X0 + MAIN_W + 72
NOTE_W = W - PAD_X - NOTE_X0

NOTE_PAD = 22
LINE_GAP = 12


def wrap(text, fnt, maxw):
    lines, cur = fixture_value('tables.table_2')
    for ch in text:
        if ch == "\n":
            lines.append(cur); cur = ""; continue
        if fnt.getlength(cur + ch) <= maxw:
            cur += ch
        else:
            if cur:
                lines.append(cur)
            cur = ch
    if cur:
        lines.append(cur)
    return lines or [""]


def measure_note(note):
    fixture_value('texts.a0288840_3')
    rows = []
    inner_w = NOTE_W - NOTE_PAD * 2 - 62
    for key, body in note:
        warn = key == "!"
        keyw = f_note_key.getlength("!")
        body_lines = wrap(body, f_note, inner_w - keyw - 10)
        h = max(len(body_lines) * (NOTE_TEXT_SIZE + LINE_GAP + 6),
                38)
        rows.append((key, warn, body_lines, h))
    return rows


def note_height(rows):
    total = NOTE_PAD * 2
    for _, _, _, h in rows:
        total += h + 6
    return total - 6


def draw_round(d, box, r, fill, edge, width=3):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=edge, width=width)


img = Image.new("RGB", (W, 300), C_BG)
d = ImageDraw.Draw(img)

# 先量高度
rows_measured = [measure_note(s["note"]) for s in STEPS]

node_h = []
for i, s in enumerate(STEPS):
    title_lines = wrap(s["title"], f_ntitle, MAIN_W - 150)
    t = len(title_lines) * (NODE_TITLE_SIZE + 14)
    node_h.append(max(96, t + 46))
    node_h[i] = max(node_h[i], note_height(rows_measured[i]))

GAP = 74
START_H = 80
END_H = 84

y = 0
TITLE_BLOCK = 0
# 标题块
tmp_lines = wrap(TITLE, f_title, W - PAD_X * 2)
TITLE_BLOCK = len(tmp_lines) * (TITLE_SIZE + 16) + 6
tmp2 = wrap(SUBTITLE, f_sub, W - PAD_X * 2)
TITLE_BLOCK += len(tmp2) * (SUB_SIZE + 14) + 26

y = 40 + TITLE_BLOCK

start_y = y
y += START_H + GAP
node_y = []
for i in range(5):
    node_y.append(y)
    y += node_h[i] + GAP
end_y = y
y += END_H

H = int(y + 42)

img = Image.new("RGB", (W, H), C_BG)
d = ImageDraw.Draw(img)

# ---------- 标题 ----------
yy = 40
for ln in tmp_lines:
    ww = f_title.getlength(ln)
    d.text(((W - ww) / 2, yy), ln, font=f_title, fill=C_TITLE)
    yy += TITLE_SIZE + 16
yy += 6
for ln in tmp2:
    ww = f_sub.getlength(ln)
    d.text(((W - ww) / 2, yy), ln, font=f_sub, fill=C_SUB)
    yy += SUB_SIZE + 14

# 标题下装饰线
d.rectangle([PAD_X + 250, yy + 6, W - PAD_X - 250, yy + 10], fill=(210, 224, 238))
yy += 26

CX = MAIN_X0 + MAIN_W / 2


def arrow(x, y0, y1, color=C_ARROW, w=4, head=15):
    d.line([x, y0, x, y1 - head], fill=color, width=w)
    d.polygon([(x - head * 0.72, y1 - head), (x + head * 0.72, y1 - head), (x, y1)], fill=color)


def chevron(d, cx, cy, color):
    '合成示例段落：用于验证文档布局与内容转换流程'
    s = 8
    d.polygon([(cx, cy - s), (cx + s + 2, cy), (cx, cy + s)], fill=color)


# ---------- 起点 ----------
bw = 300
d.rounded_rectangle([CX - bw / 2, start_y, CX + bw / 2, start_y + START_H],
                    radius=START_H / 2, fill=C_START_F, outline=C_START_E, width=3)
lw = f_small.getlength(START_LABEL)
d.text((CX - lw / 2, start_y + (START_H - SMALL_SIZE) / 2 - 3), START_LABEL, font=f_small, fill=(150, 100, 20))

arrow(CX, start_y + START_H, node_y[0])

# ---------- 各步骤 ----------
for i, s in enumerate(STEPS):
    y0 = node_y[i]
    h = node_h[i]

    # 主节点
    draw_round(d, [MAIN_X0, y0, MAIN_X0 + MAIN_W, y0 + h], 16, C_NODE_FILL, C_NODE_EDGE, 3)
    # 序号圆
    cr = 30
    ncx = MAIN_X0 + 56
    ncy = y0 + h / 2
    key = s["no"]
    fill_num = C_NUM_FILL
    d.ellipse([ncx - cr, ncy - cr, ncx + cr, ncy + cr], fill=fill_num)
    nw = f_nno.getlength(key)
    d.text((ncx - nw / 2, ncy - NODE_NO_SIZE / 2 - 4), key, font=f_nno, fill=(255, 255, 255))

    # 标题 + 副标题
    tl = wrap(s["title"], f_ntitle, MAIN_W - 150)
    sub = s.get("sub", "")
    th = len(tl) * (NODE_TITLE_SIZE + 14)
    sh = (SUB2_SIZE + 16) if sub else 0
    ty = ncy - (th + sh) / 2
    tx = ncx + cr + 22
    for ln in tl:
        d.text((tx, ty), ln, font=f_ntitle, fill=C_NODE_TEXT)
        ty += NODE_TITLE_SIZE + 14
    if sub:
        d.text((tx + 2, ty + 4), sub, font=f_sub2, fill=(96, 132, 170))

    # 注释框
    rows = rows_measured[i]
    nh = note_height(rows)
    ny0 = y0 + (h - nh) / 2
    draw_round(d, [NOTE_X0, ny0, NOTE_X0 + NOTE_W, ny0 + nh], 14, C_NOTE_FILL, C_NOTE_EDGE, 2)

    # 连接虚线
    d.line([MAIN_X0 + MAIN_W, ncy, NOTE_X0, ncy], fill=(178, 196, 214), width=2)
    chevron(d, NOTE_X0 - 4, ncy, (178, 196, 214))

    ry = ny0 + NOTE_PAD
    for keyc, warn, body_lines, rh in rows:
        # 关键标记
        if warn:
            d.ellipse([NOTE_X0 + NOTE_PAD, ry + 3, NOTE_X0 + NOTE_PAD + 34, ry + 37],
                      fill=C_WARN)
            d.text((NOTE_X0 + NOTE_PAD + 8, ry + 2), "!", font=f_note_key, fill=(255, 255, 255))
            kx = NOTE_X0 + NOTE_PAD + 44
            col = C_WARN
        else:
            d.ellipse([NOTE_X0 + NOTE_PAD, ry + 3, NOTE_X0 + NOTE_PAD + 34, ry + 37],
                      fill=(214, 230, 246))
            kw = f_note_key.getlength(keyc)
            d.text((NOTE_X0 + NOTE_PAD + 17 - kw / 2, ry + 2), keyc, font=f_note_key, fill=(41, 106, 168))
            kx = NOTE_X0 + NOTE_PAD + 44
            col = C_WARN if keyc in ("深", "频", "比") else C_NOTE_TEXT
        for bi, ln in enumerate(body_lines):
            d.text((kx, ry), ln, font=f_note, fill=col)
            ry += NOTE_TEXT_SIZE + LINE_GAP + 6
        ry += 6

    if i < 4:
        arrow(CX, y0 + h, node_y[i + 1])

# ---------- 终点 ----------
bw2 = 520
d.rounded_rectangle([CX - bw2 / 2, end_y, CX + bw2 / 2, end_y + END_H],
                    radius=END_H / 2, fill=C_END_F, outline=C_END_E, width=3)
lw = f_small.getlength(END_LABEL)
d.text((CX - lw / 2, end_y + (END_H - SMALL_SIZE) / 2 - 3), END_LABEL, font=f_small, fill=(38, 110, 66))

img.save(OUT, "PNG")
print("saved", OUT, img.size)
