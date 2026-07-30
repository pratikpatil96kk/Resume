#!/usr/bin/env python3
"""
Premium one-page Mainframe COBOL Developer resume (PDF).

Design constraints honoured:
  * modern typography, balanced spacing, clear professional hierarchy
  * clean ATS-friendly headings
  * NO graphics, NO tables, NO icons, NO text boxes, NO progress bars
  * fully machine-readable linear text (single text column)
"""
import os
import sys

from reportlab.lib.colors import Color, HexColor
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, Flowable, Frame, KeepTogether,
                                PageTemplate, Paragraph, Spacer)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import resume_content as C  # noqa: E402

# ---------------------------------------------------------------- fonts ----
FONT_DIR = "/usr/local/lib/python3.11/dist-packages/font_source_sans_pro/files"
FACES = {
    "SS": "SourceSansPro-Regular.ttf",
    "SS-Bd": "SourceSansPro-Bold.ttf",
    "SS-Sb": "SourceSansPro-Semibold.ttf",
    "SS-It": "SourceSansPro-It.ttf",
    "SS-Bk": "SourceSansPro-Black.ttf",
}
for name, fn in FACES.items():
    pdfmetrics.registerFont(TTFont(name, os.path.join(FONT_DIR, fn)))
pdfmetrics.registerFontFamily("SS", normal="SS", bold="SS-Bd", italic="SS-It",
                              boldItalic="SS-Bd")

# ---------------------------------------------------------------- palette --
INK = HexColor("#111418")     # body text
NAVY = HexColor("#0F2A47")    # name + section headings
SLATE = HexColor("#3C4A59")   # sub-headline / meta
RULE = HexColor("#0F2A47")
HAIR = Color(0.72, 0.76, 0.80)

BULLET = "\u2022"


# ------------------------------------------------------------- flowables ---
class TrackedText(Flowable):
    """One line of text drawn with letter-spacing (tracking). Real text -> ATS safe."""

    def __init__(self, text, font, size, tracking=0.0, color=INK,
                 align="left", leading=None, upper=False):
        Flowable.__init__(self)
        self.text = text.upper() if upper else text
        self.font, self.size, self.tracking = font, size, tracking
        self.color, self.align = color, align
        self.leading = leading or size * 1.16

    def wrap(self, aw, ah):
        self.aw = aw
        return aw, self.leading

    def _w(self):
        return (pdfmetrics.stringWidth(self.text, self.font, self.size)
                + self.tracking * max(len(self.text) - 1, 0))

    def draw(self):
        c = self.canv
        x = 0.0
        if self.align == "center":
            x = (self.aw - self._w()) / 2.0
        elif self.align == "right":
            x = self.aw - self._w()
        t = c.beginText(x, self.leading - self.size * 0.94)
        t.setFont(self.font, self.size)
        t.setFillColor(self.color)
        t.setCharSpace(self.tracking)
        t.textOut(self.text)
        c.drawText(t)


class SectionHeading(Flowable):
    """Uppercase tracked heading + hairline rule. ATS reads it as a plain text line."""

    def __init__(self, text, size, tracking, gap_above, gap_below, rule_gap):
        Flowable.__init__(self)
        self.text = text.upper()
        self.size, self.tracking = size, tracking
        self.gap_above, self.gap_below, self.rule_gap = gap_above, gap_below, rule_gap

    def wrap(self, aw, ah):
        self.aw = aw
        self.h = self.gap_above + self.size * 1.02 + self.rule_gap + self.gap_below
        return aw, self.h

    def draw(self):
        c = self.canv
        base = self.gap_below + self.rule_gap + self.size * 0.10
        t = c.beginText(0, base)
        t.setFont("SS-Bd", self.size)
        t.setFillColor(NAVY)
        t.setCharSpace(self.tracking)
        t.textOut(self.text)
        c.drawText(t)
        y = self.gap_below + self.rule_gap * 0.42
        c.setStrokeColor(RULE)
        c.setLineWidth(0.85)
        c.line(0, y, self.aw, y)


