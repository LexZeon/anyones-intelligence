"""Build the reviewed bilingual research pages from repository Markdown."""
from pathlib import Path
import argparse,sys,re,base64,html,shutil,json
from datetime import datetime

options=argparse.ArgumentParser(description=__doc__)
options.add_argument('--dependency-path',type=Path,help='Optional existing Python package directory')
options.add_argument('--check',action='store_true',help='Check generated files without modifying them')
args=options.parse_args()
if args.dependency_path:sys.path.insert(0,str(args.dependency_path))
from markdown_it import MarkdownIt
parser=MarkdownIt('commonmark')
REPO=Path(__file__).resolve().parent.parent
MDROOT=REPO/'docs/research'
OUT=REPO/'site/research'
BASE_URL='https://lexzeon.github.io/anyones-intelligence/'
GITHUB='https://github.com/LexZeon/anyones-intelligence/blob/main/'
LINK_TARGETS={
    'en.md':'index.html','zh-CN.md':'zh.html','../../CHANGELOG.md':'changelog.html',
    '../RESEARCH_PLAN.md':GITHUB+'docs/RESEARCH_PLAN.md',
    '../SAFETY.md':GITHUB+'docs/SAFETY.md','../../AGENTS.md':GITHUB+'AGENTS.md',
    'docs/research/en.md':'index.html','docs/research/zh-CN.md':'zh.html',
}
meta=json.loads((REPO/'version.json').read_text(encoding='utf-8'))
recorded=datetime.fromisoformat(meta['recorded_at'])
if recorded.utcoffset() is None:
    raise SystemExit('version.json recorded_at must include a UTC offset')
offset=recorded.strftime('%z')
OFFSET='UTC'+offset[:3]+':'+offset[3:]
zone_label={'-0800':'PST','-0700':'PDT'}.get(offset,OFFSET) if meta['timezone']=='America/Los_Angeles' else OFFSET
STAMP=recorded.strftime('%Y-%m-%d %H:%M:%S')+' '+zone_label

def write_artifact(path,content):
    if args.check:
        if not path.exists() or path.read_text(encoding='utf-8')!=content:
            raise SystemExit(f'Generated content is stale: {path.relative_to(REPO)}')
    else:
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(content,encoding='utf-8',newline='\n')

CONFIG={
'en':dict(file='en.md',out='index.html',html_lang='en',title='Research foundations & cognitive model hypothesis',menu='Contents',contents='CONTENTS',nav='Chapter navigation',sidebar='A study of artificial intelligence,<br>language, and cognition.',eyebrow='RESEARCH NOTES / PHILOSOPHY & COGNITION',subtitle='Studying AI, investigating cognition, and exploring language models.',tags=['Philosophical position',"Author’s hypothesis",'Scholarly context'],read='Reading mode',all='Full text',points='Key points',prose='Narrative',only_points='Key points only',only_prose='Narrative only',zoom='Enlarge ',view='View figure ↗',suggestion='Figure idea',intro='From innate mechanisms through experience, memory, and language, back to physiological responses and behavior.',close_toc='Close contents',figure_title='Conceptual figure · Scroll to explore',close_figure='Close figure',draft='Research document',back='Back to top ↑',history='Version history'),
'zh':dict(file='zh-CN.md',out='zh.html',html_lang='zh-CN',title='理论基础与认知模型假说',menu='目录',contents='CONTENTS / 阅读目录',nav='章节目录',sidebar='关于人工智能、语言<br>与认知机制的持续研究。',eyebrow='RESEARCH NOTES / 哲学与认知',subtitle='学习人工智能，研究认知机制，探索语言模型。',tags=['哲学立场','个人假说','学术参照'],read='阅读方式',all='完整阅读',points='要点',prose='连贯叙述',only_points='只看要点',only_prose='只看叙述',zoom='放大',view='查看大图 ↗',suggestion='插图设想',intro='从先天机制出发，循着经历、记忆与语言，回到具体的身体和行为。',close_toc='关闭目录',figure_title='概念图 · 可滚动查看',close_figure='关闭大图',draft='研究文档',back='返回开头 ↑',history='版本记录')
}

def render(s):
    output=parser.render(s.strip())
    def badge(m):
        label=m.group(1)
        lower=label.lower()
        cls='scholar' if ('学术' in label or 'scholarly' in lower) else 'imagine' if ('想象' in label or 'imagination' in lower or 'analogy' in lower) else 'hypothesis' if any(x in lower for x in ('假说','哲学','hypothesis','philosophical')) else 'neutral'
        return '<span class="tag '+cls+'">'+html.escape(label)+'</span>'
    output=re.sub(r'【([^【】<>]+)】',badge,output)
    for src,dst in LINK_TARGETS.items():
        output=output.replace('href="'+src+'"','href="'+dst+'"')
    output=output.replace('href="../../assets/', 'href="../assets/')
    return output

