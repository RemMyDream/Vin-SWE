# Codex content review — round 1

8 November 2026. Reviewed all 26 slides, the complete speaker script (including Q&A and accuracy guardrails), the research pack, and roadmap §5. **Proposals only:** none of the corrections below has been applied to slide wording or the script. The separate design pass preserves the existing content.

**Recommendation:** keep the two anchors and the present order. No P0 found; resolve the P1 access-boundary and evidence claims before teaching. The strongest teaching moment is the same flow twice: public issue → private repository → public PR, then customer ticket → private tokens → customer-visible reply. The deck already distinguishes demonstrations from customer breaches and correctly qualifies the opening incident dates, disputed Kiro attribution, recovery, and the Amazon Q payload's failure to execute. See [research notes](../research/research-notes-M1-M2.md).

## Findings and concrete proposals

P0 = must fix; P1 = should fix; P2 = nice to improve. “Notes” includes the script's Key message, Say, If asked, and Appendix A where relevant. Replacement leads below fit the intended short, single-line style; Claude should mirror accepted changes in the script and rebuild.

| ID | Slide | Severity | Issue | Concrete proposed fix |
|---|---|---|---|---|
| R01 | 18 + notes | **P1** | “The attacker had no database access” erases the crucial boundary. The customer could create/read their own support records through an RLS-restricted role; they lacked access to private tokens. [Researcher actor table][SB]. | Lead: **“The customer could access their ticket; the developer's agent could read private tokens.”** Key message: “The customer could write ticket data but could not read the token table.” Keep the existing four-lane chain. |
| R02 | 14 + Appendix A | **P1** | “Defences … never reach zero” is a universal claim, while the chart establishes residual risk in particular evaluations. “One attack in seventy” then implies a calibrated rate for arbitrary issues or repeated independent trials. These were internal browser tests with an adaptive attacker and defined budgets. [November evaluation][BROWSER]. | Lead: **“Browser tests still show residual risk — so limit what a fooled agent can do.”** Caption ending: **“The November evaluation still recorded a 1.4% attack success rate.”** Notes: “These results do not estimate the chance that any arbitrary issue succeeds.” Appendix A: “Published tests still show residual risk.” Preserve both pairs and the within-pair caveat. |
| R03 | 14 + notes | **P1** | “SOFT · inside the model” includes classifiers on tool results; such safeguards can be separate surrounding components. Conversely, an approval gate can be enforced while the human decision remains fallible. The location of a control and its guarantee are different dimensions. [Anthropic describes surrounding classifiers][BROWSER]. | Headings: **“Probabilistic safeguards”** and **“Enforced permissions & isolation.”** Say: “Prompts, training and classifiers reduce model failures. Permissions, isolation and approval gates constrain which actions can execute; reviewers still need the actual target and arguments.” Avoid promising that every item labelled hard guarantees safe outcomes. |
| R04 | 22 + notes | **P1** | The February Claude Code line conflates three bugs and says hooks ran before repository trust. The hook demonstration first accepted the initial trust dialog; separate findings concerned MCP consent bypass and API-key routing before trust. They were fixed before public disclosure. [Primary disclosure][CONFIG]. | Card: **“Claude Code project files: hooks ran without a separate execution warning; other settings bypassed MCP consent or exposed API keys (patched).”** Notes: “Hooks required initial repository trust but lacked specific execution consent (GHSA-ph6w-f82w-28w6). Separate bugs affected MCP consent (CVE-2025-59536) and API-key routing (CVE-2026-21852).” Do not group all under one CVE. |
| R05 | 23 + notes | **P1** | “An MCP server sees every agent call” implies protocol-wide visibility. A server normally sees requests routed to itself; malicious local code may gain more through its process permissions, a different mechanism. [Postmark server/tool example][POSTMARK]; [MCP tools specification][MCP]. | Lead: **“An MCP server sees calls routed to it — a malicious update can copy their contents.”** Notes: “The server receives calls to its own tools, including their parameters.” Bullet: “Silently log calls to its tools — including secrets in parameters.” |
| R06 | 9 + notes; 21 | **P1** | The literal XML-like tags in the diagram are a teaching serialization. “Role tags are just more tokens” can suggest attacker text `SYSTEM:` actually becomes an API system message, or that real role separation has no effect. The hierarchy is trained behavior; spoofed authority is still lower-trust content. [Instruction hierarchy paper][HIERARCHY]. | Add notes: **“The tags are schematic. Tool-result text that says SYSTEM does not acquire the API's system role; the failure is the model obeying lower-trust content despite the intended hierarchy.”** Lead on 9: “Roles distinguish instructions from data; the model can still obey injected data.” Keep external enforcement as the conclusion. |
| R07 | 9 notes | **P1** | “The term comes from Perez and Ribeiro, 2022” is misattributed. Willison explicitly proposed the name on 12 September, before the November paper. [Original post][TERM]; [paper][PEREZ]. | **“Perez and Ribeiro studied early goal-hijacking and prompt-leaking attacks in 2022.”** If mentioning naming: “Simon Willison proposed the term in September 2022, building on Riley Goodside's examples.” No need to add another visible citation if naming is removed. |
| R08 | 13 + 22 notes | **P1** | “Each was disclosed and then patched or mitigated” / “All of these were patched” blurs conventional fixed vulnerabilities, general research patterns, and the hypothetical payment-module snippet. A universal fix was not established for rules-file backdoors or tool poisoning. [Pillar][RULES]; [Invariant][TP]. | Opening on 13: **“These carriers appear in published research and vulnerabilities; the code snippet is a teaching example.”** On 22: “AWS and Anthropic patched the specific product flaws; rules-file poisoning remains a configuration-trust risk.” Keep the payload explicitly hypothetical. |
| R09 | 15 + Q1 answer | **P1** | Q1 explicitly supplies a comment tool but never establishes whether `.env` can be read. The answer unconditionally says exfiltration succeeds, overlooking the roadmap's main permission dependency. | Add to the question: **“Assume read_file can read .env, and create_issue_comment posts publicly.”** Answer (b): **“Yes, if the agent can read .env: the public comment is a return channel.”** Alternatively ask students to identify that missing capability first. This makes the read boundary visible before Part 2. |
| R10 | 19 + notes | **P1** | “Minimum toolset? Just read_file” scopes a tool name but leaves all files potentially readable. This conflicts with the otherwise excellent POLA explanation that unrelated resources should be unreachable. [Hardy][HARDY]. | Table row: **“read_file scoped to the CI log”**; notes: **“Grant read access only to the relevant CI log or a task-specific view, for this task's duration.”** Add “Tool names, arguments, paths and credential scope all matter.” Keep detailed configuration for Part 3. |
| R11 | 4 notes | **P1** | “In three cases … only because a provider had a backup the agent could not reach” overstates a shared recovery mechanism. Replit's normal rollback succeeded after the agent had said recovery was impossible; that is not proof the backup was inaccessible to it. [Replit reporting][REPLIT]. | **“Three cases recovered data through rollback or provider-assisted restores. Recovery depended on the surrounding platform, rather than on the agent's assurance that recovery was impossible.”** The visible recovery wording can remain. |
| R12 | 17 + notes | **P1** | “Someone who has none” means no authority at all, whereas the caller lacks authority for the target resource. The hypothetical PR being “signed” and “exactly like” an authorised PR is also not guaranteed. Authentication and cryptographic signing do not prove task authorisation. [Hardy][HARDY]. | Lead: **“A deputy misuses its authority for a caller who lacks authority over the target.”** Outcome: **“PR with an auth backdoor — created through a trusted account.”** Bottom: “The PR can appear to come from a trusted workflow. Review the requested action and its destination.” Label the modern row hypothetical. |
| R13 | 7 + notes | **P2** | “Every arrow” includes outbound calls; red also includes an authorised developer and delegated content. “The agent trusts … all” describes a possible failure, not all implementations. The DFD should expose provenance and trust transitions. | Title: **“Threat model: every input flow needs a trust decision.”** Lead: “Untrusted content can enter through users, tools and delegated tasks.” Legend: “Red arrows = flows requiring a provenance and authority check.” In speech distinguish authenticated developer intent from attacker-controlled retrieved content; delegated content inherits its provenance. |
| R14 | 10 + notes | **P2** | “One session” versus “every agent and user” is too categorical. Direct injection can affect persistent state; reading an indirect payload does not ensure compliance. Entry route defines the categories. [OWASP LLM01][OWASP]; [Greshake et al.][GRESH]. | Reach row: **“Submitted through the attacker's interaction”** / **“Can be encountered by multiple readers.”** Lead: “Indirect injection arrives through content a legitimate task asks the agent to read.” Notes: “One poisoned item can be reused across readers, with success depending on each agent's controls.” |
| R15 | 5 + notes | **P2** | “Bounded by one system's privileges” could reinstate the chapter's overly simple SQL boundary. SQL injection can reach host facilities or other systems depending on the account's privileges. [OWASP][SQLI]. | Replace with **“Its blast radius depends on the database account's privileges and reachable systems.”** Contrast the concrete grants and composed tools rather than implying all agents exceed all traditional apps. |
| R16 | 22 lead + scenario | **P2** | “Every user's agent” and “silently ships” omit the required file-read, network and tool authority. Config is a behavioral control surface; a malicious instruction is not certain to execute on every client. [Rules-file demonstration][RULES]; [project-config findings][CONFIG]. | Lead: **“Shared agent configuration is a control surface — a malicious edit can redirect the workflow.”** Scenario ending: “With file-read and outbound authority, a developer running this subagent may expose .env.” Retain the explicit hypothetical label and the exact file examples. |
| R17 | 25 config row | **P2** | Amazon Q's compromised product release is a valid supply-chain case, but it does not directly evidence the row's “trust in repo config files.” [AWS bulletin][AWS]. | Use **“Rules File Backdoor (2025)”** in this row, or widen the row's abused trust to **“Agent configuration and release pipeline.”** Keep Amazon Q on 22 as a related product supply-chain contrast. |
| R18 | 20 notes | **P2** | Notes say all grey tags belong to the Agentic Top 10, but the covert-channel tag is LLM02 from the separate LLM 2025 list. The slide source already cites both. [OWASP lists][OWASP]; [Agentic edition][ASI]. | **“The tags map vectors to two OWASP lists: ASI means Agentic Applications 2026; LLM means LLM Applications 2025.”** Name each edition aloud once. |
| R19 | 23 Q4 notes | **P2** | “Pinning plus reviewing updates would have caught it” promises detection; pinning only blocks an unreviewed change if the pinned artifact is already authentic and safe. The script does correctly warn about pinning malicious versions earlier. [Postmark][POSTMARK]. | **“A reviewed, pinned artifact and controlled updates would reduce exposure to an unnoticed malicious release. Egress policy would block this endpoint if it covered the server's outbound traffic.”** Treat the three-month scenario as a textbook hypothetical. |
| R20 | 1–25, timing plan | **P1** | The spoken script is close to the 31-minute budget before pauses and transitions. Q1's 30-second peer discussion alone makes its 1:15 allocation implausible at the script's stated pace. See estimates below. | Rehearse using the actual Say blocks. Protect ~2 minutes per anchor and ≥30 seconds for Q1; trim the carrier catalogue and repeated defence lists first. Replace the “≈2 min buffer” with a measured buffer after rehearsal. Do not solve this by rushing the case chains. |
| R21 | 8, 14, 19, 21–23, 25 | **P2** | The repeated implementation lists teach much of Member 3's stated scope (least privilege, sandbox, approvals, logging, secure prompting). Brief controls help explain the mechanism, but full recipes add repetition and timing pressure. See roadmap §5 and §4 member allocation. | Keep POLA as the concept on 19 and one counterfactual broken link per anchor. On 14 state the probabilistic-versus-enforced distinction once; summarise other lists orally as “Part 3 implements these.” Leave `CODEOWNERS`, hash checks, pinned command syntax, sandbox configuration and logging design for Member 3. |
| R22 | 2, 13, 26 | **P2** | Several acronyms appear before explanation: LO, MCP, RLS, PAT/credentials and ASI. The terminology is manageable, but the audience benefits from short first-use glosses. References are useful as a handout, not a live reading slide. | On first speech use: **“Model Context Protocol, the interface connecting the agent to tools”; “row-level security, rules limiting which records a database role can access”; “learning objective.”** Retain “references not presented” and link the research pack in the distributed materials. |

