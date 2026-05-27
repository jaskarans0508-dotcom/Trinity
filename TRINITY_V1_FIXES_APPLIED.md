# Trinity v1 — Fixes Applied

This file documents the fixes applied after Claude token usage ran out.

## Completed Fixes

### 1. Stronger placeholder detection
`core/activation.py` now blocks obvious placeholder/example keys before any provider API call.

Blocked examples include:

- empty strings
- `sk-...`
- `sk-ant-...`
- `AIza...`
- values containing `...`
- values containing words like `placeholder`, `insert`, `sample`, `demo`, `paste`, `replace`, or `your`
- too-short values
- wrong provider prefixes

Provider prefix checks:

- OpenAI must start with `sk-`
- Anthropic must start with `sk-ant-`
- Gemini must start with `AIza`

These checks are intentionally light. They only prevent obvious bad values. The live provider validation is still the real source of truth.

---

### 2. Dry-run mode
`main.py` now supports:

```bash
python main.py --dry-run
```

Dry-run mode checks:

- config file exists
- provider blocks exist
- required fields exist
- key values look configured
- disabled providers are respected

Dry-run mode does **not** call OpenAI, Anthropic, or Gemini.

Configured-looking keys are marked as `UNTESTED` in dry-run mode.

---

### 3. Config repair is now saved back to disk
`core/config_loader.py` now repairs missing provider blocks or missing fields and writes the repaired config back into `config/api_keys.json`.

Example repaired fields:

```json
{
    "api_key": "",
    "enabled": true
}
```

This makes the config file forward-compatible as new fields are added later.

---

### 4. Request timeouts added
Provider validation now has timeouts so Trinity does not hang forever during network/provider issues.

Current timeout:

```python
REQUEST_TIMEOUT_SECONDS = 10
```

Applied to:

- `providers/openai_provider.py`
- `providers/anthropic_provider.py`
- `providers/gemini_provider.py`

---

### 5. Safer provider validation notes
Provider files now return clearer error notes for:

- invalid keys
- permission denied
- rate limits
- network errors
- request timeouts
- model not found
- missing Python packages

---

## Tested Locally

The following commands were tested from the project folder:

```bash
python main.py --dry-run
python main.py
python -m compileall .
```

Expected result with blank keys:

- OpenAI: `MISSING`
- Anthropic / Claude: `MISSING`
- Google Gemini: `MISSING`
- Clean exit, no crash

---

## Remaining Next Steps

### v1.1 recommended next step
Add a tiny test script or built-in `--doctor` command that checks:

- Python version
- installed packages
- config path
- readable config file
- provider package import status

### v2 next step
Build the interactive Trinity shell loop:

```text
User prompt
→ Primary drafts answer/plan
→ Secondary critiques/improves
→ Gemini reviews safety/completeness
→ Trinity returns final answer
```

### Later improvement
Move model names into config so the user can change validation models without editing provider code.
