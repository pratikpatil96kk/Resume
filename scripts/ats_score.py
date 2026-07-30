#!/usr/bin/env python3
"""
ATS scoring harness.

Models the two things real ATS/resume-screening engines actually compute:

  A. PARSE / FORMAT SCORE  - can the machine read the document at all, and does
     it recover the structured fields (contact, employer, title, dates, degree)?
     This is what Jobscan/Resume Worded call "ATS parse rate" and is the score
     people usually mean by "my ATS score".

  B. JOB-MATCH SCORE       - keyword + requirement overlap against a SPECIFIC
     job description. There is no such thing as a job-independent match score,
     so we score against several real Mainframe/COBOL postings.

Job descriptions below are distilled from real, currently-posted roles
(Barclays Pune HP NonStop, FIS Pune Tandem COBOL, Insight Global Sr TAL/COBOL/TACL,
generic HP NonStop production-support, and a generic IBM z/OS COBOL role).
"""
import re
import sys

from pypdf import PdfReader

PDF = "Pratik_Shinde_Mainframe_COBOL_Developer_Resume.pdf"


def norm(s):
    s = (s.replace("\u2013", "-").replace("\u2014", "-").replace("\u2019", "'")
          .replace("\u00a0", " "))
    return re.sub(r"\s+", " ", s).strip().lower()


TEXT = norm("\n".join(p.extract_text() for p in PdfReader(PDF).pages))
RAW = "\n".join(p.extract_text() for p in PdfReader(PDF).pages)


def has(term):
    """Word-boundary-ish containment, tolerant of punctuation like sql/mp, ci/cd."""
    t = term.lower()
    if not re.search(r"[a-z0-9]", t):
        return False
    return re.search(r"(?<![a-z0-9])" + re.escape(t) + r"(?![a-z0-9])", TEXT) is not None


# ==========================================================================
# A. PARSE / FORMAT SCORE
# ==========================================================================
PARSE = []


def pcheck(pts, cond, label):
    PARSE.append((pts, bool(cond), label))


