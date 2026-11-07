"""Editable overview diagrams for the bilingual research account.

Only layout and author-provided content live here.  ``diagram_scene.Scene``
provides the shared SVG, PNG, and draw.io exporters.  ``build`` deliberately
does not export files, so the main figure build can choose its destinations.
"""

from __future__ import annotations

from diagram_scene import Scene


BLUE = "#0072B2"
ORANGE = "#D55E00"
NEUTRAL = "#334155"
INK = "#17212B"
MUTED = "#5B6775"
LINE = "#CBD5E1"
PALE_BLUE = "#F2F8FC"
PALE_GRAY = "#F8FAFC"
WHITE = "#FFFFFF"
WIDTH = 1200


def _page(number: str, title: str, subtitle: str, height: int, lang: str) -> Scene:
    scene = Scene(WIDTH, height, title=title)
    scene.rect(0, 0, WIDTH, height, fill=WHITE)
    scene.text(56, 30, f"FIGURE {number}", size=14, color=BLUE, weight="bold")
    scene.text(
        1144,
        30,
        "ANYONE'S INTELLIGENCE",
        size=14,
        color=MUTED,
        anchor="end",
    )
    scene.text(56, 62, title, size=28, color=INK, weight="bold", width=1088)
    scene.text(56, 106, subtitle, size=18, color=MUTED, width=1088)
    scene.poly([(56, 148), (1144, 148)], color=LINE, sw=1)
    return scene


def _footer(scene: Scene, height: int, text: str) -> None:
    scene.poly([(56, height - 64), (1144, height - 64)], color=LINE, sw=1)
    scene.text(56, height - 43, text, size=14, color=MUTED, width=1088)


def _source_card(
    scene: Scene, x: int, y: int, w: int, h: int,
    title: str, body: str, accent: str,
) -> None:
    scene.rect(x, y, w, h, fill=WHITE, stroke=LINE, sw=1, r=10)
    scene.rect(x, y + 18, 4, h - 36, fill=accent)
    scene.text(x + 24, y + 17, title, size=21, color=INK, weight="bold", width=w - 48)
    scene.text(x + 24, y + 52, body, size=18, color=MUTED, width=w - 48)


def _process_card(
    scene: Scene, x: int, y: int, w: int, h: int,
    kicker: str, title: str, body: str, fill: str = WHITE,
) -> None:
    scene.rect(x, y, w, h, fill=fill, stroke=LINE, sw=1, r=10)
    scene.text(x + 22, y + 20, kicker, size=14, color=BLUE, weight="bold", width=w - 44)
    scene.text(x + 22, y + 50, title, size=23, color=INK, weight="bold", width=w - 44)
    scene.text(x + 22, y + 121, body, size=18, color=MUTED, width=w - 44)


def _intellectual_roots(lang: str) -> Scene:
    zh = lang == "zh"
    height = 820
    scene = _page(
        "01",
        "认识世界的路径与项目起点" if zh else "Intellectual roots and the project's starting point",
        "不同知识与自身体验，汇合为对智能与模型的探索。" if zh
        else "Studies and lived experience converge on the exploration of intelligence and models.",
        height,
        lang,
    )

    # A shared connector collects the four sources without imposing a timeline.
    centers = [242, 384, 526, 668]
    for center in centers:
        scene.poly([(508, center), (580, center)], color=LINE, sw=2)
    scene.poly([(580, centers[0]), (580, centers[-1])], color=LINE, sw=2)
    scene.poly([(580, 473), (648, 473)], color=BLUE, sw=3, arrow=True)
    scene.dot(580, 473, r=5, fill=BLUE, stroke=WHITE, sw=2)

    sources = [
        (
            "自然科学" if zh else "Natural sciences",
            "物理、化学、生物、数学\n量子力学、地理" if zh
            else "Physics · chemistry · biology · mathematics\nQuantum mechanics · geography",
            BLUE,
        ),
        (
            "人文与艺术" if zh else "Arts and humanities",
            "艺术史、艺术、哲学、文学\n历史、政治、心理学、人文地理" if zh
            else "Art, literature, philosophy, history\nPolitics, psychology, human geography",
            ORANGE,
        ),
        (
            "自身体验" if zh else "Lived experience",
            "好奇、感受、生活中的认识与疑问\n理性理解与带着情绪的模糊感" if zh
            else "Curiosity, feelings, and everyday questions\nRational clarity and emotional ambiguity",
            NEUTRAL,
        ),
        (
            "拉康带来的启发" if zh else "Inspiration from Lacan",
            "“无意识的语言结构”\n从这一启发发展自己的解释" if zh
            else "The linguistic structure of the unconscious\nInspiration for my own explanation",
            BLUE,
        ),
    ]
    for y, (title, body, accent) in zip([180, 322, 464, 606], sources):
        _source_card(scene, 56, y, 452, 124, title, body, accent)

    scene.rect(648, 180, 496, 126, fill=PALE_GRAY, stroke=LINE, sw=1, r=10)
    scene.text(
        672, 200, "个人动机" if zh else "PERSONAL MOTIVATION",
        size=14, color=NEUTRAL, weight="bold",
    )
    scene.text(
        672, 231, "理解世界，也理解自己" if zh else "Understand the world and myself",
        size=22, color=INK, weight="bold", width=448,
    )
    scene.text(
        672, 267, "把生活中的认识与疑问积累为研究材料。" if zh
        else "Preserve everyday insights as research material.",
        size=18, color=MUTED, width=448,
    )

    scene.rect(648, 358, 496, 230, fill=PALE_BLUE, stroke=BLUE, sw=2, r=12)
    scene.text(
        676, 382, "项目方向" if zh else "PROJECT DIRECTION",
        size=14, color=BLUE, weight="bold",
    )
    scene.text(676, 417, "Anyone's Intelligence", size=26, color=INK, weight="bold", width=440)
    scene.text(
        676, 467, "学习人工智能\n探索语言模型中的模拟认知" if zh
        else "Learn about artificial intelligence\nExplore simulated cognition\nin language models",
        size=22, color=INK, width=440,
    )

    scene.rect(648, 632, 496, 98, fill=WHITE, stroke=LINE, sw=1, r=10)
    scene.rect(648, 650, 4, 62, fill=ORANGE)
    scene.text(
        672, 650, "感情与理解最终回到物理世界。\n量化是模型探索的重要部分。" if zh
        else "Feelings and understanding are physical.\nQuantification guides model exploration.",
        size=18, color=NEUTRAL, width=448,
    )

    _footer(
        scene, height,
        "个人经历与思想来源的概念图 · 箭头表示研究方向的汇合，不表示时间顺序。" if zh
        else "Concept map of personal and intellectual roots · Connections show convergence, not a timeline.",
    )
    return scene


