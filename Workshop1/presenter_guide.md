# Presenter Guide: Prompt Engineering (Workshop 1)

Present from **`workshop1.ipynb`** (Jupyter slideshow / RISE) so the live demos run on the slides.
`workshop1.slides.html` is a static backup you can open in any browser.

## Run of show (60 min)

| Time | Section | Notes |
| --- | --- | --- |
| 0–3 | Title + "Help me study machine learning" | Ask the room what's missing *before* revealing the list. |
| 3–10 | What is prompt engineering, how LLMs work | Keep the formula light. The plain-English line is what matters. |
| 10–15 | **Demo:** notebook + pen puzzle, fast vs. reasoning model | Poll the room first ("hands up for 40 cents"). |
| 15–25 | Five-part checklist, modern habits, Marcus Aurelius demo | The "spot the hallucination" slide is a strong moment. Don't skip it. |
| 25–30 | Context windows + tokens | Run the token cell. People like seeing "Em·per·ors". |
| 30–33 | Zero / one / few-shot | Same ticket throughout, so it stays easy to follow. |
| 33–45 | **Hands-on lab** + "your turn" | The core of the workshop. Protect this time. |
| 45–50 | Industry: versioning, A/B tests, optimization | Can be quick if running long. |
| 50–56 | Beyond one prompt: RAG, tools, structured outputs, coding agents, safety | **Pick 2 demos** (suggested: calculator tool + jailbreak). Talk through the rest. |
| 56–60 | Takeaways + exit challenge + Q&A | |

**Running long?** Cut, in this order: A/B testing details → structured outputs → RAG demo → coding agents. The BAML appendix is bonus-only.

## Before the session

- [ ] `.env` contains a working `OPENAI_API_KEY` for the UF NaviGator gateway.
- [ ] Run **every cell** once, the day before *and* 15 min before the session. Model availability on the gateway changes.
      If a model is gone, change `FAST_MODEL` / `REASONING_MODEL` in the setup cell .
- [ ] Save the notebook **with outputs** as a backup in case the Wi-Fi or the API fails mid-demo.
- [ ] Check that the QR code / Pulse link on the title slide is still the right one for this event.
- [ ] Have [Lakera Gandalf](https://gandalf.lakera.ai/baseline) open in a tab.

## Demo notes and expected results

These were tested live on the UF NaviGator gateway on 2026-10-14, running each demo several times. Outputs vary from run to run, so treat them as "what usually happens."

| Demo | What happened in testing |
| --- | --- |
| **Notebook + pen puzzle** (answer: **$0.20**) | `llama-3.3-70b`, answering immediately: **$0.40 (4/4 runs)**. With "think step by step": **$0.20 (4/4)**. `gpt-oss-120b`: **$0.20 (4/4)**. The original bat-and-ball puzzle got $0.05 from *both* models, which is why we use the twist. |
| **Marcus Aurelius (vague prompt)** | Long, generic, fluent essay. The live run may not contain an obvious error. That's fine: the next slide shows the one from a practice run. Ask the room: "How would you check any of this?" |
| **Roman Empire (structured prompt)** | Both models follow the six-bullet structure. In one run, gpt-oss wrote **373 words** against a 250–350 limit, and llama wrote 342. That's a good format-compliance talking point. |
| **Lab: v1 zero-shot** | ~83% accuracy, 100% format. It misses the "glitch charged me" ticket. |
| **Lab: v2 four examples** | ~67–72% for llama. **The examples didn't teach the rule and can make it worse.** That's the surprise to discuss. |
| **Lab: v3 one explicit rule** | **100% / 100%.** That's the payoff slide. |
| **Lab: smaller models** (optional: set `model="mistral-small-3.1"` or `"granite-3.3-8b-instruct"`) | With examples, these keep generating made-up `Ticket: …` lines after the label, and format compliance fell to 17–50%. That's the autocomplete behavior from the opening slides. |
| **RAG** ("latest stable Python") | Answered **Python 3.15.0**, which matches python.org. gpt-oss used its own citation style (`【1†L1-L2】`) instead of the requested `[1]`: another format-compliance example. |
| **Calculator, no tool** | llama answered **8.0000000000** (truth: **8000000072.9000006634**). Gemma 4 answered **800**. Confidently wrong by orders of magnitude. |
| **Calculator, with tool** | gpt-oss reported it correctly about 2 out of 3 times. Once it returned no text, and the notebook then points to the printed tool result. llama called the tool correctly but **misreported the result as 8.0000000729 (3/3 runs)**, which is covered on the caveat slide. |
| **Jailbreak** | All four attacks refused. Say so, then send people to Gandalf to see guardrails get beaten. |

Avoid open-ended "latest news" search queries: they return random headlines, which can include sensitive stories.

## Facts to keep accurate

- Don't quote exact context-window sizes or model version numbers on slides; they change every few months. The slides say "hundreds of thousands to over a million tokens," which holds for current frontier models.
- The system prompt shown is **illustrative**, not any company's real system prompt.
- RAG and tools *reduce* errors. They don't eliminate them.
- A five-ticket test spots problems; it doesn't prove a prompt works.
