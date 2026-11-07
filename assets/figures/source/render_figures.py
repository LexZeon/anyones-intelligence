"""Editable research diagrams. Coordinates are layout, never empirical values.

Run with Python + matplotlib. --dependency-path can point at an existing install.
No network access, inference, or generated bitmap artwork is involved.
"""
from pathlib import Path
import argparse
import sys

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--dependency-path', type=Path)
    args = parser.parse_args()
    if args.dependency_path:
        sys.path.insert(0, str(args.dependency_path))

from diagram_scene import Scene

BLUE = '#0072B2'
ORANGE = '#D55E00'
INK = '#17212B'
MUTED = '#5B6775'
SHARED = '#334155'
GRID = '#CBD5E1'


def words(lang, zh, en):
    return zh if lang == 'zh' else en


def header(scene, number, title, subtitle):
    scene.text(44, 25, f"ANYONE'S INTELLIGENCE   /   FIGURE {number:02d}", 12, MUTED, weight='bold')
    scene.text(44, 55, title, 28, INK, weight='bold')
    scene.text(44, 98, subtitle, 17, MUTED)
    scene.poly([(44, 133), (1156, 133)], GRID, 1)


def field(scene, lang, top, lane=120):
    left, right = 195, 1150
    scene.text(left, top - 35, words(lang, 'y · 抽象 / cofoundational 程度', 'y · Abstraction / cofoundational degree'), 16, MUTED)
    for i, (zh, en) in enumerate([('象征界', 'Symbolic'), ('想象界', 'Imaginary'), ('实在界', 'Real')]):
        scene.rect(left, top+i*lane, right-left, lane, ['#F1F5F9', '#F7F9FB', '#FCFDFE'][i])
        scene.poly([(left, top+i*lane), (right, top+i*lane)], GRID, 1)
        scene.text(45, top+i*lane+lane/2-18, words(lang, zh, en), 21, INK, weight='bold')
        if lang == 'zh':
            scene.text(45, top+i*lane+lane/2+12, en, 12, MUTED)
    bottom = top+3*lane
    scene.poly([(left, bottom), (right, bottom)], GRID, 1)
    scene.poly([(179, bottom), (179, top)], MUTED, 1.4, arrow=True)
    scene.rect(left, bottom+24, right-left, 45, '#E8EDF2', '#BBC6D1', 1, 3)
    scene.text((left+right)/2, bottom+35, words(lang, 'Foundation · 先天的进食与趋利避害机制', 'Foundation · Innate feeding and approach–avoidance mechanisms'), 17, SHARED, anchor='middle')
    scene.poly([(left, bottom+91), (right, bottom+91)], MUTED, 1.4, arrow=True)
    scene.text(right, bottom+104, words(lang, 'x · 链的展开（无固定单位）', 'x · Unfolding of the chain (no fixed unit)'), 15, MUTED, anchor='end')
    return bottom


def smooth(points, steps=18):
    tangents = []
    for i, point in enumerate(points):
        prev = points[max(0, i-1)]
        nxt = points[min(len(points)-1, i+1)]
        scale = .7 if i in (0, len(points)-1) else .4
        tangents.append(((nxt[0]-prev[0])*scale, (nxt[1]-prev[1])*scale))
    out = [points[0]]
    for i in range(len(points)-1):
        a,d = points[i:i+2]
        b=(a[0]+tangents[i][0]/3, a[1]+tangents[i][1]/3)
        c=(d[0]-tangents[i+1][0]/3, d[1]-tangents[i+1][1]/3)
        for j in range(1, steps+1):
            t=j/steps
            out.append(tuple((1-t)**3*a[k]+3*(1-t)**2*t*b[k]+3*(1-t)*t*t*c[k]+t**3*d[k] for k in (0,1)))
    return out


def curve(s, points, color=BLUE, width=3, dashed=False, arrow_indices=()):
    path=smooth(points)
    s.poly(path, color, width, dashed)
    for fraction in arrow_indices:
        j=max(2, min(len(path)-1, int(fraction*(len(path)-1))))
        s.poly(path[j-2:j+1], color, width, arrow=True)


def label(s, x, y, text, width=170, size=18, color=INK):
    height = size*1.35*len(text.split('\n'))+14
    s.rect(x-width/2, y-7, width, height, '#FFFFFF', GRID, .8, 4)
    s.text(x, y, text, size, color, anchor='middle')


