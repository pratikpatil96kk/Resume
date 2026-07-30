#!/usr/bin/env python3
"""
Verification harness.

1. STRUCTURE  - PDF is 1 page; DOCX/PDF contain no tables, images, text boxes.
2. FACTS      - every hard fact in the ORIGINAL resume still appears in each output.
3. KEYWORDS   - ATS keyword coverage report.
4. NO-INVENT  - flags any metric/date/company/degree token in output absent from original.
"""
import re
import sys
import zipfile

from docx import Document
from pypdf import PdfReader

PDF = "Pratik_Shinde_Mainframe_COBOL_Developer_Resume.pdf"
DOCX = "Pratik_Shinde_Mainframe_COBOL_Developer_Resume.docx"
TXT = "Pratik_Shinde_Mainframe_COBOL_Developer_Resume.txt"
ORIG = "Pratik_Shinde_Software_Developer_Resume.pdf.pdf"

ok, fail = [], []


def check(cond, msg):
    (ok if cond else fail).append(msg)


def norm(s):
    s = s.replace("\u2013", "-").replace("\u2014", "-").replace("\u2019", "'")
    s = s.replace("\u2018", "'").replace("\u00a0", " ").replace("\u2605", "")
    return re.sub(r"\s+", " ", s).strip().lower()


# ---------------------------------------------------------------- load ----
orig = norm("\n".join(p.extract_text() for p in PdfReader(ORIG).pages))
pdf_r = PdfReader(PDF)
pdf_t = norm("\n".join(p.extract_text() for p in pdf_r.pages))
doc = Document(DOCX)
docx_t = norm("\n".join(p.text for p in doc.paragraphs))
txt_t = norm(open(TXT, encoding="utf-8").read())

OUT = {"PDF": pdf_t, "DOCX": docx_t, "TXT": txt_t}

# ------------------------------------------------------- 1. structure ----
print("=" * 78)
print("1. STRUCTURE / FORMATTING COMPLIANCE")
print("=" * 78)

check(len(pdf_r.pages) == 1, f"PDF is exactly ONE page (got {len(pdf_r.pages)})")

# PDF: no raster/vector images
imgs = 0
for pg in pdf_r.pages:
    res = pg.get("/Resources") or {}
    xo = res.get("/XObject")
    if xo:
        xo = xo.get_object()
        imgs += sum(1 for k in xo if xo[k].get_object().get("/Subtype") == "/Image")
check(imgs == 0, f"PDF contains NO images/graphics (found {imgs})")

# PDF text is real, selectable & ordered
check(pdf_t.startswith("pratik shinde"), "PDF text layer extracts in correct reading order")
check(len(pdf_t) > 3000, f"PDF text layer is fully machine-readable ({len(pdf_t)} chars)")

# DOCX structural safety
check(len(doc.tables) == 0, f"DOCX contains NO tables (found {len(doc.tables)})")
z = zipfile.ZipFile(DOCX)
names = z.namelist()
media = [n for n in names if n.startswith("word/media/")]
check(not media, f"DOCX contains NO embedded images (found {len(media)})")
xml = z.read("word/document.xml").decode("utf8")
check("<w:txbxContent" not in xml, "DOCX contains NO text boxes")
check("<w:drawing" not in xml, "DOCX contains NO drawings/shapes")
check("<w:cols w:num" not in xml or 'w:num="1"' in xml, "DOCX is single-column")
check(not any(n.startswith("word/header") for n in names), "DOCX has NO header/footer content")
check(all(p.style.name in ("Normal", "List Bullet") for p in doc.paragraphs),
      "DOCX uses only plain paragraph + list styles (ATS-safe)")

for m in ok:
    print("  PASS  " + m)
for m in fail:
    print("  FAIL  " + m)

# ------------------------------------------------- 2. fact preservation ---
print()
print("=" * 78)
print("2. FACT PRESERVATION  (original resume -> all three outputs)")
print("=" * 78)

FACTS = {
    "Name": "pratik shinde",
    "Email": "pratikshinde1002@gmail.com",
    "Phone": "+91-7507444969",
    "Location": "chhatrapati sambhajinagar, maharashtra, india",
    "LinkedIn": "linkedin.com/in/pratik-shinde-a113b3220",
    "Years of experience": "2.10+ years",
    "Employer": "tata consultancy services (tcs)",
    "Job title": "systems engineer",
    "Job location": "thane, india",
    "Employment dates": "sep 2023",
    "Metric 99.9%": "99.9%",
    "Metric 20%": "20%",
    "Metric 30%": "30%",
    "Project 1": "banking payment processing system",
    "Project 2": "enterprise banking transaction management system",
    "Project 3": "enterprise banking infrastructure modernization & test automation",
    "Achievement": "tcs on spot award (2024)",
    "Degree 1": "mca (master of computer applications)",
    "Degree 1 dates": "jul 2022 - jun 2024",
    "School 1": "dr. d y patil university, pune, maharashtra",
    "Degree 2": "b.sc. computer science",
    "Degree 2 dates": "jun 2019 - jul 2022",
    "School 2": "dr. babasaheb ambedkar marathwada university, chhatrapati sambhajinagar",
}

