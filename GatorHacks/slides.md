---
theme: default
title: Agents 101
info: |
  Agents 101: How to actually work with AI coding agents.
  A GatorHacks workshop.
colorSchema: dark
fonts:
  sans: Inter
  mono: JetBrains Mono
  weights: "300,400,500,600,700"
class: text-center
transition: fade
mdc: true
---

# Agents 101

How to actually work with AI coding agents

<div class="pt-8 credit-inline">GatorHacks workshop</div>

<!--
Welcome. Goal for the next hour: you leave knowing how to get good work out of an AI coding agent, and how to avoid the common ways it goes wrong.

An "agent" here means an AI model that can read files, run commands, and edit code on its own in a loop, instead of just answering one question.

This is not a hype talk. We will cover what the agent sees, what it can touch, and where you stay in control.
-->

---
clicks: 3
---

# The two loops

<AgentLoop :focus="['all', 'config', 'agent', 'review'][$clicks]" class="mx-auto" style="max-width: 660px" />

<div class="legend">LLM: the AI model &nbsp;·&nbsp; Config: standing instructions &nbsp;·&nbsp; PR: a proposed code change</div>

**You control what goes in and what comes out. The agent runs the middle.**

<div class="credit">Diagram adapted from a talk by Airbnb senior staff engineers</div>

<!--
Read the diagram left to right. An "LLM" is the large language model, the AI brain.

Outer loop is you: you take a feature spec, write a prompt, hand it off, then review the result. If it is not right, you course correct and re-prompt. If it is right, it becomes a PR (pull request, a proposed code change someone must approve).

Inner dashed loop is the agent: it loads its config (the system prompt, the standing instructions), calls the LLM, uses its environment (files, shell, tools), and guardrails check each step.

Click through: the first click lights up what you hand in (prompt and config), the second the agent's own loop, the third what comes back out (review).

Green boxes are the places you have leverage: the prompt, the config, the guardrails, and the review.

Tie to the software development lifecycle (SDLC): plan, build, test, review, ship. The old loop had a human doing every step. Now the agent does build and test inside its loop, and the human moves up to planning and review. The whole talk is about doing those two parts well.
-->

---

# The lifecycle is shifting

<SdlcShift />

<v-click at="2">

**Your time moves to planning and reviewing.**

</v-click>

<!--
The software development lifecycle (SDLC) is the set of steps every feature goes through: plan, build, test, review, ship.

Before agents, a person did every step. Now the agent handles build and test inside its own loop. That does not remove work, it moves it. Planning (the spec) and review become the main human jobs, and mistakes there get more expensive because the agent moves fast.

This is the theme of the rest of the talk: what the agent sees (context), where it gets worse (dumb zone), how to scale it (multi-agent loops), and how you check it (review).
-->

---

# What is in the context window

<div class="grid grid-cols-3 gap-4 pt-6">
<div class="card info">

### Instructions
System prompt, rules file (`CLAUDE.md`), skills

</div>
<div class="card info">

### What it read
Files and tool output

</div>
<div class="card info">

### The conversation
Everything you and the agent said

</div>
</div>

<v-click>

> The agent only knows what is in its context.

</v-click>

<!--
The context window is the model's working memory: everything it can see right now. It is measured in tokens (roughly word pieces; 1 token is about three quarters of a word).

Everything on the left competes for the same space. System prompt and config files load at the start. Skills load when relevant. Every file it reads and every command output gets added. So does every message in the chat.

If something is not in the window, the agent does not know it. It cannot see your head, your Slack, or last week's chat. That is why writing things down (specs, config files) works so well.
-->

---

# The dumb zone

<DumbZoneBar class="mt-10" />

<div class="pt-10">

Quality starts to slip around **40% full** and falls off fast past 70%.

</div>

<!--
Models advertise huge windows, but in practice answers get worse once the window is filled with a lot of material, often starting around 40%.

Why: more noise to sort through, important instructions get buried, and old wrong turns keep influencing new answers.

Watch the bar fill. Green is the smart zone, yellow is the warning range, red is the dumb zone. The dashed line is roughly 40%. Treat this as a rule of thumb, not an exact number. It varies by model and task.
-->

---
clicks: 5
---

# How a session grows and shrinks

<ContextTimeline :step="$clicks" />

<!--
This is one working session, left to right. The line is how full the context window is.

Click through each step. Growth is the blue line. The green dotted line is a drop.

Terms: /compact is a command that asks the agent to summarize the conversation so far and replace the long history with that summary. It frees space but loses detail, and you do not choose what is dropped. /clear empties the window completely. On its own that loses everything, so first have the agent write a plan or handoff file, then start the new session from that file. That is the cleanest way back to the green zone.

The dashed lines at 40% and 70% are rules of thumb, not exact limits.
-->

---

# Staying in the smart zone

<div class="grid grid-cols-3 gap-4 pt-6">
<v-click>
<div class="card good">

### Fresh sessions
New task, new session. Clear the old one.

</div>
</v-click>
<v-click>
<div class="card good">

### Compact on purpose
Summarize the work into a plan file, then restart from it.

