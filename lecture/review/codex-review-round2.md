# Codex review — round 2

8 November 2026. Checked Claude's response against the rebuilt slide text, all 26 slide-note sections, the complete speaker script including both appendices, and the research pack. Visually inspected the requested changed slides **4, 5, 7, 9, 10, 13, 14, 15, 17, 18, 19, 22, 23, 25**, plus the polished slides **11 and 20**. Content wording was not edited in this pass.

**Result: 21 of 22 round-1 items are resolved; R01 needs one small but material correction.** No P0 or new material factual error found. The modified decisions on R12 and R21 are acceptable.

## Remaining correction — exact text for Claude

| ID | Location | Severity | Remaining issue | Proposed replacement |
|---|---|---|---|---|
| **R2-01** (R01) | Slide 18 lead; script Slide 18 Key message; Say paragraph beginning “Map it to the deputy” | **P1 — should fix before approval** | “Could only file a ticket” and “had write access to their own ticket, nothing more” still exclude the customer's ability to read their own ticket/messages. That read is essential: step 6 shows the attacker reading the copied tokens. The researcher describes an RLS-restricted customer role, customer-visible messages and the return-channel read. Appendix B already correctly says “restricted ticket access.” [Primary actor table and attack flow][SB]. | **Lead:** “The customer could access their own ticket — the developer's agent could read private tokens.” **Key message:** “The customer could read and write their own ticket, but could not read private tokens.” **Say:** “The customer could read and write their own ticket, but could not read the private token table.” Replace only the corresponding sentence; keep the following deputy explanation. |

This correction scopes the customer's authority rather than implying its absence. It also makes the visible lead consistent with the existing six-step diagram and with the script's Appendix B. Keep the case labelled as a July 2025 demonstration using dummy data; it is not evidence of a current vulnerability or customer breach. [Researcher account][SB].

## R01–R22 verification

“Resolved” means the current slide and its script communicate the correction accurately; it does not require copying my original proposed wording.

| Round-1 ID | Status | Verification |
|---|---|---|
| R01 | **Open: R2-01** | The developer's elevated token access is clear, but the customer is still described as having write-only ticket access. Correct the three locations above. |
| R02 | Resolved | Slide 14 and Appendix A now report residual risk in published tests. The arbitrary-issue probability and “one in seventy” extrapolation are gone; the within-pair caveat remains. November values agree with the vendor evaluation. [Anthropic][BROWSER]. |
| R03 | Resolved | Slide 14 distinguishes probabilistic safeguards from enforced limits. Classifiers are no longer called internal model components. Notes qualify approval through the actual target and arguments shown to the reviewer. |
| R04 | Resolved | Slide 22 separates hooks without an additional execution warning from MCP consent/API-key issues. Appendix B lists GHSA-ph6w-f82w-28w6, CVE-2025-59536 and CVE-2026-21852 separately, with fixes before disclosure. This agrees with the disclosure, whose hook demo first accepted the initial trust prompt. [Check Point][CONFIG]. |
| R05 | Resolved | Slide 23 and notes scope server visibility to routed calls/its tools. The unofficial package and malicious implementation are distinguished from model-side injection. |
| R06 | Resolved | Slide 9 visibly labels the serialization schematic, and slides 9/21 notes explicitly say a fake SYSTEM line remains tool-result content. The retained lead is acceptable in that stated behavioral sense: roles do not guarantee the model obeys the intended priority. Do not teach it as absence of an API role distinction or as an impossibility proof. [Hierarchy research][HIERARCHY]. |
| R07 | Resolved | Naming is attributed to Willison in September 2022; Perez and Ribeiro are credited for studying early attacks. The original naming post predates the paper. [Original post][TERM]. |
| R08 | Resolved | Slide 13 labels the payment snippet as a teaching example. Notes distinguish published carriers from product flaws and stop claiming every general pattern was patched. Slide 22 correctly limits the patch statement to specific AWS/Anthropic findings. |
| R09 | Resolved | Slide 15 and its answer explicitly assume `.env` is readable; slide 11 notes identify both necessary grants, file-read and public write. The question now tests the intended return-channel point. |
| R10 | Resolved | Slide 19 retains `read_file` only for this run's CI log. Notes explain path, argument and credential scope, aligning the tool table with POLA. |
| R11 | Resolved | Slide 4 and its notes describe platform rollback/provider restores. They no longer assert all recovered copies were inaccessible to the agent; Replit's mistaken recovery claim is attributed. |
| R12 | **Resolved — modification accepted** | Slide 17 now says lack of authority **over the target**, removes the cryptographic signing claim, and labels the modern row “chapter scenario.” Keeping “in your usual style” is acceptable as part of this hypothetical; the bottom line says “can look like,” rather than asserting an observed indistinguishable PR. |
| R13 | Resolved | Slide 7 focuses on inbound flows and trust decisions. The legend no longer declares the authenticated developer categorically untrusted; notes distinguish principal intent, attacker-controlled content and inherited provenance. |
| R14 | Resolved | Slide 10's reach row and notes describe potential readers, usual session scope, entry route and conditional success. The retained lead is a reasonable teaching summary when delivered with those qualifications. |
| R15 | Resolved | Slide 5 bases the SQL-injection blast radius on grants and account privileges; it no longer confines damage categorically to database contents. |
| R16 | Resolved | Slide 22 uses “can” / “may” and states the file-read/network prerequisites. The diff remains explicitly hypothetical. “Config files are code” is acceptable as the configuration-review analogy in this context. |
| R17 | Resolved | Slide 25 now uses Rules File Backdoor for repository-configuration trust. Amazon Q remains a related product supply-chain example on slide 22. |
| R18 | Resolved | Slide 20 notes explicitly distinguish ASI from LLM tags and identify the two OWASP editions. |
| R19 | Resolved | Slide 23 notes stop promising that pinning guarantees discovery and explicitly warn that an already-malicious pinned version remains malicious. Controlled updates reduce exposure; endpoint-blocking assumes an egress policy that covers the server's traffic. Keep that assumption when answering Q4. |
| R20 | Resolved for draft approval | Say blocks are materially shorter; slide 15 now allocates 2:10 including the 30-second pair discussion. My extraction gives roughly 1,950 words for Part 1 and 1,400 for Part 2, about 14 and 10 minutes at 140 wpm before real pauses/transitions. Minor tokenisation differences from Claude's counts do not affect the conclusion. Rehearsal remains necessary. |
| R21 | **Resolved — modification accepted** | Keeping the canonical distinction on slide 14 and the §9.4.3 POLA rules on slide 19 respects the chapter allocation. The shorter spoken treatment on slides 22/23 avoids repeating Member 3's implementation lesson. No need to remove the visible lists. |
| R22 | Resolved | First-use glosses now cover LO on slide 2, MCP on slide 6 and RLS on slide 18, with a script glossary as well. |