class RoleLine(Flowable):
    """Left title (bold) + right-aligned date on one baseline. No table used."""

    def __init__(self, left, right, size, lfont="SS-Bd", rfont="SS-Sb",
                 lcolor=INK, rcolor=SLATE, lead=None):
        Flowable.__init__(self)
        self.left, self.right = left, right
        self.size = size
        self.lfont, self.rfont = lfont, rfont
        self.lcolor, self.rcolor = lcolor, rcolor
        self.lead = lead or size * 1.22

    def wrap(self, aw, ah):
        self.aw = aw
        return aw, self.lead

    def draw(self):
        c = self.canv
        y = self.lead - self.size * 0.96
        c.setFont(self.lfont, self.size)
        c.setFillColor(self.lcolor)
        c.drawString(0, y, self.left)
        if self.right:
            c.setFont(self.rfont, self.size * 0.95)
            c.setFillColor(self.rcolor)
            c.drawRightString(self.aw, y, self.right)


class HeaderRule(Flowable):
    def __init__(self, gap_above, gap_below, width=1.1, color=RULE):
        Flowable.__init__(self)
        self.ga, self.gb, self.lw, self.color = gap_above, gap_below, width, color

    def wrap(self, aw, ah):
        self.aw = aw
        return aw, self.ga + self.gb + self.lw

    def draw(self):
        c = self.canv
        c.setStrokeColor(self.color)
        c.setLineWidth(self.lw)
        c.line(0, self.gb, self.aw, self.gb)


