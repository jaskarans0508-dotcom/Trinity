# Trinity v1 — Local BYOK Shell Review + Handoff

## Current status

Trinity v1 is a local Python CLI prototype for validating three user-owned API keys from a local JSON file:

- OpenAI = Primary
- Anthropic / Claude = Secondary
- Google Gemini = Safety / Reviewer

The current v1 scope is intentionally small: config loading, key sanity checks, live provider validation, status reporting, and a clean exit if no provider is available.

## Confirmed working behavior

Tested with blank local keys:

- `python main.py` starts correctly when files are placed in the intended folder structure.
- The shell reads `config/api_keys.json`.
- Blank keys are marked as `MISSING`.
- The terminal shows all three missing providers clearly.
- The app exits cleanly when no valid providers exist.

## Required folder structure

```txt
Trinity/
├── main.py
├── requirements.txt
├── README.md
├── config/
│   ├── api_keys.json
│   └── api_keys.example.json
├── providers/
│   ├── __init__.py
│   ├── openai_provider.py
│   ├── anthropic_provider.py
│   └── gemini_provider.py
└── core/
    ├── __init__.py
    ├── config_loader.py
    ├── activation.py
    └── status.py
```

`__init__.py` files are included so Python treats `core` and `providers` as packages reliably.

## What is solid

1. The local JSON key workflow is the right move for v1.
2. The provider abstraction is clean enough to expand later.
3. Status reporting is readable and user-friendly.
4. API keys are masked in output.
5. Missing providers do not crash the app.
6. The fixed role mapping is simple and good for the first prototype.

## Missing or worth improving before v2

### 1. Placeholder detection needs to catch example keys

Right now `_looks_valid_key()` catches very short or obvious placeholder values, but it may still treat example strings like `sk-...`, `sk-ant-...`, or `AIza...` as realistic enough to attempt validation.

Suggested improvement:

```python
PLACEHOLDER_FRAGMENTS = [
    "your_", "your-", "placeholder", "insert", "example", "test",
    "sk-...", "sk-ant-...", "AIza..."
]
```

Then reject any key containing those fragments.

### 2. Config merge should save missing fields back to disk

`load_config()` merges missing provider fields in memory, but it does not write the corrected structure back into `config/api_keys.json`. This is fine for now, but saving the repaired config would make upgrades cleaner.

### 3. Add timeout handling for live validation

Provider calls can hang because of internet/network issues. Each validation should have a reasonable timeout where supported by the SDK.

Suggested target:

- OpenAI: timeout around 10 seconds
- Anthropic: timeout around 10 seconds
- Gemini: catch timeout/network exceptions clearly

### 4. Gemini SDK may need updating later

Current dependency uses `google-generativeai`. Google’s newer Gemini examples increasingly use the newer Gen AI SDK direction. The current code may still work, but we should keep an eye on SDK changes before v2.

### 5. Model names should become config values

Hardcoding model names is okay for activation testing, but v2 should allow model selection through config.

Example future config:

```json
"openai": {
  "api_key": "",
  "enabled": true,
  "model": "gpt-5-mini"
}
```

### 6. Activation should separate `MISSING` from `INVALID_FORMAT`

Right now a blank key and a fake-looking key both become `MISSING`. That is okay for the user, but internally it may help to distinguish:

- `MISSING`: no key entered
- `INVALID_FORMAT`: placeholder or obviously fake key
- `INVALID`: provider rejected the key

### 7. Add a no-network dry run mode

A future command like this would be useful:

```bash
python main.py --dry-run
```

It would check config structure and key presence without contacting providers.

## API key acquisition plan for three test cycles

### OpenAI

1. Go to the OpenAI Platform.
2. Create or sign in to a developer account.
3. Open the API keys page.
4. Create a new secret key.
5. Add billing/credits if required by the account.
6. Paste the key into:

```json
"openai": { "api_key": "YOUR_OPENAI_KEY", "enabled": true }
```

OpenAI does not reliably provide free API testing for every account. Plan for a very small paid top-up if the account has no credits.

### Anthropic / Claude

1. Go to the Claude Console.
2. Create or sign in to a Console account.
3. Open account/API key settings.
4. Generate an API key.
5. Add billing/credits if required.
6. Paste the key into:

```json
"anthropic": { "api_key": "YOUR_ANTHROPIC_KEY", "enabled": true }
```

Claude API access usually requires a Console account and API key. Free credits/promotions vary by account and region, so do not assume free access.

### Google Gemini

1. Go to Google AI Studio.
2. Sign in with a Google account.
3. Create or view a Gemini API key.
4. Paste the key into:

```json
"gemini": { "api_key": "YOUR_GEMINI_KEY", "enabled": true }
```

Gemini has a free tier for developers and small projects, so it is the easiest of the three for low-cost testing.

## Recommended 3-cycle test method

Do three tiny activation cycles only:

### Cycle 1 — blank config

Expected:

- OpenAI = MISSING
- Anthropic = MISSING
- Gemini = MISSING

### Cycle 2 — Gemini only

Expected:

- OpenAI = MISSING
- Anthropic = MISSING
- Gemini = VALID

### Cycle 3 — all three keys

Expected:

- OpenAI = VALID
- Anthropic = VALID
- Gemini = VALID

Use the smallest possible validation calls only. Do not run full Trinity orchestration until v2.

## Message to Claude

```txt
Current Trinity v1 review:

The local Python BYOK shell architecture is good. The uploaded code works when placed into the intended folder structure with `core/`, `providers/`, and `config/`. I tested the blank-key run and it correctly reports all three providers as MISSING and exits cleanly.

Please focus on these improvements next:

1. Add `__init__.py` to both `core/` and `providers/`.
2. Improve placeholder detection so strings like `sk-...`, `sk-ant-...`, `AIza...`, `YOUR_KEY`, and example values are treated as missing/invalid format before any network call.
3. Consider saving repaired config files back to disk if fields/providers are missing.
4. Add timeout handling to provider validation calls where the SDK supports it.
5. Keep model names configurable later, but hardcoded minimal validation models are fine for v1.
6. Keep API keys local in `config/api_keys.json`; no GitHub/environment variables required for the prototype.
7. For v2, add the interactive shell loop only after all three provider validators are stable.

For API keys, we should only use official user-owned keys:
- OpenAI Platform API key
- Anthropic Claude Console API key
- Google AI Studio Gemini API key

Do not use public GitHub keys or shared leaked keys. Trinity is a BYOK shell, so the user should own and control every provider key.
```
