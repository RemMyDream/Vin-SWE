"""Prepare clean presenter notes from the reviewed source, without scheduling metadata."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[2]
source = (root / "COMP5320_Ch9_Part1-2_Speaker_Script.md").read_text(encoding="utf8")
parts = re.split(r"^## Slide (\d+)\b(.*)$", source, flags=re.M)
old = {}
for i in range(1, len(parts), 3):
    old[int(parts[i])] = (parts[i+1].strip(" ·"), parts[i+2].split("\n---")[0].strip())

new_cases = {
21: ("2.2 · Authority spoofing", """A repository file is untrusted task data. In the Copilot CVE-2025-53773 demonstration, an instruction in that data caused workspace approval settings to change. That change allowed a later command-execution path without the expected confirmation.

Trace the four stages: poisoned repository content, model obedience, approval configuration changed, then privileged command execution. The key mistake is allowing content read for a coding task to control the policy that approves future tool calls. The string SYSTEM in the illustrative payload never becomes an actual system message.

The payload is paraphrased and defanged. This specific flaw was patched. The general limiting control is to prevent the agent from approving its own actions or weakening externally enforced permission policy.

Source: https://embracethered.com/blog/posts/2025/github-copilot-remote-code-execution-via-prompt-injection/"""),
22: ("2.3 · DNS exfiltration", """The attacker plants instructions in a source file the agent is reviewing. The agent can read a local secret and can invoke an allow-listed DNS-capable utility. It places secret-derived text into a hostname, so the attacker's DNS service receives the lookup name.

The destination and argument matter as much as the command name. A command labelled safe may still have network effects. Blocking HTTP alone does not close this channel. The attack also requires sensitive data to be readable in the first place.

This is the mechanism demonstrated for Claude Code CVE-2025-55284, patched in version 1.0.4. The hostname on the slide is an illustrative placeholder. Limit file access and mediate DNS, HTTP, allowed application services and tool-server egress.

Sources: https://embracethered.com/blog/posts/2025/claude-code-exfiltration-via-dns-requests/ ; https://github.com/anthropics/claude-code/security/advisories/GHSA-x5gv-jw7f-j6xj"""),
23: ("2.4 · Configuration supply chain", """Pillar Security's March 2025 Rules File Backdoor was a controlled demonstration against Cursor and Copilot guidance files. Hidden Unicode helped conceal instructions that influenced the code the assistant generated. An unwanted external script reference appeared in the HTML while the assistant's explanation omitted that addition.

Trace the flow: poisoned shared rules, agent loads those rules, code-writing tool inserts the reference, and a future execution of that page may load the script. The observed result is the generated code change; do not claim that real users were compromised by running it.

The trust boundary is shared repository guidance becoming policy for generated code. Review such files as code, reveal hidden Unicode, inspect the actual generated diff, and constrain runtime loading of external scripts. AGENTS.md and .claude/ are analogous configuration surfaces, not the exact artifacts in this demonstration.

Source: https://www.pillar.security/blog/new-vulnerability-in-github-copilot-and-cursor-how-hackers-can-weaponize-code-agents"""),
24: ("2.5 · MCP tool poisoning", """Invariant Labs demonstrated that tool descriptions themselves can carry malicious instructions. The agent reads a server's metadata before choosing a tool. That metadata can ask it to use another trusted tool to read a local key and pass the contents as an argument to the malicious server.

Follow the source, reader, authority and sink: untrusted server description, agent planning context, trusted file-reading authority, and attacker-visible tool parameters. Tool approval is not permission for one server to direct another server's tools or receive unrelated secrets.

The payload is a defanged paraphrase of the mechanism, not a reproduced exploit. Inspect and pin tool definitions, separate trust domains, and enforce limits on file access and data flow. A metadata rug pull changes a definition after approval, so updates must be re-reviewed.

Source: https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks"""),
25: ("2.5 · Malicious MCP update", """postmark-mcp was an unofficial npm look-alike, not Postmark's official service. A malicious update at version 1.0.16 added BCC behavior that copied outgoing mail to an attacker-controlled address.

Trace the flow: developer trusts and updates a connector, the agent calls its normal email tool, server code adds a hidden copy, and the attacker receives the mail. The agent can follow the user perfectly; no prompt injection is necessary because the malicious behavior is inside the implementation.

The authority comes from the real email API credential supplied to the server. Verify publisher identity, use authentic reviewed versions, review updates and isolate the connector. Pinning an already-malicious version does not help. Egress policy must cover the server process, not just model-directed browser actions.

Source: https://postmarkapp.com/blog/information-regarding-malicious-postmark-mcp-package"""),
26: ("2.6 · Autonomous amplification", """AppOmni's November 2025 ServiceNow research showed that hidden record text could redirect an agent and recruit other agents through discovery, acting with the user's authority.

Trace the four stages: attacker-controlled record, initial agent accepts an objective from that record, discovery and delegation recruit helpers, and downstream agents use their own tools under the available user authority. The incoming message must not lose its original low-trust provenance simply because an orchestrator repeats it.

Amplification depends on what each recipient trusts and can do; propagation is not automatic. Validate delegated tasks and enforce independent minimal tool scopes. The Morris II email-assistant worm was a separate 2024 lab demonstration of self-replicating prompts, useful as an analogy rather than evidence that every agent delegation self-replicates.

Sources: https://appomni.com/ao-labs/ai-agent-to-agent-discovery-prompt-injection/ ; https://arxiv.org/abs/2403.02817"""),
}