def _research_direction(lang: str) -> Scene:
    zh = lang == "zh"
    height = 790
    scene = _page(
        "02",
        "从认知链到模型探索" if zh else "From a cognitive chain to model exploration",
        "以作者提出的关系结构为参考，通过量化与原型探索模拟认知。" if zh
        else "Use the proposed relational structure to explore simulated cognition through quantification and prototypes.",
        height,
        lang,
    )

    for start, end in [(376, 440), (760, 824)]:
        scene.poly([(start + 8, 286), (end - 8, 286)], color=BLUE, sw=3, arrow=True)

    columns = [
        (
            56,
            "理论参考" if zh else "THEORETICAL REFERENCE",
            "作者提出的\n认知链" if zh else "The proposed\ncognitive chain",
            "经历、记忆、语言与状态\n共同参与理解与反应" if zh
            else "Experience and memory\nLanguage and state\nJointly shape understanding",
            WHITE,
        ),
        (
            440,
            "研究过程" if zh else "RESEARCH PROCESS",
            "量化与\n语言模型原型" if zh else "Quantification\nand implementation",
            "状态变化与联系形成\n权重差异及其共同作用" if zh
            else "Language-model prototypes\nStates and connections\nWeights acting together",
            PALE_BLUE,
        ),
        (
            824,
            "实现目标" if zh else "IMPLEMENTATION AIM",
            "在模型中\n模拟认知" if zh else "Simulated cognition\nin a model",
            "探索感受、语言与记忆\n怎样共同参与认知过程" if zh
            else "Feelings and language\ninteract with memory\nin cognitive processes.",
            WHITE,
        ),
    ]
    for x, kicker, title, body, fill in columns:
        _process_card(scene, x, 184, 320, 202, kicker, title, body, fill)

    scene.poly([(56, 437), (1144, 437)], color=LINE, sw=1)
    scene.text(
        56, 459, "长期愿景" if zh else "Long-term aims",
        size=23, color=INK, weight="bold",
    )
    scene.text(
        1144, 465, "研究目标 · 尚非成果" if zh else "RESEARCH AIMS · NOT ESTABLISHED RESULTS",
        size=14, color=ORANGE, anchor="end", weight="bold",
    )

    aims = [
        (
            56,
            "可靠理解与可解释性" if zh else "Reliability and\ninterpretability",
            "减少并尝试消除幻觉\n逐步消除黑箱\n提高使用安全性" if zh
            else "Seek to eliminate hallucinations\nand black-box opacity.\nImprove safety in use.",
        ),
        (
            428,
            "对人文领域的深入理解" if zh else "Depth of understanding",
            "艺术\n文化\n政治" if zh
            else "Art\nCulture\nPolitics",
        ),
        (
            800,
            "自主思考与意识探索" if zh else "Independent thought\nand consciousness",
            "自主思考与创新解题\n探索模型产生“意识”的可能" if zh
            else "Independent thinking and\ninnovative problem-solving.\nExplore possible consciousness.",
        ),
    ]
    for x, title, body in aims:
        scene.rect(x, 516, 344, 190, fill=WHITE, stroke=LINE, sw=1, r=10)
        scene.rect(x + 22, 535, 34, 4, fill=ORANGE)
        scene.text(x + 22, 553, title, size=21, color=INK, weight="bold", width=300)
        scene.text(x + 22, 621, body, size=18, color=MUTED, width=300)

    _footer(
        scene, height,
        "研究方向示意 · 模型架构保持开放 · 长期愿景需要后续研究与验证。" if zh
        else "Research direction · The model architecture remains open · Long-term aims require further research and validation.",
    )
    return scene