</div>
</v-click>
<v-click>
<div class="card good">

### Sub-agents
Push heavy exploration to a separate window.

</div>
</v-click>
</div>

<!--
Fresh sessions: do not let one chat run all day. Old context is a cost, not an asset.

Intentional compaction: "compaction" means summarizing the conversation to free space. Automatic compaction is lossy and you do not control it. Do it on purpose instead: ask the agent to write a plan or handoff file with the goal, what is done, what is next, and key file paths. Then start a clean session that reads only that file.

Sub-agents: a sub-agent is a second agent with its own clean window. We cover them properly later in the talk. For now: they let you read a lot without filling your main window.
-->

---

# What is a skill

````md {3|all}
---
name: grill-me
description: Interview me about a plan until every branch is resolved.
---
# Grill me
1. Ask one question at a time.
2. Offer your recommended answer.
3. Stop when no open branches remain.
````

<v-click>

Only the short **description** sits in context. The body loads when needed.

</v-click>

<!--
A skill is a Markdown file, usually named SKILL.md, that holds instructions for one kind of task. Markdown is just plain text with light formatting.

The top block between the dashes is frontmatter: metadata. The name and description are all the agent keeps in context all the time. That is a few dozen tokens.

When your request matches the description (or you call the skill by name), the agent loads the full body. So you can install many skills without filling the window. That is why skills add expertise cheaply.

This example is simplified for the slide. Real skills can also include extra files and scripts.
-->

---

# Matt Pocock's skills

```bash
claude plugin install mattpocock-skills@claude-plugins-official
```

<div class="text-sm pt-2">

| Skill | Where it fits on the loop |
| --- | --- |
| `grill-me`, `to-spec`, `to-tickets` | Spec, into the **Prompt** arrow |
| `tdd`, `diagnosing-bugs` | **Guardrails** box |
| `code-review` | **Review** step |

</div>

<div class="credit">github.com/mattpocock/skills</div>

<!--
After installing, run /setup-matt-pocock-skills once in each repo you want to use them in.

Matt Pocock publishes an open source set of skills. Install command and skill names here were checked against the live repo. Other agents (like Codex) use different install commands, listed in the repo README.

grill-me: the agent interviews you about your plan until every branch of the design is settled. Great for turning a vague idea into a clear spec.
to-spec: turns that conversation into a written spec. (Older name: to-prd, a product requirements document.)
to-tickets: splits the spec into small tasks. (Older name: to-issues.)
tdd: test-driven development. The agent writes a failing test first, then code to pass it. Tests become an automatic gate.
diagnosing-bugs: a disciplined loop for hard bugs. (Older name: diagnose.)
code-review: reviews the diff against your standards and the spec.

Guardrails are covered with hooks on the guardrails slide.
-->

---
layout: center
class: text-center
---

# DEMO

## Live: grill-me on a project idea

<!--
Placeholder for the live demo (about 8 to 10 minutes).

Plan: ask for one project idea from the audience. Run grill-me on it. Show the agent asking one question at a time and recommending answers. End by running to-spec to show the output as a written spec.

Point out during the demo: this is the left side of the loop. We are improving what goes IN before any code is written.

Backup plan if the network fails: have a recorded run or a pre-made transcript ready.
-->

---

# Environments and sandboxes

<div class="grid grid-cols-2 gap-8 pt-4">
<div>

**What the agent can touch**

- Files
- A shell (runs commands)
- The network and tools

</div>
<v-click>
<div>

**More permission, more isolation**

- Git worktree: its own branch folder
- Container: a disposable mini computer
- Cloud sandbox: someone else's machine

</div>
</v-click>
</div>

<!--
The environment is everything the agent can reach: your files, a shell where it runs commands, the internet, and extra tools (like a database or browser).

Rule of thumb: the more you let it do on its own, the more you should fence it in.

Git worktree: a second checkout of your repo in another folder, so the agent works on its own branch without touching yours.
Devcontainer / container: a disposable mini computer on your machine. If the agent breaks it, you delete it.
Cloud sandbox: the same idea, running on someone else's machine, so a mistake cannot reach your laptop at all.
-->

---

# Guardrails

<div class="grid grid-cols-2 gap-4 pt-4">
<v-click><div class="card warn">

### Permission prompts
The agent asks before risky actions.

</div></v-click>
<v-click><div class="card warn">

### Allow and deny lists
Pre-approve safe commands, block the rest.

</div></v-click>
<v-click><div class="card good">

### Hooks
Scripts that block commands like <code>rm -rf</code> or a force push.

</div></v-click>
<v-click><div class="card good">

### Tests and linters
Automatic gates. A linter is a code checker.

</div></v-click>
</div>

<!--
Guardrails are checks that run whether or not the agent "wants" them.

Permission prompts: the agent asks before risky actions. Fine for learning, tiring over time.
Allow and deny lists: pre-approve safe commands (run tests) and block dangerous ones.
Hooks: small scripts that run before or after a tool call. A hook can refuse a command like rm -rf (delete everything) or git push --force (overwrite shared history). This is stronger than telling the agent "please do not" in a prompt, because it is enforced by code.
Tests and linters (a linter is a tool that flags style and likely bugs): the agent runs them after every change, and failures send it back to fix things before you ever look.

