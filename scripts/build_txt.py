#!/usr/bin/env python3
"""Plain-text resume for ATS copy/paste fields (Workday, Taleo, iCIMS, Naukri)."""
import os
import sys
import textwrap

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import resume_content as C  # noqa: E402

W = 98


def wrap(t, indent=""):
    return textwrap.fill(t, width=W, initial_indent=indent,
                         subsequent_indent=indent)


def bullet(t):
    return textwrap.fill(t, width=W, initial_indent="- ", subsequent_indent="  ")


def main(path):
    L = []
    L.append(C.NAME)
    L.append(C.HEADLINE.replace("  |  ", " | "))
    L.append(" | ".join(C.CONTACT))
    L.append("")

    def head(t):
        L.append(t.upper())
        L.append("=" * len(t))

    head("Professional Summary")
    L.append(wrap(C.SUMMARY))
    L.append("")

    head("Professional Experience")
    for j in C.EXPERIENCE:
        L.append(f'{j["role"]} | {j["company"]} | {j["location"]} | {j["dates"]}')
        for b in j["bullets"]:
            L.append(bullet(b))
        L.append("")

    head("Key Projects")
    for p in C.PROJECTS:
        L.append(bullet(f'{p["name"]} - {p["desc"]} Technologies: {p["tech"]}.'))
    L.append("")

    head("Technical Skills")
    for label, items in C.SKILLS:
        L.append(bullet(f"{label}: {items}"))
    L.append("")

    head("Achievements")
    for t, d in C.ACHIEVEMENTS:
        L.append(bullet(f"{t} - {d}"))
    L.append("")

    head("Education")
    for e in C.EDUCATION:
        L.append(f'{e["degree"]} | {e["dates"]}')
        L.append(f'{e["school"]}')
    L.append("")

    out = "\n".join(L).replace("\u2013", "-").replace("\u2014", "-")
    out = out.replace("\u2019", "'").replace("\u2018", "'")
    with open(path, "w", encoding="utf-8") as f:
        f.write(out)
    print("wrote", path)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1
         else "Pratik_Shinde_Mainframe_COBOL_Developer_Resume.txt")