r = PdfReader(PDF)
pcheck(8, len(r.pages) == 1, "Single page")
pcheck(10, len(TEXT) > 2500, "Real, extractable text layer (not scanned/outlined)")
pcheck(8, TEXT.startswith("pratik shinde"), "Name is the first parsed token")
pcheck(6, re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", TEXT), "Email detected")
pcheck(6, re.search(r"\+?\d[\d\-\s]{8,}\d", TEXT), "Phone detected")
pcheck(4, "linkedin.com/in/" in TEXT, "LinkedIn URL detected")
pcheck(4, "maharashtra" in TEXT and "india" in TEXT, "Location detected")

STD_HEADS = ["professional summary", "professional experience", "technical skills",
             "education", "achievements", "key projects"]
found_heads = sum(1 for h in STD_HEADS if h in TEXT)
pcheck(12, found_heads >= 5, f"Standard section headings ({found_heads}/6)")

pcheck(10, re.search(r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+\d{4}\s*-\s*"
                     r"((jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+\d{4}|present)",
                     TEXT), "Unambiguous MMM YYYY - MMM YYYY date ranges")
pcheck(6, "tata consultancy services" in TEXT, "Employer name parseable")
pcheck(6, "systems engineer" in TEXT, "Job title parseable")
pcheck(6, "master of computer applications" in TEXT or "mca" in TEXT, "Degree parseable")

# structural hazards
imgs = 0
for pg in r.pages:
    xo = (pg.get("/Resources") or {}).get("/XObject")
    if xo:
        xo = xo.get_object()
        imgs += sum(1 for k in xo if xo[k].get_object().get("/Subtype") == "/Image")
pcheck(8, imgs == 0, "No images/graphics/icons")

# multi-column detection: look for two distinct text x-origins forming columns
import fitz  # noqa: E402
pg = fitz.open(PDF)[0]
xs = sorted({round(b[0]) for b in pg.get_text("blocks")})
pcheck(6, len(xs) <= 3, f"Single-column layout (distinct x-origins: {len(xs)})")

# only count fonts that actually render glyphs (unused resource entries are harmless)
drawn = {}
for b in pg.get_text("dict")["blocks"]:
    if not b.get("lines"):
        continue
    for l in b["lines"]:
        for sp in l["spans"]:
            drawn[sp["font"]] = drawn.get(sp["font"], 0) + len(sp["text"])
pcheck(4, all("Source" in f for f in drawn),
       f"All rendered glyphs use embedded sans fonts ({len(drawn)} faces)")

sizes = [round(s["size"], 1) for b in pg.get_text("dict")["blocks"] if b.get("lines")
         for l in b["lines"] for s in l["spans"]]
pcheck(6, min(sizes) >= 8.0, f"No text below 8pt (min {min(sizes)}pt)")

meta = r.metadata or {}
pcheck(4, meta.get("/Title") and meta.get("/Keywords"), "PDF metadata populated")

wc = len(TEXT.split())
pcheck(6, 400 <= wc <= 900, f"Word count in optimal band ({wc})")

parse_earned = sum(p for p, c, _ in PARSE if c)
parse_total = sum(p for p, _, _ in PARSE)
PARSE_SCORE = round(100 * parse_earned / parse_total)

# ==========================================================================
# B. JOB-MATCH SCORES vs REAL POSTINGS
# ==========================================================================
# weight 3 = hard/mandatory requirement, 2 = important, 1 = nice-to-have
JOBS = {
    "HP NonStop (Tandem) Developer - Barclays, Pune": {
        "min_years": 6,
        "kw": [("cobol", 3), ("tacl", 3), ("hp nonstop", 3), ("enscribe", 3),
               ("fup", 2), ("enform", 2), ("pathway", 2), ("guardian", 2),
               ("batch", 2), ("oss", 1), ("shell scripting", 1), ("python", 1),
               ("db2", 1), ("jcl", 1), ("screen cobol", 1), ("scobol", 1),
               ("banking", 2), ("financial", 2), ("code review", 1),
               ("unit testing", 1), ("peruse", 1), ("spooler", 1)],
    },
    "Tandem COBOL / Mainframe COBOL Developer - FIS, Pune": {
        "min_years": 6,
        "kw": [("cobol", 3), ("tandem", 3), ("sql", 3), ("tacl", 2),
               ("pathway", 2), ("agile scrum", 2), ("java", 2), ("oss", 1),
               ("c++", 1), ("support", 3), ("enhancement", 3),
               ("troubleshoot", 2), ("documentation", 1), ("communication", 1)],
    },
    "Sr TAL/COBOL/TACL HP NonStop Developer - Insight Global": {
        "min_years": 7,
        "kw": [("tal", 3), ("cobol", 3), ("tacl", 3), ("hp nonstop", 3),
               ("guardian", 3), ("pathway", 2), ("payment", 3),
               ("settlement", 2), ("transaction", 2), ("enscribe", 2),
               ("sql", 2), ("high availability", 2), ("fault-tolerant", 1),
               ("performance tuning", 2), ("debugging", 2), ("banking", 2),
               ("financial services", 2), ("migration", 1), ("monitoring", 2)],
    },
    "HP NonStop Production Support Engineer (generic L2/L3)": {
        "min_years": 3,
        "kw": [("hp nonstop", 3), ("production support", 3), ("incident", 3),
               ("root cause analysis", 3), ("cobol", 2), ("tacl", 2),
               ("batch", 2), ("monitoring", 2), ("sql", 2), ("banking", 2),
               ("payment", 2), ("swift", 1), ("sepa", 1), ("mq", 2),
               ("sftp", 2), ("change management", 2), ("sla", 1),
               ("jira", 1), ("escalation", 1), ("troubleshoot", 2)],
    },
    "Mainframe COBOL Developer - IBM z/OS (banking)": {
        "min_years": 5,
        "kw": [("cobol", 3), ("mainframe", 3), ("jcl", 3), ("cics", 3),
               ("vsam", 3), ("db2", 3), ("batch", 2), ("sql", 2),
               ("banking", 2), ("production support", 2), ("changeman", 1),
               ("mq", 2), ("assembler", 1), ("endevor", 1), ("tso", 1),
               ("ispf", 1), ("rexx", 1)],
    },
}

CAND_YEARS = 2.10


def score_job(spec):
    tot = sum(w for _, w in spec["kw"])
    got = sum(w for k, w in spec["kw"] if has(k))
    missing_hard = [k for k, w in spec["kw"] if w == 3 and not has(k)]
    return round(100 * got / tot), missing_hard


print("=" * 78)
print("  ATS SCORE REPORT")
print("  Pratik_Shinde_Mainframe_COBOL_Developer_Resume.pdf")
print("=" * 78)

print("\nA. FORMAT / PARSE-RATE SCORE  (job-independent)")
print("-" * 78)
for pts, cond, label in PARSE:
    print(f"   [{'x' if cond else ' '}] {label:<62} {pts if cond else 0:>2}/{pts}")
print("-" * 78)
print(f"   PARSE-RATE SCORE: {parse_earned}/{parse_total}  =  {PARSE_SCORE}%")

print("\n\nB. JOB-MATCH SCORE  (keyword/requirement overlap vs REAL postings)")
print("-" * 78)
rows = []
for name, spec in JOBS.items():
    sc, miss = score_job(spec)
    gap = spec["min_years"] - CAND_YEARS
    rows.append((name, sc, spec["min_years"], gap, miss))
    print(f"\n   {name}")
    print(f"     keyword match        : {sc}%")
    print(f"     posting wants        : {spec['min_years']}+ yrs   (you: {CAND_YEARS} yrs"
          f"  -> short by {gap:.1f})")
    print(f"     missing MUST-HAVES   : {', '.join(miss) if miss else 'none'}")

avg = round(sum(r[1] for r in rows) / len(rows))
best = max(rows, key=lambda x: x[1])
worst = min(rows, key=lambda x: x[1])

print("\n" + "=" * 78)
print("  HEADLINE NUMBERS")
print("=" * 78)
print(f"   Format / parse-rate score      : {PARSE_SCORE}%")
print(f"   Avg keyword match (5 real JDs) : {avg}%")
print(f"   Best fit  : {best[1]}%  {best[0]}")
print(f"   Worst fit : {worst[1]}%  {worst[0]}")
print("=" * 78)
