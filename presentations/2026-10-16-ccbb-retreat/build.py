"""Build the CCBB Retreat 2026 AI-education deck (.pptx) from the CCBB template.

Usage:  python3 build.py [-o OUTPUT.pptx]

Slide content lives in slides.py; this file holds the drawing helpers and the
package assembly. Only the Python standard library is needed.
"""
import argparse, os, re, shutil, sys, tempfile, zipfile
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("-o", "--output", default=os.path.join(HERE, "output", "ccbb-retreat-2026-ai-education.pptx"))
args = ap.parse_args()
OUT = os.path.abspath(args.output)

# Unpack the template into a scratch folder; every build starts from the pristine template.
U = tempfile.mkdtemp(prefix="deck-build-")
with zipfile.ZipFile(os.path.join(HERE, "template", "ccbb-template.pptx")) as z:
    z.extractall(U)

EMU = 914400
def e(v): return str(int(round(v * EMU)))

RED, DARK, TXT, GRAY, CARD, RULE = "990000", "690304", "404041", "6B6B6C", "F3F1EF", "D9D4CF"
NS = ('xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
      'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"')

class Slide:
    def __init__(self):
        self.parts, self.nid, self.links = [], 2, []
    def id(self):
        self.nid += 1; return self.nid

def run(text, sz=None, b=False, color=None, i=False, link=None):
    a = ' lang="en-US"'
    if sz: a += f' sz="{int(sz*100)}"'
    if b: a += ' b="1"'
    if i: a += ' i="1"'
    inner = f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>' if color else ''
    if link: inner += f'<a:hlinkClick r:id="{link}"/>'
    return f'<a:r><a:rPr{a} dirty="0">{inner}</a:rPr><a:t>{escape(text, quote=False)}</a:t></a:r>'

def para(runs, align="l", bullet=False, after=0, lvl_marl=None, plain=True):
    if isinstance(runs, str): runs = [run(runs)]
    ppr = f'<a:pPr algn="{align}"'
    if bullet:
        ppr += ' marL="228600" indent="-228600"'
    elif plain:
        ppr += ' marL="0" indent="0"'
    ppr += '>'
    if after: ppr += f'<a:spcAft><a:spcPts val="{int(after*100)}"/></a:spcAft>'
    if bullet: ppr += f'<a:buClr><a:srgbClr val="{RED}"/></a:buClr><a:buFont typeface="Arial"/><a:buChar char="&#8226;"/>'
    elif plain: ppr += '<a:buNone/>'
    ppr += '</a:pPr>'
    return f'<a:p>{ppr}{"".join(runs)}</a:p>'

def body(paras, anchor="t", inset=(0.0, 0.0, 0.0, 0.0), autofit=False):
    l, t, r, b = inset
    fit = '<a:normAutofit/>' if autofit else ''
    return (f'<p:txBody><a:bodyPr wrap="square" lIns="{e(l)}" tIns="{e(t)}" rIns="{e(r)}" bIns="{e(b)}" anchor="{anchor}">{fit}</a:bodyPr>'
            f'<a:lstStyle/>{"".join(paras)}</p:txBody>')

def ph(s, kind, idx, paras, name="Placeholder"):
    attr = (f' type="{kind}"' if kind else '') + (f' idx="{idx}"' if idx is not None else '')
    s.parts.append(f'<p:sp><p:nvSpPr><p:cNvPr id="{s.id()}" name="{name} {s.nid}"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
                   f'<p:nvPr><p:ph{attr}/></p:nvPr></p:nvSpPr><p:spPr/><p:txBody><a:bodyPr/><a:lstStyle/>{"".join(paras)}</p:txBody></p:sp>')

def box(s, x, y, w, h, paras, fill=None, line=None, anchor="t", inset=None, geom="rect", name="TextBox"):
    fillx = f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill>' if fill else '<a:noFill/>'
    linex = f'<a:ln w="12700"><a:solidFill><a:srgbClr val="{line}"/></a:solidFill></a:ln>' if line else '<a:ln><a:noFill/></a:ln>'
    tx = ' txBox="1"' if not fill and geom == "rect" else ''
    if inset is None: inset = (0.15, 0.12, 0.15, 0.12) if fill else (0, 0, 0, 0)
    s.parts.append(f'<p:sp><p:nvSpPr><p:cNvPr id="{s.id()}" name="{name} {s.nid}"/><p:cNvSpPr{tx}/><p:nvPr/></p:nvSpPr>'
                   f'<p:spPr><a:xfrm><a:off x="{e(x)}" y="{e(y)}"/><a:ext cx="{e(w)}" cy="{e(h)}"/></a:xfrm>'
                   f'<a:prstGeom prst="{geom}"><a:avLst/></a:prstGeom>{fillx}{linex}</p:spPr>'
                   f'{body(paras, anchor, inset) if paras else body([para([run("")])])}</p:sp>')

