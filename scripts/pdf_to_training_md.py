#!/usr/bin/env python3
"""Convert _pdf_extract.txt to knowledge/training/*.md"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXTRACT = ROOT / "knowledge" / "training" / "_pdf_extract.txt"
OUT_DIR = ROOT / "knowledge" / "training"

# CJK compatibility variants from PDF extraction -> standard chars
NORMALIZE = str.maketrans(
    {
        "\u2f00": "\u4e00",  # 一 radical
        "\u2f42": "\u8f66",  # 车
        "\u2f08": "\u4eba",  # 人
        "\u2f06": "\u4e8c",  # 二
        "\u2f0a": "\u516b",  # 八
        "\u2f1a": "\u5341",  # 十
        "\u2f29": "\u5927",  # 大
        "\u2f31": "\u5c0f",  # 小
        "\u2f3c": "\u5e74",  # 年
        "\u2f45": "\u91cc",  # 里
        "\u2f64": "\u95ee",  # 问
        "\u2f6f": "\u9ad8",  # 高
        "\u2f74": "\u957f",  # 长
        "\u2f7f": "\u95e8",  # 门
        "\u2f8f": "\u9a6c",  # 马
        "\u2f9f": "\u9a71",  # 驱
        "\u2fa6": "\u9ed1",  # 黑
        "\u2fb3": "\u9ed8",  # 默
        "\uff65": "\u7684",  # weird の
    }
)
# Common broken chars in this PDF
EXTRA_MAP = {
    "⻋": "车",
    "⻔": "门",
    "⻓": "长",
    "⻛": "风",
    "⻢": "马",
    "⼀": "一",
    "⼆": "二",
    "⼈": "人",
    "⼉": "儿",
    "⼊": "入",
    "⼋": "八",
    "⼏": "几",
    "⼑": "刀",
    "⼒": "力",
    "⼤": "大",
    "⼩": "小",
    "⼴": "广",
    "⼿": "手",
    "⼗": "十",
    "⼘": "卜",
    "⼚": "厂",
    "⼜": "又",
    "⼝": "口",
    "⼟": "土",
    "⼤": "大",
    "⼥": "女",
    "⼦": "子",
    "⼨": "寸",
    "⼊": "入",
    "⼋": "八",
    "⼏": "几",
    "⼑": "刀",
    "⼒": "力",
    "⼔": "匕",
    "⼗": "十",
    "⼘": "卜",
    "⼚": "厂",
    "⼜": "又",
    "⼝": "口",
    "⼞": "口",
    "⼟": "土",
    "⼠": "士",
    "⼤": "大",
    "⼥": "女",
    "⼦": "子",
    "⼩": "小",
    "⼪": "尸",
    "⼫": "尸",
    "⼬": "目",
    "⼭": "山",
    "⼯": "工",
    "⼰": "己",
    "⼲": "干",
    "⼴": "广",
    "⼸": "弓",
    "⼼": "心",
    "⼿": "手",
    "⼖": "爪",
    "⼗": "十",
    "⼘": "卜",
    "⼚": "厂",
    "⼛": "口",
    "⼜": "又",
    "⼝": "口",
    "⼞": "口",
    "⼟": "土",
    "⼠": "士",
    "⼡": "幺",
    "⼢": "厶",
    "⼣": "夕",
    "⼤": "大",
    "⼥": "女",
    "⼦": "子",
    "⼧": "寸",
    "⼨": "寸",
    "⼩": "小",
    "⼪": "尸",
    "⼫": "尸",
    "⼬": "目",
    "⼭": "山",
    "⼯": "工",
    "⼰": "己",
    "⼱": "巾",
    "⼲": "干",
    "⼳": "幺",
    "⼴": "广",
    "⼵": "广",
    "⼶": "幺",
    "⼷": "幺",
    "⼸": "弓",
    "⼹": "斤",
    "⼺": "斤",
    "⼻": "彳",
    "⼼": "心",
    "⼽": "心",
    "⼾": "户",
    "⼿": "手",
    "⼽": "心",
    "⽽": "而",
    "⽬": "目",
    "⽤": "用",
    "⽆": "无",
    "⽇": "日",
    "⽉": "月",
    "⽌": "止",
    "⽐": "比",
    "⽑": "毛",
    "⽒": "氏",
    "⽓": "气",
    "⽔": "水",
    "⽕": "火",
    "⽖": "爪",
    "⽗": "父",
    "⽘": "爻",
    "⽙": "爪",
    "⽚": "片",
    "⽛": "牙",
    "⽜": "牛",
    "⽝": "犬",
    "⽞": "玄",
    "⽟": "玉",
    "⽠": "瓜",
    "⽡": "瓦",
    "⽢": "甘",
    "⽣": "生",
    "⽤": "用",
    "⽥": "田",
    "⽩": "白",
    "⽪": "皮",
    "⽬": "目",
    "⽭": "矛",
    "⽮": "矢",
    "⽯": "石",
    "⽰": "示",
    "⽱": "禸",
    "⽲": "禾",
    "⽳": "穴",
    "⽴": "立",
    "⽵": "立",
    "⽶": "米",
    "⽷": "糸",
    "⽸": "缶",
    "⽹": "网",
    "⽺": "羊",
    "⽻": "羽",
    "⽼": "老",
    "⽚": "片",
    "⽛": "牙",
    "⽜": "牛",
    "⽝": "犬",
    "⽞": "玄",
    "⽟": "玉",
    "⽠": "瓜",
    "⽡": "瓦",
    "⽢": "甘",
    "⽣": "生",
    "⽤": "用",
    "⽥": "田",
    "⽩": "白",
    "⽪": "皮",
    "⽬": "目",
    "⽭": "矛",
    "⽮": "矢",
    "⽯": "石",
    "⽰": "示",
    "⽱": "禸",
    "⽲": "禾",
    "⽳": "穴",
    "⽴": "立",
    "⽵": "立",
    "⽶": "米",
    "⽷": "糸",
    "⽸": "缶",
    "⽹": "网",
    "⽺": "羊",
    "⽻": "羽",
    "⽼": "老",
    "⽚": "片",
    "⽛": "牙",
    "⽜": "牛",
    "⽝": "犬",
    "⽞": "玄",
    "⽟": "玉",
    "⽠": "瓜",
    "⽡": "瓦",
    "⽢": "甘",
    "⽣": "生",
    "⽤": "用",
    "⽥": "田",
    "⽩": "白",
    "⽪": "皮",
    "⽬": "目",
    "⽭": "矛",
    "⽮": "矢",
    "⽯": "石",
    "⽰": "示",
    "⽱": "禸",
    "⽲": "禾",
    "⽳": "穴",
    "⽴": "立",
    "⽵": "立",
    "⽶": "米",
    "⽷": "糸",
    "⽸": "缶",
    "⽹": "网",
    "⽺": "羊",
    "⽻": "羽",
    "⽼": "老",
    "⾃": "自",
    "⾄": "至",
    "⾆": "舌",
    "⾇": "舟",
    "⾈": "舟",
    "⾊": "色",
    "⾍": "虫",
    "⾎": "血",
    "⾏": "行",
    "⾐": "衣",
    "⾒": "见",
    "⾓": "角",
    "⾔": "言",
    "⾕": "谷",
    "⾖": "豆",
    "⾚": "赤",
    "⾛": "走",
    "⾜": "足",
    "⾝": "身",
    "⾞": "车",
    "⾟": "辛",
    "⾠": "辰",
    "⾡": "辵",
    "⾢": "邑",
    "⾣": "酉",
    "⾤": "采",
    "⾥": "里",
    "⾦": "金",
    "⾧": "长",
    "⾨": "门",
    "⾩": "阜",
    "⾪": "隶",
    "⾫": "隹",
    "⾬": "雨",
    "⾭": "青",
    "⾮": "非",
    "⾯": "面",
    "⾰": "革",
    "⾱": "革",
    "⾲": "韭",
    "⾳": "音",
    "⾴": "页",
    "⾵": "风",
    "⾶": "飞",
    "⾷": "食",
    "⾸": "首",
    "⾹": "香",
    "⾺": "马",
    "⾻": "骨",
    "⾼": "高",
    "⾽": "高",
    "⾾": "高",
    "⾿": "高",
    "⿊": "黑",
    "⿏": "鼠",
    "⿐": "鼻",
    "⿑": "齐",
    "⿒": "齿",
    "⿓": "龙",
    "⿔": "龙",
    "⿕": "龙",
    "ﬁ": "fi",
    "ﬂ": "fl",
    "饿": "的",  # OCR typo in PDF
}

SKIP_LINES = re.compile(
    r"^(内部资料|产品100问|LEARNING|CENTER|严禁转发|===== PAGE|\s*$|待监管机构批准)"
)

SECTIONS = [
    ("00-preface-fabg.md", "前言", [r"^前\s*言", r"^祝各位同事"]),
    (
        "01-products.md",
        "一、产品类信息",
        [r"^一、\s*产品", r"^⼀、\s*产品", r"^一、产品", r"全系车型配置"],
    ),
    ("02-charging.md", "二、充电类信息", [r"^二、\s*充电", r"^⼆、\s*充电"]),
    ("03-purchase.md", "三、购买类信息", [r"^三、\s*购买", r"^三、购买"]),
    ("04-safety.md", "四、安全类信息", [r"^四、\s*安全"]),
    ("05-after-sales.md", "五、售后类信息", [r"^五、\s*售后"]),
    (
        "06-hot-topics.md",
        "六、舆论热点类",
        [r"^六、\s*舆论", r"^六、\s*热点"],
    ),
    (
        "07-corporate-culture.md",
        "七、企业文化类",
        [r"^七、\s*企业", r"^七、企业"],
    ),
]

Q_START = re.compile(r"^(\d+)\.\s*(.+)$")
Q_CONFIG = re.compile(r"^(\d+)\.\s*【(.+?)】")


def normalize(text: str) -> str:
    for a, b in EXTRA_MAP.items():
        text = text.replace(a, b)
    return text.translate(NORMALIZE)


def clean_lines(raw: str) -> list[str]:
    lines = []
    for line in raw.splitlines():
        line = normalize(line.strip())
        if not line or SKIP_LINES.match(line):
            continue
        if line in ("目录", "目 录") or re.match(r"^\d+-\d+$", line):
            continue
        if line.startswith("•") and "FABG" in line and len(line) < 20:
            continue
        lines.append(line)
    return lines


def detect_section(line: str) -> str | None:
    for _, title, patterns in SECTIONS[1:]:
        for p in patterns:
            if re.match(p, line):
                return title
    return None


def split_questions(lines: list[str]) -> list[tuple[str, str, list[str]]]:
    """Return list of (num, title, body_lines)."""
    items: list[tuple[str, str, list[str]]] = []
    cur_num, cur_title, body = "", "", []

    def flush():
        nonlocal cur_num, cur_title, body
        if cur_num and cur_title:
            items.append((cur_num, cur_title, body))
        cur_num, cur_title, body = "", "", []

    for line in lines:
        m = Q_CONFIG.match(line) or Q_START.match(line)
        if m:
            flush()
            cur_num = m.group(1)
            cur_title = m.group(2).strip()
            continue
        if cur_num:
            body.append(line)
    flush()
    return items


def format_qa_block(num: str, title: str, body: list[str]) -> str:
    text = "\n".join(body).strip()
    if not text:
        text = "（PDF 提取无正文，请对照原稿补全。）"
    return f"### {num}. {title}\n\n{text}\n"


def write_file(path: Path, title: str, section_title: str, content: str, tags: str):
    header = f"""# {title}

