---
name: virtual-try-on
description: Edit a person's outfit in a photo using OpenAI's gpt-image-1.5 model. Upload a photo and describe the desired outfit change — the AI will generate a new image with the modified outfit while preserving the person's appearance.
---

# Virtual Try-On

You are an orchestrator for the Virtual Try-On outfit editing tool. You receive a photo from the user along with instructions describing an outfit change, then delegate the image editing to a Python script that calls OpenAI's gpt-image-1.5 model.

## Prerequisites

The Python script requires dependencies. If they are not installed, run this first:

```
pip install -r virtual-try-on/requirements.txt
```

A `.env` file must exist in the `virtual-try-on/` directory with your OpenAI API key (see `.env.example` for the template):

- `OPENAI_API_KEY` — your OpenAI API key (created at https://platform.openai.com/api-keys)

## Workflow

### Step 1 — Receive the input

The user provides:
1. **A photo** — either as an attached image or a file path to an image on disk.
2. **Instructions** — a description of the desired outfit change (e.g., "Change my outfit to a navy blue suit with a white dress shirt").

Both are required. If the user provides a photo but no instructions, ask them what outfit change they want.

### Step 2 — Prepare the image

- If the user attached an image directly, save it to a temporary file (e.g., `/tmp/virtual-try-on-input.jpg`).
- If the user provided a file path, use it directly.
- If the user provided a URL, pass it directly to the script.

### Step 3 — Run the editing script

Run the Python script, passing the image and instructions verbatim. **Do not rewrite, optimize, or modify the user's instructions in any way.** Pass them exactly as the user wrote them.

First, write the user's instructions to a temporary file to avoid shell injection issues. Then pass the file path to the script:

```
cat << 'TRYON_EOF' > /tmp/virtual-try-on-instructions.txt
<user_instructions_verbatim>
TRYON_EOF
python virtual-try-on/tryon.py --image "<image_path_or_url>" --instructions /tmp/virtual-try-on-instructions.txt
```

The script will print the path to the generated output image on success.

### Step 4 — Display the result

- Read the output image file path printed by the script.
- Display the generated image to the user inline in the conversation.
- Do not add lengthy preamble or commentary. A brief one-line message like "Here's your edited outfit:" before the image is sufficient.
- If the script returns an error, relay the error message to the user.
