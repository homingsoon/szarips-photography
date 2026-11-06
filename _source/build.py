"""
Build the portfolio as one static index.html.

Edit SITE, PHOTOS, CHAPTERS, HOME and GALLERY below, then run:
    python3 build.py meta.json ../site/index.html
meta.json comes from images.py (pixel sizes, available widths, average colour).
"""
import sys, json, html

meta = json.load(open(sys.argv[1]))
OUT = sys.argv[2]

# ---------------------------------------------------------------- site details
SITE = {
    "name": "Syarif Lazuardi",
    "aliases": ["Syarif Lazuardi", "Szarips", "Asaca Rei"],   # cycled under the portrait
    "email": "syariflazuardi02@gmail.com",
    "instagram": "@szarips",
    "instagram_url": "https://www.instagram.com/szarips/",
    "linkedin": "syarif-lazuardi",
    "linkedin_url": "https://www.linkedin.com/in/syarif-lazuardi",
    "year": "2026",
}

# ---------------------------------------------------------------- photographs
# chapter, plate title (descriptive only), optional exif line, optional date
PHOTOS = {
 "s01": ("theatre", "A single spot on the red floor"),
 "s02": ("theatre", "Hat, coat, and the house lights"),
 "s03": ("theatre", "The striped cane"),
 "s04": ("theatre", "Floral dress, close"),
 "s05": ("theatre", "Floral dress, the whole stage"),
 "s06": ("theatre", "Face to face"),
 "s07": ("theatre", "Duet, half in shadow"),
 "s08": ("theatre", "White lace, red shawl"),
 "s09": ("theatre", "Striped dress, waiting"),
 "s10": ("theatre", "Striped dress, reaching"),
 "s11": ("theatre", "One finger raised"),
 "s12": ("theatre", "The telephone"),
 "s13": ("theatre", "Warm light, laughing"),
 "s14": ("theatre", "Warm light, the kiss"),
 "s15": ("theatre", "Blue light, hands joined"),
 "c01": ("concert", "Glove, microphone, sequins"),
 "p01": ("costume", "Lace veil"),
 "p02": ("costume", "Red sleeve, gold pins"),
 "p03": ("costume", "Red hair, red hands"),
 "p04": ("costume", "Bandaged nurse, standing"),
 "p05": ("costume", "Bandaged nurse, arms raised"),
 "p06": ("costume", "Painted tears, striped sleeves"),
}
EXIF = {
 "c01": ("Canon EOS 700D", "18 mm  f/5.6  1/200 s  ISO 3200", "9 August 2026"),
 "p01": ("Canon EOS M50 Mark II", "28 mm  f/4.5  1/60 s  ISO 800", "30 October 2026"),
 "p02": ("Canon EOS M50 Mark II", "37 mm  f/5.6  1/60 s  ISO 800", "30 October 2026"),
 "p03": ("Canon EOS M50 Mark II", "28 mm  f/4.5  1/60 s  ISO 800", "30 October 2026"),
 "p04": ("Canon EOS M50 Mark II", "37 mm  f/5.6  1/60 s  ISO 800", "30 October 2026"),
 "p05": ("Canon EOS M50 Mark II", "27 mm  f/4.5  1/60 s  ISO 800", "30 October 2026"),
 "p06": ("Fujifilm X-A3", "25.6 mm  f/10  1/50 s  ISO 1000", ""),
}
CHAPTERS = {
 "theatre": ("I", "Theatre", "Actors on stage, lit by a single spot or a warm wash. Low light, black around every figure, the gesture held for a second.", "2026"),
 "concert": ("II", "Concert", "A singer at the microphone, the hall dark behind him.", "August 2026"),
 "costume": ("III", "Costume", "Portraits of people who came dressed as someone else: lace, gold pins, bandages and stage blood.", ""),
}