**文档类型:** training  
**section:** {section_title}  
**source:** 最新产品100问.pdf（内部培训）  
**tags:** {tags}  

> 内部资料，仅供 Skill 知识库使用。价格、补贴等易变信息答复时须结合 `knowledge/META.md` 的 `effective_date` 标注时效。

---

"""
    path.write_text(header + content, encoding="utf-8")


def main():
    raw = EXTRACT.read_text(encoding="utf-8")
    # drop page markers blocks
    raw = re.sub(r"===== PAGE \d+ =====", "", raw)
    lines = clean_lines(raw)

    # Preface: before first section
    preface_lines: list[str] = []
    section_buckets: dict[str, list[str]] = {s[1]: [] for s in SECTIONS[1:]}
    current = "前言"

    for line in lines:
        sec = detect_section(line)
        if sec:
            current = sec
            section_buckets[current].append(line)
            continue
        if current == "前言":
            if detect_section(line):
                continue
            preface_lines.append(line)
        else:
            section_buckets[current].append(line)

    # Also capture FABG from early lines in preface
    fabg_content = []
    in_preface = True
    for line in lines:
        if detect_section(line):
            in_preface = False
            break
        if any(
            k in line
            for k in (
                "FABG",
                "Feature",
                "Advantage",
                "Benefit",
                "Grabber",
                "问答赞",
                "Product Specialist",
                "加速世界",
            )
        ):
            fabg_content.append(line)
        elif line.startswith("•") and in_preface:
            fabg_content.append(line)

    file_map = {
        "一、产品类信息": ("01-products.md", "产品类信息（100问）", "产品, 车型, 配置, 电池, 智能"),
        "二、充电类信息": ("02-charging.md", "充电类信息", "充电, 家充, 超充"),
        "三、购买类信息": ("03-purchase.md", "购买类信息", "购买, 价格, 贷款, 订车, 置换"),
        "四、安全类信息": ("04-safety.md", "安全类信息", "安全, 刹车, 电池, AP"),
        "五、售后类信息": ("05-after-sales.md", "售后类信息", "售后, 质保, 保养"),
        "六、舆论热点类": ("06-hot-topics.md", "舆论热点类", "热点, 舆论, 刹车事件"),
        "七、企业文化类": ("07-corporate-culture.md", "企业文化类", "企业文化"),
    }

    preface_md = "\n".join(fabg_content) or "\n".join(preface_lines[:40])
    write_file(
        OUT_DIR / "00-preface-fabg.md",
        "前言：FABG 沟通方法",
        "前言",
        preface_md + "\n",
        "FABG, 沟通技巧",
    )

    stats = {}
    for sec_title, bucket in section_buckets.items():
        if sec_title not in file_map:
            continue
        fname, doc_title, tags = file_map[sec_title]
        items = split_questions(bucket)
        blocks = [format_qa_block(n, t, b) for n, t, b in items]
        body = "\n---\n\n".join(blocks) if blocks else "\n".join(bucket)
        write_file(OUT_DIR / fname, doc_title, sec_title, body, tags)
        stats[fname] = len(items)

    # Remove placeholders
    for p in ["placeholder.md"]:
        fp = OUT_DIR / p
        if fp.exists():
            fp.unlink()

    print("Wrote files:", stats)
    total = sum(stats.values())
    print("Total Q&A blocks:", total)


if __name__ == "__main__":
    main()
