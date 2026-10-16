# Presentations

Talks about the workshop and ODSAI's AI education work. Each talk has its own folder named `YYYY-MM-DD-event/`.

## 2026-10-16-ccbb-retreat

A 10-minute talk at the CCBB Retreat 2026: "IUSM – Office of Data Science and AI: AI Education Initiatives" (Marcus R. Breese, PhD). It exists in two versions with the same content.

| Path | What it is |
|---|---|
| `slides.py` | Content of the PowerPoint version: every slide's text, layout and speaker notes. Edit this. |
| `build.py` | Drawing helpers and package assembly. Rebuilds the .pptx from `template/` and `slides.py`. |
| `render.py` | Renders each slide to PNG with macOS QuickLook, for checking layout. |
| `template/ccbb-template.pptx` | The IU School of Medicine CCBB template the PowerPoint version is built on. Never edit it. |
| `artifact/` | Source of the cream-and-crimson version: `deck.json` (slide order, fonts) and one HTML file per slide in `slides/`, speaker notes in each slide's `<aside>`. |
| `output/ccbb-retreat-2026-ai-education.pptx` | Built PowerPoint version (12 slides, CCBB template). |
| `output/ai-education-initiatives.pdf` | PDF of the cream-and-crimson version (13 slides). |
| `sources.md` | Research behind the slides: verified facts, source URLs, and what came from Marcus directly. |

### Rebuilding the PowerPoint version

Only the Python standard library is needed.

```bash
python3 build.py                       # writes output/ccbb-retreat-2026-ai-education.pptx
python3 render.py output/ccbb-retreat-2026-ai-education.pptx /tmp/slides   # one PNG per slide (macOS)
```

After every change:

1. Rebuild, then look at the rendered PNGs of the slides you changed. Check for text that overflows its box, a single word wrapped onto its own line, and anything running into the footer bar (content must end above y = 4.55 in). Fix by rewording or resizing the box; don't drop below 13 pt body text.
2. If the pptx skill is available, also run its `scripts/office/validate.py output/ccbb-retreat-2026-ai-education.pptx --original template/ccbb-template.pptx`.
3. If Marcus has edited the .pptx by hand in PowerPoint, compare its text with a fresh build first (for example with `markitdown`) and carry his edits into `slides.py` before rebuilding, or the rebuild will overwrite them.

How `slides.py` works: `content(title)` makes a slide on the template's white content layout with the right-aligned "CCBB Retreat 2026" tag; `section(title, subtitle)` uses the grey section layout. Shapes are placed in inches on a 10 × 5.625 in slide: `box()` for text boxes and cards, `table()` for plain tables, `bullets()` for bullet lists, `s.links` plus `run(..., link="rIdLinkN")` for hyperlinks, `s.notes` for speaker notes. Slide 1 and slide 10 reuse the template's own two slides (`"keep"` and `keep_src`).

### Updating the cream-and-crimson version

It is a Claude Slides artifact: https://claude.ai/artifact/WSr8WFZsXBswuB9eoR3USo. Edit the files in `artifact/` and publish them to that artifact's `project/` paths (`project/deck.json`, `project/slides/<id>.html`) with the Artifact tool, then export a new PDF from the artifact page (download button › PDF, "Best" quality, no speaker notes) and replace `output/ai-education-initiatives.pdf`. Copy any edits made in the artifact editor back into `artifact/` before committing.

### Keeping the versions in sync

Content changes go into both `slides.py` and `artifact/slides/*.html`, then both outputs are rebuilt. The cream version has one extra slide (`role.html`, ODSAI's role as a crimson callout); in the PowerPoint version that line sits on slide 2.

### Style rules Marcus has set

- Short, plain titles. Don't frame ODSAI as a gatekeeper: "ODSAI can help", never "talk to ODSAI first".
- ODSAI's focus is using AI to accelerate basic and computational research; education is a main pillar. Clinical work is a bonus, not the focus.
- Look facts up and cite them in `sources.md` and the speaker notes; never guess names, titles or dates. Facts Marcus gave directly are marked as such in `sources.md`.
