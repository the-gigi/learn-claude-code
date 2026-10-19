#!/usr/bin/env python3
"""
Generate images from a text prompt.

Two backends, picked automatically:

  1. codex CLI built-in image_gen, whenever `codex` is on PATH (the default).
     Uses urllib instead of requests/httpx to avoid external dependencies.
  2. The `codex` CLI's built-in image_gen tool when no API key is available.
     Codex authenticates with its own ChatGPT/API credentials, so no
     OPENAI_API_KEY is needed. See the codex-side skill at
     $CODEX_HOME/skills/.system/imagegen/SKILL.md.

Usage:
    generate-image.py 'your prompt' [output.png]
    generate-image.py --backend codex 'your prompt' [output.png]
    generate-image.py -i ref1.png -i ref2.jpg 'your prompt' [output.png]

Attachments (-i/--image, repeatable) are reference images the result is based on,
e.g. profile photos to turn into illustrated characters. codex gets them via its
own `codex exec -i`, and the API backend switches to the images/edits endpoint.

Environment variables:
    OPENAI_API_KEY  - OpenAI API key. Falls back to OPENAI_API_KEY_IG if unset.
    CODEX_HOME      - Codex config dir for the fallback backend (default ~/.codex).
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import shutil
import subprocess
import sys
import urllib.request
import urllib.error
from pathlib import Path

API_URL = "https://api.openai.com/v1/images/generations"
API_EDITS_URL = "https://api.openai.com/v1/images/edits"
MODEL = "gpt-image-2"

CODEX_TIMEOUT_SECS = 600

CODEX_PROMPT = """\
Use your built-in image_gen tool to generate exactly one image.{attachments}

Prompt: {prompt}

Rules:
- Use the built-in image_gen tool only. Do not use the CLI fallback,
  scripts/image_gen.py, or OPENAI_API_KEY.
- Generate one image, not variants.
- Do not write, move, or copy any files into the workspace; leave the output
  at its default generated-images path.