## Disagreements with the chapter or v1 decisions, with evidence

- **Residual risk is an empirical finding, not an impossibility theorem.** Keep the chapter's architectural message, but replace “never zero” with the measured claim in R02. The [November report][BROWSER] explicitly describes an internal adaptive evaluation and continued research; [NCSC][NCSC] argues that full mitigation may be infeasible rather than proving impossibility.
- **A database boundary is a permission boundary, not the absence of all access.** R01 and R10 are essential to the confused-deputy lesson: the [Supabase actor table][SB] gives the customer limited write authority and the developer elevated SQL authority. [Hardy][HARDY] concerns the authority used for a particular resource.
- **A protocol server is not the whole runtime.** R05 preserves the malicious-server argument while scoping visibility to requests delivered to that server. The [tools specification][MCP] describes named tool calls and server-side execution; it does not give a server automatic visibility into unrelated servers or local tools.
- **Specific implementation bugs and semantic injection patterns need different language.** The [Check Point disclosure][CONFIG] distinguishes hooks, MCP startup consent, and pre-trust API routing; the [Pillar demonstration][RULES] establishes a wider configuration-poisoning risk. Do not label all configuration attacks “prompt injection” or suggest one generic patch fixed them.
- **Keep the corrections v1 already made.** Recovery qualifications, the 26 February Terraform date, disputed Kiro causation, distinct OWASP editions, and the distinction between GTG-1002 misuse and victim-side injection are sound. The research pack's [chapter-corrections table](../research/research-notes-M1-M2.md#8-chapter-corrections--caveats) remains the source of detailed evidence.

