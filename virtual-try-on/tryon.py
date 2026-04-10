#!/usr/bin/env python3
"""Virtual try-on: edit a person's outfit using OpenAI's gpt-image-1.5 model."""

import argparse
import base64
import mimetypes
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

SCRIPT_DIR = Path(__file__).resolve().parent

MAX_IMAGE_SIZE = 50 * 1024 * 1024  # 50 MB for GPT image models

SUPPORTED_MIME_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}

DEFAULT_OUTPUT_DIR = "/tmp"


def load_image(image_path: str) -> tuple[bytes, str]:
    """Load image from a local path or URL. Returns (bytes, mime_type)."""
    if image_path.startswith(("http://", "https://")):
        try:
            req = urllib.request.Request(
                image_path,
                headers={"User-Agent": "virtual-try-on/1.0"},
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


def sanitize_output(text: str, api_key: str) -> str:
    """Remove any accidental API key leakage from the output."""
    if api_key:
        text = text.replace(api_key, "[REDACTED]")
    return text


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Edit a person's outfit using OpenAI's gpt-image-1.5"
    )
    parser.add_argument(
        "--image",
        required=True,
        help="Path or URL to the person's photo",
    )
    parser.add_argument(
        "--instructions",
        required=True,
        help="Outfit change instructions: a text string, '-' to read from stdin, or a file path",
    )
    parser.add_argument(
        "--output",
        default=None,
        help=f"Path to save the output image (default: auto-generated in {DEFAULT_OUTPUT_DIR})",
    )
    args = parser.parse_args()

    instructions = args.instructions
    if instructions == "-":
        instructions = sys.stdin.read().strip()
    elif Path(instructions).is_file():
        instructions = Path(instructions).read_text(encoding="utf-8").strip()

    if not instructions:
        print("Error: Instructions cannot be empty.", file=sys.stderr)
        sys.exit(1)

    # Load configuration from .env
    env_path = SCRIPT_DIR / ".env"
    if not env_path.exists():
        env_path = SCRIPT_DIR.parent / ".env"
    load_dotenv(env_path)

    api_key = os.environ.get("OPENAI_API_KEY", "")

    if not api_key:
        print(
            "Error: OPENAI_API_KEY not set. "
            "Create a .env file in the virtual-try-on directory with your key. "
            "See .env.example for the template.",
            file=sys.stderr,
        )
        sys.exit(1)

    image_data, mime_type = load_image(args.image)

    client = OpenAI(api_key=api_key)

    # Map MIME types to file extensions for the upload tuple
    ext_map = {
        "image/jpeg": "input.jpg",
        "image/png": "input.png",
        "image/webp": "input.webp",
    }
    filename = ext_map.get(mime_type, "input.png")

    try:
        response = client.images.edit(
            model="gpt-image-1.5",
            image=(filename, image_data, mime_type),
            prompt=instructions,
            quality="auto",
            input_fidelity="high",
            size="auto",
            output_format="png",
            n=1,
            extra_body={"moderation": "low"},
        )
    except Exception as e:
        error_msg = sanitize_output(str(e), api_key)
        print(f"Error: OpenAI API call failed: {error_msg}", file=sys.stderr)
        if "401" in str(e) or "Unauthorized" in str(e):
            print(
                "\nTroubleshooting: Check that your OPENAI_API_KEY is valid "
                "and has access to gpt-image-1.5.",
                file=sys.stderr,
            )
        if "429" in str(e) or "Rate" in str(e):
            print(
                "\nTroubleshooting: Rate limit reached. Wait a moment and try again.",
                file=sys.stderr,
            )
        sys.exit(1)

    # gpt-image-1.5 always returns base64-encoded images
    if not response.data or not response.data[0].b64_json:
        print("Error: OpenAI returned an empty response.", file=sys.stderr)
        sys.exit(1)

    try:
        image_bytes = base64.b64decode(response.data[0].b64_json)
    except Exception as e:
        print(f"Error: Failed to decode image data: {e}", file=sys.stderr)
        sys.exit(1)

    # Generate a unique output path if none specified
    if args.output:
        output_path = Path(args.output)
    else:
        timestamp = int(time.time() * 1000)
        output_path = Path(DEFAULT_OUTPUT_DIR) / f"virtual-try-on-{timestamp}.png"

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_bytes(image_bytes)
    except OSError as e:
        print(f"Error: Failed to save output image: {e}", file=sys.stderr)
        sys.exit(1)

    print(str(output_path))


if __name__ == "__main__":
    main()