# ----------------------------------------------------------------- build ---
def build(path, s=1.0):
    """s = global scale used to auto-fit exactly one page."""
    PW, PH = A4
    LM = RM = 12.7 * mm      # 0.5in - ATS-safe standard minimum
    TM = 10.6 * mm
    BM = 9.0 * mm

    body = max(9.35 * s, 8.05)
    lead = body * 1.26

    st_sum = ParagraphStyle("sum", fontName="SS", fontSize=body, leading=lead,
                            textColor=INK, alignment=TA_JUSTIFY)
    st_bul = ParagraphStyle("bul", fontName="SS", fontSize=body, leading=lead,
                            textColor=INK, alignment=TA_JUSTIFY,
                            leftIndent=9.6 * s, bulletIndent=0,
                            bulletFontName="SS", bulletFontSize=body,
                            spaceAfter=2.35 * s)
    st_prj = ParagraphStyle("prj", fontName="SS", fontSize=body, leading=lead,
                            textColor=INK, alignment=TA_JUSTIFY,
                            leftIndent=9.6 * s, bulletIndent=0,
                            bulletFontName="SS", bulletFontSize=body,
                            spaceAfter=2.7 * s)
    st_skl = ParagraphStyle("skl", fontName="SS", fontSize=body, leading=lead * 0.985,
                            textColor=INK, alignment=TA_LEFT,
                            leftIndent=9.6 * s, bulletIndent=0,
                            bulletFontName="SS", bulletFontSize=body,
                            spaceAfter=1.95 * s)
    def f8(v):
        """Clamp a scaled font size to an 8pt ATS-readability floor."""
        return max(v, 8.05)

    st_meta = ParagraphStyle("meta", fontName="SS-It", fontSize=max(body * 0.985, 8.05),
                             leading=lead * 0.96, textColor=SLATE)

    F = []

    # ---------------- header ----------------
    F.append(TrackedText(C.NAME, "SS-Bk", 21.4 * s, tracking=2.05 * s,
                         color=NAVY, align="center", leading=22.6 * s))
    F.append(Spacer(1, 2.6 * s))
    F.append(TrackedText(C.HEADLINE, "SS-Sb", f8(9.25 * s), tracking=0.24 * s,
                         color=SLATE, align="center", leading=10.6 * s))
    F.append(Spacer(1, 2.9 * s))
    F.append(TrackedText("  |  ".join(C.CONTACT), "SS", f8(8.95 * s), tracking=0.06 * s,
                         color=INK, align="center", leading=10.2 * s))
    F.append(Spacer(1, 2.4 * s))
    F.append(TrackedText(C.TARGET_ROLE, "SS-Sb", f8(8.9 * s), tracking=0.10 * s,
                         color=NAVY, align="center", leading=9.8 * s))
    F.append(HeaderRule(0, 4.4 * s, width=1.15))

    def heading(t, first=False):
        return SectionHeading(t, 10.05 * s, 1.30 * s,
                              gap_above=(2.2 if first else 8.2) * s,
                              gap_below=4.0 * s,
                              rule_gap=3.0 * s)

    # ---------------- summary ----------------
    F.append(heading("Professional Summary", first=True))
    F.append(Paragraph(C.SUMMARY, st_sum))

    # ---------------- experience ----------------
    F.append(heading("Professional Experience"))
    for job in C.EXPERIENCE:
        F.append(RoleLine(job["role"], job["dates"], 10.35 * s, lead=11.9 * s))
        F.append(Spacer(1, 0.7 * s))
        F.append(Paragraph(f'{job["company"]}  |  {job["location"]}', st_meta))
        F.append(Spacer(1, 3.1 * s))
        for b in job["bullets"]:
            F.append(Paragraph(b, st_bul, bulletText=BULLET))

    # ---------------- projects ----------------
    F.append(heading("Key Projects"))
    for p in C.PROJECTS:
        txt = (f'<font name="SS-Bd">{p["name"]}</font> \u2014 {p["desc"]} '
               f'<font name="SS-Sb">Technologies:</font> <i>{p["tech"]}</i>.')
        F.append(Paragraph(txt, st_prj, bulletText=BULLET))

    # ---------------- skills ----------------
    F.append(heading("Technical Skills"))
    for label, items in C.SKILLS:
        F.append(Paragraph(f'<font name="SS-Bd">{label}:</font> {items}',
                           st_skl, bulletText=BULLET))

    # ---------------- achievements ----------------
    F.append(heading("Achievements"))
    for title, desc in C.ACHIEVEMENTS:
        F.append(Paragraph(f'<font name="SS-Bd">{title}</font> \u2014 {desc}',
                           st_prj, bulletText=BULLET))

    # ---------------- education ----------------
    F.append(heading("Education"))
    for i, e in enumerate(C.EDUCATION):
        if i:
            F.append(Spacer(1, 2.5 * s))
        F.append(RoleLine(e["degree"], e["dates"], 9.85 * s, lead=11.2 * s))
        F.append(Spacer(1, 0.5 * s))
        F.append(Paragraph(e["school"], st_meta))

    doc = BaseDocTemplate(path, pagesize=A4,
                          leftMargin=LM, rightMargin=RM,
                          topMargin=TM, bottomMargin=BM,
                          title="Pratik Shinde - Mainframe COBOL Developer Resume",
                          author="Pratik Shinde",
                          subject="Mainframe COBOL Developer | HP NonStop (Tandem) | "
                                  "Banking Payment Systems | L3 Production Support",
                          keywords=("COBOL, Mainframe, HP NonStop, HP Tandem, Guardian, TACL, TAL, "
                                    "ENFORM, DDL, SQL, SQLCI, DBUX, FUP, Enscribe, SQL/MP, NonStop SQL, "
                                    "TMF, EMS, OSS, Production Support, L3 Production Support, Banking, "
                                    "Financial Services, Payment Processing, SWIFT, SEPA, IBM MQ, RabbitMQ, "
                                    "SFTP, Incident Management, Root Cause Analysis, Application Maintenance, "
                                    "Application Enhancement, Enterprise Applications, Mission-Critical Systems, "
                                    "Performance Optimization, Java, REST APIs, Spring Boot, Microservices, "
                                    "Agile Scrum, SDLC"),
                          creator="Pratik Shinde")
    frame = Frame(LM, BM, PW - LM - RM, PH - TM - BM,
                  leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
                  id="body")
    doc.addPageTemplates([PageTemplate(id="resume", frames=[frame])])
    doc.build(F)


def pages(path):
    from pypdf import PdfReader
    return len(PdfReader(path).pages)


def min_font_pt(path):
    """Smallest rendered glyph size - ATS parsers penalise anything under 8pt."""
    import fitz
    pg = fitz.open(path)[0]
    return min(round(sp["size"], 2)
               for b in pg.get_text("dict")["blocks"] if b.get("lines")
               for l in b["lines"] for sp in l["spans"])


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "Pratik_Shinde_Mainframe_COBOL_Developer_Resume.pdf"
    lo, hi, best = 0.80, 1.16, None
    for _ in range(26):                       # binary search for the largest 1-page scale
        mid = (lo + hi) / 2
        build(out, mid)
        if pages(out) == 1:
            best, lo = mid, mid
        else:
            hi = mid
        if hi - lo < 0.0015:
            break
    if best is None:
        best = 0.80
    build(out, best)
    print(f"scale={best:.4f}  pages={pages(out)}  min_font={min_font_pt(out)}pt  -> {out}")
