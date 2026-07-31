"""
Single source of truth for Pratik Shinde's Mainframe COBOL Developer resume.

PROVENANCE RULE
---------------
Every fact below is traceable to the original document:
    Pratik_Shinde_Software_Developer_Resume.pdf.pdf

Nothing has been removed. Wording is optimised for Mainframe / COBOL / HP NonStop
ATS keyword density; no company, date, degree, metric, project or achievement has
been altered, dropped or invented.
"""

# --------------------------------------------------------------------------
# HEADER
# --------------------------------------------------------------------------
NAME = "PRATIK SHINDE"

# Target-role line: states the role being applied for, not a claimed past title.
TARGET_ROLE = ("Target Roles: Mainframe Developer  |  COBOL Developer  |  Mainframe Application "
               "Developer  |  Production Support Engineer")

HEADLINE = "Mainframe Software Engineer  |  COBOL  |  HP NonStop"

CONTACT = [
    "pratikshinde1002@gmail.com",
    "+91-7507444969",
    "Chhatrapati Sambhajinagar, Maharashtra, India",
    "linkedin.com/in/pratik-shinde-a113b3220",
]

# --------------------------------------------------------------------------
# PROFESSIONAL SUMMARY
# --------------------------------------------------------------------------
SUMMARY = (
    "Mainframe Software Engineer with 2.10+ years of experience spanning Mainframe Development, "
    "Application Development, Application Maintenance and Application Enhancement for mission-critical "
    "banking and financial services applications at Tata Consultancy Services (TCS). "
    "Skilled in COBOL, TAL, TACL, TACL Macro, ENFORM, DDL, SQL and Shell Scripting across HP NonStop "
    "(HP Tandem) Guardian and OSS environments, with exposure to Enscribe, NonStop SQL/MP, TMF, EMS and "
    "the FUP, DBUX and SQLCI utilities. Experienced in high-volume SWIFT and SEPA payment processing, "
    "batch processing and real-time online transaction processing, Oracle SQL development, and IBM MQ, "
    "RabbitMQ and SFTP integration. Recognised for L3 production support, incident management, Root Cause "
    "Analysis, performance tuning and software maintenance that sustain high availability and system "
    "reliability across fault-tolerant enterprise applications, delivered in Agile Scrum SDLC environments."
)

# --------------------------------------------------------------------------
# WORK EXPERIENCE  (all 8 original bullets preserved, 1:1, reworded only)
# --------------------------------------------------------------------------
EXPERIENCE = [
    {
        "role": "Systems Engineer",
        "company": "Tata Consultancy Services (TCS)",
        "location": "Thane, India",
        "dates": "Sep 2023 \u2013 Present",
        "bullets": [
            # 1 :: original -> Java-based payment systems, 99.9% availability
            "Engineered and maintained Java-based payment processing systems handling high-volume banking "
            "transactions, sustaining 99.9% availability and system reliability across mission-critical "
            "enterprise banking infrastructure spanning HP NonStop (Tandem) and distributed platforms.",
            # 2 :: original -> SWIFT/SEPA batch + real-time, ~20% reduction
            "Optimized batch processing and real-time online transaction processing flows for SWIFT and SEPA "
            "payments, achieving an approximate 20% reduction in processing time through performance tuning, "
            "code optimization and SQL query optimization.",
            # 3 :: original -> L3 support, 30% downtime reduction, RCA
            "Delivered L3 production support across mission-critical, fault-tolerant banking applications, "
            "troubleshooting and diagnosing critical incidents and reducing downtime by 30% through disciplined "
            "Root Cause Analysis (RCA), incident management and corrective action.",
            # 4 :: original -> debugged/enhanced core Java components
            "Debugged and enhanced core application components, applying systematic debugging and performance "
            "tuning to improve stability and maintainability of enterprise banking systems under continuous "
            "application maintenance, software maintenance and enhancement.",
            # 5 :: original -> reconciliation & settlement modules
            "Designed and implemented reconciliation and settlement modules, ensuring accurate financial "
            "reporting and full compliance with banking regulatory standards.",
            # 6 :: original -> IBM MQ + SFTP integration
            "Integrated IBM MQ and SFTP interfaces enabling secure file processing and reliable data exchange "
            "across distributed enterprise banking platforms.",
            # 7 :: original -> Agile Scrum collaboration
            "Collaborated with cross-functional teams in an Agile Scrum environment to deliver on-time "
            "releases, manage sprint deliverables and align delivery with business objectives across the SDLC.",
            # 8 :: original -> code reviews, testing, CI/CD
            "Contributed to peer code review, unit testing, system testing and CI/CD pipeline execution, "
            "upholding code quality standards and providing deployment support and technical documentation "
            "that accelerated release cycles.",
        ],
    }
]

