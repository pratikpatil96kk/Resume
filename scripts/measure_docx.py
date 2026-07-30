#!/usr/bin/env python3
"""
Estimate the rendered height of the DOCX in Word.

Uses Carlito, which is metric-compatible with Calibri, so line-wrap counts and
therefore total page height closely match Microsoft Word / LibreOffice output.
"""
import os
import sys

from docx import Document
from docx.shared import Pt
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

CF = "/tmp/carlfonts"
pdfmetrics.registerFont(TTFont("Cal", f"{CF}/Carlito-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Cal-B", f"{CF}/Carlito-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Cal-I", f"{CF}/Carlito-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Cal-BI", f"{CF}/Carlito-BoldItalic.ttf"))

EMU_PT = 12700.0


def face(bold, italic):
    return {(0, 0): "Cal", (1, 0): "Cal-B", (0, 1): "Cal-I", (1, 1): "Cal-BI"}[
        (int(bool(bold)), int(bool(italic)))]


def measure(path):
    doc = Document(path)
    sec = doc.sections[0]
    page_h = sec.page_height / EMU_PT
    usable_w = (sec.page_width - sec.left_margin - sec.right_margin) / EMU_PT
    usable_h = page_h - (sec.top_margin + sec.bottom_margin) / EMU_PT

    total = 0.0
    for p in doc.paragraphs:
        pf = p.paragraph_format
        li = (pf.left_indent.pt if pf.left_indent else 0)
        avail = usable_w - li
        # bullet glyph + tab occupy roughly the hanging indent, already netted out
        segs = []
        maxsz = 0.0
        for r in p.runs:
            sz = (r.font.size.pt if r.font.size else 9.5)
            maxsz = max(maxsz, sz)
            segs.append((r.text, face(r.font.bold, r.font.italic), sz))
        if not segs:
            maxsz = 9.5

        # greedy word wrap across mixed runs.
        # Word does not count a trailing space when deciding to break, so the
        # overflow test uses the bare word width and the space is added after.
        line_w, lines = 0.0, 1
        for text, fn, sz in segs:
            for word in text.replace("\t", " ").split(" "):
                if not word:
                    line_w += pdfmetrics.stringWidth(" ", fn, sz)
                    continue
                ww = pdfmetrics.stringWidth(word, fn, sz)
                sw = pdfmetrics.stringWidth(" ", fn, sz)
                if line_w + ww > avail and line_w > 0:
                    lines += 1
                    line_w = ww + sw
                else:
                    line_w += ww + sw
        if not p.text.strip():
            lines = 1

        ls = pf.line_spacing or 1.0
        lead = maxsz * 1.22 * (ls if isinstance(ls, float) else 1.0)
        before = pf.space_before.pt if pf.space_before else 0
        after = pf.space_after.pt if pf.space_after else 0
        total += lines * lead + before + after

    return total, usable_h, page_h


if __name__ == "__main__":
    f = sys.argv[1] if len(sys.argv) > 1 else "Pratik_Shinde_Mainframe_COBOL_Developer_Resume.docx"
    used, avail, ph = measure(f)
    print(f"estimated content height : {used:7.1f} pt")
    print(f"usable page height       : {avail:7.1f} pt")
    print(f"fill                     : {100*used/avail:6.1f} %")
    print("VERDICT:", "ONE PAGE (fits)" if used <= avail else
          f"OVERFLOW by {used-avail:.1f} pt")
