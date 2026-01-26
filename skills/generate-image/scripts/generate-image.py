#!/usr/bin/env python3
"""
Generate images using OpenAI's gpt-image-1.5 model.

Uses urllib instead of requests/httpx to avoid external dependencies.

Usage:
    generate-image.py 'your prompt' [output.png]

Environment variables:
    OPENAI_API_KEY - Required. Your OpenAI API key.
"""

import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error

API_URL = "https://api.openai.com/v1/images/generations"
MODEL = "gpt-image-1.5"


def get_format_from_filename(filename: str) -> str:
    """Infer output format from file extension."""
    ext = os.path.splitext(filename)[1].lower()
    if ext in (".jpg", ".jpeg"):
        return "jpeg"
    if ext == ".webp":
        return "webp"
    return "png"


def generate_image(prompt: str, output: str) -> int:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY not set", file=sys.stderr)
        return 1

    output_format = get_format_from_filename(output)
    print(f"🖼️  Generating: {prompt}")
    print(f"📁 Output: {output} ({output_format})")

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "n": 1,
        "size": "auto",
        "output_format": output_format,
    }

    try:
        req = urllib.request.Request(
            API_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
        )
        with urllib.request.urlopen(req) as resp:
            data = json.load(resp)
    except urllib.error.HTTPError as e:
        print(f"❌ API Error ({e.code}):", file=sys.stderr)
        try:
            error = json.load(e).get("error", {})
            print(error.get("message", "Unknown error"), file=sys.stderr)
        except Exception:
            pass
        return 1
    except urllib.error.URLError as e:
        print(f"❌ Network error: {e.reason}", file=sys.stderr)
        return 1

    b64 = data.get("data", [{}])[0].get("b64_json")
    if not b64:
        print("❌ No image data in response", file=sys.stderr)
        return 1

    try:
        with open(output, "wb") as f:
            f.write(base64.b64decode(b64))
        size_kb = os.path.getsize(output) / 1024
        print(f"✅ Saved to {output} ({size_kb:.1f}KB)")
        return 0
    except Exception as e:
        print(f"❌ Failed to save image: {e}", file=sys.stderr)
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate images using OpenAI's gpt-image-1.5 model.")
    parser.add_argument("prompt", help="The image generation prompt")
    parser.add_argument("output", nargs="?", default="image.png", help="Output filename (default: image.png)")
    args = parser.parse_args()
    return generate_image(args.prompt, args.output)


if __name__ == "__main__":
    sys.exit(main())
