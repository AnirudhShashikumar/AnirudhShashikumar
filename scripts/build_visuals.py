"""Build the local V2 visual system. Standard-library only; no network or raster assets."""
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PALETTES = {
    'dark': dict(bg='#09121e', panel='#101f30', inset='#0c1927', ink='#eff5fb', muted='#a4b8cc', border='#30465d', grid='#20374e', cyan='#71e3e5', blue='#88b5ff', violet='#b6a8f5', trace='#456b89'),
    'light': dict(bg='#f5f8fc', panel='#eaf1f7', inset='#ffffff', ink='#142a42', muted='#506982', border='#bdcddd', grid='#d3e0eb', cyan='#006f80', blue='#245fae', violet='#7151aa', trace='#8aa6bc'),
}

def text(x, y, value, size=16, fill='var(--ink)', weight=400, mono=False, **attrs):
    family = 'ui-monospace,Consolas,monospace' if mono else 'Arial,Helvetica,sans-serif'
    extra = ''.join(f' {key.rstrip("_").replace("_", "-")}="{escape(str(val), quote=True)}"' for key, val in attrs.items())
    return f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{fill}"{extra}>{escape(value)}</text>'

def rect(x,y,w,h,fill='var(--panel)',stroke='var(--border)',r=10,**attrs):
    extra=''.join(f' {k.rstrip("_").replace("_", "-")}="{v}"' for k,v in attrs.items())
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}"{extra}/>'

def path(d,stroke='var(--trace)',fill='none',**attrs):
    extra=''.join(f' {k.rstrip("_").replace("_", "-")}="{v}"' for k,v in attrs.items())
    return f'<path d="{d}" stroke="{stroke}" fill="{fill}"{extra}/>'

def circle(x,y,r=3,fill='var(--cyan)',**attrs):
    extra=''.join(f' {k.rstrip("_").replace("_", "-")}="{v}"' for k,v in attrs.items())
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"{extra}/>'

