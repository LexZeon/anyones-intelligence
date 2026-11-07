"""Bilingual, editable supporting diagrams for sections 5.3, 5.9 and 5.10.

Only the author-described relationships are drawn. Positions, colors and widths
are layout choices, not data or an additional computational architecture.
Call ``build('zh')`` or ``build('en')`` and save each returned Scene externally.
"""

from diagram_scene import Scene


BLUE = '#0072B2'
ORANGE = '#D55E00'
NEUTRAL = '#334155'
TEXT = '#17212B'
MUTED = '#5B6775'
LINE = '#CBD5E1'
WHITE = '#FFFFFF'
SOFT_BLUE = '#F2F8FC'
SOFT_ORANGE = '#FFF6F0'
SOFT = '#F8FAFC'


def _choose(lang, zh, en):
    return zh if lang == 'zh' else en


def _page(number, title, subtitle, height):
    scene = Scene(1200, height, title)
    scene.text(50, 28, f'FIGURE {number:02d}', 15, MUTED,
               weight='bold', width=1100)
    scene.text(50, 62, title, 31, TEXT, weight='bold', width=1100)
    scene.text(50, 111, subtitle, 18, MUTED, width=1100)
    scene.poly([(50, 174), (1150, 174)], LINE, 1.5)
    return scene


def _card(scene, x, y, w, h, title, body='', accent=NEUTRAL,
          fill=WHITE, title_size=23, body_size=20):
    scene.rect(x, y, w, h, fill, LINE, 1.5, 7)
    scene.rect(x, y, 5, h, accent, accent, 0, 0)
    scene.text(x + 23, y + 20, title, title_size, TEXT,
               weight='bold', width=w - 46)
    if body:
        scene.text(x + 23, y + 59, body, body_size, MUTED, width=w - 46)


def _footer(scene, y, text):
    scene.poly([(50, y), (1150, y)], LINE, 1)
    scene.text(50, y + 18, text, 16, MUTED, width=1100)


def _memory_encoding(lang):
    t = lambda zh, en: _choose(lang, zh, en)
    scene = _page(
        4,
        t('记忆写入：经历、生理状态与记忆属性',
          'Memory encoding: experience, state, and memory properties'),
        t('本文假说｜以“因胖被嘲笑”的经历为例；区分基础权重与基色。',
          'Author\'s hypothesis | Using mockery about body weight to illustrate base weight and affective tone.'),
        1060,
    )

    # Connections end at card borders; no connector passes through a label.
    scene.poly([(295, 355), (295, 393), (505, 393), (505, 430)], BLUE, 2.8, arrow=True)
    scene.poly([(905, 355), (905, 393), (695, 393), (695, 430)], ORANGE, 2.8, arrow=True)
    scene.poly([(505, 540), (505, 591), (295, 591), (295, 640)], BLUE, 2.8, arrow=True)
    scene.poly([(695, 540), (695, 591), (905, 591), (905, 640)], ORANGE, 2.8, arrow=True)
    scene.poly([(295, 795), (295, 865)], BLUE, 2.8, arrow=True)
    # A dashed, unheaded link denotes association rather than a fixed outcome.
    scene.poly([(905, 795), (905, 865)], ORANGE, 2.8, dash=True)

    _card(scene, 50, 210, 490, 145,
          t('一次经历', 'An experience'),
          t('因“胖”被嘲笑', 'Being mocked for being “fat”'), BLUE, SOFT_BLUE)
    _card(scene, 660, 210, 490, 145,
          t('写入时的生理状态', 'Bodily state during encoding'),
          t('例如压力反应，以及皮质醇、\n肾上腺素等生理变化',
            'For example, stress responses involving\ncortisol and adrenaline'),
          ORANGE, SOFT_ORANGE, title_size=22, body_size=19)
    _card(scene, 400, 430, 400, 110,
          t('记忆写入', 'Memory encoding'),
          t('经历与当时身体状态相联系',
            'Experience and bodily state are linked'),
          NEUTRAL, SOFT, body_size=18)
    _card(scene, 50, 640, 490, 155,
          t('基础权重', 'Base weight'),
          t('在本例中获得较高权重\n影响之后被调用的倾向',
            'Higher in this example;\ninfluences the tendency to be recalled'),
          BLUE, SOFT_BLUE, body_size=19)
    _card(scene, 660, 640, 490, 155,
          t('基色', '“Base color”'),
          t('记忆所带有的感受\n例如焦虑、恐惧',
            'The affective tone a memory carries,\nsuch as anxiety or fear'),
          ORANGE, SOFT_ORANGE, body_size=19)

    scene.rect(50, 865, 490, 86, WHITE, BLUE, 1.5, 7)
    scene.text(295, 882,
               t('之后更容易被相关线索唤起',
                 'More readily evoked by related cues'),
               20, TEXT, anchor='middle', width=446)
    scene.text(295, 916, t('调用倾向，不是保证被调用',
                          'A recall tendency, not guaranteed recall'),
               16, MUTED, anchor='middle', width=446)
    scene.rect(660, 865, 490, 86, WHITE, ORANGE, 1.5, 7)
    scene.text(905, 882, t('与之后的回避反应相关',
                          'Associated with later avoidance'),
               20, TEXT, anchor='middle', width=446)
    scene.text(905, 916, t('也联系着先天趋利避害机制',
                          'Also linked to innate approach–avoidance'),
               16, MUTED, anchor='middle', width=446)
    _footer(scene, 985,
            t('箭头呈现本文提出的关系，虚线表示关联；不表示固定公式、概率或已经验证的写入机制。',
              'Arrows show proposed relations; the dashed line marks an association.\nNo fixed formula, probability, or validated encoding mechanism is specified.'))
    return '04_memory_encoding', scene