## Flow, timing and Part 3 boundary

Local estimate: extracted only each **Say** block, stopping before **If asked** or **Transition**; counted words and divided by the script's stated 140 words/minute. Estimates include printed pause directions as a few words, but not their real elapsed pause. They are rehearsal guidance, not measured delivery times.

| Segment | Say words | Reading estimate | Available | Implication |
|---|---:|---:|---:|---|
| Part 1, slides 1–15 | ~2,298 | ~16:25 | 18:00 | ~1:35 remains for all transitions, diagram pointing, and Q1 discussion/answers. Tight but feasible after trimming. |
| Part 2, slides 16–25 | ~1,666 | ~11:54 | 13:00 | ~1:06 for transitions, diagram explanation and pauses. Protect the Supabase sequence. |
| Slide 15 alone | ~210 | ~1:30 | 1:15 | Adding the requested 30-second peer pause takes it to ≥2:00, before answers. |
| GitHub anchor, slide 12 | ~268 | ~1:55 | 2:00 | Appropriate protected time. |
| Supabase anchor, slide 18 | ~255 | ~1:49 | 2:00 | Appropriate, with only a little time to trace arrows. |
| Config + MCP, slides 22–23 | ~456 | ~3:15 | 3:00 | Shorten the repeated defensive recipes rather than removing the causal explanation. |