def table(s, x, y, w, cols, rows, sz=14, rowh=0.36):
    grid = "".join(f'<a:gridCol w="{e(w*c)}"/>' for c in cols)
    trs = []
    for ri, row in enumerate(rows):
        hdr = ri == 0
        tcs = []
        for cell in row:
            fill = f'<a:solidFill><a:srgbClr val="{DARK if hdr else ("FFFFFF" if ri % 2 else CARD)}"/></a:solidFill>'
            ln = f'<a:lnB w="9525"><a:solidFill><a:srgbClr val="{RULE}"/></a:solidFill></a:lnB>'
            p = para([run(cell, sz, b=hdr, color="FFFFFF" if hdr else TXT)])
            tcs.append(f'<a:tc><a:txBody><a:bodyPr/><a:lstStyle/>{p}</a:txBody>'
                       f'<a:tcPr marL="{e(0.12)}" marR="{e(0.12)}" marT="{e(0.05)}" marB="{e(0.05)}" anchor="ctr">'
                       f'<a:lnL><a:noFill/></a:lnL><a:lnR><a:noFill/></a:lnR><a:lnT><a:noFill/></a:lnT>{ln}{fill}</a:tcPr></a:tc>')
        trs.append(f'<a:tr h="{e(rowh)}">{"".join(tcs)}</a:tr>')
    s.parts.append(f'<p:graphicFrame><p:nvGraphicFramePr><p:cNvPr id="{s.id()}" name="Table {s.nid}"/>'
                   f'<p:cNvGraphicFramePr><a:graphicFrameLocks noGrp="1"/></p:cNvGraphicFramePr><p:nvPr/></p:nvGraphicFramePr>'
                   f'<p:xfrm><a:off x="{e(x)}" y="{e(y)}"/><a:ext cx="{e(w)}" cy="{e(rowh*len(rows))}"/></p:xfrm>'
                   f'<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/table">'
                   f'<a:tbl><a:tblPr firstRow="1" bandRow="1"/><a:tblGrid>{grid}</a:tblGrid>{"".join(trs)}</a:tbl></a:graphicData></a:graphic></p:graphicFrame>')

def card(s, x, y, w, h, head, text, sz=14, hsz=16):
    ps = [para([run(head, hsz, b=True, color=RED)], after=4)]
    for t in ([text] if isinstance(text, str) else text):
        ps.append(para([run(t, sz, color=TXT)], after=2))
    box(s, x, y, w, h, ps, fill=CARD, name="Card")

def source(s, text):
    box(s, 1.3, 4.62, 7.8, 0.3, [para([run(text, 10, color=GRAY)])], name="Source")

def bullets(items, sz=15):
    return [para([run(t, sz, color=TXT)], bullet=True, after=5) for t in items]

def content(title, header="CCBB Retreat 2026"):
    s = Slide(); s.layout = "slideLayout6.xml"
    ph(s, "ctrTitle", None, [para([run(title)], plain=False)], "Title")
    ph(s, "body", 10, [para([run(header)], align="r", plain=False)], "Header")
    return s

def section(title, sub, layout="slideLayout4.xml"):
    s = Slide(); s.layout = layout
    ph(s, "title", None, [para([run(title)], plain=False)], "Title")
    ph(s, "body", 10, [para([run(sub)], plain=False)], "Subtitle")
    return s


# ---- slide content ----
exec(open(os.path.join(HERE, "slides.py"), encoding="utf-8").read())

# ---- package assembly ----
def read(p): return open(os.path.join(U, p), encoding="utf-8").read()
def write(p, x):
    os.makedirs(os.path.dirname(os.path.join(U, p)), exist_ok=True)
    open(os.path.join(U, p), "w", encoding="utf-8").write(x)

