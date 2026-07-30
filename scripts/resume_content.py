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

HEADLINE = (
    "Mainframe COBOL Developer  |  HP NonStop (Tandem) Developer  |  "
    "Banking Payment Systems  |  L3 Production Support"
)

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
    "Results-driven Mainframe and Enterprise Application Developer with 2.10+ years of experience building, "
    "enhancing and supporting mission-critical banking and financial services applications at Tata Consultancy "
    "Services (TCS). Skilled in COBOL, TAL, TACL, TACL Macro, ENFORM, DDL and SQL across HP NonStop (HP Tandem) "
    "Guardian environments, with exposure to Enscribe, NonStop SQL/MP, TMF, EMS, OSS and the FUP, DBUX and SQLCI "
    "utilities. Strong in high-volume SWIFT and SEPA payment processing, batch and real-time flows, IBM MQ, "
    "RabbitMQ and SFTP integration, and Java, Spring Boot and REST API development across distributed banking "
    "applications. Recognised for L3 production support, incident management, Root Cause Analysis, performance "
    "optimization and application maintenance and enhancement in Agile Scrum SDLC environments."
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
            "transactions, sustaining 99.9% availability across enterprise banking infrastructure spanning "
            "HP NonStop (Tandem) and distributed platforms.",
            # 2 :: original -> SWIFT/SEPA batch + real-time, ~20% reduction
            "Optimized batch and real-time payment processing flows for SWIFT and SEPA transactions, achieving "
            "an approximate 20% reduction in processing time through performance tuning and code optimization.",
            # 3 :: original -> L3 support, 30% downtime reduction, RCA
            "Delivered L3 production support for mission-critical banking applications, resolving critical "
            "incidents and reducing downtime by 30% through disciplined Root Cause Analysis (RCA), incident "
            "management and corrective action.",
            # 4 :: original -> debugged/enhanced core Java components
            "Debugged and enhanced core Java components, measurably improving performance, stability and "
            "maintainability of mission-critical enterprise banking applications under ongoing application "
            "maintenance and enhancement.",
            # 5 :: original -> reconciliation & settlement modules
            "Designed and implemented reconciliation and settlement modules, ensuring accurate financial reporting "
            "and full compliance with banking regulatory standards.",
            # 6 :: original -> IBM MQ + SFTP integration
            "Integrated IBM MQ and SFTP interfaces enabling secure, reliable and efficient data exchange across "
            "distributed enterprise banking platforms.",
            # 7 :: original -> Agile Scrum collaboration
            "Collaborated with cross-functional teams in an Agile Scrum environment to deliver on-time releases, "
            "manage sprint deliverables and align delivery with business objectives.",
            # 8 :: original -> code reviews, testing, CI/CD
            "Contributed to code reviews, unit testing, system testing and CI/CD pipeline execution to uphold "
            "code quality standards and accelerate deployment cycles across the SDLC.",
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
     "Java, COBOL, TAL, TACL, TACL Macro, ENFORM, DDL, SQL, Shell Scripting, Python, HTML, CSS, JavaScript"),
    ("Mainframe Technologies",
     "HP NonStop, HP Tandem, Guardian, Enscribe, SQL/MP, NonStop SQL, TMF, EMS, OSS"),
    ("Mainframe Utilities",
     "FUP, DBUX, ENSCRIBE, SQLCI"),
    ("Environment / Platforms",
     "HP TANDEM, HP NONSTOP, CAIL NODES, RMS, SFTP, RabbitMQ, IBM MQ"),
    ("Backend & Integration",
     "Java 8 (Collections, Streams API, Lambda, Functional Interfaces, Exception Handling, Concurrency), "
     "Spring Boot, REST APIs, Microservices, Hibernate, JPA, Apache Kafka, IBM MQ, RabbitMQ, SFTP, "
     "Event-Driven Architecture, Spring Security, JWT Authentication, OAuth"),
    ("Databases",
     "Oracle SQL, PostgreSQL, SQL, Database Optimization"),
    ("Testing",
     "JUnit, Mockito"),
    ("DevOps & CI/CD",
     "Git, Bitbucket, Maven, Jenkins, Docker, CI/CD Pipelines"),
    ("Methodologies & Tools",
     "Agile Scrum, JIRA, IntelliJ IDEA, Root Cause Analysis (RCA), Production Support, L3 Production Support, "
     "Incident Management, Application Monitoring, Software Development Life Cycle (SDLC), Change Management"),
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
