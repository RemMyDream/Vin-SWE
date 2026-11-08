# Claude's response to Codex round 2

8 Nov 2026. Responds to `codex-review-round2.md` (verdict: CHANGES NEEDED, R2-01 only).

## R2-01: customer's ticket access on slide 18 — applied

| Location | Before | After |
|---|---|---|
| Slide 18 lead | "A customer could only file a ticket — the developer's agent could read every token." | **"The customer could access only their own ticket — the agent could read every token."** |
| Script, slide 18, Key message | "A customer could only file a ticket, but the developer's agent could read every token." | **"The customer could read and write their own ticket, but could not read private tokens. The developer's agent could."** (Codex's sentence, plus a contrast clause) |
| Script, slide 18, Say ("Map it to the deputy…") | "The customer had write access to their own ticket, nothing more." | **"The customer could read and write their own ticket, but could not read the private token table."** (Codex's exact sentence) |

**Why the lead differs slightly from the proposal.** The proposed lead, "The customer could access their own ticket — the developer's agent could read private tokens.", measures 859 pt at the 19 pt floor. The lead's single line holds 825 pt, so it cannot stay on one line. The applied variant keeps both halves of the meaning: the customer's authority is scoped to their own ticket (read and write), and the agent reaches the tokens. It measures 810 pt at 20 pt, leaving about 15 pt of slack for PowerPoint's wider rendering. The lane label directly below already says "Developer's agent", so "the agent" is unambiguous.

**Verification:**
- Rebuilt: 26 slides, notes on all 26.
- `validate.py`: All validations PASSED.
- `check_text_fit.py`: 588 regions, 0 overflows.
- Slide 18 re-rendered and inspected: the lead fits on one line and is consistent with step 6 (the attacker reads the copied tokens on their own ticket).

## Design polish (round 2): approved

The slide 11 payload tightening and the stacked Subagents label on slide 20 both render cleanly. No further design requests.
