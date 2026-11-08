# Security of Agentic AI Coding Tools — presenter notes

Body typeface: Montserrat. Titles and key information: Poppins. Code: Consolas.

Presentation roster: Bui Khac Chien — V2026003377; three name/ID placeholders remain editable.

Each attack case traces input → agent → authority/tool → impact, then explains the failed boundary.


## Slide 1 · Cover

**Say:**
Today we examine how agentic coding tools can be redirected through text, configuration and tools. We will follow concrete attack flows, identify the authority each attack uses, and explain which boundary failed.

---


## Slide 2 · Where Parts 1–2 fit in today's lecture

**Say:**
Part 1 covers why security changes when an agent can use tools, how to model the threat, and how direct and indirect prompt injection work. Part 2 follows the confused deputy, authority spoofing, covert exfiltration, configuration poisoning, MCP attacks and autonomous amplification. One running example connects them: an agent summarises public GitHub issues while holding private reads and public writes.

---


## Slide 3 · Part 1 divider

**Say:**
Part 1: foundations. We start with the systems and credentials an agent can reach.

---


## Slide 4 · No attacker needed: four agent incidents in ten months

**Key message:** A trusted agent with real credentials and one destructive action is enough for an incident. No attacker is needed.

**Say:**
Before we talk about attackers, look at four incidents that had none.

- July 2025: Replit's agent ignored an explicit code freeze and deleted a production database of about 1,200 executive records.
- December 2025: reports linked Amazon's Kiro agent to a 13-hour Cost Explorer outage. Amazon disputes this and blames a misconfigured role, which is itself a permissions story.
- February 2026: Claude Code ran `terraform destroy` against production and wiped nearly two million rows in one table.
- April 2026: a Cursor agent made one API call that deleted a startup's database and its volume-level backups. The founder says it took nine seconds.

Notice two things. First, the number on the right: zero attackers. The agent was trusted, the credentials were real, and the action was destructive. Second, three of the four got their data back through platform rollbacks or provider restores. Recovery came from the surrounding platform, not from the agent. In the Replit case, the agent had even claimed recovery was impossible.

Functional correctness is not safety. If an agent can do this by mistake, imagine it being steered.

**If asked:** *Were these "irreversible". Were they?* They were destructive and high-consequence. Data in three cases was recovered later through infrastructure outside the agent.

**Transition:** So what changed compared with normal software?

---


## Slide 5 · Why agents are a security inflection point (1.1)

**Key message:** The rule is the same as ever, but the blast radius is far larger.

**Say:**
Security has always meant one thing: a system should do exactly what it was designed to do, and nothing more. What changed is the blast radius.

On the left is a classic SQL injection. The damage depends on what that database account's grants can reach. That is serious, but it is set by one account's privileges.

On the right is an agent with tools and credentials. Influence it, and you inherit everything it can do. You can read and exfiltrate files, commit code, push to production, open pull requests in someone's name, call APIs with their credentials, and even spawn more agents. Its power to take many steps across many tools is exactly what makes it dangerous when misdirected.

So security is a design constraint from the first line of configuration, not a retrofit.

**Transition:** To design for this, we need a threat model.

---


## Slide 6 · Threat-modelling an agent: who, what, how (1.2)

**Key message:** List who can reach the agent, what they want, and how they get in. Then use STRIDE as a checklist.

**Say:**
A threat model answers three questions.

Who attacks? Anyone who can put text where the agent reads: an issue author, a web page, a package or MCP maintainer, even a teammate's pull request. MCP is the Model Context Protocol, the standard way to plug tools into an agent.

What do they want? Secrets, code, production data, and the agent's own identity, because the agent can act as you.

How? Through every information flow into the agent's context.

STRIDE still works if you map it to agents. Read the tiles left to right:
- Spoofing: text posing as "SYSTEM".
- Tampering: an edited AGENTS.md.
- Repudiation: "the agent did it", with no log.
- Information disclosure: your `.env` in a public comment.
- Denial of service: a dropped database.
- Elevation of privilege: the attacker borrows the agent's credentials. That is Part 2.

One attack can hit several letters at once. STRIDE is a checklist, not a classifier.

**Transition:** Now let's draw the flows.

---


## Slide 7 · Threat model: every inbound flow needs a trust decision (1.2)

**Key message:** Untrusted content can enter through users, tools and delegated tasks, so each inbound flow needs a trust decision.

**Say:**
This diagram maps the agent's data and control flows. The developer instructs an orchestrator agent. The orchestrator calls local tools and external ones, such as MCP servers, databases and issue trackers, and delegates work to subagents.