mapping = {**{n:n for n in range(1,21)}, 27:25, 28:26, 29:26}
replacement_say = {
1: "Today we examine how agentic coding tools can be redirected through text, configuration and tools. We will follow concrete attack flows, identify the authority each attack uses, and explain which boundary failed.",
2: "Part 1 covers why security changes when an agent can use tools, how to model the threat, and how direct and indirect prompt injection work. Part 2 follows the confused deputy, authority spoofing, covert exfiltration, configuration poisoning, MCP attacks and autonomous amplification. One running example connects them: an agent summarises public GitHub issues while holding private reads and public writes.",
3: "Part 1: foundations. We start with the systems and credentials an agent can reach.",
10: "The top row shows direct injection: a user submits a malicious task instruction, the agent obeys it, file-read and network tools access a local key, and the key leaves the workspace. The local key belongs to the agent's environment, not necessarily to the person typing the task. This is an illustrative flow, not a reported breach.\n\nThe lower row shows indirect injection: an attacker plants a request in a public issue; a legitimate issue-summary task makes the agent read it; file and comment tools publish .env; the attacker reads the public comment.\n\nThe entry route defines direct versus indirect. Neither route guarantees success. The attack succeeds only if the agent follows the instruction and the necessary read and output authority exists. Removing fetch_url does not prevent a public comment from being the return channel.",
13: "The six cards trace different carriers into an impact. A public issue can lead to a private-repository read and a public pull request. A README can change approval settings and enable shell execution. A webpage can alter an answer through hidden instructions. An email can make retrieved context leave through an image URL. A poisoned rule can change generated HTML. Tool metadata can cause a file read and send secrets as tool arguments.\n\nThe payment-module snippet is an illustrative example: a review request is turned into a logging command that sends environment variables. The common failure is content being treated as authority for a different action. The following cases show which tools and credentials make each path possible.",
16: "Part 2: attack mechanisms. For each flow, identify the attacker-controlled input, the borrowed authority and the impact.",
20: "The five numbered surfaces identify where the attack crosses a boundary: context, egress, shared configuration, tool servers and delegated agents. The following case studies show a complete flow and causal analysis for every surface. ASI tags refer to the Agentic Applications 2026 list released in December 2025; LLM tags refer to the LLM Applications 2025 list.",
27: "Compare the attacks by input, authority, outcome and first limiting control. The agent's credentials do not establish that an attacker-supplied objective is authorised. Enforce resource, action and data-flow limits outside the model, even when prompting and classifiers lower the chance of failure.",
28: "Reference material for research and frameworks.", 29: "Reference material for cases and disclosures."
}

labels = [("§9.3.2–9.3.3","1.3"),("§9.3.4–9.3.5","1.3"),("§9.4.1–9.4.2","2.1"),
          ("§9.4.3","2.1"),("§9.3.1","1.3"),("§9.3.3","1.3"),("§9.1","1.1"),("§9.2","1.2")]
def clean(value):
    value=re.sub(r"^\*\*Presenter:\*\*.*\n?", "", value, flags=re.M)
    value=re.sub(r"\(name of Member [234]\)", "the next topic", value)
    for a,b in labels: value=value.replace(a,b)
    for a,b in [("The book's code example", "A common defensive pattern"),
                ("One correction to the book: ", ""), ("The chapter's four POLA rules", "The four POLA rules"),
                ("the chapter's scenario", "an illustrative scenario"), ("the chapter's central message", "the central message"),
                ("The chapter", "The framework"), ("the chapter", "the framework"),
                ("Review Question 1", "a quick check"), ("Review Question 2 asks about", "Consider"),
                ("Part 3 builds these.", "These controls constrain what can execute."),
                ("Part 3 covers how.", "Apply the controls to the actual tool and resource boundary."),
                ("Over to the next topic.", "Next, the confused deputy."),
                ("The book calls these", "Were these"), ("Chapter 9", "agent security")]:
        value=value.replace(a,b)
    value=value.replace("Quick check: this is a quick check.", "Quick check.")
    value=value.replace("This is the framework's threat-model diagram, redrawn.", "This diagram maps the agent's data and control flows.")
    value=value.replace("The framework says every arrow is a potential injection point. More precisely, every inbound flow needs a trust decision:", "Every inbound flow needs a trust decision:")
    value=value.replace("The framework then lists five more attack vectors.", "Next, we follow five attack vectors.")
    return value.strip()

out=["# Security of Agentic AI Coding Tools — presenter notes\n\n"
     "Body typeface: Montserrat. Titles and key information: Poppins. Code: Consolas.\n\n"
     "Presentation roster: Bui Khac Chien — V2026003377; three name/ID placeholders remain editable.\n\n"
     "Each attack case traces input → agent → authority/tool → impact, then explains the failed boundary.\n"]
for n in range(1,30):
    if n in new_cases:
        title,say=new_cases[n]; body="**Say:**\n"+say
    else:
        title,body=old[mapping[n]]
        body=clean(body)
        if n in replacement_say:
            body="**Say:**\n"+replacement_say[n]
    for a,b in labels: title=title.replace(a,b)
    title=title.replace("(§9.5)","(2.2–2.6)").replace("Chapter 9", "")
    out.append(f"\n## Slide {n} · {title}\n\n{body}\n\n---\n")
(root / "COMP5320_Agentic_Security_Speaker_Notes.md").write_text("\n".join(out),encoding="utf8")
print("Prepared notes for 29 slides")
