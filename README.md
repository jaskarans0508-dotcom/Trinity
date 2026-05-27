# Trinity — Multi-Provider AI Shell (V1.4)

A local Python-based BYOK (Bring Your Own Key) orchestration shell.
No environment variables required. No cloud setup. Paste your keys into `config/api_keys.json` and run it from Command Prompt or VS Code.

V1.4 changes the design so **Python does as much orchestration work as possible**. The AIs are used as controlled advisors:

```text
Python = routing, prompts, parsing, cost control, fallbacks, and logs
Gemini = creative ideas
Claude = JSON-only reasoning/safety checker
GPT/OpenAI = final answer lead
```

---

## Quickstart

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

If needed:

```bash
py -m pip install -r requirements.txt
```

### 2. Add your API keys

Open `config/api_keys.json` in Notepad or VS Code and paste your keys:

```json
{
    "openai": {
        "api_key": "sk-...",
        "enabled": true,
        "model": "gpt-4o-mini"
    },
    "anthropic": {
        "api_key": "sk-ant-...",
        "enabled": true,
        "model": "claude-haiku-4-5-20251001"
    },
    "gemini": {
        "api_key": "AIza...",
        "enabled": true,
        "model": "gemini-2.5-flash-lite"
    },
    "trinity": {
        "mode": "auto",
        "dev_log": true,
        "log_folder": "logs",
        "simple_prompt_word_limit": 12,
        "max_creative_tokens": 120,
        "max_checker_tokens": 60,
        "max_final_tokens": 600
    }
}
```

### 3. Validate providers only

```bash
python main.py --no-shell
```

or:

```bash
py main.py --no-shell
```

### 4. Run TrinityFlow

```bash
python main.py
```

or:

```bash
py main.py
```

Then type at:

```text
[You] >
```

Exit commands:

```text
exit
quit
q
```

---

## Provider Roles

| Provider | Trinity Role | What it does in V1.4 |
|---|---|---|
| OpenAI / GPT | Lead / Primary Orchestrator | Writes the final user-facing answer |
| Anthropic / Claude | Reasoning + Safety Checker | Returns JSON only: safe/logic/useful/decision/note |
| Google Gemini | Creative Thinking | Gives short creative ideas, alternatives, and angles |
| Python | Orchestrator | Routes, builds prompts, parses Claude JSON, logs, controls cost |

---

## V1.4 Modes

### Auto Mode

Default mode:

```json
"mode": "auto"
```

Python decides whether a prompt is simple or worth full orchestration.

### Simple Mode

Used for very short prompts. Trinity sends the request directly to GPT/OpenAI mini to save cost.
Gemini and Claude are skipped.

Force it with:

```text
/cheap your prompt here
```

### Full TrinityFlow Mode

Used for larger planning, strategy, reasoning, comparison, coding, or architecture prompts.

Flow:

```text
Gemini = short creative ideas
Claude = JSON safety/reasoning checker
GPT = final answer lead
Python = routing, logging, parsing, cost control, fallback logic
```

Force it with:

```text
/full your prompt here
```

---

## V1.4 Economical Orchestration

Default token caps:

```text
Gemini creative step: 120 output tokens
Claude checker step: 60 output tokens
OpenAI final step: 600 output tokens
```

Claude is intentionally JSON-only. Example:

```json
{"safe":"Y","logic":"Y","useful":"Y","decision":"GREENLIGHT","note":"Explain role separation and auditability."}
```

Python parses this instead of asking Claude for a paragraph. This is cheaper and easier to audit.

---

## Dev Log / Notepad Output

V1.4 creates a `logs` folder automatically. Every user prompt creates a `.txt` file like:

```text
logs/trinityflow_2026-05-15_14-30-10.txt
```

The log includes:

```text
User prompt
Python routing decision
Exact visible prompt sent to Gemini
Gemini visible output
Exact visible prompt sent to Claude
Claude raw visible output
Claude parsed checker JSON
Python final assembly brief
Exact visible prompt sent to GPT/OpenAI
GPT final visible output
Routing summary
Errors/fallbacks
```