The dashed box is the key: the model reads everything inside it as text. The red arrows are flows into that context:
1. user input,
2. files, code and web pages,
3. delegated context,
4. MCP, database and issue results.

Every inbound flow needs a trust decision: where did this text come from, and what authority should it carry? The developer's request is authenticated intent. An issue body is attacker-controllable content. Delegated context inherits the provenance of whatever went into it.

**Transition:** Here is a quick test for the most dangerous combination.

---


## Slide 8 · A quick risk test: the lethal trifecta

**Key message:** Private data, untrusted content and external communication together make data theft possible. Remove any one leg.

**Say:**
Simon Willison calls this the lethal trifecta. An agent is at risk of data theft when it has all three:
- access to private data,
- exposure to untrusted content,
- a way to communicate externally.

Our triage agent has all three. It can read `.env`, it reads public issues, and it can post comments.

Break any one leg and this exfiltration path breaks. Meta's 2025 Agents Rule of Two turns that into a design rule: in one session, give an agent at most two of the three properties, and add human approval if a task truly needs all three.

External communication isn't just HTTP. A pull request, a comment or a DNS lookup counts too, and that matters in the cases ahead.

**Transition:** So how does untrusted content take control? That's prompt injection.

---


## Slide 9 · Prompt injection: one channel for instructions and data (1.3)

**Key message:** Instructions and data arrive as one token stream, with no enforced boundary.

**Say:**
Prompt injection means malicious instructions hidden in content the agent processes, so it follows the attacker instead of the user, or as well as the user. Simon Willison coined the name in September 2022, and Perez and Ribeiro studied early goal-hijacking attacks the same year.

On the left is how we design it: separate roles for system rules, the user's request, and a tool result such as an issue body. On the right is what the model receives: one context. The tags are schematic. Real APIs mark roles with special tokens, and a line saying "SYSTEM" inside an issue does not become a real system message. The failure is that the model can still obey that lower-trust text.

Compare SQL injection. Parameterised queries give a hard boundary. LLMs have no equivalent yet: the role hierarchy is learned, not enforced. So the status is "mitigated, not solved". The UK's NCSC says prompt injection is not SQL injection, and may be worse.

**Transition:** The attacker's text can get in two ways.

---


## Slide 10 · Direct vs indirect prompt injection (1.3)

**Say:**
The top row shows direct injection: a user submits a malicious task instruction, the agent obeys it, file-read and network tools access a local key, and the key leaves the workspace. The local key belongs to the agent's environment, not necessarily to the person typing the task. This is an illustrative flow, not a reported breach.

The lower row shows indirect injection: an attacker plants a request in a public issue; a legitimate issue-summary task makes the agent read it; file and comment tools publish .env; the attacker reads the public comment.

The entry route defines direct versus indirect. Neither route guarantees success. The attack succeeds only if the agent follows the instruction and the necessary read and output authority exists. Removing fetch_url does not prevent a public comment from being the return channel.

---


## Slide 11 · Running example: the poisoned GitHub issue (1.3)

**Key message:** A routine summary task becomes secret exfiltration, and nobody notices.

**Say:**
Issue 247 looks like a normal performance report. Inside it, a block claims to be a SYSTEM message asking the agent to read `.env` and post it as a comment, as a "routine diagnostic". Wrapped in an HTML comment, it's invisible on github.com, but the agent reads the raw text.

Follow the steps:
1. The developer asks for a summary.
2. The agent reads issue 247.
3. It reads `.env`.
4. It posts the contents as a public comment.
5. It returns a tidy, accurate summary.

The developer sees a helpful summary, while the secrets are now public. Nothing in the output looks wrong.

This works only because two grants are present: the agent can read `.env` and it can post publicly. Keep those two grants in mind.

**Transition:** Is this just a textbook story? No. Researchers demonstrated almost exactly this in 2025.

---


## Slide 12 · Real case: GitHub MCP "toxic agent flow" (May 2025)

**Key message:** A malicious public issue made an agent leak private-repo data into a public PR. The cause was the architecture, not a bug.

**Say:**
In May 2025, Invariant Labs demonstrated what they called a "toxic agent flow" with the official GitHub MCP server. The setup had one public repo and several private ones, Claude Desktop running Claude 4 Opus, and tool calls set to always-allow.

Walk the chain:
1. The attacker files an issue in the public repo, framed as a friendly "about the author" request.
2. The developer says, "have a look at the open issues in my public repo".
3. The agent reads the issue and is injected.
4. With the developer's token, it reads the private repositories.
5. It opens a pull request in the public repo containing the private information, so now anyone can read it.