# ---------------------------------------------------------------- sequences
# A spread is a list of placements on a 12-column grid.
#   ("img", id, "colstart / colend", align, top-offset, mobile)
#   ("pair", [id, id], "colstart / colend", align, top-offset)   equal-height diptych
#   ("text", chapter, "colstart / colend", align)                 chapter opener
# align: start | end | center   offset: CSS length pushed down on desktop
# mobile: full | l | r | s  (width & side on phones)
HOME = [
  [("img","s01","5 / 10","start","0","full")],
  [("img","s15","2 / 6","start","0","l"), ("img","p02","8 / 12","start","14vw","r")],
  [("img","s04","3 / 12","start","0","full")],
  [("pair",["s13","s14"],"1 / 10","start","0")],
  [("img","s02","1 / 8","end","0","full"), ("img","s12","9 / 12","end","0","r")],
  [("img","p05","5 / 13","start","0","full")],
]
GALLERY = {
 "theatre": [
  [("img","s01","2 / 8","start","0","full"), ("text","theatre","9 / 13","end")],
  [("pair",["s02","s03"],"1 / 13","start","0")],
  [("img","s04","1 / 8","start","0","full"), ("img","s05","9 / 13","end","0","r")],
  [("pair",["s06","s07"],"4 / 12","start","0")],
  [("img","s08","8 / 12","start","0","l")],
  [("img","s09","1 / 9","end","0","full"), ("img","s10","10 / 13","start","0","r")],
  [("pair",["s11","s12"],"2 / 9","start","0")],
  [("pair",["s13","s14"],"1 / 13","start","0")],
  [("img","s15","5 / 10","start","0","s")],
 ],
 "concert": [
  [("text","concert","1 / 4","start"), ("img","c01","4 / 13","start","0","full")],
 ],
 "costume": [
  [("pair",["p01","p02"],"1 / 9","start","0"), ("text","costume","10 / 13","end")],
  [("img","p06","3 / 11","start","0","full")],
  [("img","p04","1 / 5","start","0","l"), ("img","p05","6 / 13","end","0","full")],
  [("img","p03","2 / 9","start","0","full")],
 ],
}

# plate numbers follow the gallery sequence
ORDER = []
for ch in GALLERY.values():
    for spread in ch:
        for it in spread:
            if it[0] == "img": ORDER.append(it[1])
            elif it[0] == "pair": ORDER.extend(it[1])
assert sorted(ORDER) == sorted(PHOTOS), "every photograph must appear exactly once"
PLATE = {k: i + 1 for i, k in enumerate(ORDER)}

E = html.escape
MAXW = 1440  # content width in px

def span(cols):
    a, b = [int(x) for x in cols.split("/")]
    return b - a

def picture(pid, vw_frac, eager=False, cls=""):
    m = meta[pid]
    srcset = ", ".join(f"assets/img/{pid}-{w}.webp {w}w" for w in m["widths"])
    px = round(MAXW * vw_frac)
    sizes = f"(max-width: 760px) 92vw, min({vw_frac*100:.1f}vw, {px}px)"
    small = m["widths"][1] if len(m["widths"]) > 1 else m["widths"][0]
    chapter, title = PHOTOS[pid]
    alt = f"{title}. {CHAPTERS[chapter][1]}, plate {PLATE[pid]}."
    load = 'fetchpriority="high" decoding="async"' if eager else 'loading="lazy" decoding="async"'
    return (f'<img class="ph {cls}" src="assets/img/{pid}-{small}.webp" srcset="{srcset}" sizes="{sizes}" '
            f'width="{m["w"]}" height="{m["h"]}" alt="{E(alt)}" {load} '
            f'style="--c:{m["color"]}">')

def figure(pid, vw_frac, eager=False):
    chapter, title = PHOTOS[pid]
    return (f'<figure class="plate" data-id="{pid}">'
            f'<button class="open" type="button" aria-label="View plate {PLATE[pid]}, {E(title)}">'
            f'{picture(pid, vw_frac, eager)}</button>'
            f'<figcaption><span class="no">{PLATE[pid]}</span><span class="t">{E(title)}</span></figcaption>'
            f'</figure>')

def ratio(pid):
    return meta[pid]["w"] / meta[pid]["h"]

def spread_html(spread):
    out = []
    for it in spread:
        kind = it[0]
        if kind == "img":
            _, pid, cols, align, off, mob = it
            style = f"grid-column:{cols};--al:{align};--off:{off}"
            out.append(f'<div class="cell" data-m="{mob}" style="{style}">{figure(pid, span(cols)/12)}</div>')
        elif kind == "pair":
            _, ids, cols, align, off = it
            total = sum(ratio(i) for i in ids)
            inner = "".join(
                f'<div class="pi" style="flex:{ratio(i):.4f} 1 0">{figure(i, span(cols)/12*ratio(i)/total)}</div>'
                for i in ids)
            out.append(f'<div class="cell pair" style="grid-column:{cols};--al:{align};--off:{off}">{inner}</div>')
        elif kind == "text":
            _, ch, cols, align = it
            num, name, desc, when = CHAPTERS[ch]
            count = sum(1 for p in PHOTOS.values() if p[0] == ch)
            out.append(
                f'<header class="cell chapter-head" style="grid-column:{cols};--al:{align}">'
                f'<p class="num">{num}</p><h2>{name}</h2><p class="desc">{E(desc)}</p>'
                f'<p class="meta">{count} {"photograph" if count == 1 else "photographs"}{", " + when if when else ""}</p></header>')
    return f'<div class="spread">{"".join(out)}</div>'

# ---------------------------------------------------------------- views
home_spreads = "\n".join(spread_html(s) for s in HOME)