def _chain_to_model(lang: str) -> Scene:
    zh = lang == "zh"
    height = 840
    scene = _page(
        "03",
        "从参考链到模型模拟" if zh else "From the reference chain to model simulation",
        "以物理基础和量化为出发点，探索状态与关系的模型对应。" if zh
        else "Start from a physical basis and quantification to explore model representations of states and relations.",
        height,
        lang,
    )
    scene.text(
        56, 172, "作者假说中的参考链" if zh else "Reference chain in the author's hypothesis",
        size=22, color=INK, weight="bold",
    )
    scene.text(
        1144, 178, "参考来源" if zh else "REFERENCE",
        size=14, color=NEUTRAL, anchor="end", weight="bold",
    )

    # The two-way connection follows the stated interaction of memory and state.
    scene.poly([(384, 283), (432, 283)], color=BLUE, sw=2, arrow=True)
    scene.poly([(432, 313), (384, 313)], color=BLUE, sw=2, arrow=True)
    scene.poly([(768, 298), (816, 298)], color=BLUE, sw=3, arrow=True)

    references = [
        (
            56,
            "生理状态" if zh else "Physiological states",
            "经历发生时的状态\n当前饥饿与生理反应" if zh
            else "State during an experience\nCurrent hunger and\nphysiological responses",
        ),
        (
            440,
            "记忆及其联系" if zh else "Memory connections",
            "联系的形成与强化、基础权重\n共同的词／词元（token）和关系" if zh
            else "Formation and strengthening\nBase weights; shared words /\ntokens and relations",
        ),
        (
            824,
            "反应与行为" if zh else "Response and action",
            "多条联系共同参与\n结果随权重和当前状态变化" if zh
            else "Connections act together\nOutcomes depend on weights\nand the current state",
        ),
    ]
    for x, title, body in references:
        scene.rect(x, 218, 320, 164, fill=WHITE, stroke=LINE, sw=1, r=10)
        scene.text(x + 22, 239, title, size=21, color=INK, weight="bold", width=276)
        scene.text(x + 22, 282, body, size=18, color=MUTED, width=276)

    # One collective mapping, not an invented one-to-one module architecture.
    for center in [216, 600, 984]:
        scene.poly([(center, 382), (center, 414)], color=LINE, sw=2)
    scene.poly([(216, 414), (984, 414)], color=LINE, sw=2)
    scene.poly([(600, 414), (600, 526)], color=BLUE, sw=2, dash=True, arrow=True)
    scene.rect(332, 433, 536, 65, fill=WHITE, stroke=LINE, sw=1, r=10)
    scene.text(
        600, 451 if zh else 441,
        "具体模型对应关系尚待阐述" if zh
        else "Specific model correspondences\nremain to be explained",
        size=18, color=MUTED, anchor="middle", width=488,
    )

    scene.rect(56, 526, 1088, 214, fill=PALE_BLUE, stroke=BLUE, sw=2, r=12)
    scene.text(
        84, 549, "实现目标" if zh else "IMPLEMENTATION AIM",
        size=14, color=BLUE, weight="bold",
    )
    scene.text(
        84, 581, "语言模型中的模拟认知" if zh else "Simulated cognition in a language model",
        size=26, color=INK, weight="bold", width=1032,
    )
    scene.text(
        84, 625,
        "将状态变化与关系结构转化为可量化、可运行的机制。" if zh
        else "Translate changes in state and relational structure into quantifiable, executable mechanisms.",
        size=18, color=INK, width=1032,
    )
    scene.poly([(84, 662), (1116, 662)], color=LINE, sw=1)
    scene.text(
        84, 681,
        "量化关注：状态变化 · 联系形成与强化 · 各条联系的参与程度" if zh
        else "Quantification: state changes · connection formation and strengthening · degree of participation",
        size=18, color=MUTED, width=1032,
    )

    _footer(
        scene, height,
        "概念示意 · 区分参考来源与实现目标 · 未使用测量数值或激素曲线。" if zh
        else "Conceptual diagram · Reference sources and implementation aims · No measured values or hormone curves.",
    )
    return scene


def build(lang: str) -> list[tuple[str, Scene]]:
    """Return the three overview scenes in ``zh`` or ``en`` without exporting."""
    if lang not in {"zh", "en"}:
        raise ValueError("lang must be 'zh' or 'en'")
    return [
        ("01_intellectual_roots", _intellectual_roots(lang)),
        ("02_research_direction", _research_direction(lang)),
        ("03_chain_to_model", _chain_to_model(lang)),
    ]