## Design polish implemented

Only layout in `lecture/build/build_deck.py` changed; all wording, notes, chart values, slide count and order were preserved exactly against the round-2 input deck.

- **Slide 11:** tightened the red payload block from 1.72 to 1.46 inches high, reduced top padding, and moved the visibility note/icon upward by 0.22 inches. Kept the 11 pt code, complete payload and closing marker intact.
- **Slide 20:** stacked **Subagents** above the now single-line **spawned to work in parallel** label. Increased the container height from 0.51 to 0.64 inches and centred its icon vertically. The arrow, numbering and five taxonomy cards remain clear.
- **Slide 4:** no edit needed. All four description boxes already start at **y = 3.98 inches** with identical typography; the native coordinates and rendered baselines agree. Product-name line counts do not shift the descriptions.
- **Visual regressions:** none found in the requested changed slides. In particular, the new slide 9 explanatory caption, slide 14 headings/caption, slide 17 longer caller header, slide 19 scoped-read row and slide 22 longer final case fit without overlap or clipping.

## Build and verification

Executed from `lecture/build`:

```powershell
python build_deck.py
python assets/check_text_fit.py
powershell -ExecutionPolicy Bypass -File render_slides.ps1 -Deck ../COMP5320_Ch9_Part1-2_Slides.pptx -OutDir _render -Width 1600
python "C:/Users/Chien/.claude/skills/synced/f8b8bc25-3518-46e7-9613-b52046d2dc66_712e8ad8-06da-457b-af1e-93204e49fbda/pptx/scripts/office/validate.py" ../COMP5320_Ch9_Part1-2_Slides.pptx --original "../../COMP5320 Slide Template.pptx"
python make_grid.py _render
```

| Check | Result |
|---|---|
| Rebuild | 26 slides, notes on all 26 |
| Package validation | **All validations PASSED!** |
| PowerPoint text fit | **588 regions, 0 overflows**, 1.5 pt measurement tolerance |
| Render | All 26 slides exported at 1600 × 900 by installed Microsoft PowerPoint |
| Visual review | All 14 requested changed slides plus 11/20 inspected individually |
| Preservation | Per-slide text arrays, table cells, chart-series serialisations and notes exactly equal to the supplied round-2 input deck |
| Content edits by Codex | None; R2-01 remains a proposal for Claude |

Updated contact sheets: [1–4](../build/_render/grid-01.png), [5–8](../build/_render/grid-02.png), [9–12](../build/_render/grid-03.png), [13–16](../build/_render/grid-04.png), [17–20](../build/_render/grid-05.png), [21–24](../build/_render/grid-06.png), [25–26](../build/_render/grid-07.png).

## Evidence

The research pack remains the evidence base for the previously verified cases and framework mappings. The Supabase, November Anthropic, Check Point and original naming pages were reopened for this round; no exploit was run or downloaded.

[SB]: https://generalanalysis.com/blog/supabase-mcp-blog/
[BROWSER]: https://www.anthropic.com/research/prompt-injection-defenses
[CONFIG]: https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/
[TERM]: https://simonwillison.net/2022/Sep/12/prompt-injection/
[HIERARCHY]: https://arxiv.org/abs/2404.13208

## Verdict

**CHANGES NEEDED** — **R2-01 only:** correct the customer's read/write ticket access in slide 18's lead and the two corresponding script sentences, then rebuild and recheck slide 18 text fit/render. All other R01–R22 fixes, the modified R12/R21 decisions, and the visual design are approved.

## Round 3 sign-off

8 November 2026. Text-only verification of `claude-response-round2.md`, slide 18 in the rebuilt PPTX, its embedded notes, and the corresponding speaker-script section. No rebuild, PowerPoint operation or render was performed in this round.

**R2-01 is resolved.** The shortened lead, “The customer could access only their own ticket — the agent could read every token,” preserves the intended authority contrast within this demonstration. The script Key message explicitly includes the customer's ticket read/write access and lack of private-token access; the Say paragraph correctly distinguishes that from the developer agent's elevated authority. The embedded slide notes contain the same corrections. This now agrees with the attacker reading the copied tokens in step 6 and with the [researcher account][SB].

Claude's reported build, validation and fit checks remain the latest verification evidence; they were not repeated during the concurrent final-PDF export. No content or design issue remains open from these review rounds.

**Final verdict: APPROVED.** This sign-off supersedes the round-2 CHANGES NEEDED verdict above.