def _foundation_and_history(lang):
    t = lambda zh, en: _choose(lang, zh, en)
    scene = _page(
        7,
        t('Foundation 与带着经历的当前状态',
          'Foundation and present states shaped by experience'),
        t('本文定义｜共同的先天基础，不等于经历之后的当下实在界。',
          'Author-defined terms | A shared innate basis is distinct from the current Real shaped by experience.'),
        1030,
    )

    scene.poly([(295, 385), (295, 480)], BLUE, 2.8, arrow=True)
    scene.poly([(905, 385), (905, 480)], ORANGE, 2.8, arrow=True)
    # Both current states remain grounded in the same innate basis. This is not
    # a temporal sequence of developmental stages.
    scene.poly([(295, 795), (295, 655)], NEUTRAL, 2.8, arrow=True)
    scene.poly([(905, 795), (905, 655)], NEUTRAL, 2.8, arrow=True)

    for x, suffix, color, fill in ((50, 'A', BLUE, SOFT_BLUE),
                                    (660, 'B', ORANGE, SOFT_ORANGE)):
        _card(scene, x, 230, 490, 155,
              t(f'经历路径 {suffix}', f'Experience path {suffix}'),
              t('经历、学习、记忆\n其中形成的联系被保留下来',
                'Experience, learning, and memory\nleave a history of connections'),
              color, fill, body_size=19)
        scene.text(x + 275, 407,
                   t('过去经历\n继续参与', 'Past experience\nstill contributes'),
                   17, MUTED, width=192)
        _card(scene, x, 480, 490, 175,
              t(f'当前实在界 {suffix}', f'Current Real — {suffix}'),
              t('当下具体的生理状态与反应\n也受到过去记忆与想象影响',
                'Concrete bodily states and responses,\nalso influenced by memory\nand imagination'),
              color, fill, title_size=23, body_size=19)

    scene.text(600, 694, t('接近 ≠ 等同', 'Close does not mean identical'),
               23, TEXT, anchor='middle', weight='bold', width=480)
    scene.text(600, 734,
               t('回到低处，经历仍有影响', 'Returning lower does not erase history'),
               18, MUTED, anchor='middle', width=480)
    scene.rect(50, 795, 1100, 125, SOFT, NEUTRAL, 1.7, 7)
    scene.text(600, 817, 'Foundation', 27, TEXT, anchor='middle', weight='bold', width=1020)
    scene.text(600, 860,
               t('共同的先天基础：进食、趋利避害',
                 'Shared innate mechanisms: feeding and approach–avoidance'),
               21, MUTED, anchor='middle', width=1020)
    _footer(scene, 951,
            t('A / B 仅区分不同经历路径，不表示发展阶段。向上箭头表示先天机制的作用；当前状态不是空白起点。',
              'A / B distinguish histories, not developmental stages. Upward arrows show the influence of innate mechanisms.\nThe present state is not a blank starting point.'))
    return '07_foundation_and_history', scene