Colors: yellow means it still depends on a person paying attention. Green means it is enforced by code, no matter what.
-->

---

# Lock files

```diff
  "dependencies": {
    "express": "4.19.2",
+   "leftpad-utils": "0.0.1"
  }
```

<v-click>

Pinned versions mean agents cannot silently add or upgrade packages. Read every new line in the diff. Never heard of it? Stop and check.

</v-click>

<!--
A dependency is code written by someone else that your project uses. A lock file (package-lock.json, pnpm-lock.yaml, uv.lock) records the exact version of every dependency.

Why it matters with agents: models sometimes invent package names that sound real. Attackers register those names with malicious code (called slopsquatting). An agent that runs install on a made-up name can pull it into your project.

Defense: commit the lock file, and treat any lock file diff as suspicious. Read it line by line. Ask: do I recognize every new package? Is the name spelled correctly? Does it have real users?

The snippet is a simplified diff for illustration. Real lock files are thousands of lines, which is exactly why you read the diff, not the file.
-->

---

# Sub-agents are about context

<SubAgents />

<v-click>

<div class="pt-6">Each one reads a lot. Only a short result comes back.</div>

</v-click>

<!--
Sub-agents are not job titles like "designer" or "tester". They are a way to manage context.

Each sub-agent starts with a clean window, does the heavy reading (hundreds of files, long logs), and returns a short summary. Your main agent stays in the smart zone because the noise never entered its window.

Good uses: exploring an unfamiliar codebase, searching many files, reading long logs.
Weak use: giving a sub-agent a vague task and trusting the summary blindly. The summary is only as good as what the sub-agent looked at.
-->

---

# Multi-agent loops

<div class="grid grid-cols-3 gap-4 pt-6">
<v-click>
<div class="card info">

### Fan-out
Many agents research in parallel.

</div>
</v-click>
<v-click>
<div class="card info">

### Pipeline
Planner, then implementer, then reviewer.

</div>
</v-click>
<v-click>
<div class="card info">

### Until it passes
Loop until tests go green.

</div>
</v-click>
</div>

<v-click>

<div class="pt-6 accent-warn">More agents means more output for you to review.</div>

</v-click>

<!--
Three common patterns.

Fan-out: several agents investigate different questions at once and report back. Fast, good for research.
Pipeline: one agent plans, one writes code, one reviews. Each step has a clear handoff document.
Until it passes: the agent runs the tests, reads failures, fixes, and repeats until green. Set a cap on attempts so it cannot loop forever and burn money.

The caveat in yellow is the important part. Every agent produces output, and all of it lands on a human eventually. Do not add agents just because you can.
-->

---

# Review is the bottleneck

<div class="grid grid-cols-3 gap-4 pt-6">
<v-click>
<div class="card good">

### Read the diff
Every changed line, not just the summary.

</div>
</v-click>
<v-click>
<div class="card good">

### Run it
Do not trust "tests pass" alone.

</div>
</v-click>
<v-click>
<div class="card good">

### Keep PRs small
Big agent PRs get rubber stamped.

</div>
</v-click>
</div>

<!--
Agents make writing code cheap. Reading code is still slow, so review becomes the limit on how fast you can safely go.

Read the diff: the agent's summary tells you what it intended, not what it did. Check the actual changes.
Run it: tests only check what someone thought to test. Click through the feature yourself.
Keep PRs small: ask the agent to work in small slices (this is what to-tickets and tdd help with). A 2,000 line PR gets skimmed, and skimming is how bugs and bad dependencies ship.

Multi-agent loops make this worse, not better, because more agents produce more to review. A reviewer agent can help as a first pass, but a human still signs off.
-->

---

# The human at the end

<div class="grid grid-cols-2 gap-6 items-center">
<AgentLoop focus="review" />
<div>

**The agent opens the PR.**

**A human merges it.**

<v-click>

<div class="accent-bad pt-4">If you cannot explain a line, it does not ship.</div>

</v-click>

</div>
</div>

<div class="credit">Diagram adapted from a talk by Airbnb senior staff engineers</div>

<!--
Back to the loop with the review path lit up. Look at the arrow from Review to PR. That arrow is yours.

You must understand 100% of the code you merge. Not "it passed the tests." Not "the agent said it works." Tests only check what someone thought to test.

Practical habits: read the diff, run it yourself, ask the agent to explain any line you do not follow. If you still cannot explain it, rewrite it or cut it.

This is also why the whole SDLC shifts: planning and review become your main jobs, and both need real understanding.
-->

---
layout: center
class: text-center
---

# Questions?

<div class="pt-6 text-left inline-block text-base">

- github.com/mattpocock/skills

</div>

<!--
Open the floor. Resources are listed on the slide.

The skills repo is the one to start with.

Closing thought: agents are good at the middle of the loop. You are responsible for the two ends.
-->
