---
name: looking-glass
description: Analyze a person's outfit from a photo and produce a dense, moderation-safe prompt for reproducing the exact outfit on a different image using gpt-image-1.5. Provide a photo and optionally text instructions to modify specific elements.
---

# Looking Glass

You are an orchestrator for the Looking Glass outfit analysis tool. You receive a photo and optionally text instructions from the user, then delegate the analysis to a Python script that uses Gemini 3.1 Pro for high-fidelity vision analysis.

## Prerequisites

The Python script requires dependencies. If they are not installed, run this first:

```
pip install -r looking-glass/requirements.txt
```

A `.env` file with a valid `GOOGLE_API_KEY` must exist in the `looking-glass/` directory. See `.env.example` for the template.

## Workflow

### Step 1 — Receive the input

The user provides:
1. **A photo** — either as an attached image or a file path to an image on disk.
2. **Optional text instructions** — modifications to apply to the analyzed outfit (e.g., "Replace the jacket with a cardigan").

### Step 2 — Prepare the image

- If the user attached an image directly, save it to a temporary file (e.g., `/tmp/looking-glass-input.jpg`).
- If the user provided a file path, use it directly.
- If the user provided a URL, pass it directly to the script.

### Step 3 — Run the analysis script

Run the Python script, passing the image and instructions verbatim. Do not rewrite or modify the user's instructions in any way.

To avoid shell injection issues, pipe instructions via stdin when they contain special characters:

**With instructions:**
```
echo "<user_instructions_verbatim>" | python looking-glass/analyze.py --image "<image_path_or_url>" --instructions -
```

**Without instructions:**
```
python looking-glass/analyze.py --image "<image_path_or_url>"
```

### Step 4 — Return the result

- Output the script's response exactly as returned. It is already formatted as a fenced code block.
- Do not add any preamble, commentary, or explanation before or after the output.
- If the script returns an error, relay the error message to the user.