# --------------------------------------------------------------------------
# PROJECTS  (all 3 names + descriptions + technologies preserved)
# --------------------------------------------------------------------------
PROJECTS = [
    {
        "name": "Banking Payment Processing System",
        "desc": "Developed and maintained Java Spring Boot microservices for high-volume SWIFT and SEPA payment "
                "processing. Built REST APIs, optimized backend performance and resolved critical L3 production "
                "issues safeguarding transaction throughput and system stability.",
        "tech": "Java, Spring Boot, Microservices, REST APIs, Oracle SQL",
    },
    {
        "name": "Enterprise Banking Transaction Management System",
        "desc": "Architected backend services for transaction validation, reconciliation and settlement using "
                "Java, Spring Boot and Oracle SQL to ensure data integrity, accurate financial reporting and "
                "regulatory compliance.",
        "tech": "Java, Spring Boot, Oracle SQL, Hibernate",
    },
    {
        "name": "Enterprise Banking Infrastructure Modernization & Test Automation",
        "desc": "Enhanced legacy banking applications with scalable microservices architecture and REST APIs. "
                "Contributed to CI/CD automation, testing and controlled production deployments across "
                "enterprise environments.",
        "tech": "Java, Spring Boot, Jenkins, Docker, Git",
    },
]

# --------------------------------------------------------------------------
# TECHNICAL SKILLS  (requested grouping; every original skill retained)
# --------------------------------------------------------------------------
SKILLS = [
    ("Programming Languages",
     "COBOL, TAL, TACL, TACL Macro, ENFORM, DDL, SQL, Shell Scripting, Java, Python, HTML, CSS, JavaScript"),
    ("Mainframe Technologies",
     "HP NonStop, HP Tandem, Guardian, OSS, SQL/MP, NonStop SQL, Enscribe, TMF, EMS"),
    ("Utilities",
     "FUP, DBUX, ENSCRIBE, SQLCI"),
    ("Environment / Platforms",
     "HP TANDEM, HP NONSTOP, CAIL NODES, RMS, OSS"),
    ("Messaging & Integration",
     "IBM MQ, RabbitMQ, SFTP, FTP, Apache Kafka, REST APIs, Event-Driven Architecture"),
    ("Databases",
     "SQL, Oracle SQL, PostgreSQL, Database Optimization"),
    ("Backend & Application Development",
     "Java 8 (Collections, Streams API, Lambda, Functional Interfaces, Exception Handling, Concurrency), "
     "Spring Boot, Microservices, Hibernate, JPA, Spring Security, JWT Authentication, OAuth"),
    ("Testing",
     "JUnit, Mockito"),
    ("DevOps & Version Control",
     "Git, Bitbucket, Jenkins, Docker, Maven, CI/CD"),
    ("Methodologies & Tools",
     "Agile Scrum, JIRA, IntelliJ IDEA, Software Development Life Cycle (SDLC), Incident Management, "
     "Problem Management, Change Management, Production Support, L3 Production Support, Root Cause Analysis "
     "(RCA), Application Monitoring, Performance Optimization, Performance Tuning, Troubleshooting, "
     "Debugging, SLA Management, Incident Escalation, Code Review, Technical Documentation, "
     "Stakeholder Communication, High Availability, Fault-Tolerant Systems"),
]

# --------------------------------------------------------------------------
# ACHIEVEMENTS  (same single achievement, reworded only)
# --------------------------------------------------------------------------
ACHIEVEMENTS = [
    ("TCS On Spot Award (2024)",
     "Recognised for outstanding technical contribution and measurable system stability improvements in "
     "high-pressure financial environments, demonstrating exceptional problem-solving and dedication to "
     "operational excellence."),
]

# --------------------------------------------------------------------------
# EDUCATION  (verbatim \u2013 untouched)
# --------------------------------------------------------------------------
EDUCATION = [
    {
        "degree": "MCA (Master of Computer Applications)",
        "school": "Dr. D Y Patil University, Pune, Maharashtra",
        "dates": "Jul 2022 \u2013 Jun 2024",
    },
    {
        "degree": "B.Sc. Computer Science",
        "school": "Dr. Babasaheb Ambedkar Marathwada University, Chhatrapati Sambhajinagar",
        "dates": "Jun 2019 \u2013 Jul 2022",
    },
]
