#!/usr/bin/env python3
"""Analyze an outfit photo using Gemini via Vertex AI and produce a reproduction prompt."""

import argparse
import mimetypes
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

SCRIPT_DIR = Path(__file__).resolve().parent

DEFAULT_MODEL = "gemini-3.1-pro-preview"
DEFAULT_LOCATION = "us-central1"
MAX_IMAGE_SIZE = 20 * 1024 * 1024  # 20 MB inline upload limit

SUPPORTED_MIME_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/gif",
    "image/heic",
    "image/heif",
}


def load_text_file(filename: str) -> str:
    path = SCRIPT_DIR / filename
    if not path.exists():
        print(f"Error: Required file not found: {path}", file=sys.stderr)
        sys.exit(1)
    return path.read_text(encoding="utf-8")


def load_image(image_path: str) -> tuple[bytes, str]:
    """Load image from a local path or URL. Returns (bytes, mime_type)."""
    if image_path.startswith(("http://", "https://")):
        try:
            req = urllib.request.Request(
                image_path,
                headers={"User-Agent": "looking-glass/1.0"},
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                mime_type = resp.headers.get_content_type() or "image/jpeg"
                data = resp.read()
        except (urllib.error.URLError, urllib.error.HTTPError) as e:
            print(f"Error: Failed to download image: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        path = Path(image_path)
        if not path.exists():
            print(f"Error: Image file not found: {image_path}", file=sys.stderr)
            sys.exit(1)
        mime_type = mimetypes.guess_type(str(path))[0] or "image/jpeg"
        data = path.read_bytes()

    if mime_type not in SUPPORTED_MIME_TYPES:
        print(
            f"Error: Unsupported image type '{mime_type}'. "
            f"Supported: {', '.join(sorted(SUPPORTED_MIME_TYPES))}",
            file=sys.stderr,
        )
        sys.exit(1)

    if len(data) > MAX_IMAGE_SIZE:
        size_mb = len(data) / (1024 * 1024)
        print(
            f"Error: Image too large ({size_mb:.1f} MB). "
            f"Maximum supported size is {MAX_IMAGE_SIZE // (1024 * 1024)} MB.",
            file=sys.stderr,
        )
        sys.exit(1)

    return data, mime_type


def build_system_instruction() -> str:
    system_prompt = load_text_file("system-prompt.md")
    checklist = load_text_file("outfit-checklist.md")
    return f"{system_prompt}\n\n---\n\n{checklist}"


def sanitize_output(text: str, api_key: str) -> str:
    """Remove any accidental API key leakage from the output."""
    if api_key:
        text = text.replace(api_key, "[REDACTED]")
    return text


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Analyze an outfit photo using Gemini via Vertex AI"
    )
    parser.add_argument(
        "--image",
        required=True,
        help="Path or URL to the outfit photo",
    )
    parser.add_argument(
        "--instructions",
        default="",
        help="Optional text instructions (pass '-' to read from stdin)",
    )
    args = parser.parse_args()

    instructions = args.instructions
    if instructions == "-":
        instructions = sys.stdin.read().strip()

    # Load configuration from .env in script dir or the parent dir (next to the zip)
    env_path = SCRIPT_DIR / ".env"
    if not env_path.exists():
        env_path = SCRIPT_DIR.parent / ".env"
    load_dotenv(env_path)

    api_key = os.environ.get("GOOGLE_API_KEY", "")
    project_id = os.environ.get("GOOGLE_PROJECT_ID", "")
    location = os.environ.get("GOOGLE_LOCATION", DEFAULT_LOCATION)
    model = os.environ.get("GEMINI_MODEL", DEFAULT_MODEL)

    if not api_key:
        print(
            "Error: GOOGLE_API_KEY not set. "
            "Create a .env file in the looking-glass directory with your key. "
            "See .env.example for the template.",
            file=sys.stderr,
        )
        sys.exit(1)
    if not project_id:
        print(
            "Error: GOOGLE_PROJECT_ID not set. "
            "Add your Google Cloud project ID to the .env file. "
            "See .env.example for the template.",
            file=sys.stderr,
        )
        sys.exit(1)

    image_data, mime_type = load_image(args.image)
    system_instruction = build_system_instruction()

    # Build user message parts
    user_parts: list[types.Part] = [
        types.Part.from_bytes(data=image_data, mime_type=mime_type),
    ]
    if instructions:
        user_parts.append(types.Part.from_text(text=instructions))

    client = genai.Client(
        vertexai=True,
        project=project_id,
        location=location,
        api_key=api_key,
    )

    try:
        response = client.models.generate_content(
            model=model,
            contents=[types.Content(role="user", parts=user_parts)],
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=1.0,
                thinking_config=types.ThinkingConfig(thinking_level="high"),
                media_resolution=types.MediaResolution.MEDIA_RESOLUTION_HIGH,
                max_output_tokens=2048,
                safety_settings=[
                    types.SafetySetting(
                        category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        threshold="BLOCK_ONLY_HIGH",
                    ),
                    types.SafetySetting(
                        category="HARM_CATEGORY_HATE_SPEECH",
                        threshold="BLOCK_ONLY_HIGH",
                    ),
                    types.SafetySetting(
                        category="HARM_CATEGORY_HARASSMENT",
                        threshold="BLOCK_ONLY_HIGH",
                    ),
                    types.SafetySetting(
                        category="HARM_CATEGORY_DANGEROUS_CONTENT",
                        threshold="BLOCK_ONLY_HIGH",
                    ),
                ],
            ),
        )
    except Exception as e:
        error_msg = sanitize_output(str(e), api_key)
        print(f"Error: Gemini API call failed: {error_msg}", file=sys.stderr)
        if "403" in str(e) or "Forbidden" in str(e):
            print(
                "\nTroubleshooting tips for 403 Forbidden:\n"
                "  1. Ensure the Vertex AI API is enabled on your Google Cloud project.\n"
                f"  2. Verify your API key belongs to project '{project_id}'.\n"
                f"  3. Check that model '{model}' is available in region '{location}'.\n"
                "  4. Confirm your API key has no IP or referrer restrictions that "
                "block this environment.",
                file=sys.stderr,
            )
        sys.exit(1)

    # Surface detailed error information for blocked or empty responses
    if not response.text:
        print("Error: Gemini returned an empty response.", file=sys.stderr)
        if hasattr(response, "prompt_feedback") and response.prompt_feedback:
            feedback = response.prompt_feedback
            if hasattr(feedback, "block_reason") and feedback.block_reason:
                print(f"Block reason: {feedback.block_reason}", file=sys.stderr)
            if hasattr(feedback, "safety_ratings") and feedback.safety_ratings:
                for rating in feedback.safety_ratings:
                    print(
                        f"Safety: {rating.category} = {rating.probability}",
                        file=sys.stderr,
                    )
        if response.candidates:
            candidate = response.candidates[0]
            if hasattr(candidate, "finish_reason") and candidate.finish_reason:
                print(f"Finish reason: {candidate.finish_reason}", file=sys.stderr)
            if hasattr(candidate, "safety_ratings") and candidate.safety_ratings:
                for rating in candidate.safety_ratings:
                    print(
                        f"Safety: {rating.category} = {rating.probability}",
                        file=sys.stderr,
                    )
        sys.exit(1)

    output = sanitize_output(response.text, api_key)
    print(output)


if __name__ == "__main__":
    main()