def _transformer_analogy(lang):
    t = lambda zh, en: _choose(lang, zh, en)
    scene = _page(
        8,
        t('记忆网络与 Transformer：类比，不是组件等价',
          'Memory networks and attention: an analogy, not equivalence'),
        t('将作者的相似感与注意力的技术定义并列；不据此指定新模型架构。',
          'An author-proposed resemblance beside the technical definition of attention; no new architecture is specified.'),
        1110,
    )
    scene.text(76, 207, t('作者的记忆网络｜本文假说',
                          'The author\'s memory network'),
               23, BLUE, weight='bold', width=488)
    scene.text(658, 207, t('Transformer 注意力｜技术定义',
                           'Transformer attention | Definition'),
               22, ORANGE, weight='bold', width=488)
    scene.rect(50, 249, 514, 570, SOFT_BLUE, LINE, 1, 7)
    scene.rect(636, 249, 514, 570, SOFT_ORANGE, LINE, 1, 7)

    # The panels deliberately have no cross-panel correspondence arrows.
    scene.poly([(307, 403), (307, 474)], BLUE, 2.8, arrow=True)
    scene.poly([(307, 601), (307, 670)], BLUE, 2.8, arrow=True)
    _card(scene, 83, 283, 448, 120,
          t('5.4 词／词元（token）', '5.4 Words / tokens'),
          t('词与关系怎样牵动相关记忆',
            'How words and relations engage\nrelevant memories'),
          BLUE, WHITE, title_size=22, body_size=19)
    _card(scene, 83, 474, 448, 127,
          t('5.5 权重、共同参与与当前状态', '5.5 Weights and joint contribution'),
          t('多条联系按不同权重共同参与\n当下生理状态调节参与程度',
            'Multiple weighted contributions,\nmodulated by the current bodily state'),
          BLUE, WHITE, title_size=18.5, body_size=19)
    _card(scene, 83, 670, 448, 100,
          t('当前理解与反应', 'Present understanding and response'),
          t('相关内容共同参与', 'Relevant contents contribute together'),
          BLUE, WHITE, title_size=19, body_size=18)

    scene.poly([(770, 373), (770, 407), (798, 407), (798, 440)], ORANGE, 2.8, arrow=True)
    scene.poly([(1012, 373), (1012, 407), (990, 407), (990, 440)], ORANGE, 2.8, arrow=True)
    scene.poly([(893, 540), (893, 581), (991, 581), (991, 628)], ORANGE, 2.8, arrow=True)
    scene.poly([(812, 696), (864, 696)], ORANGE, 2.8, arrow=True)
    _card(scene, 668, 283, 204, 90, 'Q', t('Query 向量', 'Query vectors'),
          ORANGE, WHITE, body_size=18)
    _card(scene, 906, 283, 212, 90, 'K', t('Key 向量', 'Key vectors'),
          ORANGE, WHITE, body_size=18)
    _card(scene, 668, 440, 450, 100,
          t('Q / K 的匹配 → 权重', 'Q / K compatibility → weights'),
          t('通过 query 与 key 的匹配计算权重',
            'Compatibility determines the weights'),
          ORANGE, WHITE, title_size=22, body_size=18)
    _card(scene, 668, 638, 144, 132, 'V', t('Value\n向量', 'Value\nvectors'),
          ORANGE, WHITE, body_size=18)
    _card(scene, 864, 628, 254, 142,
          t('对 V 加权求和', 'Weighted sum'),
          t('由这些权重对 V 求和\n得到注意力输出',
            'of V vectors\n→ attention output'),
          ORANGE, WHITE, title_size=21, body_size=18)

    scene.rect(50, 856, 1100, 144, WHITE, NEUTRAL, 1.5, 7)
    scene.text(76, 880,
               t('类比关注：联系、权重与不同内容的共同参与',
                 'The analogy concerns connections, weights, and multiple contributions'),
               23, TEXT, weight='bold', width=1048)
    scene.text(76, 925,
               t('本文尚未说明具体组件对应；不表示记忆等于 V、词元等于 Q / K，\n也不表示生理状态等于注意力权重。',
                 'This account does not specify component correspondences: memory is not identified with V,\ntokens with Q / K, or physiological states with attention weights.'),
               19, MUTED, width=1048)
    _footer(scene, 1034,
            t('左侧：本文假说与类比。右侧：Vaswani 等，§3.2 的注意力技术定义。图中没有实验数据或新增模型机制。',
              'Left: the author\'s hypothesis and analogy. Right: the attention definition in Vaswani et al., §3.2.\nNo experimental data or additional model mechanism is shown.'))
    return '08_transformer_analogy', scene


def build(lang):
    """Return file stems and editable scenes without writing output files."""
    if lang not in ('zh', 'en'):
        raise ValueError("lang must be 'zh' or 'en'")
    return [_memory_encoding(lang), _foundation_and_history(lang), _transformer_analogy(lang)]
