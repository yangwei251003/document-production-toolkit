# Sanitized session source; synthetic fixture values and explicit execution gate.
from document_toolkit.runtime import enter_archive
from document_toolkit.session_runtime import session_path, fixture_value
enter_archive('session/2026-09-15-10-34-50/_work/make_payload.py')
# -*- coding: utf-8 -*-
fixture_value('texts.e12ad698_1')
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
FID = "e456d9a2-d67a-4306-83b6-b8c37f0497fb"

RPR = {"font_family": "宋体", "font_size": 10.5}
BPR = {"font_family": "宋体", "font_size": 10.5, "bold": True}


def P(text, indent=True, align="both", bold=False, after=0):
    return {
        "runs": [{"text": text, "format": BPR if bold else RPR}],
        "line_spacing": 1.5,
        "line_spacing_rule": 1,
        "spacing_after": after,
        "horizontal_align": align,
        "first_line_indent": 420 if indent else 0,
    }


# ---------------- 实训原理 ----------------
YUANLI = [
    P(fixture_value('texts.e12ad698_2')),
    P(fixture_value('texts.e12ad698_3')),
]

# ---------------- 实训步骤或过程 ----------------
BUZHOU = [
    P(fixture_value('texts.e12ad698_4')),
    P(fixture_value('texts.e12ad698_5')),
    P(fixture_value('texts.e12ad698_6')),
    P(fixture_value('texts.e12ad698_7')),
    P(fixture_value('texts.e12ad698_8')),
    P(fixture_value('texts.e12ad698_9')),
]

# ---------------- 流程图单元格 ----------------
TUSHUO = [
    P("图 1  触电急救流程图", indent=False, align="center", bold=True, after=60),
    P(fixture_value('texts.e12ad698_10')),
]

# ---------------- 实训结论与心得 ----------------
JIELUN = [
    P(fixture_value('texts.e12ad698_11')),
    P(fixture_value('texts.e12ad698_12')),
    P(fixture_value('texts.e12ad698_13')),
    P(fixture_value('texts.e12ad698_14')),
]

# ---------------- 教师评语 ----------------
PINGYU = [
    P(fixture_value('texts.e12ad698_15')),
]

TAIL = {"runs": [{"text": " ", "format": RPR}], "line_spacing": 1.5, "line_spacing_rule": 1,
        "spacing_after": 0, "horizontal_align": "both", "first_line_indent": 0}

YUANLI = YUANLI + [TAIL]
BUZHOU = BUZHOU + [TAIL]
TUSHUO = TUSHUO + [TAIL]
JIELUN = JIELUN + [TAIL]
PINGYU = PINGYU + [TAIL]

payloads = {
    "yuanli": {"file_id": FID, "table_id": "8l2bf5jr",
               "cells": [{"row": 1, "col": 2, "paragraphs": YUANLI}]},
    "buzhou": {"file_id": FID, "table_id": "yfib5r63",
               "cells": [{"row": 1, "col": 2, "paragraphs": BUZHOU}]},
    "jielun": {"file_id": FID, "table_id": "w4zr1jv4",
               "cells": [{"row": 1, "col": 2, "paragraphs": JIELUN},
                         {"row": 2, "col": 2, "paragraphs": PINGYU}]},
    "tupian": {"file_id": FID, "table_id": "yfib5r63",
               "cells": [{"row": 2, "col": 2, "paragraphs": TUSHUO,
                          "image": {"content": os.path.join(HERE, "flowchart.png").replace("\\", "/"),
                                    "width": 440, "height": 565}}]},
}

for k, v in payloads.items():
    with open(os.path.join(HERE, "args_%s.json" % k), "w", encoding="utf-8") as f:
        json.dump(v, f, ensure_ascii=False, indent=1)
    print("wrote args_%s.json" % k)
