# Codex design pass — round 1

8 November 2026. Implemented in the reproducible Python build and icon generator. Output: [26-slide deck](../COMP5320_Ch9_Part1-2_Slides.pptx). Content proposals are separate in [codex-review-round1.md](codex-review-round1.md); none has been applied to slide wording or the speaker script.

## System changes

- Preserved the template's photograph, logo, navy `114984`, red `CA1F27`, title band, side triangle and bottom brand bar. Rendered the original two template slides for comparison in `build/assets/template-review/`.
- Set editable cover and content-title text explicitly to Arial. Body text remains Arial; code remains Consolas. Content titles, eyebrows, leads and source footnotes retain their shared positions.
- Kept all leads on one line using measured Arial Bold widths, bounded to 19–20 pt. Disabled Latin word splitting in generated text frames. Footnotes now use the available content width rather than an unnecessarily narrow box.
- Standardised cards and chips to restrained, nearly square corners; softened the neutral card fill to `F3F5F7`, used a clearer muted text colour `536376`, and quieter rules `D1D9E2`. Removed the divider accent underline and watermark treatment. No gradients or new decorative stripes.
- Reduced Tabler icon stroke width to 1.7 and regenerated the icon assets, including the matching slate colour. Retained white-on-colour circles for people/agents and plain line icons for subordinate labels; their different sizes reflect diagram versus heading roles.
- Kept native PowerPoint text, shapes, tables and the editable chart. No diagrams were flattened into screenshots. No changes to slide order, count, script, research pack, source PDF or source template.

## Slide changes

| Slide(s) | Implemented design change and reason |
|---|---|
| 1 | Rebalanced the four cover lines in Arial at 25/21/25/18 pt; set college and year labels to Arial; removed explicit/inherited effect references on the edited labels. Preserved the original photo and brand composition. |
| 2 | Tightened the two part cards, moved questions and learning-objective chips into a more balanced vertical rhythm, and reduced unused bottom space. Retained the proportional 75-minute agenda. |
| 3, 16 | Replaced watermark icons and accent underline with clean section typography: large pale 01/02 in the upper right, stable part/title/subtitle/presenter positions, and generous navy space. Long Part 2 title wraps at a phrase boundary. |
| 4–5 | Applied the shared flatter card and icon treatment; retained the timeline and authority-radius diagrams. |
| 6 | Changed the STRIDE tiles to flat light-grey cards, raised their example copy, and improved copy fit. Kept the left who/what/how column and six-letter scan order. |
| 7 | Retained the editable data-flow diagram; applied the shared text and neutral-colour refinements. Technical/provenance wording concerns are proposals in the review, not silent diagram changes. |
| 8 | Increased the Rule of Two body to 12 pt and expanded its copy area. Kept the three-circle overlap because the intersection directly expresses the three simultaneous properties. |
| 9 | Preserved the role-to-context comparison and SQL table; applied common fonts and word-preserving wrapping. |
| 10 | Raised the direct-payload type to 11 pt and increased the final comparison-table row height so it has comfortable space. |
| 11 | Raised the payload to 11 pt, aligned it at the top with consistent internal padding, and placed the closing HTML-comment marker on its own paragraph. Retained every payload word and character. |
| 12 | Widened the attack-step copy slightly within each card to remove edge pressure. Kept the five-step chain and three causal/mitigation panels. |
| 13 | Adjusted code to 11.5 pt so complete source lines fit; raised the six carrier descriptions to 11 pt and widened their copy area slightly. |
| 14 | Increased chart height, gave its caption a separate clear area, and tightened the two safeguard panels. Kept the same four values, categories, legend wording and within-pair caveat. |
| 15 | Applied the common flat style; retained the question-versus-recap split. The timing and missing-permission assumption remain content proposals. |
| 17 | Applied the common shape/font treatment; kept the classic/agent comparison. Signing and authority wording remain content proposals. |
| 18 | Raised all six attack events to 11 pt and their number badges to 9.5 pt. Used compact left badge padding and expanded the lane subtitle space; the full return path now reads clearly at lecture scale. |
| 19 | Applied squarer permission chips and shared card styling. Kept the read/drop table and four task-scope principles. |
| 20 | Rebuilt the cramped half-width schematic as a full-width control path. Repository config → agent context ↔ tools/MCP → egress now sit above five equal numbered taxonomy cards; subagents branch below the context. Matching numbers connect each surface to its chapter subsection and OWASP tag. All existing labels and descriptions are preserved. |
| 21 | Widened the spoofed-authority example, raised it from 9.5 to 11 pt, and narrowed/repositioned the hierarchy tiers and promotion arrow. Complete phrases fit without squeezing. |
| 22 | Improved the case-text fit and applied flatter entry-source chips. Preserved the diff, dates, cases and defence copy exactly. |
| 23 | Applied the shared card/icon treatment; retained the release timeline and malicious-server-versus-defence comparison. |
| 24 | Replaced crossing diagonal fan-out with orthogonal branches. Replaced four tiny shield badges with one clear delegation-boundary gateway; kept four scoped subagents and their tools. This is an abstract policy gateway, not a claim that one classifier guarantees protection. Raised evidence-card body text to 11 pt. |
| 25 | Retained the editable recap matrix and handoff; applied the shared neutral palette and typography. |
| 26 | Replaced two uninterrupted text blocks with individually measured reference rows, preserving all references and the two existing headings. Added a quiet vertical separator; 10.5 pt text is appropriate for the distributed reference page. |