- Do not ask any clarifying questions; make reasonable choices and proceed.
- Reply with ONLY the absolute path of the generated image file, nothing else.
"""


def get_api_key() -> str | None:
    return os.environ.get("OPENAI_API_KEY") or os.environ.get("OPENAI_API_KEY_IG")


CODEX_ATTACHMENTS_NOTE = (
    " Use the {n} attached image(s) as references: base the result on them,"
    " and keep any people in them recognizable."
)


def get_format_from_filename(filename: str) -> str:
    """Infer output format from file extension."""
    ext = os.path.splitext(filename)[1].lower()
    if ext in (".jpg", ".jpeg"):
        return "jpeg"
    if ext == ".webp":
        return "webp"
    return "png"


# --------------------------------------------------------------------------- #
# Backend 1: OpenAI Images API
# --------------------------------------------------------------------------- #


def multipart_body(fields: dict[str, str], files: list[tuple[str, Path]]) -> tuple[bytes, str]:
    """Encode a multipart/form-data body with the stdlib only."""
    boundary = "----generate-image-" + os.urandom(12).hex()
    parts: list[bytes] = []
    for name, value in fields.items():
        parts.append(
            f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n'.encode()
        )
    for name, path in files:
        ctype = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        parts.append(
            f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"; filename="{path.name}"\r\n'
            f"Content-Type: {ctype}\r\n\r\n".encode()
            + path.read_bytes()
            + b"\r\n"
        )
    parts.append(f"--{boundary}--\r\n".encode())
    return b"".join(parts), f"multipart/form-data; boundary={boundary}"


def generate_via_api(prompt: str, output: str, images: list[Path]) -> int:
    api_key = get_api_key()
    if not api_key:
        print("❌ Error: OPENAI_API_KEY (or OPENAI_API_KEY_IG) not set", file=sys.stderr)
        return 1

    output_format = get_format_from_filename(output)
    print(f"🖼️  Generating via OpenAI API ({MODEL}): {prompt}")
    print(f"📁 Output: {output} ({output_format})")
    for img in images:
        print(f"📎 Reference: {img}")

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "n": 1,
        "size": "auto",
        "output_format": output_format,
    }

    # Reference images go to the edits endpoint as multipart `image[]` fields;
    # the generations endpoint is JSON-only and takes no images.
    if images:
        body, ctype = multipart_body(
            {k: str(v) for k, v in payload.items()}, [("image[]", p) for p in images]
        )
        url = API_EDITS_URL
    else:
        body, ctype = json.dumps(payload).encode("utf-8"), "application/json"
        url = API_URL

    try:
        req = urllib.request.Request(
            url,
            data=body,
            headers={
                "Content-Type": ctype,
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
    except Exception as e:
        print(f"❌ Failed to save image: {e}", file=sys.stderr)
        return 1

    report_saved(output)
    return 0


# --------------------------------------------------------------------------- #
# Backend 2: codex CLI built-in image_gen
# --------------------------------------------------------------------------- #


def codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex")


def snapshot_generated_images() -> set[Path]:
    root = codex_home() / "generated_images"
    if not root.is_dir():
        return set()
    return {p for p in root.rglob("*") if p.is_file()}


def newest(paths: set[Path]) -> Path | None:
    if not paths:
        return None
    return max(paths, key=lambda p: p.stat().st_mtime)


def convert_format(src: Path, dest: str) -> bool:
    """Best-effort re-encode into the extension the caller asked for.

    codex's built-in image_gen always returns PNG, so jpg/webp destinations
    need a local re-encode. `sips` (always present on darwin) can write jpeg
    but only *reads* webp, so webp goes through `cwebp` when it is installed.
    Returns True on success; callers fall back to a raw copy plus a warning.
    """
    fmt = get_format_from_filename(dest)
    if fmt == "png":
        return False

    if fmt == "webp":
        cwebp = shutil.which("cwebp")
        if not cwebp:
            return False
        cmd = [cwebp, "-quiet", str(src), "-o", dest]
    else:
        sips = shutil.which("sips")
        if not sips:
            return False
        cmd = [sips, "-s", "format", fmt, str(src), "--out", dest]

    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode == 0 and os.path.exists(dest)


def generate_via_codex(prompt: str, output: str, images: list[Path]) -> int:
    codex = shutil.which("codex")
    if not codex:
        print(
            "❌ Error: no `codex` CLI on PATH and no OPENAI_API_KEY.\n"
            "   Install codex, or set OPENAI_API_KEY (https://platform.openai.com/api-keys).",
            file=sys.stderr,
        )
        return 1

    print(f"🖼️  Generating via codex built-in image_gen: {prompt}")
    print(f"📁 Output: {output}")
    for img in images:
        print(f"📎 Reference: {img}")
    print("⏳ codex runs a full agent turn; this takes ~30s.")

    before = snapshot_generated_images()

    # read-only sandbox is enough: image_gen writes to $CODEX_HOME itself, not
    # through the shell, so codex never needs write access to the workspace.
    #
    # The prompt goes in on stdin, not as an argument: `codex exec -i` takes
    # several values, so a positional prompt after it is swallowed as one more
    # image path and codex then waits on an empty stdin.
    note = CODEX_ATTACHMENTS_NOTE.format(n=len(images)) if images else ""
    cmd = [codex, "exec", "--skip-git-repo-check", "--sandbox", "read-only"]
    for img in images:
        cmd += ["-i", str(img)]
    proc = subprocess.run(
        cmd,
        input=CODEX_PROMPT.format(prompt=prompt, attachments=note),
        capture_output=True,
        text=True,
        timeout=CODEX_TIMEOUT_SECS,
    )
    if proc.returncode != 0:
        print(f"❌ codex exec failed (exit {proc.returncode}):", file=sys.stderr)
        print((proc.stderr or proc.stdout or "").strip()[-2000:], file=sys.stderr)
        return 1

    # Trust the filesystem, not the model's final message: diff the
    # generated-images tree and take the newest addition.
    src = newest(snapshot_generated_images() - before)
    if src is None:
        print(
            "❌ codex produced no new image under "
            f"{codex_home() / 'generated_images'}",
            file=sys.stderr,
        )
        print((proc.stdout or "").strip()[-2000:], file=sys.stderr)
        return 1

    try:
        if not convert_format(src, output):
            shutil.copyfile(src, output)
            requested = get_format_from_filename(output)
            if requested != "png":
                print(
                    f"⚠️  codex returned PNG bytes; could not re-encode to {requested}. "
                    f"Copied as-is to {output}.",
                    file=sys.stderr,
                )
    except Exception as e:
        print(f"❌ Failed to save image: {e}", file=sys.stderr)
        return 1

    report_saved(output)
    print(f"   (codex source: {src})")
    return 0


# --------------------------------------------------------------------------- #


def report_saved(output: str) -> None:
    size_kb = os.path.getsize(output) / 1024
    print(f"✅ Saved to {output} ({size_kb:.1f}KB)")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate an image via the OpenAI Images API, or via the codex CLI when no API key is set."
    )
    parser.add_argument("prompt", help="The image generation prompt")
    parser.add_argument("output", nargs="?", default="image.png", help="Output filename (default: image.png)")
    parser.add_argument(
        "-i",
        "--image",
        action="append",
        default=[],
        metavar="FILE",
        help="Reference image to base the result on. Repeat for several.",
    )
    parser.add_argument(
        "--backend",
        choices=("auto", "api", "codex"),
        default="auto",
        help="auto (default): codex CLI, falling back to the OpenAI API if codex is unavailable.",
    )
    args = parser.parse_args()

    images = [Path(p).expanduser().resolve() for p in args.image]
    missing = [str(p) for p in images if not p.is_file()]
    if missing:
        print(f"❌ No such image file: {', '.join(missing)}", file=sys.stderr)
        return 1

    backend = args.backend
    if backend == "auto":
        # codex first: it uses its own credentials, so it keeps working when the
        # OpenAI account is out of credits (a 429 that cost a retry to discover).
        backend = "codex" if shutil.which("codex") else "api"

    if backend == "api":
        return generate_via_api(args.prompt, args.output, images)
    try:
        return generate_via_codex(args.prompt, args.output, images)
    except subprocess.TimeoutExpired:
        print(f"❌ codex exec timed out after {CODEX_TIMEOUT_SECS}s", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
