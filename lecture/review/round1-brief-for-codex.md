# Round 1 brief for Codex: design pass + content review

**From:** Claude (content owner, deck v1 author) · **To:** Codex (research lead, now **design owner** and reviewer)
**Date:** 8 Nov 2026 · **Status:** v1 deck built from your research pack. All 14 verified cards are reflected, and the chapter corrections have been applied.

The user's division of labour: Claude writes the content and the first build. **Codex owns visual design and aesthetics.** Then we review each other's work and converge.

## 1. What exists now

| Artifact | Path | Owner |
|---|---|---|
| Deck v1 (26 slides, 16:9, on the VinUni template) | `lecture/COMP5320_Ch9_Part1-2_Slides.pptx` | built by script |
| Deck generator | `lecture/build/build_deck.py`: one function per slide (`s_hook`, `s_blast`, …) | shared (see §3) |
| Drawing kit + design tokens | `lecture/build/pptx_kit.py`: colours in `C`, `FONT`, `MONO`, and helpers `box`, `card`, `chip`, `icon_circle`, `code_panel`, `table`, `grouped_bar_chart`, … | **Codex** |
| Icons | `lecture/build/make_icons.js`: Tabler icons via react-icons → `assets/icons/<name>-<color>.png`. Run `node make_icons.js` after adding names. | **Codex** |
| Speaker script (source of the speaker notes) | `lecture/COMP5320_Ch9_Part1-2_Speaker_Script.md` | **Claude** |
| Research pack | `lecture/research/research-notes-M1-M2.md` | Codex |
| Template | `COMP5320 Slide Template.pptx` (repo root) | read-only |

**Build, render and check** (run from `lecture/build`):
```
python build_deck.py
powershell -ExecutionPolicy Bypass -File render_slides.ps1 -Deck ../COMP5320_Ch9_Part1-2_Slides.pptx -OutDir _render -Width 1600
python make_grid.py _render              # 2x2 contact sheets: _render/grid-NN.png
python "C:/Users/Chien/.claude/skills/synced/f8b8bc25-3518-46e7-9613-b52046d2dc66_712e8ad8-06da-457b-af1e-93204e49fbda/pptx/scripts/office/validate.py" ../COMP5320_Ch9_Part1-2_Slides.pptx --original "../../COMP5320 Slide Template.pptx"
```
`render_slides.ps1` drives the installed Microsoft PowerPoint through COM, so the render is exactly what the class will see. Run one render at a time; Claude will not render while you are working.

**Slide map:** 1 cover · 2 lecture map · 3 Part 1 divider · 4 opening incidents · 5 blast radius · 6 who/what/how + STRIDE · 7 threat-model DFD · 8 lethal trifecta · 9 one token stream · 10 direct vs indirect · 11 poisoned issue (running example) · 12 GitHub MCP case · 13 injection carriers · 14 why prompting can't fix it (chart) · 15 Part 1 recap + Review Q1 · 16 Part 2 divider · 17 confused deputy 1988→agents · 18 Supabase case (swimlane) · 19 ambient authority → POLA · 20 five vectors map · 21 hierarchy spoofing + covert channels · 22 config supply chain · 23 MCP silent update · 24 amplification · 25 Part 2 recap matrix · 26 references.

## 2. Task A: content review (proposals only)

Please review **all 26 slides plus the speaker script** and write `lecture/review/codex-review-round1.md`. Check:
1. **Technical accuracy** against your research pack. Flag any claim that is overstated, misdated or misattributed, on the slides or in the notes.
2. **Clarity for graduate SE students.** Is there one message per slide, and does the lead sentence state it? Is there jargon without explanation?
3. **Flow and timing.** Part 1 should take about 18 min (slides 1–15) and Part 2 about 13 min (slides 16–25). Is anything redundant or missing for §9.1–9.5 and the roadmap (team plan §5)?
4. **Visual explanation.** Does each diagram or chart actually prove its lead sentence? Suggest a better visual where one does not.
5. **Boundary with Part 3 (§9.6–9.7, Member 3).** Did we steal too much of the defences content?

Format: a table of findings with **ID · slide · severity (P0 must fix / P1 should fix / P2 nice) · issue · concrete proposed fix (exact replacement text where possible)**. Put any disagreement with the chapter or with v1 decisions in its own section, with evidence. **Do not edit slide wording, facts or the speaker script yourself.** Claude will apply or answer each item in round 2.

## 3. Task B: design pass (you own this)

Improve the aesthetics and visual clarity directly in code. You may restyle substantially, for example:
- card and diagram styling,
- icon treatment,
- typographic hierarchy, spacing and alignment,
- chart styling,
- better visual metaphors on specific slides,
- divider and cover polish.

Hard constraints:
- **Keep the template brand.** Use the navy title band and red accents from the template (`114984`, `CA1F27`), keep the cover photo slide, and use Arial for text with Consolas for code. Match the instructor's Course Briefing look: clean, flat, light-grey cards.
- **Keep content and meaning.** Do not change any slide's facts, wording meaning, order or count. If a layout needs shorter text, shorten it without changing the claim, and list each change in your notes so Claude can mirror it in the script.
- **Readability.** No text overflow, no overlaps, no word broken across lines. Body text ≥ 11 pt wherever possible, captions/sources ≥ 9.5 pt. Lead sentences stay on **one line** at 19–20 pt bold. Titles, eyebrows, leads and footnotes stay at the same positions on every content slide.
- **No AI-slide clichés.** No accent underline under titles. No decorative full-width stripes beyond the template's own band and bar. No gradients. No shadows heavier than subtle.
- **Keep it reproducible.** Everything stays generated by `python build_deck.py`. Never hand-edit the `.pptx`. `validate.py` must pass.
- **Edit scope:** `lecture/build/pptx_kit.py`, `lecture/build/make_icons.js`, `lecture/build/assets/**`, and the layout/visual parts of `lecture/build/build_deck.py` (positions, colours, shapes, visual elements). **Do not edit** `lecture/COMP5320_Ch9_Part1-2_Speaker_Script.md`, `lecture/research/**`, the template, or `chapter_9.pdf`.

Write a short design changelog in `lecture/review/codex-design-notes-round1.md`:
- what you changed and why, per slide or system-wide;
- any text you shortened;
- known remaining visual issues.

Known v1 weak spots you may want to address:
- Some cards have empty bottom space (slides 2, 6, 8, 11, 14).
- Slide 20's schematic is small and dense.
- Slide 24's shield-on-boundary motif is a little busy.
- The references slide (26) is plain.
- Divider slides (3, 16) could be stronger.
- Overall, check consistency of card radius, icon sizes and gaps.

## 4. Done when

- The deck is rebuilt with your design changes, `validate.py` passes, and every slide is rendered and visually checked (attach or point to `_render/grid-*.png`).
- `codex-review-round1.md` and `codex-design-notes-round1.md` exist.
- You report via `worker_done`: the top P0/P1 content findings, the main design changes, and any open questions for Claude. A non-zero exit from a render or validate run must be investigated. Report it if it is not fixed, and do not report success over a failing validate.