Why did it work? One token reached every repo, which is ambient authority. Untrusted issue text went straight into the context. And a public PR is an exfiltration channel. All three trifecta legs were present.

What did not fail matters too. The MCP server worked as designed, so there was no bug to patch. A strongly aligned model still followed the injection. Per-call approvals existed but were set to always-allow.

What would have stopped it?
- A repo-scoped token, so private repos are out of reach.
- A read-only summariser, with no PR or comment tool.
- A human reviewing the actual diff and where it goes.

This was a controlled demonstration, not a customer breach, but it shows the mechanism exactly.

**If asked:** *Couldn't GitHub just patch it?* There is nothing to patch in the server. The fix is to scope authority and control where data flows: private content should not reach a public sink without review.

**Transition:** Issues are just one carrier.

---


## Slide 13 · Injection hides wherever the agent reads (1.3)

**Say:**
The six cards trace different carriers into an impact. A public issue can lead to a private-repository read and a public pull request. A README can change approval settings and enable shell execution. A webpage can alter an answer through hidden instructions. An email can make retrieved context leave through an image URL. A poisoned rule can change generated HTML. Tool metadata can cause a file read and send secrets as tool arguments.

The payment-module snippet is an illustrative example: a review request is turned into a logging command that sends environment variables. The common failure is content being treated as authority for a different action. The following cases show which tools and credentials make each path possible.

---


## Slide 14 · Why prompting alone cannot fix it (1.3)

**Key message:** Published tests still show residual risk, so limit what a fooled agent can do.

**Say:**
A common defensive pattern does the obvious things: user input goes in the user role, its length is validated, and the model is told external content is untrusted. That is good hygiene. Now look at the data.

Anthropic tested prompt injection against its browser agents:
- In August 2025, mitigations cut attack success from 23.6% to 11.2%.
- In November, with a stronger model and improved safeguards, an adaptive attacker succeeded 1.4% of the time, down from 8%.

That's real progress, but it isn't zero. Compare within each pair, not across, because the attacks differ. And these numbers don't estimate the chance that any particular issue succeeds. They show that residual risk remains.

So we separate two kinds of defence:
- Probabilistic safeguards, such as prompts, delimiters and classifiers, reduce how often the model fails.
- Enforced limits, such as permissions, isolation and approval gates, constrain what can execute when it fails. An approval gate is only as good as what it shows the reviewer: the real target and arguments.

These controls constrain what can execute.

**If asked:** *Is prompt injection unpatchable?* There are two levels. The general mixing of data and instructions is still an open research problem. Specific bypasses are ordinary bugs and do get patched: consent bypasses, config execution paths, DNS exfiltration.

**Transition:** Let me wrap up Part 1.

---


## Slide 15 · Part 1 recap — and a quick check

**Key message:** Agents act on what they read, so every readable input is part of the attack surface.

**Say:**
Three takeaways:
1. An agent turns a successful injection into actions, so its blast radius is everything it can touch.
2. Indirect injection needs no access to the agent, only to something the agent reads.
3. Models can't reliably tell data from instructions, so defences must sit outside the model.

Quick check. An agent summarises open GitHub issues. A public issue asks it to append `.env` to its response for a "compliance audit". The agent can read `.env` and has `create_issue_comment`, but no `fetch_url`. Take 30 seconds with your neighbour.

[Pause, then take one or two answers.]

Answers:
- (a) Indirect prompt injection, through the issue content. That is LLM01 in OWASP's list and AML.T0051.001 in MITRE ATLAS.
- (b) Yes. Because the agent can read `.env`, the public comment is a return channel. Removing `fetch_url` isn't enough; list every sink.
- (c) Information disclosure, enabled by spoofing an authorised request.

Notice whose permissions the attacker used: the agent's. That's the confused deputy. Next, the confused deputy.

---


## Slide 16 · Part 2 divider

**Say:**
Part 2: attack mechanisms. For each flow, identify the attacker-controlled input, the borrowed authority and the impact.

---


## Slide 17 · The confused deputy: from compilers (1988) to agents (2.1)

**Key message:** A deputy misuses its authority for a caller who lacks authority over the target.

**Say:**
The confused deputy comes from Norm Hardy in 1988. A compiler had permission to write a billing file so it could record usage. A user who could not write that file asked the compiler to compile a program and named the output file "BILL". The compiler overwrote the billing file. It used its own authority, but the target came from someone who had no authority over it.