## Wording / script coordination

**No wording was shortened, removed or substantively changed.** A per-slide, whitespace-normalised word-multiset comparison against v1 found the same original words on every slide. The only added visible text is the divider numbering **01 / 02**. The slide 11 closing `-->` marker is separated into its own paragraph; it is not a payload change. Chart series names and values remain unchanged. The complete speaker script remains the source of all 26 slide-note sections.

Claude can apply accepted review proposals in round 2. Changes to leads should remain single-line at 19–20 pt; longer replacement paragraphs need another fit check and render.

## Verification and reproducibility

Executed from `lecture/build`:

```powershell
node make_icons.js
python build_deck.py
powershell -ExecutionPolicy Bypass -File render_slides.ps1 -Deck ../COMP5320_Ch9_Part1-2_Slides.pptx -OutDir _render -Width 1600
python make_grid.py _render
python "C:/Users/Chien/.claude/skills/synced/f8b8bc25-3518-46e7-9613-b52046d2dc66_712e8ad8-06da-457b-af1e-93204e49fbda/pptx/scripts/office/validate.py" ../COMP5320_Ch9_Part1-2_Slides.pptx --original "../../COMP5320 Slide Template.pptx"
python assets/check_text_fit.py
```

- **Build:** 26 slides, notes present for all 26.
- **Package validation:** `All validations PASSED!` on the final rebuilt deck.
- **PowerPoint render:** all 26 slides rendered by installed Microsoft PowerPoint at 1600 × 900, individually visually inspected. Changed slides were re-rendered and checked after fixes.
- **Text fit:** read-only COM audit of **587 text regions**, including table cells; **0 overflows** above a 1.5 pt measurement tolerance. It compares PowerPoint text bounds with available shape dimensions after margins. The audit helper is `build/assets/check_text_fit.py`; it does not modify the deck.
- **Typeface/size inspection:** no explicit text run below 9.5 pt in the final deck. Diagram events and ordinary body text are ≥11 pt; small technical labels, metadata, sources and reference entries use 9.5–10.5 pt where needed.
- **Preservation:** all original slide words retained, all chart values retained, original template cover picture retained, 26 slides in the original order.
- Initial fit checks identified small box-bound issues on slides 3/6/12/13/16/18/20/21/22; each was corrected with spacing, width or internal-margin changes and rechecked. No unresolved failing build/render/validate command.

Contact sheets, with the final rendered slide 1/11/18 updates included:

- [grid-01: slides 1–4](../build/_render/grid-01.png)
- [grid-02: slides 5–8](../build/_render/grid-02.png)
- [grid-03: slides 9–12](../build/_render/grid-03.png)
- [grid-04: slides 13–16](../build/_render/grid-04.png)
- [grid-05: slides 17–20](../build/_render/grid-05.png)
- [grid-06: slides 21–24](../build/_render/grid-06.png)
- [grid-07: slides 25–26](../build/_render/grid-07.png)

## Remaining considerations

No known visual overflow, unintended overlap, broken Latin words or missing assets remains. Slide 26 is deliberately a dense reference handout and should stay unpresented, as scripted. The cover retains the template's small year-label frame/shadow. Content concerns such as the absolute leads on slides 14/18/23 remain visible because this pass was not authorised to resolve factual wording; they are explicitly tracked in the content review. Timing requires rehearsal and the final room/projector may justify a later content reduction, rather than shrinking text.