def document(w,h,title,description,body,theme='dark',css='',defs=''):
    colors=''.join(f'--{k}:{v};' for k,v in PALETTES[theme].items())
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>
<defs>{defs}</defs>
<style>:root{{{colors}}}{css}@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>
{body}
</svg>\n'''

def frame(w,h,grid=False):
    body=rect(.5,.5,w-1,h-1,'var(--bg)',r=16)
    if grid:
        body+=rect(1,1,w-2,h-2,'url(#grid)','none',15)
    return body

GRID='<pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" fill="none" stroke="var(--grid)" stroke-opacity=".35" stroke-width=".5"/></pattern>'

SIGNAL_CSS='''
.packet{stroke-dasharray:2 98;stroke-dashoffset:100;animation:packet 16s linear infinite}
.reply{animation-delay:-8s;stroke:var(--violet)}
.node{animation:node 8s ease-in-out infinite}.late{animation-delay:-3s}
@keyframes packet{0%,12%{stroke-dashoffset:100;opacity:0}18%{opacity:1}65%{stroke-dashoffset:0;opacity:1}75%,100%{stroke-dashoffset:0;opacity:0}}
@keyframes node{0%,100%{opacity:.45}45%,60%{opacity:1}}
'''

def hero(mobile=False,theme='dark'):
    w,h=(480,360) if mobile else (960,324)
    b=frame(w,h,True)
    b+=path('M28 30h10v10h10v-10h10','var(--cyan)',stroke_width=2)
    b+=text(70,39,'RESEARCH → PRODUCTION',12 if mobile else 13,'var(--muted)',mono=True,letter_spacing=1.3)
    if mobile:
        b+=text(26,105,'ANIRUDH',43,weight=700,letter_spacing=-1)
        b+=text(26,154,'SHASHIKUMAR',43,weight=700,letter_spacing=-1)
        b+=text(28,194,'Engineering the Next Era of AI.',24,'var(--cyan)')
        b+=text(28,234,'AI / ML · COMPUTER VISION',16,'var(--muted)',mono=True)
        b+=text(28,260,'FULL-STACK · RESEARCH',16,'var(--muted)',mono=True)
        b+=path('M28 282H452','var(--border)')
        b+=text(28,310,'OBSERVE → REASON → BUILD',14,'var(--cyan)',mono=True)
        b+=text(28,337,'VALIDATE → DEPLOY',14,'var(--muted)',mono=True)
        b+=text(452,337,'BENGALURU',11,'var(--muted)',mono=True,text_anchor='end')
        points=[(379,32),(409,53),(450,26),(446,81),(390,85)]
        route='M379 32 409 53 450 26 446 81 390 85 409 53'
        b+=path(route,stroke_opacity=.6)
        b+=path(route,'var(--cyan)',pathLength=100,stroke_width=2,class_='packet')
        for i,(x,y) in enumerate(points):b+=circle(x,y,2.6,class_='node late' if i%2 else 'node')
        css=SIGNAL_CSS
    else:
        b+=text(924,39,'ANIRUDH.SH / ENGINEERING',10,'var(--muted)',mono=True,text_anchor='end',letter_spacing=1)
        b+=text(32,116,'ANIRUDH SHASHIKUMAR',41,weight=700,letter_spacing=-1.1)
        b+=text(34,165,'Engineering the Next Era of AI.',28,'var(--cyan)')
        b+=text(34,207,'AI / ML · COMPUTER VISION',14,'var(--muted)',mono=True,letter_spacing=1.2)
        b+=text(34,233,'FULL-STACK · RESEARCH',14,'var(--muted)',mono=True,letter_spacing=1.2)
        # A directed network: observations converge, then fan out to system outputs.
        b+='<g id="intelligence-network">'
        b+=circle(774,150,104,'none',stroke='var(--border)',stroke_dasharray='2 8')
        b+='<g class="orbital">'+path('M670 150a104 104 0 0 1 132-100','var(--cyan)',stroke_opacity=.7)+circle(802,50,3)+'</g>'
        b+=path('M662 242 901 65','var(--grid)',stroke_dasharray='3 8')
        routes=['M657 107 717 83 774 149 838 115 895 148','M668 195 722 218 774 149 839 210 895 148','M657 107 720 149 668 195','M717 83 838 115 839 210 722 218']
        for r in routes:b+=path(r,'var(--trace)')
        b+=path(routes[0],'var(--cyan)',pathLength=100,stroke_width=2.2,class_='packet')
        b+=path(routes[1],'var(--violet)',pathLength=100,stroke_width=2.2,class_='packet reply')
        for i,(x,y) in enumerate([(657,107),(717,83),(774,149),(838,115),(895,148),(668,195),(722,218),(839,210),(720,149)]):
            b+=circle(x,y,4 if i==2 else 3.2,'var(--cyan)' if i<5 else 'var(--blue)',class_='node late' if i%2 else 'node')
        b+=circle(774,149,18,'var(--inset)',stroke='var(--cyan)')
        b+=path('M766 149h16M774 141v16','var(--cyan)',stroke_width=1.5)
        b+=text(646,66,'INPUT',10,'var(--muted)',mono=True)
        b+=text(906,234,'INFERENCE',10,'var(--muted)',mono=True,text_anchor='end')
        b+=path('M661 68v177','var(--cyan)',stroke_opacity=.17,class_='scanner')
        b+='</g>'
        b+=path('M34 267H926','var(--border)')
        for i,label in enumerate(['OBSERVE','REASON','BUILD','VALIDATE','DEPLOY']):
            x=34+i*148
            b+=text(x,298,f'0{i+1}',10,'var(--muted)',mono=True)
            b+=text(x+24,298,label,12,'var(--cyan)' if i==0 else 'var(--muted)',mono=True,letter_spacing=.6)
            if i<4:b+=path(f'M{x+118} 294h14','var(--trace)')
        b+=text(926,298,'BENGALURU, IN',10,'var(--muted)',mono=True,text_anchor='end')
        css=SIGNAL_CSS+'''.orbital{transform-origin:774px 150px;animation:orbit 48s linear infinite}.scanner{animation:scan 18s ease-in-out infinite alternate}@keyframes orbit{to{transform:rotate(360deg)}}@keyframes scan{to{transform:translateX(234px)}}'''
    return document(w,h,'Anirudh Shashikumar — Engineering the Next Era of AI.','Research to production: observe, reason, build, validate, deploy. AI / ML, computer vision, full-stack, research. Decorative intelligence network; no live-status claims.',b,theme,css,GRID)


def sensor(x,y):
    b=rect(x,y,48,48,'var(--inset)','var(--trace)',4)
    b+=path(f'M{x+3} {y+30}l13-22 9 31 12-24 8 19','var(--trace)',stroke_width=5)
    b+=path(f'M{x+13} {y+4}l15 16-8 13 16 12','var(--cyan)',stroke_width=1.2)
    return b

def core(x,y):
    b=path(f'M{x+4} {y+6}l39 17-39 18 17-18 22-17M{x+4} {y+6}l17 17 22 18','var(--trace)')
    for i,(dx,dy) in enumerate([(4,6),(4,41),(21,23),(43,6),(43,41)]):b+=circle(x+dx,y+dy,3,'var(--blue)' if i%2 else 'var(--cyan)')
    return b

def evidence(x,y):
    b=rect(x,y,48,48,'var(--inset)','var(--trace)',4)
    b+=path(f'M{x+7} {y+16}v-8h9m17 0h8v8m0 17v8h-8m-17 0H{x+7}v-8','var(--cyan)',stroke_width=1.4)
    b+=path(f'M{x+15} {y+25}l7 7 13-17','var(--cyan)',stroke_width=1.5)
    return b


def satquery(mobile=False,theme='dark'):
    w,h=(480,324) if mobile else (960,250)
    b=frame(w,h)
    b+=path('M1 43V16Q1 1 16 1H220','var(--cyan)',stroke_width=2)
    b+=text(24 if mobile else 32,31,'PROJECT://01 · CURRENT MISSION',12,'var(--cyan)',mono=True,letter_spacing=.5)
    b+=text(24 if mobile else 30,76,'SatQuery AI',35,weight=700)
    if not mobile:b+=text(928,31,'WORKFLOW SCHEMATIC',10,'var(--muted)',mono=True,text_anchor='end')
    stages=[('OBSERVE','SAR + optical','Sentinel-1 / Sentinel-2',sensor),('ANALYZE','Intelligence core','VQA / fusion / temporal',core),('INVESTIGATE','Spatial evidence','Grounding / change',evidence)]
    for i,(label,name,detail,icon) in enumerate(stages):
        if mobile:
            x,y,cw,ch=24,94+i*74,432,62
            b+=rect(x,y,cw,ch,'var(--panel)',r=8)+icon(x+10,y+7)
            b+=text(x+74,y+23,f'0{i+1} / {label}',12,'var(--cyan)',mono=True)
            b+=text(x+74,y+48,name,22,weight=600)
            if i<2:
                d=f'M{x+34} {y+63}v10'
                b+=path(d)+path(d,'var(--cyan)',pathLength=100,stroke_width=2,class_='packet')
        else:
            x,y,cw,ch=32+i*314,110,268,103
            b+=rect(x,y,cw,ch,'var(--panel)',r=8)+icon(x+14,y+26)
            b+=text(x+78,y+27,f'0{i+1} / {label}',11,'var(--cyan)',mono=True)
            b+=text(x+78,y+53,name,19,weight=600)
            b+=text(x+78,y+78,detail,12,'var(--muted)')
            if i<2:
                d=f'M{x+269} {y+51}h44'
                b+=path(d)+path(d,'var(--cyan)',pathLength=100,stroke_width=2,class_='packet reply' if i else 'packet')
    if not mobile:b+=text(32,236,'FROM OBSERVATION TO EVIDENCE',10,'var(--muted)',mono=True,letter_spacing=1)
    return document(w,h,'SatQuery AI: observe, analyze, investigate.','Schematic satellite inputs pass through an intelligence core to spatial evidence. These are abstract diagrams, not real sensor imagery, model output, or benchmark results.',b,theme,SIGNAL_CSS)


def project_map(mobile=False,theme='dark'):
    w,h=(480,340) if mobile else (960,268)
    b=frame(w,h)
    if mobile:
        cx,cy=240,170
        cards=[(16,18,'01','SatQuery AI','Remote sensing'),(250,18,'03','MediFit','Applied AI'),(16,238,'04','Gesture Globe','Vision × interaction'),(250,238,'02','Dayflow','Full-stack systems')]
        cw,ch=214,84
    else:
        cx,cy=480,134
        cards=[(28,26,'01','SatQuery AI','Remote sensing intelligence'),(648,26,'03','MediFit','Applied AI / health insights'),(28,160,'04','Gesture Globe','Vision × interaction'),(648,160,'02','Dayflow','Full-stack systems')]
        cw,ch=284,82
    for i,(x,y,num,name,domain) in enumerate(cards):
        startx=x+cw/2 if mobile else (x+cw if x<cx else x)
        starty=y+ch if y<cy else y
        if not mobile:starty=y+ch/2
        d=f'M{startx} {starty}Q{cx} {starty} {cx} {cy}'
        b+=path(d)
        if i<2:b+=path(d,'var(--cyan)' if i==0 else 'var(--violet)',pathLength=100,stroke_width=1.6,class_='packet reply' if i else 'packet')
    b+=circle(cx,cy,25 if mobile else 33,'var(--panel)',stroke='var(--cyan)',stroke_width=1)
    b+=text(cx,cy+5,'R → P',13 if mobile else 16,'var(--cyan)',mono=True,text_anchor='middle')
    if not mobile:
        b+=text(cx,43,'RESEARCH + AI',11,'var(--muted)',mono=True,text_anchor='middle')
        b+=text(cx,236,'INTERACTION + SYSTEMS',11,'var(--muted)',mono=True,text_anchor='middle')
    for x,y,num,name,domain in cards:
        b+=rect(x,y,cw,ch,'var(--panel)',r=8)
        b+=text(x+14,y+23,num,11,'var(--cyan)',mono=True)
        b+=text(x+43,y+30,name,21 if mobile else 23,weight=600)
        b+=text(x+14,y+61,domain,14 if mobile else 15,'var(--muted)')
    return document(w,h,'Project constellation: four systems, one engineering practice.','SatQuery AI connects research and remote sensing; MediFit connects AI and health interfaces; Gesture Globe connects vision and interaction; Dayflow connects backend and product engineering. This is a conceptual map, not an expertise score.',b,theme,SIGNAL_CSS)


def pipeline(mobile=False,theme='dark'):
    w,h=(480,332) if mobile else (960,180)
    b=frame(w,h)
    stages=[('PERCEPTION',['Computer vision · Deep learning','Remote sensing']),('GENERATION',['Transformers · Generative models','Image-to-image translation']),('REASONING',['Multimodal AI · Evidence fusion','Temporal understanding']),('DEPLOYMENT',['Inference APIs · Evaluation','AI-assisted engineering'])]
    for i,(label,topics) in enumerate(stages):
        if mobile:
            x,y=24,32+i*76
            if i<3:b+=path(f'M{x+14} {y+7}v57','var(--trace)')
            b+=circle(x+14,y-3,13,'var(--panel)',stroke='var(--cyan)')
            b+=text(x+14,y+1,str(i+1),11,'var(--cyan)',mono=True,text_anchor='middle')
            b+=text(x+44,y+2,label,19,weight=600)
            for j,t in enumerate(topics):b+=text(x+44,y+25+j*20,t,16,'var(--muted)')
        else:
            x,y=26+i*234,31
            b+=circle(x+12,y,12,'var(--panel)',stroke='var(--cyan)')
            b+=text(x+12,y+4,str(i+1),11,'var(--cyan)',mono=True,text_anchor='middle')
            if i<3:b+=path(f'M{x+35} {y}h178','var(--trace)')
            b+=text(x,y+47,label,19,weight=600)
            # Explicit line breaks retain readable widths without SVG foreignObject.
            a=topics[0].split(' · ')
            for j,t in enumerate(a+[topics[1]]):b+=text(x,y+76+j*21,t,14,'var(--muted)')
    return document(w,h,'Research pipeline: perception, generation, reasoning, deployment.','Technical interests: computer vision, deep learning, remote sensing; transformers, generative models, image-to-image translation; multimodal AI, evidence fusion, temporal understanding; inference APIs, evaluation, AI-assisted engineering.',b,theme)


def divider():
    b=path('M0 10H405l10-5h45l10 5H960','#476b80',stroke_opacity=.4)
    b+=path('M0 10H405l10-5h45l10 5H960','#4eabb7',pathLength=100,stroke_width=1.8,class_='packet')
    return document(960,20,'Signal trace','Decorative section divider.',b,'dark',SIGNAL_CSS)


def build():
    assets=ROOT/'assets'
    for stem,render in [('hero-v2',hero),('satquery-v2',satquery),('project-map',project_map),('research-pipeline',pipeline)]:
        for mobile in [False,True]:
            for theme in ['dark','light']:
                name=stem+('-mobile' if mobile else '')+('-light' if theme=='light' else '')+'.svg'
                (assets/name).write_text(render(mobile,theme))
    (assets/'divider.svg').write_text(divider())
    print('Generated 17 native SVG compositions; contribution files were not touched.')

if __name__=='__main__':build()