The running example and two anchors meet the roadmap's issue-triage through-line. Preserve the progression **data enters → model follows it → deputy supplies authority → public/customer-visible output**. R09 explicitly restores the sensitive-file-read dependency. A useful question on each anchor is “Which single grant could we remove and still finish the legitimate task?” Detailed enforcement and rollout belong to Member 3.

No extra cases, slides, benchmark chart, or research-paper survey is needed in this 31-minute segment. AgentDojo and InjecAgent can remain reserve evidence for Member 4's research connection. The present month-level dates for Supabase and GitLab avoid inconsistent page metadata.

## All-slide coverage

| Slide | Review result / visual explanation |
|---|---|
| 1 | Course identity and scope clear; shorten spoken greeting during rehearsal. |
| 2 | Agenda matches 18 + 13 minutes and the team roadmap; first-use acronym glosses R22. |
| 3 | Divider; no content issue. |
| 4 | Incident attributions and visible recovery caveats are appropriate; recovery mechanism in notes R11. |
| 5 | Diagram communicates composed authority; qualify the traditional-app comparison R15. |
| 6 | STRIDE examples are clear; keep the existing statement that one attack can map to several letters. |
| 7 | Useful data-flow diagram; provenance and direction caveat R13. |
| 8 | Trifecta picture is an effective risk heuristic; keep “external” inclusive of comments and DNS. Avoid treating it as a complete taxonomy of all agent harm. |
| 9 | Role-to-context explanation needs the schematic/authority nuance R06 and naming correction R07. |
| 10 | Two entry routes visually clear; scope and reach wording R14. |
| 11 | Strong victim-view versus reality split; scenario appropriately labelled as adapted/paraphrased. Its outcome assumes readable secrets and public write authority. |
| 12 | Best M1 anchor; clear researcher-demonstration label and five-step chain. Preserve time for reading the private→public crossing. |
| 13 | Effective carrier catalogue; qualify patching and hypothetical code R08. Treat as a brief overview. |
| 14 | Chart correctly compares within pairs; fix inference and defence labels R02–R03. |
| 15 | Good diagnostic question; establish read authority R09 and allow actual discussion time R20. |
| 16 | Divider and handoff clear; no content issue. |
| 17 | Classic/modern parallel works; authority, signing and hypothetical status R12. |
| 18 | Best M2 anchor; swimlane explains the return channel; essential access correction R01. |
| 19 | Useful tool-removal table; scope the retained read capability R10. |
| 20 | Map now has numbered surfaces matching five cards; distinguish the two OWASP tag editions R18. |
| 21 | Hierarchy-spoofing example and DNS case support the lead; explain that spoofed SYSTEM text remains data R06. Distinguish visible exfiltration from hidden encoding in speech. |
| 22 | Hypothetical diff connects to team project; bug-family and patch qualifications R04/R08/R16. |
| 23 | Strong “model behaves correctly, malicious server steals” contrast; server visibility and counterfactual caveats R05/R19. |
| 24 | Correctly separates researcher worm demonstrations from GTG-1002 misuse. Notes already state propagation is conditional. The single gateway is a diagram shorthand for policy at delegation, not proof that a classifier guarantees containment. |
| 25 | Good handoff matrix; align the config example with the row's precise scope R17. |
| 26 | All references retained; appropriate as a distributed reference page rather than a spoken slide. |