def legend(s, lang, y, include_weight=False):
    entries=[(BLUE,False,words(lang,'甜食 / 进食相关链','Sweets / feeding chain')),
             (ORANGE,True,words(lang,'嘲笑 / 回避相关链','Mockery / avoidance chain'))]
    for x,(color,dash,text) in zip((195,520),entries):
        s.poly([(x,y+11),(x+42,y+11)],color,3,dash)
        s.text(x+55,y,text,16,INK)
    if include_weight:
        s.poly([(890,y+5),(928,y+5)],SHARED,5.5)
        s.poly([(890,y+19),(928,y+19)],SHARED,2)
        s.text(940,y,words(lang,'较强 / 较弱','Stronger / weaker'),16,INK)
    else:
        s.dot(936,y+11,5,SHARED,SHARED,1)
        s.text(953,y,words(lang,'共享连接','Shared link'),16,INK)


def footer(s, lang, y, note):
    s.poly([(44,y-14),(1156,y-14)],GRID,1)
    s.text(44,y,note,15,INK)
    s.text(44,y+27,words(lang,'概念示意 · 三界采用作者定义 · 坐标、曲线与线宽不表示测量值',
                       'Conceptual diagram · Author-defined registers · Geometry and widths are not measurements'),14,MUTED)


def single_chain(lang):
    s=Scene(1200,805,'Single cognitive chain')
    header(s,5,words(lang,'一条认知链：从状态到关系，再回到反应','A cognitive chain: state, relations, and response'),
           words(lang,'同一条链贯穿三个层次；返回低处时，经历的影响仍然保留。',
                 'One chain spans three levels; returning to a lower level preserves the influence of experience.'))
    field(s,lang,190,115)
    p=[(245,470),(435,265),(610,215),(780,264),(948,370),(1095,470)]
    curve(s,p,width=3.4,arrow_indices=(.13,.36,.66,.91))
    for x,y in p:s.dot(x,y,5.5,'#FFFFFF',BLUE,2.5)
    s.text(285,485,words(lang,'饥饿\n进食驱力','Hunger\nFeeding drive'),16,INK,anchor='middle')
    label(s,435,207,words(lang,'糖','Sugar'),95,19)
    label(s,610,244,words(lang,'胖','“Fat”'),95,19)
    label(s,780,203,words(lang,'嘲笑','Mockery'),115,19)
    s.poly([(948,370),(984,350)],GRID,1)
    label(s,1067,306,words(lang,'我再吃，\n就会再被嘲笑','If I eat sweets\nagain, I will be\nmocked again.'),166,16)
    s.text(1045,485,words(lang,'恐惧的生理反应\n回避甜食','Fear-related physiology\nAvoiding sweets'),16,INK,anchor='middle')
    s.poly([(195,700),(240,700)],BLUE,3.4,arrow=True)
    s.text(252,689,words(lang,'链的展开方向','Direction of unfolding'),16,INK)
    s.dot(575,700,5.5,'#FFFFFF',BLUE,2)
    s.text(591,689,words(lang,'状态、词／词元或想象内容','State, word / token, or imagined content'),16,INK)
    footer(s,lang,748,words(lang,'图示为吃糖例子的特定结果；Foundation 与当前生理状态保持区分。',
                               'The outcome belongs to this example; foundation remains distinct from current physiology.'))
    return '01_single_chain',s


def intersecting(lang):
    s=Scene(1200,875,'Intersecting memory chains')
    header(s,6,words(lang,'记忆链通过共享的词与关系相连','Memory chains connect through shared words and relations'),
           words(lang,'两种来源分别保留；实心节点标出真正共享的连接。',
                 'The two origins remain distinct; filled nodes identify shared connections.'))
    field(s,lang,190,130)
    A,B,S,M,P,Q,E=(495,518),(250,518),(590,295),(440,219),(800,257),(920,400),(1100,515)
    curve(s,[A,S,P],BLUE,3.3,False,(.24,.74))
    curve(s,[B,M,P],ORANGE,3.3,True,(.28,.80))
    curve(s,[P,(858,315),Q],BLUE,3.3,False,(.6,))
    curve(s,[P,(825,409),(870,429),Q],ORANGE,3.3,True,(.58,))
    curve(s,[Q,(1010,420),E],SHARED,3.3,False,(.64,))
    for p,c in [(A,BLUE),(B,ORANGE),(S,BLUE),(M,ORANGE),(E,SHARED)]:s.dot(*p,5.5,'#FFFFFF',c,2.5)
    for p in (P,Q):s.dot(*p,7,SHARED,SHARED,1)
    s.text(495,539,words(lang,'甜食相关的\n生理体验','Physiology associated\nwith sweets'),17,BLUE,anchor='middle')
    s.text(265,539,words(lang,'被嘲笑时的\n生理反应','Physiological response\nduring mockery'),17,ORANGE,anchor='middle')
    s.text(612,291,words(lang,'糖','Sugar'),19,BLUE)
    label(s,440,176,words(lang,'嘲笑','Mockery'),115,19)
    label(s,836,203,words(lang,'共享词／词元：「胖」','Shared word / token: “fat”'),266,17)
    label(s,1025,325,words(lang,'我再吃，就会\n再被嘲笑','If I eat sweets again,\nI will be mocked again.'),232,17)
    label(s,1018,540,words(lang,'当下生理反应与行为','Current physiology\nand behavior'),236,17)
    legend(s,lang,738)
    footer(s,lang,815,words(lang,'颜色与线型只区分链的来源；共享末段不表示新增的认知模块。',
                               'Color and line style identify origins; the shared final segment introduces no new module.'))
    return '02_intersecting_memory_chains',s