Important: the log does **not** claim to expose private hidden chain-of-thought. It only records visible orchestration prompts, visible outputs, and Python's routing/assembly decisions.

---

## Best Test Prompts

Simple mode test:

```text
hello
```

Full orchestration test:

```text
/full explain exactly why Trinity is useful compared to using one AI directly, including when it is overkill and when it is worth it
```

Larger product test:

```text
Build me a simple plan for Trinity V2 as a web app, including core features, security concerns, pricing model, and a 4-week prototype roadmap.
```

---

## Provider Status

| Status | Meaning |
|---|---|
| MISSING | No key found in `config/api_keys.json` |
| UNTESTED | Key present but not live-tested |
| VALID | Key tested and accepted by the provider |
| INVALID | Key tested and rejected by the provider |
| ERROR | Unexpected error during validation |
| DISABLED | Provider set to `"enabled": false` in config |

---

## File Structure

```text
Trinity/
├── main.py
├── requirements.txt
├── config/
│   ├── api_keys.json
│   └── api_keys.example.json
├── providers/
│   ├── openai_provider.py
│   ├── anthropic_provider.py
│   └── gemini_provider.py
└── core/
    ├── config_loader.py
    ├── activation.py
    ├── shell.py
    └── status.py
```

---

## Safety and Cost Notes

- `config/api_keys.json` stays local. Do not share it.
- Trinity masks API keys in terminal output.
- Use `python main.py --no-shell` first after adding keys.
- Use `/cheap` for short tests.
- Use `/full` only when the prompt is large enough to benefit from orchestration.
- If a provider returns quota/rate-limit errors, Trinity logs the error and keeps the shell stable where possible.

---

## Trinity V1.5 — Tool-Grounded Economical Orchestration

V1.5 changes the flow so Python does more of the work and the models only run when their role is useful.

### Roles

- **Python** = router, tool runner, source verifier, CSV retention, logger, parser, fallback handler.
- **GPT/OpenAI** = lead final writer.
- **Claude/Anthropic** = short JSON reasoning/safety/grounding checker.
- **Gemini** = creative advisor only. Gemini is skipped for normal factual/regurgitation prompts.

### Runtime Routes

Trinity now auto-routes prompts:

```txt
/cheap     -> GPT only, fastest/cheapest
/math      -> Python calculator first, then optional GPT explanation
/grounded  -> Python source search/fetch/verify, GPT writes with sources, Claude checks grounding
/creative  -> Gemini ideas, Claude JSON check, GPT final
/full      -> GPT + Claude standard route, Gemini skipped
```

In auto mode:

- short prompts use simple mode
- math-like prompts use Python calculator tooling
- factual prompts use source grounding
- creative prompts use Gemini
- larger planning/reasoning prompts use GPT + Claude without Gemini

### Grounding and Source Checks

For factual questions, Python extracts keywords, searches the web, fetches pages, checks URL/title/body keyword matches, and only sends accepted source snippets to GPT. Source checks are stored in CSV.

Installed packages required for grounding:

```bash
pip install -r requirements.txt
```

V1.5 adds:

```txt
requests
beautifulsoup4
```

### CSV Retention

CSV files are stored in the configured data folder, default:

```txt
data/
```

Files created:

```txt
session_memory_active.csv   active session keywords/sources
session_dump_*.csv          dumped memory when exit/quit/q is used
source_checks.csv           accepted/rejected URL checks
tool_runs.csv               tool runtime and status
instruction_profiles.csv    routing-role instruction profiles
```

The active session memory is cleared when you exit, while a session dump remains for inspection.

### Speed Improvements

- Gemini is skipped unless the prompt needs imagination/creative ideation.
- Source fetching runs in parallel using Python threads.
- Claude returns short JSON only.
- Python performs math/source checks directly instead of asking models to guess.

### Good Tests

```txt
hello
```
Should use simple mode.

```txt
what is 14*27
```
Should use Python math/tool mode.

```txt
/grounded explain the lore of Doom The Dark Ages with sources
```
Should use source grounding.

```txt
/creative generate a flowchart containing a company's employment process
```
Should use Gemini because the task benefits from creative/visual structuring.