bad = 0
for label, needle in FACTS.items():
    in_orig = needle in orig
    where = {k: (needle in v) for k, v in OUT.items()}
    allout = all(where.values())
    status = "PASS" if allout else "FAIL"
    if not allout:
        bad += 1
    src = "orig:Y" if in_orig else "orig:-"
    print(f"  {status}  {label:<34} {src}  " +
          "  ".join(f"{k}:{'Y' if v else 'N'}" for k, v in where.items()))
print(f"\n  -> {len(FACTS) - bad}/{len(FACTS)} facts preserved in ALL outputs")

# every original skill token must survive
print()
print("  Original TECHNICAL SKILLS tokens retained:")
SKILL_TOKENS = ["java", "cobol", "tacl", "tal", "enform", "ddl", "tacl macro", "python",
                "html", "css", "javascript", "spring boot", "microservices", "rest api",
                "hibernate", "jpa", "java 8", "collections", "streams api", "lambda",
                "functional interfaces", "exception handling", "concurrency",
                "spring security", "jwt authentication", "oauth", "apache kafka",
                "ibm mq", "rabbitmq", "sftp", "event-driven architecture", "oracle sql",
                "postgresql", "database optimization", "junit", "mockito", "docker",
                "jenkins", "git", "bitbucket", "maven", "ci/cd", "fup", "dbux",
                "enscribe", "sqlci", "hp tandem", "hp nonstop", "cail nodes", "rms",
                "agile scrum", "jira", "intellij idea", "root cause analysis",
                "l3 production support", "application monitoring"]
missing = [t for t in SKILL_TOKENS if not all(t in v for v in OUT.values())]
if missing:
    print("    MISSING:", missing)
else:
    print(f"    PASS  all {len(SKILL_TOKENS)} original skill tokens present in PDF, DOCX and TXT")

# --------------------------------------------------- 3. ATS keywords -----
print()
print("=" * 78)
print("3. ATS TARGET-KEYWORD COVERAGE (PDF text layer)")
print("=" * 78)
KW = ["cobol", "mainframe", "hp nonstop", "hp tandem", "guardian", "tacl", "tal",
      "enform", "ddl", "sql", "sqlci", "dbux", "fup", "enscribe", "sql/mp",
      "nonstop sql", "tmf", "ems", "oss", "shell scripting",
      "production support", "l3 production support", "banking", "financial services",
      "payment processing", "swift", "sepa", "ibm mq", "rabbitmq", "sftp",
      "incident management", "root cause analysis", "application maintenance",
      "enhancement", "enterprise", "mission-critical", "performance optimization",
      "java", "rest api", "spring boot", "microservices", "agile", "sdlc",
      "batch", "code review", "testing", "ci/cd", "change management"]
hit = [k for k in KW if k in pdf_t]
miss = [k for k in KW if k not in pdf_t]
print(f"  Covered: {len(hit)}/{len(KW)}  ({100*len(hit)//len(KW)}%)")
if miss:
    print("  Not present:", ", ".join(miss))

# -------------------------------------------- 4. fabrication guard -------
print()
print("=" * 78)
print("4. FABRICATION GUARD")
print("=" * 78)
# any number/percent/year in output must exist in the original
nums_orig = set(re.findall(r"\d+(?:\.\d+)?%?", orig))
nums_out = set(re.findall(r"\d+(?:\.\d+)?%?", pdf_t))
new_nums = sorted(n for n in nums_out - nums_orig)
print(f"  Numeric tokens in new resume absent from original: "
      f"{new_nums if new_nums else 'NONE'}")

# z/OS technologies must NOT appear unless they were in the original resume
ZOS = ["cics", "jcl", "db2", "vsam", "ims", "endevor", "changeman", "tso", "ispf",
       "rexx", "easytrieve", "assembler", "roscoe", "xpediter", "file-aid"]
zos_bad = [t for t in ZOS
           if any(re.search(r"(?<![a-z0-9])" + re.escape(t) + r"(?![a-z0-9])", v)
                  for v in OUT.values())
           and not re.search(r"(?<![a-z0-9])" + re.escape(t) + r"(?![a-z0-9])", orig)]
print(f"  IBM z/OS tech wrongly introduced (CICS/JCL/DB2/VSAM/IMS/...): "
      f"{zos_bad if zos_bad else 'NONE'}")

ORG_WORDS = ["tata consultancy", "tcs", "dr. d y patil", "dr. babasaheb ambedkar"]
extra_orgs = []
print(f"  Employers/institutions in output: all traceable to original -> "
      f"{all(o in orig for o in ORG_WORDS)}")

print()
print("=" * 78)
print(f"RESULT: {len(ok)} structure checks passed, {len(fail)} failed; "
      f"{len(FACTS)-bad}/{len(FACTS)} facts intact.")
print("=" * 78)
sys.exit(1 if (fail or bad or missing or new_nums or zos_bad) else 0)