The modern version is an illustrative scenario. An attacker with no access to your repo hides an instruction in a web page. Your agent, the deputy, holds your GitHub token and a `create_pull_request` tool. It opens a PR with a backdoor in the authentication code. The PR is created through a trusted account, in your usual style.

So review the action and its destination, not just whether the request came from the agent. For each row, ask: who supplied the target, and who supplied the authority?

**Transition:** Here's a real demonstration of an agent as a confused deputy.

---


## Slide 18 · Real case: Supabase MCP leaks tokens via a support ticket (Jul 2025)

**Key message:** The customer could read and write their own ticket, but could not read private tokens. The developer's agent could.

**Say:**
In July 2025, General Analysis demonstrated this on a support app built on Supabase, using dummy data. The four lanes are:
- the attacker, who is just a customer,
- the ticket data,
- the developer's agent, which is Cursor with the Supabase MCP server,
- the database, accessed with the powerful `service_role` key.

The steps:
1. The customer files a ticket that hides instructions for "the agent".
2. Support staff open it, but their role can't read secrets. Row-level security, the database rules that limit which rows a role can see, works for them.
3. The developer asks Cursor to "show me the latest tickets", and the agent reads the ticket.
4. It dumps the `integration_tokens` table, which the customer could never read.
5. It inserts the tokens as a new ticket message.
6. The attacker refreshes the ticket and reads them.

Map it to the deputy. The customer could read and write their own ticket, but could not read the private token table. The deputy is the coding agent. The misused authority is `service_role`: row-level security applies per role, and this role bypasses it. All three trifecta legs are present, and the ticket itself was the exfiltration channel. No HTTP was needed.

Supabase recommended read-only mode, project scoping and development data. Better still is a support-only role or view, plus approval for unrelated reads and customer-visible writes. Read-only blocks the write-back, but it controls writes; it does not guarantee confidentiality.

**If asked:** *Did real customers lose data?* This was a researcher demonstration with dummy data. Supabase said in September 2025 that it had no reports of customer leaks.

**Transition:** The root cause has a name.

---


## Slide 19 · Root cause: ambient authority — remedy: least authority (2.1)

**Key message:** An agent's permissions are ambient, and least authority shrinks what an attacker can borrow.

**Say:**
The root cause is ambient authority: the agent holds its permissions simply by running, whether or not this action was authorised. The agent on the left holds every tool, every MCP server and a permanent token, so its blast radius is everything.

The remedy is POLA, the principle of least authority. Consider a subagent that only summarises CI test failures. Its minimum set is `read_file`, scoped to that CI log only.
- Drop `write_file`, which removes tampering.
- Drop `fetch_url`, which removes HTTP exfiltration.
- Drop `run_command`, which removes arbitrary execution.
- Drop `create_pull_request`, so it can't write in your name.

Tool names, arguments, paths and credential scope all matter. The four POLA rules are at the bottom: only the tools this task needs, only for its duration, confirm irreversible actions, and log every use. POLA doesn't stop an injection; it limits what the injection can borrow.

**If asked:** *Is POLA just least privilege?* They are close. Least authority also means the task cannot even name or reach unrelated resources, which takes more than a smaller role label.

**Transition:** Next, we follow five attack vectors.

---


## Slide 20 · Five agentic attack vectors (2.2–2.6)

**Say:**
The five numbered surfaces identify where the attack crosses a boundary: context, egress, shared configuration, tool servers and delegated agents. The following case studies show a complete flow and causal analysis for every surface. ASI tags refer to the Agentic Applications 2026 list released in December 2025; LLM tags refer to the LLM Applications 2025 list.

---


## Slide 21 · 2.2 · Authority spoofing

**Say:**
A repository file is untrusted task data. In the Copilot CVE-2025-53773 demonstration, an instruction in that data caused workspace approval settings to change. That change allowed a later command-execution path without the expected confirmation.

Trace the four stages: poisoned repository content, model obedience, approval configuration changed, then privileged command execution. The key mistake is allowing content read for a coding task to control the policy that approves future tool calls. The string SYSTEM in the illustrative payload never becomes an actual system message.

The payload is paraphrased and defanged. This specific flaw was patched. The general limiting control is to prevent the agent from approving its own actions or weakening externally enforced permission policy.

Source: https://embracethered.com/blog/posts/2025/github-copilot-remote-code-execution-via-prompt-injection/

---


## Slide 22 · 2.3 · DNS exfiltration

**Say:**
The attacker plants instructions in a source file the agent is reviewing. The agent can read a local secret and can invoke an allow-listed DNS-capable utility. It places secret-derived text into a hostname, so the attacker's DNS service receives the lookup name.