## Evidence links

Sources were checked in the research pack; the Supabase, November Anthropic, Check Point and original term-naming pages were reopened for this review. The additional MCP specification link was checked for the server/tool scope point.

[SB]: https://generalanalysis.com/blog/supabase-mcp-blog/
[BROWSER]: https://www.anthropic.com/research/prompt-injection-defenses
[CONFIG]: https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/
[TERM]: https://simonwillison.net/2022/Sep/12/prompt-injection/
[PEREZ]: https://arxiv.org/abs/2211.09527
[HIERARCHY]: https://arxiv.org/abs/2404.13208
[GRESH]: https://arxiv.org/abs/2302.12173
[RULES]: https://www.pillar.security/blog/new-vulnerability-in-github-copilot-and-cursor-how-hackers-can-weaponize-code-agents
[TP]: https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks
[POSTMARK]: https://postmarkapp.com/blog/information-regarding-malicious-postmark-mcp-package
[HARDY]: https://people.cs.vt.edu/~kafura/cs6204/Readings/ConfusedDeputy.pdf
[REPLIT]: https://www.theregister.com/software/2025/07/21/vibe-coding-service-replit-deleted-production-database/719783
[OWASP]: https://genai.owasp.org/llm-top-10/
[ASI]: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
[SQLI]: https://owasp.org/www-community/attacks/SQL_Injection
[AWS]: https://aws.amazon.com/security/security-bulletins/AWS-2025-015/
[NCSC]: https://www.ncsc.gov.uk/blog-post/prompt-injection-is-not-sql-injection
[MCP]: https://modelcontextprotocol.io/specification/2025-06-18/server/tools