def language_switch(lang):
    return '<nav class="language-switch" aria-label="Language"><a class="language-link" href="index.html"'+(' aria-current="page"' if lang=='en' else '')+'>English</a><span class="divider">/</span><a class="language-link" href="zh.html"'+(' aria-current="page"' if lang=='zh' else '')+'>简体中文</a></nav>'

def build(lang):
    t=CONFIG[lang]
    md=(MDROOT/t['file']).read_text(encoding='utf-8')
    units=re.split(r'(?m)^(## (?:[一二三四五]|[1-5]) [^\n]*|### 5\.\d+[^\n]*)\n',md)
    content=[];nav=[];figures=[];counts={'points':0,'prose':0,'notes':0,'suggestions':0}
    for index in range(1,len(units),2):
        heading=units[index].lstrip('#').strip();text=units[index+1]
        ident='section-'+str((index+1)//2)
        is_sub=heading.startswith('5.');num,title=heading.split(' ',1)
        order={'一':'01','二':'02','三':'03','四':'04','五':'05','1':'01','2':'02','3':'03','4':'04','5':'05'}.get(num,num)
        nav.append((ident,order,title,is_sub));shared=[]
        def take_quote(m):
            q=m.group(0)
            if q.startswith('> **【学术释义') or q.lower().startswith('> **【scholarly note'):
                shared.append('<aside class="scholarly-note">'+render(q)+'</aside>');counts['notes']+=1;return ''
            if any(x in q for x in ('阅读说明','Reading guide','Reading note','How to read this page')):
                shared.append('<aside class="reading-note">'+render(q)+'</aside>');return ''
            return q
        text=re.sub(r'(?m)^>[^\n]*(?:\n>[^\n]*)*',take_quote,text)
        def take_figure(m):
            alt,src,caption=m.group(1),m.group(2),m.group(3) or ''
            path=(MDROOT/src).resolve()
            assert path.is_file(),path
            mime='image/svg+xml' if path.suffix.lower()=='.svg' else 'image/png'
            data='data:'+mime+';base64,'+base64.b64encode(path.read_bytes()).decode('ascii')
            figures.append(src)
            shared.append('<figure><button class="figure-button" type="button" aria-label="'+html.escape(t['zoom']+alt,quote=True)+'"><img src="'+data+'" alt="'+html.escape(alt,quote=True)+'"><span class="zoom-hint">'+t['view']+'</span></button><figcaption>'+render(caption)+'</figcaption></figure>')
            return ''
        text=re.sub(r'!\[([^\]]+)\]\(([^)]+)\)\s*\n(?:\n)?([^\n]+)?',take_figure,text)
        def take_placeholder(m):
            shared.append('<aside class="figure-note"><span>'+t['suggestion']+'</span><p>'+html.escape(m.group(1))+'</p></aside>');counts['suggestions']+=1;return ''
        text=re.sub(r'\[(?:建议插图：|Suggested figure:\s*)([^\]]+)\]',take_placeholder,text)
        splits=re.split(r'(?m)^#{3,4} (要点(?:版)?[^\n]*|(?:连贯)?叙述(?:版)?[^\n]*|Key points[^\n]*|Narrative[^\n]*)\n',text)
        prefix=splits[0]
        body='<div class="section-meta">'+render(prefix)+'</div>' if prefix.strip() else ''
        for pos in range(1,len(splits),2):
            kind='points' if splits[pos].startswith(('要点','Key points')) else 'prose'
            counts[kind]+=1
            body+='<div class="reading-part '+kind+'"><div class="part-label">'+t[kind]+'</div>'+render(splits[pos+1])+'</div>'
        if len(splits)==1 and not prefix.strip():body+='<p class="chapter-intro">'+t['intro']+'</p>'
        level='h3' if is_sub else 'h2'
        content.append('<section class="content-section '+('subsection' if is_sub else 'chapter')+'" id="'+ident+'"><header class="section-heading"><span class="section-number">'+order+'</span><'+level+'>'+html.escape(title)+'</'+level+'></header>'+body+''.join(shared)+'</section>')
    assert len(figures)==9,figures
    assert counts=={'points':16,'prose':16,'notes':4,'suggestions':0},counts
    nav_html=''.join('<a href="#'+ident+'" class="'+('sub' if sub else 'main')+'"><span>'+order+'</span><span>'+html.escape(title)+'</span></a>' for ident,order,title,sub in nav)
    page=f'''<!doctype html><html lang="{t['html_lang']}" class="html-{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Anyone's Intelligence · {t['title']} · {meta['version']}</title><link rel="stylesheet" href="./research.css?v=1.0.0"><meta name="theme-color" content="#080808"><meta name="description" content="{html.escape(t['subtitle'],quote=True)}"><link rel="canonical" href="{BASE_URL}research/{'zh.html' if lang=='zh' else ''}"><link rel="icon" href="../favicon.svg" type="image/svg+xml"></head><body data-mode="all" id="top">
<header class="topbar"><a class="brand" href="#top">Anyone's Intelligence</a><div class="top-actions"><a class="back-home" href="../{'zh.html' if lang=='zh' else ''}">{'项目首页' if lang=='zh' else 'Project home'}</a><a class="journal-link" href="../{'zh.html' if lang=='zh' else ''}#research-log">{'研究日志' if lang=='zh' else 'Research log'}</a>{language_switch(lang)}<button class="menu-button" type="button">{t['menu']} ☰</button></div></header><div class="progress"></div>
<div class="layout"><aside class="sidebar"><p class="sidebar-label">{t['contents']}</p><nav class="toc" aria-label="{t['nav']}">{nav_html}</nav><div class="sidebar-foot">{t['sidebar']}</div></aside>
<main class="document"><header class="hero"><p class="eyebrow">{t['eyebrow']}</p><h1>Anyone's<br>Intelligence</h1><p class="subtitle">{t['subtitle']}</p><div class="edition-line"><span class="version-chip">v{meta['version']}</span><time datetime="{meta['recorded_at']}">{STAMP}</time><a href="changelog.html">{t['history']} ↗</a></div><p class="timezone">America/Los_Angeles · UTC−08:00</p><div class="hero-foot">{''.join('<span>'+x+'</span>' for x in t['tags'])}</div></header>
<div class="reading-toolbar"><span class="toolbar-label">{t['read']}</span><div class="mode-switch" role="group" aria-label="{t['read']}"><button data-set-mode="all" aria-pressed="true">{t['all']}</button><button data-set-mode="points" aria-pressed="false">{t['only_points']}</button><button data-set-mode="prose" aria-pressed="false">{t['only_prose']}</button></div></div><article class="reading-body">{''.join(content)}</article><footer class="document-footer"><span>Anyone's Intelligence · {t['draft']} · {meta['version']}</span><a href="#top">{t['back']}</a></footer></main></div>
<dialog class="modal" id="toc-dialog"><div class="modal-head"><span>{t['menu']}</span><button class="close-button" data-close>{t['close_toc']}</button></div><nav class="toc">{nav_html}</nav></dialog><dialog class="modal zoom-modal" id="figure-dialog"><div class="modal-head"><span>{t['figure_title']}</span><button class="close-button" data-close>{t['close_figure']}</button></div><div class="zoom-content"></div></dialog><script src="./research.js?v=1.0.0" defer></script></body></html>'''
    page=page.replace('?v=1.0.0','?v='+meta['version'])
    page=page.replace('America/Los_Angeles · UTC−08:00',html.escape(meta['timezone']+' · '+OFFSET))
    write_artifact(OUT/t['out'],page)
    return {'language':lang,'file':t['out'],'figures':len(figures),**counts}

reports=[build(lang) for lang in ('en','zh')]
history='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Version history · Anyone\'s Intelligence</title><link rel="stylesheet" href="./research.css?v=1.0.0"></head><body><main class="document history" style="max-width:850px;margin:30px auto"><a href="./">Research document</a> · <a href="../">Project home</a>'+render((REPO/'CHANGELOG.md').read_text(encoding='utf-8'))+'</main></body></html>'
write_artifact(OUT/'changelog.html',history.replace('?v=1.0.0','?v='+meta['version']))
if args.check:
    def asset_files(root):
        return {p.relative_to(root):p for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc'}
    source_assets=asset_files(REPO/'assets')
    site_assets=asset_files(REPO/'site/assets')
    if source_assets.keys()!=site_assets.keys():
        raise SystemExit('Site asset file lists differ: rebuild missing files and remove obsolete site/assets copies after reviewing source deletions')
    for relative,source in source_assets.items():
        if source.read_bytes()!=site_assets[relative].read_bytes():
            raise SystemExit(f'Site asset is stale: {relative}')
else:
    shutil.copytree(REPO/'assets',REPO/'site/assets',dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
print(json.dumps(reports,ensure_ascii=False))
