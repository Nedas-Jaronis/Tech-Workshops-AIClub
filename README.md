# AI Club — Prompt Engineering Workshop

A **beginner-friendly 60-minute** introduction to writing, testing, and improving prompts. The session uses the support-ticket classification example to teach a repeatable five-part prompt framework: **task, context, constraints, examples, and output format**.

## Workshop flow (60 minutes)

| Time | Activity |
| --- | --- |
| 0–5 min | Welcome + vague-prompt hook |
| 5–12 min | LLMs, limitations, and why specificity matters |
| 12–22 min | Five-part prompt framework + live comparison |
| 22–32 min | Zero-shot vs one-shot vs few-shot examples |
| 32–42 min | Guided classification lab + evaluation |
| 42–49 min | Improve a failed case and compare versions |
| 49–56 min | Grounding, reliability, and advanced concepts (brief) |
| 56–60 min | Exit challenge + Q&A |

## Materials

- `Workshop1/workshop1.ipynb` — primary live-demo notebook and optional advanced content.
- `Workshop1/mainOutline.ipynb` — slides / facilitator outline.
- `Workshop1/mainOutline.slides.html` — pre-exported slides; regenerate from the outline after slide edits.
- `Workshop1/commands/` — optional advanced structured workflows.

## Preparation

1. Install Python 3.10+ and create a virtual environment.
2. Install requirements: `python -m pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and add a UF AI Gateway API key **only if running the live model demos**. Never commit `.env` or share keys with participants.
4. Open the notebooks using `jupyter notebook` or `jupyter lab` from the repository root.
5. Verify which models the UF gateway currently supports, and test a live call before the workshop. Some optional provider features (tool calling, web search) may not be available.
6. For participants without credentials, use the prompt text and offline exercises; the instructor can run the live comparison.

### Optional: regenerate HTML slides

```bash
jupyter nbconvert --to slides Workshop1/mainOutline.ipynb \
  --output mainOutline --output-dir Workshop1
```

The generated slides use Reveal.js resources at view time and may require internet connectivity. Keep a PDF or screenshots available if the room's network is unreliable.

## Teaching guidance

**Core session:** stop after the `Core workshop takeaways` section in `workshop1.ipynb`. The remaining workflows, BAML examples, tool-calling implementation, and adversarial tests are optional follow-up material.

**Exercise:** compare zero-shot and few-shot classification across the same five held-out tickets. Track both label accuracy and compliance with the single-category output rule. The five-ticket dataset is illustrative, not evidence of production quality.

**Safety:** Treat fetched text as untrusted data, not as new instructions. The demo calculator restricts arithmetic syntax and does not execute model-generated Python code.