def state_dependent(lang):
    s=Scene(1200,1420,'State-dependent participation')
    header(s,9,words(lang,'同一关系网络，不同的参与程度','One relational network, different degrees of participation'),
           words(lang,'两面板保持相同的节点与连接；只改变当前状态及其参与分配。',
                 'Both panels retain identical nodes and connections; current states and contributions differ.'))
    legend(s,lang,151,True)
    for idx,top in enumerate((272,842)):
        s.text(44,top-84,'A' if idx==0 else 'B',28,BLUE if idx==0 else ORANGE,weight='bold')
        s.text(86,top-79,words(lang,
            '进食驱动影响较强' if idx==0 else '回避相关影响较强',
            'Feeding drive has greater influence' if idx==0 else 'Avoidance has greater influence'),23,INK,weight='bold')
        field(s,lang,top,110)
        start=(250,top+283); P=(440,top+100); end=(1095,top+283)
        # The common part is drawn as a neutral reference segment so neither
        # colored path can hide the other. Width comparisons apply after P.
        curve(s,[start,(345,top+191),P],SHARED,2.8,False,(.55,))
        eat=[P,(609,top+86),(838,top+220),end]
        avoid=[P,(658,top+23),(928,top+171),end]
        curve(s,eat,BLUE,5.4 if idx==0 else 2.1,False,(.4,.8))
        curve(s,avoid,ORANGE,2.1 if idx==0 else 5.4,True,(.35,.77))
        s.dot(*start,5.5,'#FFFFFF',SHARED,2)
        s.dot(*P,7,SHARED,SHARED,1)
        s.dot(*end,5.5,'#FFFFFF',SHARED,2)
        s.text(250,top+297,words(lang,'当下状态','Current state'),18,SHARED,anchor='middle')
        s.poly([(392,top+90),(440,top+100)],GRID,1)
        label(s,350,top+65,words(lang,'糖','Sugar'),84,18)
        label(s,955,top+8,words(lang,'糖—胖—嘲笑','Sugar–“fat”–mockery'),270,17,ORANGE)
        label(s,610,top+174,words(lang,'进食相关经验','Feeding-related\nexperience'),170,15,BLUE)
        label(s,1070,top+130,words(lang,'再次被嘲笑\n的想象','Imagining being\nmocked again'),160,15,ORANGE)
        s.text(1097,top+297,words(lang,'共同影响反应与选择','Joint influence on response and choice'),17,SHARED,anchor='end')
    s.poly([(195,1342),(236,1342)],SHARED,2.8)
    s.text(248,1331,words(lang,'共同起始段（不编码参与强弱）','Shared initial segment (does not encode contribution strength)'),16,INK)
    footer(s,lang,1375,words(lang,'线宽仅表示定性参与程度；较弱的路径仍然参与，不预先指定必然选择。',
                                'Widths indicate qualitative contribution; weaker paths still contribute, with no inevitable choice.'))
    return '03_state_dependent_participation',s


def main():
    import json
    from render_supporting_overview import build as overview
    from render_supporting_mechanisms import build as mechanisms
    out=Path(__file__).resolve().parent.parent
    manifest=[]
    for lang in ('zh','en'):
        folder=out if lang=='zh' else out/'en'
        folder.mkdir(parents=True,exist_ok=True)
        scenes=[single_chain(lang),intersecting(lang),state_dependent(lang)]+overview(lang)+mechanisms(lang)
        assert len(scenes)==9
        for name,scene in scenes:
            scene.save(folder/name)
            manifest.append({'language':lang,'name':name,'width':scene.width,'height':scene.height,'elements':len(scene.items)})
    (out/'source'/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'figures':len(manifest),'formats':['svg','png','drawio'],'output':str(out)}))


if __name__=='__main__':main()