def add_from_layout(layout):
    """Register a new, empty slide that uses ppt/slideLayouts/<layout>; return its file name."""
    nums = [int(m.group(1)) for f in os.listdir(os.path.join(U, "ppt", "slides")) if (m := re.fullmatch(r"slide(\d+)\.xml", f))]
    name = f"slide{max(nums) + 1}.xml"
    write(f"ppt/slides/_rels/{name}.rels",
          '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
          f'<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/{layout}"/></Relationships>')
    write(f"ppt/slides/{name}", "")
    ct = read("[Content_Types].xml").replace("</Types>",
        f'<Override PartName="/ppt/slides/{name}" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/></Types>')
    write("[Content_Types].xml", ct)
    rels = read("ppt/_rels/presentation.xml.rels").replace("</Relationships>",
        f'<Relationship Id="rIdNew{name[5:-4]}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/{name}"/></Relationships>')
    write("ppt/_rels/presentation.xml.rels", rels)
    return name

order, notes_list = [], []
for s in slides:
    if isinstance(s, tuple):
        order.append(s[1]); notes_list.append((s[1], s[2])); continue
    fname = s.keep_src if getattr(s, "keep_src", None) else add_from_layout(s.layout)
    tree = "".join(p for p in s.parts if p)
    write(f"ppt/slides/{fname}",
          f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<p:sld {NS}><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
          f'<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>{tree}</p:spTree></p:cSld>'
          f'<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>')
    if s.links:
        rp = f"ppt/slides/_rels/{fname}.rels"
        x = read(rp).replace("</Relationships>", "".join(
            f'<Relationship Id="rIdLink{i+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" Target="{escape(u)}" TargetMode="External"/>'
            for i, u in enumerate(s.links)) + "</Relationships>")
        write(rp, x)
    order.append(fname); notes_list.append((fname, s.notes))

# speaker notes
ct = read("[Content_Types].xml")
for n, (fname, text) in enumerate(notes_list, 1):
    nf = f"notesSlide{n}.xml"
    paras = "".join(f'<a:p><a:r><a:rPr lang="en-US" dirty="0"/><a:t>{escape(l, quote=False)}</a:t></a:r></a:p>' if l else '<a:p><a:endParaRPr lang="en-US"/></a:p>'
                    for l in text.split("\n"))
    write(f"ppt/notesSlides/{nf}",
          f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<p:notes {NS}><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
          f'<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
          f'<p:sp><p:nvSpPr><p:cNvPr id="2" name="Slide Image Placeholder 1"/><p:cNvSpPr><a:spLocks noGrp="1" noRot="1" noChangeAspect="1"/></p:cNvSpPr><p:nvPr><p:ph type="sldImg"/></p:nvPr></p:nvSpPr><p:spPr/></p:sp>'
          f'<p:sp><p:nvSpPr><p:cNvPr id="3" name="Notes Placeholder 2"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr><p:ph type="body" idx="1"/></p:nvPr></p:nvSpPr><p:spPr/>'
          f'<p:txBody><a:bodyPr/><a:lstStyle/>{paras}</p:txBody></p:sp></p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:notes>')
    write(f"ppt/notesSlides/_rels/{nf}.rels",
          '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
          '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesMaster" Target="../notesMasters/notesMaster1.xml"/>'
          f'<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="../slides/{fname}"/></Relationships>')
    rp = f"ppt/slides/_rels/{fname}.rels"
    x = read(rp)
    x = re.sub(r'<Relationship [^>]*notesSlide[^>]*/>', '', x)
    x = x.replace("</Relationships>", f'<Relationship Id="rIdNotes" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide" Target="../notesSlides/{nf}"/></Relationships>')
    write(rp, x)
    ct = ct.replace("</Types>", f'<Override PartName="/ppt/notesSlides/{nf}" ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml"/></Types>')
write("[Content_Types].xml", ct)

# slide order
rels = read("ppt/_rels/presentation.xml.rels")
rid = {t: i for i, t in re.findall(r'Id="([^"]+)"[^>]*Target="slides/([^"]+)"', rels)}
pres = read("ppt/presentation.xml")
lst = "".join(f'<p:sldId id="{300 + k}" r:id="{rid[f]}"/>' for k, f in enumerate(order))
pres = re.sub(r"<p:sldIdLst>.*?</p:sldIdLst>", f"<p:sldIdLst>{lst}</p:sldIdLst>", pres, flags=re.S)
write("ppt/presentation.xml", pres)


os.makedirs(os.path.dirname(OUT), exist_ok=True)
if os.path.exists(OUT): os.remove(OUT)
with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
    z.write(os.path.join(U, "[Content_Types].xml"), "[Content_Types].xml")
    for root, _, files in os.walk(U):
        for f in files:
            full = os.path.join(root, f); arc = os.path.relpath(full, U)
            if arc != "[Content_Types].xml": z.write(full, arc)
shutil.rmtree(U, ignore_errors=True)
print("wrote", OUT, "slides:", len(order))
