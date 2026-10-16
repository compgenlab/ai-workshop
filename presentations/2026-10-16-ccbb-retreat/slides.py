# Slide definitions for the 10-minute version; exec'd by build.py in place of the long list.
slides = []
X0, W = 0.4, 8.75
cw, g = (W - 0.5) / 3, 0.25

# 1. Title (template's own)
slides.append(("keep", "slide1.xml", "About 30 seconds. ODSAI is the IU School of Medicine’s Office of Data Science and AI. Three points in ten minutes: where AI education already lives at IU, how ODSAI connects IUSM researchers to it, and the hands-on workshop ODSAI runs."))

# 2. Landscape + one place to look + scope line
s = content("AI training is spread across many units")
cards = [("UITS Research Technologies", "HPC, GPU and LLM workshops"),
         ("IU Research", "AI Research Network; AI Research Brown Bag Talk"),
         ("Indiana CTSI", "Monthly AI Workshop Series for investigators"),
         ("UITS Academic and AI Innovation", "GenAI 101, office hours, faculty fellows"),
         ("Schools and centers", "Luddy AI Center, Kelley, IU Libraries"),
         ("IU School of Medicine", "Departments, student groups, ODSAI")]
for k, (h, t) in enumerate(cards):
    card(s, X0 + (k % 3) * (cw + g), 1.35 + (k // 3) * 1.2, cw, 1.1, h, t, sz=13, hsz=14)
box(s, X0, 3.78, W, 0.4, [para([run("ODSAI’s role: ", 15, b=True, color=RED), run("IUSM’s office to help you accelerate your research using AI.", 15, color=TXT)])])
box(s, X0, 4.22, W, 0.35, [para([run("Not covered: IUSM’s efforts on AI in clinical education.", 13, i=True, color=GRAY)])])
s.notes = ("About 2 minutes. AI education at IU is good but scattered. ODSAI’s job is to amplify it, not duplicate it, so IUSM researchers have one place to look. ODSAI is IUSM’s office to help researchers accelerate their research using AI: not just learning about AI, but learning how to apply it directly to their own work. IU’s AI Research Network is big and covers all of IU; ODSAI is small and can be more hands-on when needed. IUSM also has separate efforts on using AI in clinical education, driven by Anthony Shanks; those are out of scope for this talk. Per the IUSM MD student news (Mar 2, 2026), AI content is being added to Phase 1 health systems science courses, fourth-year specialty electives are in development, and a two-year AI scholarly concentration pilot has been proposed. Source: https://medicine.iu.edu/blogs/md-student-news/2026/students-launch-ai-in-medicine-sig\n\n"
           "Detail if asked:\n"
           "UITS Research Technologies, Supercomputing for Everyone Series (SC4ES) via IU IT Training: GPU Computing and AI on HPC; Large Language Models (LLMs) on High Performance Computing; Intro to HPC; HPC for Biologists; Getting Started with Jetstream2; Storage 101/201; Practical Coding for Researchers. Intro to Deep Learning on Big Red 200 is listed by the AI Research Network.\n"
           "IU Research AI Research Network, AI Research Brown Bag Talk, fall 2026: Oct 26 Cindy E. Hmelo-Silver; Nov 9 Jingzhi Pu; Nov 23 Jiang Bian; Dec 7 Garim Lee.\n"
           "Indiana CTSI AI Workshop Series (Data Science and Informatics program, co-lead Titus Schleyer): monthly, hybrid at the Regenstrief Social Hub, recorded. 2026 sessions included Overview of AI Concepts in Research, Third-party AI tools for research at IU, and Research Technologies AI tools for research at IU.\n"
           "UITS Academic and AI Innovation (Anne Leftwich, UITS Chief Academic and AI Innovation Officer): GenAI 101, AI Innovation Hub Open Office Hours, GenAI Faculty Fellows Program, 3-for-30 Generative AI Series. Also the new IU Faculty Group on Student Learning in the Age of AI (Oct 14, 2026).\n\n"
           "Sources:\nhttps://ittraining.iu.edu/explore-topics/titles/hpc/index.html\nhttps://research.iu.edu/research-networks/ai/index.html\nhttps://research.iu.edu/news-events/events/research-events.html\n"
           "https://indianactsi.org/new-ai-workshop-series-from-the-indiana-ctsi-will-educate-investigators-and-grow-community-around-artificial-intelligence/\nhttps://ai.iu.edu\nhttps://depi.iu.edu/events/ai-innovation/index.html\n"
           "https://edscoop.com/indiana-university-technology-plan/\nhttps://today.iu.edu/live/news/53982-iu-launches-faculty-led-effort-to-define-what")
slides.append(s)

# 2b. Research-focused training
s = content("Where IUSM researchers can start")
s.links += ["https://ittraining.iu.edu/explore-topics/titles/scfes/index.html",
            "https://indianactsi.org/research/data-informatics/ai-resources/ai-workshop-series/",
            "https://research.iu.edu/research-networks/ai"]
def grouped_table(s, x, y, w, cols, header, groups, sz=13, rowh=0.55, linkh=0.32):
    def tc(text_runs, fill, bottom, span=None, merged=False):
        attr = f' gridSpan="{span}"' if span else (' hMerge="1"' if merged else '')
        ln = f'<a:lnB w="9525"><a:solidFill><a:srgbClr val="{RULE}"/></a:solidFill></a:lnB>' if bottom else '<a:lnB><a:noFill/></a:lnB>'
        return (f'<a:tc{attr}><a:txBody><a:bodyPr/><a:lstStyle/>{para(text_runs)}</a:txBody>'
                f'<a:tcPr marL="{e(0.12)}" marR="{e(0.12)}" marT="{e(0.04)}" marB="{e(0.04)}" anchor="ctr">'
                f'<a:lnL><a:noFill/></a:lnL><a:lnR><a:noFill/></a:lnR><a:lnT><a:noFill/></a:lnT>{ln}'
                f'<a:solidFill><a:srgbClr val="{fill}"/></a:solidFill></a:tcPr></a:tc>')
    trs = [f'<a:tr h="{e(0.42)}">' + "".join(tc([run(h, sz, b=True, color="FFFFFF")], DARK, False) for h in header) + '</a:tr>']
    height = 0.42
    for k, (cells, label, url_text, rid) in enumerate(groups):
        fill = "FFFFFF" if k % 2 == 0 else CARD
        trs.append(f'<a:tr h="{e(rowh)}">' + "".join(tc([run(c, sz, color=TXT)], fill, False) for c in cells) + '</a:tr>')
        link = [run(label, 12, b=True, color=TXT), run(url_text, 12, link=rid)]
        trs.append(f'<a:tr h="{e(linkh)}">' + tc(link, fill, True, span=3) + tc([run("", 12)], fill, True, merged=True) * 2 + '</a:tr>')
        height += rowh + linkh
    grid = "".join(f'<a:gridCol w="{e(w*c)}"/>' for c in cols)
    s.parts.append(f'<p:graphicFrame><p:nvGraphicFramePr><p:cNvPr id="{s.id()}" name="Table {s.nid}"/>'
                   f'<p:cNvGraphicFramePr><a:graphicFrameLocks noGrp="1"/></p:cNvGraphicFramePr><p:nvPr/></p:nvGraphicFramePr>'
                   f'<p:xfrm><a:off x="{e(x)}" y="{e(y)}"/><a:ext cx="{e(w)}" cy="{e(height)}"/></p:xfrm>'
                   f'<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/table">'
                   f'<a:tbl><a:tblPr firstRow="1"/><a:tblGrid>{grid}</a:tblGrid>{"".join(trs)}</a:tbl></a:graphicData></a:graphic></p:graphicFrame>')
grouped_table(s, X0, 1.4, W, [0.33, 0.25, 0.42], ["Series", "Run by", "For example"], [
    (["Supercomputing for Everyone Series", "UITS", "LLMs on HPC; GPU Computing and AI on HPC"], "Series page: ", "ittraining.iu.edu/explore-topics/titles/scfes", "rIdLink1"),
    (["AI Workshop Series", "Indiana CTSI", "Next: Oct 27, competency-based AI training; Dec 8, AI and human subjects research (IRB)"], "Series page: ", "indianactsi.org/research/data-informatics/ai-resources/ai-workshop-series", "rIdLink2"),
    (["AI Research Brown Bag Talk", "IU AI Research Network", "Noon talks; next: Oct 26, Nov 9, Nov 23, Dec 7"], "All IU AI events: ", "research.iu.edu/research-networks/ai", "rIdLink3")])
s.notes = ("About 1 minute. The three series most useful to IUSM researchers. SC4ES page: https://ittraining.iu.edu/explore-topics/titles/scfes/index.html (the AI and GPU sessions are listed on https://ittraining.iu.edu/explore-topics/titles/hpc/index.html). CTSI series page: https://indianactsi.org/research/data-informatics/ai-resources/ai-workshop-series/ . The AI Research Network page (https://research.iu.edu/research-networks/ai) links to all IU AI events (https://events.iu.edu/all/tags/Artificial%20Intelligence). CTSI fall 2026 sessions, all at noon: Aug 18, Mary Bourke, Reimagining Instructional Design: GenAI Resilient and GenAI Integrative Instructional Design for Evaluating Learning Outcomes (recorded); Sep 22, Adam Wilk, Panel: Principles and Best Practices for using AI in Qualitative Research (recorded); Oct 27, Andrea Krussel, Building Competency-Based AI Training for Research and Clinical Workforces; Dec 8, Purna Garimella, AI and Human Subjects Research: An IRB Perspective. No November session listed. Full session lists are in the notes on the previous slide.\n\n"
           "Sources:\nhttps://ittraining.iu.edu/explore-topics/titles/hpc/index.html\nhttps://indianactsi.org/new-ai-workshop-series-from-the-indiana-ctsi-will-educate-investigators-and-grow-community-around-artificial-intelligence/\nhttps://research.iu.edu/research-networks/ai/index.html")
slides.append(s)

# 2c. AI resources at IU
s = content("AI resources available at IU")
table(s, X0, 1.35, W, [0.2, 0.24, 0.56], [
    ["Resource", "Access", "Notes"],
    ["ChatGPT Edu", "IU license", "General chat and coding with Codex; restricted data OK; monthly credits go fast"],
    ["Google Gemini / Gemini Notebook", "IU access", "General chat and light coding; restricted data OK"],
    ["Microsoft Copilot", "Azure", "Restricted data OK; some costs may apply"],
    ["Jetstream2 and NRP.ai", "NSF resources", "Open research that fits their allocation requirements; API access; no PHI or critical data on Jetstream2"],
    ["REALLMS", "UITS Research Technologies", "The only option approved for PHI"]], sz=14, rowh=0.5)
s.notes = ("About 1 minute. The AI resources IUSM researchers can use today. ChatGPT Edu (IU license) and Google Gemini, including Gemini Notebook (formerly NotebookLM, renamed July 2026), are best for general chat and light coding. ChatGPT Edu, Gemini and Microsoft Copilot can all be used with restricted data. ChatGPT Edu includes Codex for coding, but use is limited by its free monthly credits, which go fast; Copilot (through Azure) can have some cost associated. NSF resources, Jetstream2 and NRP (the National Research Platform), are great for projects that fit their allocation requirements. Jetstream2 is primarily an NSF production cloud for open, publishable, or general academic and scientific research, so no PHI or critical data. Jetstream2 also offers API access; NRP offers free LLM access for researchers and educators through a chat interface and an OpenAI-compatible API (https://nrp.ai/llms). REALLMS is the only one approved for PHI; details on the next slide.")
slides.append(s)

# 2d. REALLMS
s = content("REALLMS: IU’s local LLMs")
cw2r = (W - 0.3) / 2
box(s, X0, 1.4, cw2r, 1.9, [para([run("Models", 16, b=True, color=RED)], after=6)] + bullets(
    ["gpt-oss-120b", "Qwen3.8-27B", "glm5.3-flash (coming soon)"], sz=15), fill=CARD)
box(s, X0 + cw2r + 0.3, 1.4, cw2r, 1.9, [para([run("Access", 16, b=True, color=RED)], after=6)] + bullets(
    ["Chat interface", "API (through RT projects)", "Run on-premise by UITS Research Technologies"], sz=15), fill=CARD)
box(s, X0, 3.5, W, 0.55, [para([run("The only IU option approved for PHI", 17, b=True, color="FFFFFF")])], fill=RED, anchor="t", inset=(0.2, 0.12, 0.2, 0.08))
s.links.append("https://researchdata.iu.edu/resource-catalog/about-reallms-at-iu/index.html")
box(s, X0, 4.2, W, 0.35, [para([run("About REALLMS: ", 13, b=True, color=TXT), run("researchdata.iu.edu/resource-catalog/about-reallms-at-iu", 13, link="rIdLink1")])])
s.notes = ("About 1 minute. REALLMS (Research and Academic LLM Services) is IU’s on-premise LLM service, run by UITS Research Technologies in the IU Data Center and free to the IU community. It is the only IU option approved for PHI. Current models: gpt-oss-120b and Qwen3.8-27B, with glm5.3-flash coming soon. Access is through a chat interface or an API (through RT projects). This is also what the workshop VMs will use.\n\n"
           "Source: https://researchdata.iu.edu/resource-catalog/about-reallms-at-iu/index.html")
slides.append(s)

# 3. Who to ask (governance committee + AI office + ODSAI)
s = content("Who to ask about AI in your research")
for k, (h, items) in enumerate([
        ("ODSAI", ["Focus: using AI to accelerate basic and computational research", "Education: how to actively apply AI tools to your research today", "Hands-on help when you need it", "Connects you with the right people"]),
        ("AI Governance Committee", ["Members from IUSM, IU Health and Regenstrief", "Education, clinical, research and IT leaders", "Advisory group on running an AI research program the right way: approved tools, protected data, compliance"]),
        ("Dean’s office AI group", ["Includes David Hanson, director of artificial intelligence", "Supports AI in clinical and education settings", "Proof-of-concept development and consulting"])]):
    box(s, X0 + k * (cw + g), 1.4, cw, 2.95, [para([run(h, 15, b=True, color=RED)], after=6)] + bullets(items, sz=13), fill=CARD)
s.notes = ("About 2 minutes. Three places to go for help with AI in research. ODSAI is IUSM’s office to help you accelerate your research using AI. Its focus is supporting the use of AI to accelerate biomedical research, both basic and computational, and education is a main pillar of that work: teaching researchers how to actively apply these tools to their research today (the workshop later in this talk is one example). It is small enough to be hands-on, helping researchers apply AI directly to their own work, and connecting them onward when needed. "
           "The Fall 2025 IUSM All School Meeting recap says an AI Governance Committee has been formed, made up of education, clinical, research and IT leaders, to focus on policies and guidance for faculty, staff and students; its members come from IUSM, IU Health and Regenstrief; for researchers it acts as an advisory group on the logistics of running an AI research program the right way (which tools are approved, handling protected data, compliance, who to talk to). "
           "The Dean’s office AI group, which includes David Hanson, director of artificial intelligence, supports AI in clinical and education settings through proof-of-concept development and consulting. ODSAI works with them on joint consults such as the example on the next slide. "
           "\n\n"
           "Source: https://medicine.iu.edu/blogs/dean/fall-2025-all-school-meeting-recap")
slides.append(s)

# 4b. Consult example (clinical research)
s = content("Example: a joint consult")
box(s, X0, 1.4, W, 0.4, [para([run("IU School of Medicine–Northwest-Gary", 16, b=True, color=TXT)])])
fw2, aw2 = 3.9, 0.55
for k, (h, t) in enumerate([("The question", "A group wanted to use AI tools to capture conversations in a clinical learning environment"),
                            ("The consult", "ODSAI and the Dean’s office AI group met with the faculty members to discuss feasibility and implementation options for their project")]):
    x0 = X0 + k * (fw2 + aw2 + 0.3)
    card(s, x0, 2.0, fw2, 1.5, h, t, sz=15)
    if k < 1:
        box(s, x0 + fw2 + 0.15, 2.57, aw2, 0.36, None, fill=RED, geom="rightArrow", name="Arrow")
s.notes = ("About 1 minute. One example of a joint consult: a group at IU School of Medicine–Northwest-Gary wanted to use AI tools to capture conversations in a clinical learning environment, and ODSAI and the Dean’s office AI group met with the faculty members to discuss feasibility and implementation options for their project. This is only an example; the outcome is not part of the talk. ODSAI’s focus is supporting the needs of basic and computational labs; helping with clinical projects like this one is a bonus.\n\nSource: https://medicine.iu.edu/gary")
slides.append(s)

# 5. Classroom (small)
s = content("Coordinating classroom efforts")
box(s, X0, 1.45, W, 0.5, [para([run("Dayu Sun (Biostatistics) is developing a course on AI Literacy.", 16, color=TXT)])])
box(s, X0, 2.1, W, 1.6, [para([run("ODSAI’s role", 15, b=True, color=RED)], after=6)] + bullets(
    ["Coordinate across classes with similar AI needs, so each class doesn’t reinvent the wheel", "Share notes on AI tools and how to get students access", "For this course: computing needs, available LLMs for coursework"], sz=14), fill=CARD)
s.notes = "About 30 seconds. Dayu Sun in Biostatistics is developing a course on AI Literacy (still in development). ODSAI is involved so solutions can be shared between any other classes that have similar needs: we help coordinate so each class doesn’t need to reinvent the wheel, and we can share notes on AI tools and how to get students access. For this course that includes logistics such as computing needs and which LLMs are available for coursework."
slides.append(s)

# 5b. Challenges
s = content("What makes biomedical AI different")
cw4, ch4 = (W - 0.25) / 2, 1.3
for k, (h, t) in enumerate([("Protected data", "Patient data and IRB terms limit which tools can see what"),
                            ("Checking output", "Fluent answers, citations and code can still be wrong"),
                            ("Reproducibility", "Analyses still have to be rerun, reviewed and documented"),
                            ("Your own data", "General tools don’t know your lab’s data, methods or literature")]):
    card(s, X0 + (k % 2) * (cw4 + 0.25), 1.45 + (k // 2) * (ch4 + 0.25), cw4, ch4, h, t, sz=15)
s.notes = "About 1 minute. Why ODSAI does its own work on AI in biomedical research: these problems are what the workshop is built around. Draft wording; edit to match how you describe ODSAI’s priorities."
slides.append(s)

# 6. Workshop overview (template's own slide 2)
s = Slide(); s.keep_src = "slide2.xml"
ph(s, "ctrTitle", None, [para([run("AI Tools for Biomedical Researchers")], plain=False)], "Title")
ph(s, "body", 10, [para([run("CCBB Retreat 2026")], align="r", plain=False)], "Header")
box(s, X0, 1.4, W, 0.4, [para([run("We’re planning a hands-on workshop", 16, b=True, color=TXT)])])
for k, (big, small) in enumerate([("3", "weekly sessions, 3.5 hours each"), ("20–25", "participants per session, with TAs"), ("Hands-on", "a personal VM using IU REALLMS local LLMs")]):
    box(s, X0 + k * (cw + g), 1.95, cw, 1.35, [para([run(big, 28, b=True, color=RED)], after=2), para([run(small, 14, color=TXT)])], fill=CARD)
box(s, X0, 3.55, W, 0.9, [para([run("Open to all IUSM research trainees (graduate students, postdocs, and clinical residents and fellows doing research rotations) and faculty.", 15, color=TXT)])])
s.notes = "About 1 minute. ODSAI is planning a hands-on workshop, AI Tools for Biomedical Researchers: A Hands-On Workshop. Plan: three weekly 3.5-hour sessions on the same weekday, 20 to 25 participants per session, one or two TAs, and a personal VM for each participant using IU REALLMS local LLMs (REALLMS: Research and Academic LLM Services, run by UITS Research Technologies in the IU Data Center; https://researchdata.iu.edu/resource-catalog/about-reallms-at-iu/index.html). [Add dates and registration.]"
slides.append(s)

# 6b. Goals
s = content("Workshop goals: removing the magic")
dw = (W - 0.5) / 3
for k, (d, h, t) in enumerate([
        ("DAY 1", "How AI works (and where it breaks)", "Build a classifier, watch an LLM sample, trace an agent loop"),
        ("DAY 2", "Getting your data accessible to LLMs", "A retrieval index and an MCP server connected to your own chat interface"),
        ("DAY 3", "A coding analysis exercise", "Direct an AI coding harness (such as OpenCode or Codex) through a full RNA-seq analysis from a written plan with pre-registered checks")]):
    box(s, X0 + k * (dw + g), 1.4, dw, 2.35, [para([run(d, 12, b=True, color=RED)], after=4), para([run(h, 15, b=True, color=TXT)], after=6),
                                              para([run(t, 13, color=TXT)])], fill=CARD)
box(s, X0, 3.92, W, 0.35, [para([run("Three weekly 3.5-hour sessions · IUSM research trainees and faculty", 13, i=True, color=GRAY)])])
s.notes = "About 1.5 minutes. The goal across all three days is to remove the magic. Day 1: how AI works and where it breaks. Day 2: getting your data accessible to LLMs. Day 3: a coding analysis exercise with an AI coding harness."
slides.append(s)

# 7. Link
s = section("", "WORKSHOP WEBSITE")
s.links.append("https://ai-workshop.compgenlab.org")
s.parts[0] = (f'<p:sp><p:nvSpPr><p:cNvPr id="{s.id()}" name="Title"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr><p:ph type="title"/></p:nvPr></p:nvSpPr><p:spPr/>'
              f'<p:txBody><a:bodyPr><a:normAutofit/></a:bodyPr><a:lstStyle/>{para([run("ai-workshop.compgenlab.org", sz=28, link="rIdLink1")], plain=False)}</p:txBody></p:sp>')
box(s, 0.58, 3.35, 8.9, 1.1, [para([run("Thinking of using AI or LLM tools in your research? ODSAI can help.", 18, b=True)], after=4),
                              para([run("We’ll connect you with the right people.", 16)])], name="Contact")
s.notes = "About 1 minute. Click the link to show the workshop site. Then the ask: whatever the question (tools, data, policy, methods), ODSAI can help, and can bring in the governance committee, the Dean’s office AI group, UITS Research Technologies, the CTSI or others as needed. No sign-off from ODSAI is needed to use AI in your projects; this is an offer of help."
slides.append(s)