The destination and argument matter as much as the command name. A command labelled safe may still have network effects. Blocking HTTP alone does not close this channel. The attack also requires sensitive data to be readable in the first place.

This is the mechanism demonstrated for Claude Code CVE-2025-55284, patched in version 1.0.4. The hostname on the slide is an illustrative placeholder. Limit file access and mediate DNS, HTTP, allowed application services and tool-server egress.

Sources: https://embracethered.com/blog/posts/2025/claude-code-exfiltration-via-dns-requests/ ; https://github.com/anthropics/claude-code/security/advisories/GHSA-x5gv-jw7f-j6xj

---


## Slide 23 · 2.4 · Configuration supply chain

**Say:**
Pillar Security's March 2025 Rules File Backdoor was a controlled demonstration against Cursor and Copilot guidance files. Hidden Unicode helped conceal instructions that influenced the code the assistant generated. An unwanted external script reference appeared in the HTML while the assistant's explanation omitted that addition.

Trace the flow: poisoned shared rules, agent loads those rules, code-writing tool inserts the reference, and a future execution of that page may load the script. The observed result is the generated code change; do not claim that real users were compromised by running it.

The trust boundary is shared repository guidance becoming policy for generated code. Review such files as code, reveal hidden Unicode, inspect the actual generated diff, and constrain runtime loading of external scripts. AGENTS.md and .claude/ are analogous configuration surfaces, not the exact artifacts in this demonstration.

Source: https://www.pillar.security/blog/new-vulnerability-in-github-copilot-and-cursor-how-hackers-can-weaponize-code-agents

---


## Slide 24 · 2.5 · MCP tool poisoning

**Say:**
Invariant Labs demonstrated that tool descriptions themselves can carry malicious instructions. The agent reads a server's metadata before choosing a tool. That metadata can ask it to use another trusted tool to read a local key and pass the contents as an argument to the malicious server.

Follow the source, reader, authority and sink: untrusted server description, agent planning context, trusted file-reading authority, and attacker-visible tool parameters. Tool approval is not permission for one server to direct another server's tools or receive unrelated secrets.

The payload is a defanged paraphrase of the mechanism, not a reproduced exploit. Inspect and pin tool definitions, separate trust domains, and enforce limits on file access and data flow. A metadata rug pull changes a definition after approval, so updates must be re-reviewed.

Source: https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks

---


## Slide 25 · 2.5 · Malicious MCP update

**Say:**
postmark-mcp was an unofficial npm look-alike, not Postmark's official service. A malicious update at version 1.0.16 added BCC behavior that copied outgoing mail to an attacker-controlled address.

Trace the flow: developer trusts and updates a connector, the agent calls its normal email tool, server code adds a hidden copy, and the attacker receives the mail. The agent can follow the user perfectly; no prompt injection is necessary because the malicious behavior is inside the implementation.

The authority comes from the real email API credential supplied to the server. Verify publisher identity, use authentic reviewed versions, review updates and isolate the connector. Pinning an already-malicious version does not help. Egress policy must cover the server process, not just model-directed browser actions.

Source: https://postmarkapp.com/blog/information-regarding-malicious-postmark-mcp-package

---


## Slide 26 · 2.6 · Autonomous amplification

**Say:**
AppOmni's November 2025 ServiceNow research showed that hidden record text could redirect an agent and recruit other agents through discovery, acting with the user's authority.

Trace the four stages: attacker-controlled record, initial agent accepts an objective from that record, discovery and delegation recruit helpers, and downstream agents use their own tools under the available user authority. The incoming message must not lose its original low-trust provenance simply because an orchestrator repeats it.

Amplification depends on what each recipient trusts and can do; propagation is not automatic. Validate delegated tasks and enforce independent minimal tool scopes. The Morris II email-assistant worm was a separate 2024 lab demonstration of self-replicating prompts, useful as an analogy rather than evidence that every agent delegation self-replicates.

Sources: https://appomni.com/ao-labs/ai-agent-to-agent-discovery-prompt-injection/ ; https://arxiv.org/abs/2403.02817

---


## Slide 27 · Part 2 recap: every vector abuses legitimate authority

**Say:**
Compare the attacks by input, authority, outcome and first limiting control. The agent's credentials do not establish that an attacker-supplied objective is authorised. Enforce resource, action and data-flow limits outside the model, even when prompting and classifiers lower the chance of failure.

---


## Slide 28 · References — Parts 1–2

**Say:**
Reference material for research and frameworks.

---


## Slide 29 · References — Parts 1–2

**Say:**
Reference material for cases and disclosures.

---