chapter_index = []
for ch, (num, name, desc, when) in CHAPTERS.items():
    ids = [p for p in ORDER if PHOTOS[p][0] == ch]
    thumbs = "".join(f'<span class="th">{picture(i, 0.08)}</span>' for i in ids[:5])
    chapter_index.append(
        f'<li><a href="#gallery" data-filter="{ch}"><span class="num">{num}</span>'
        f'<span class="name">{name}</span><span class="cnt">{len(ids)}</span>'
        f'<span class="strip" aria-hidden="true">{thumbs}</span></a></li>')

gallery_chapters = []
for ch, spreads in GALLERY.items():
    gallery_chapters.append(
        f'<section class="chapter" data-chapter="{ch}" aria-label="{CHAPTERS[ch][1]}">'
        + "\n".join(spread_html(s) for s in spreads) + '</section>')

index_items = "".join(
    f'<li data-chapter="{PHOTOS[p][0]}" style="--r:{ratio(p):.4f}"><button class="open" type="button" data-id="{p}" '
    f'aria-label="View plate {PLATE[p]}, {E(PHOTOS[p][1])}">{picture(p, 0.12)}</button>'
    f'<span class="no">{PLATE[p]}</span></li>' for p in ORDER)

counts = {ch: sum(1 for p in PHOTOS.values() if p[0] == ch) for ch in CHAPTERS}
filters = (f'<button type="button" class="f is-on" data-f="all" aria-pressed="true">All <sup>{len(ORDER)}</sup></button>'
           + "".join(f'<button type="button" class="f" data-f="{ch}" aria-pressed="false">{CHAPTERS[ch][1]} <sup>{counts[ch]}</sup></button>'
                     for ch in CHAPTERS))

# data for the viewer
VIEW = []
for p in ORDER:
    ch, title = PHOTOS[p]
    m = meta[p]
    cam, exp, date = EXIF.get(p, ("", "", ""))
    VIEW.append({"id": p, "n": PLATE[p], "t": title, "ch": CHAPTERS[ch][1], "c": ch,
                 "src": f"assets/img/{p}-{m['widths'][-1]}.webp",
                 "mid": f"assets/img/{p}-{m['widths'][1] if len(m['widths'])>1 else m['widths'][0]}.webp",
                 "w": m["w"], "h": m["h"], "cam": cam, "exp": exp.replace("  ", "\u2002"), "date": date or CHAPTERS[ch][3] or ""})

S = SITE
insta = ""
if S.get("instagram"):
    insta += f'<div class="row"><dt>Instagram</dt><dd><a href="{E(S["instagram_url"])}" rel="noopener" target="_blank">{E(S["instagram"])}</a></dd></div>'
if S.get("linkedin"):
    insta += f'<div class="row"><dt>LinkedIn</dt><dd><a href="{E(S["linkedin_url"])}" rel="noopener" target="_blank">{E(S["linkedin"])}</a></dd></div>'

pm = meta["me"]
portrait = (f'<img class="me" src="assets/img/me-{pm["widths"][0]}.webp" '
            f'srcset="{", ".join(f"assets/img/me-{w}.webp {w}w" for w in pm["widths"])}" '
            f'sizes="(max-width: 760px) 52vw, 250px" width="{pm["w"]}" height="{pm["h"]}" '
            f'alt="Portrait of {E(S["name"])}" fetchpriority="high" decoding="async" style="--c:{pm["color"]}">')
names = "".join(f'<span class="nm">{E(n)}</span>' for n in S["aliases"])
names_label = S["aliases"][0] + (", also known as " + " and ".join(S["aliases"][1:]) if len(S["aliases"]) > 1 else "")

tpl = open(sys.argv[3] if len(sys.argv) > 3 else "template.html").read()
page = (tpl.replace("{{NAME}}", E(S["name"]))
           .replace("{{EMAIL}}", E(S["email"]))
           .replace("{{YEAR}}", S["year"])
           .replace("{{INSTA}}", insta)
           .replace("{{TOTAL}}", str(len(ORDER)))
           .replace("{{PORTRAIT}}", portrait)
           .replace("{{NAMES}}", names)
           .replace("{{NAMES_LABEL}}", E(names_label))
           .replace("{{ALIASES_TEXT}}", E(" and ".join(S["aliases"][1:])))
           .replace("{{HOME_SPREADS}}", home_spreads)
           .replace("{{CHAPTER_INDEX}}", "".join(chapter_index))
           .replace("{{FILTERS}}", filters)
           .replace("{{GALLERY}}", "\n".join(gallery_chapters))
           .replace("{{INDEX}}", index_items)
           .replace("{{ABOUT_IMG}}", figure("s08", 0.3))
           .replace("{{VIEWDATA}}", json.dumps(VIEW, separators=(",", ":"))))
open(OUT, "w").write(page)
print("wrote", OUT, len(page)//1024, "KB;", len(ORDER), "plates")
