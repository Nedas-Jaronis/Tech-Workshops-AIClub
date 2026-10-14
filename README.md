# AI Club: Prompt Engineering Workshop

A **beginner-friendly 60-minute** introduction to writing, testing, and improving prompts, updated for how people use AI today: reasoning models, context engineering, RAG, tool calling, coding agents, and prompt injection.

No prior AI or prompting experience needed. Attendees without an API key can follow along in any chat app (ChatGPT, Claude, Gemini, NaviGator Chat).

## Materials

| File | What it is |
| --- | --- |
| `Workshop1/workshop1.ipynb` | **The presentation.** Slides + live demos + hands-on lab in one notebook. |
| `Workshop1/workshop1.slides.html` | Static HTML export of the slides (backup / sharing). |
| `Workshop1/presenter_guide.md` | Run of show, timing, prep checklist, expected demo results. |
| `Workshop1/commands/` | Example engineered prompts for AI coding agents (`/research_codebase`, `/create_plan`, `/implement_plan`). |

## What attendees learn

1. How LLMs generate text, and why that means **fluent ≠ true**
2. A five-part prompt checklist: **task, context, constraints, examples, output format**
3. Fast vs. reasoning models, and how to prompt each
4. Zero-, one-, and few-shot prompting, **measured** in a hands-on lab
5. How industry versions, tests, and A/B tests prompts
6. What sits around a prompt in real apps: RAG, tool calling, structured outputs, agents, and prompt-injection risks

## Setup

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt
cp .env.example .env                                  # then add your UF NaviGator API key
jupyter notebook Workshop1/workshop1.ipynb
```

- Live demos need a UF NaviGator AI gateway key. **Never commit `.env` or show your key on screen.**
- Without a key, every cell still runs and prints a "demo skipped" message.
- To present: use Jupyter's slideshow view (RISE), or open the HTML export.

### Regenerate the HTML slides after editing

```bash
jupyter nbconvert --to slides Workshop1/workshop1.ipynb --output workshop1 --output-dir Workshop1
```

The export loads reveal.js from a CDN, so it needs internet access to display.
