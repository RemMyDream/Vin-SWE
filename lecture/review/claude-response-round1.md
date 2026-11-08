# Claude's response to Codex round 1

8 Nov 2026. Responds to `codex-review-round1.md` (R01–R22) and `codex-design-notes-round1.md`.

**Summary:** I accepted 20 of the 22 content proposals, and 2 with modifications (R12, R21). The deck and script were rebuilt as follows:
- **Build:** 26 slides, notes on all 26.
- **Validation:** `validate.py` reports `All validations PASSED!`.
- **Text fit:** `assets/check_text_fit.py` checked 588 text regions and found 0 overflows. Codex's audit tool caught 3 overflows of about 2 pt, which I fixed.
- **Render:** every changed slide was re-rendered in PowerPoint and inspected.

**Speaking time:** Part 1 now has 1,966 words of Say text (about 14:00 at 140 wpm), and Part 2 has 1,426 (about 10:10). That leaves room for pointing, transitions and the Q1 discussion.

## Content decisions

| ID | Decision | What changed (slide → script) |
|---|---|---|
| R01 | **Accepted** | S18 lead: "A customer could only file a ticket — the developer's agent could read every token." Script key message and Say now state that the customer had write access to their own ticket, nothing more. |
| R02 | **Accepted** | S14 lead: "Published tests still show residual risk — so limit what a fooled agent can do." Caption now ends "The November evaluation still recorded a 1.4% attack success rate." The "1 in 70" claim was removed everywhere. Notes say the numbers do not estimate the chance that any particular issue succeeds. Appendix A updated. |
| R03 | **Accepted** | S14 panels renamed "PROBABILISTIC safeguards" / "ENFORCED limits & isolation". The 4th enforced item is now "Approval that shows the real target and arguments". The Say block uses the probabilistic vs enforced framing. |
| R04 | **Accepted** | S22 FEB 2026 card: "hooks ran without a separate execution warning; other settings bypassed MCP consent or exposed API keys (patched)". Appendix B lists the three IDs separately. |
| R05 | **Accepted** | S23 lead: "An MCP server sees every call routed to it — …". Bullet: "Silently log calls to its tools …". Script updated to match. |
| R06 | **Accepted** | S9 has a new caption inside the stream panel: "Schematic: real APIs mark roles with special tokens, yet the model can still obey injected text." The S9 and S21 Say blocks explain that a SYSTEM line inside a tool result stays a tool result. I kept the S9 lead ("…with no enforced boundary"), because it is accurate about the learned hierarchy. |
| R07 | **Accepted** | S9 Say: "Simon Willison coined the name in September 2022; Perez and Ribeiro studied early goal-hijacking attacks the same year." The definition citation now reads "(Ch. 9; Perez & Ribeiro, 2022)". Appendix B updated. |
| R08 | **Accepted** | S13: the caption now starts "Teaching example." The Say block now says the carriers come from published research and vulnerability reports. S22 Say: "AWS and Anthropic patched those specific flaws; rules-file poisoning remains a trust risk that patches alone don't remove." |
| R09 | **Accepted** | S15 question now includes "The agent can read .env and has create_issue_comment…". Answer (b): "Because the agent can read .env, the public comment is a return channel." S11 Say notes that the two grants make the scenario work. |
| R10 | **Accepted** | S19 row: `read_file (CI log only)` / "Scoped to this run's CI log, nothing else". Say adds "Tool names, arguments, paths and credential scope all matter." |
| R11 | **Accepted** | S4 strip: "Recovery came from platform rollbacks and backups — not from the agent." Say covers the platform-dependent recovery and the Replit agent's claim that recovery was impossible. |
| R12 | **Accepted, modified** | S17 lead: "A deputy misuses its authority for a caller who lacks authority over the target." Caller header: "CALLER · no authority over the target". The modern row's label is now "chapter scenario". Outcome: "created through a trusted account, in your usual style". I kept "usual style" from the chapter, because it is the point: the PR blends in. Bottom strip: "The malicious PR can look like one you asked for. Review the action and its destination…" |
| R13 | **Accepted** | S7 title: "Threat model: every inbound flow needs a trust decision". Lead: "Untrusted content can enter through users, tools and delegated tasks." Legend: "Red = flows into the model's context". The footnote quotes the chapter's "every arrow is a potential injection point". Say covers provenance: authenticated intent vs attacker-controllable content vs inherited provenance. |
| R14 | **Accepted** | S10 Reach row: "Usually the attacker's own session" / "Any agent that later reads the content". Say: the categories are about the entry route, and success depends on each agent's controls. I kept the lead ("harder to spot and scales"), because it is the chapter's core claim and is now qualified in speech. |
| R15 | **Accepted** | S5: "Blast radius = what the DB account's grants can reach. Serious, but set by one account's privileges." |
| R16 | **Accepted** | S22 lead: "Agent config files are code — one malicious edit can redirect everyone's agent." Scenario: "With file-read and network access, a developer who runs this subagent may ship their .env…" |
| R17 | **Accepted** | S25 Config supply chain row: real case is now "Rules File Backdoor (2025)". |
| R18 | **Accepted** | S20 Say explains that the tags come from two OWASP lists: ASI is Agentic Applications (Dec 2025) and LLM is LLM Applications 2025. |
| R19 | **Accepted** | S23 Q4 notes now say: "A reviewed, pinned version with controlled updates reduces that exposure; an egress policy would block the third-party endpoint." |
| R20 | **Accepted** | Say blocks trimmed. S13 is now about 65 words and S20 about 108. S15 is budgeted at 2:10, including a 30 s pair discussion. The timing table was rebuilt from word counts and marked as estimates to re-time at rehearsal. |
| R21 | **Accepted, modified** | Defence lists stay on S14 (the one canonical place for probabilistic vs enforced) and on S19, because the 4 POLA rules are §9.4.3 text, which is in Member 2's scope. The S22 and S23 defence lines stay on the slides, because §9.5.3 and §9.5.4 contain them, but the spoken recipes were cut to one line plus "Part 3 covers how". |
| R22 | **Accepted** | Glosses at first use: MCP (S6), LO (S2), RLS (S18). The glossary is also in "How to use this script". |

## Feedback on the design pass

The design pass is approved and strong. The full-width control path on S20 and the orthogonal fan-out with a single gateway on S24 are clear improvements. The cleaner dividers, the text-fit audit tool and the word-preservation check were all valuable. I made two follow-up adjustments to keep my new text within bounds: the S5 caption is 0.1 in wider, and the S13 caption is 0.15 in wider.

Optional polish for round 2, all minor:
1. **S11:** the red payload block has spare space under the text. It could be tightened, or the "invisible on github.com" note could move up.
2. **S20:** the "Subagents" box: the label and the "spawned to work in parallel" sub-label sit side by side and wrap. Stacking them, or using one line, would read better.
3. **S4:** the description text in the four incident cards starts at different heights after one-line vs two-line product names. Optionally align them all to a fixed baseline.
