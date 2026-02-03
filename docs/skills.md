# Overview

Agent skills are lightweight pieces of knowledge, workflows and procedures that loaded dynamically into the context on
demand (by the LLM)

## What are skills?

Directory with SKILL.md file and optional scripts, template and additional documents.

The SKILL.md file has a front matter that must include a name and description as in:

```
---
name: awsome-skill
description: awesome skill for doing cool stuff!!!
---
```

The rest is free form Markdown more or less.

## The history of agent skills

Skills were developed by Anthropic originally, but then contributed to the world. 

Check out - https://agentskills.io/

They were eagerly adopted by all other players in the AI agent arena.

## Skills and context engineering

Skills live in .claude/skills directories. These can be at different levels:

- Enterprise
- Personal: `~/.claude/skills`
- Sub-directory: `foo/.claude/skills`
- Project: `.claude/skills`
- Plugin: `<plugin>/skills`

Nested skills behave like nested CLAUDE.md files: the closer the skill is to the file you're working on, the more
specific it is. If there are two skills with the same name, higher-priority locations win (enterprise > personal >
sub-directory > project). Plugin skills use a `plugin-name:skill-name` namespace, so they don't conflict with other
levels. If a skill and a command share the same name, the skill takes precedence.

## Creating your own skills

A skill is just a directory with a `SKILL.md` file. Here's a practical example.

### Example: generate-image skill

Directory structure:

```
skills/generate-image/
├── SKILL.md
└── scripts/
    └── generate-image.py
```

**SKILL.md** - Instructions for Claude:

```markdown
---
name: generate-image
description: Generate images using OpenAI's gpt-image-1.5 model
---

# Generate Image

Create images from text prompts using the `scripts/generate-image.py` script.

## Usage

./scripts/generate-image.py "prompt" [output_file]

## Parameters

- **prompt** (required): Description of the image to generate
- **output_file** (optional): Output path. Defaults to `image.png`
  - Use `.png` for images needing transparency (icons, logos)
  - Use `.jpg` for photos
  - Use `.webp` for smaller file size

## When to use

- User asks for an image, icon, logo, illustration
- Visual content would help explain something

## Requirements

`OPENAI_API_KEY` environment variable must be set.
```

**scripts/generate-image.py** - The actual script Claude will run:

```python
#!/usr/bin/env python3
"""Generate images using OpenAI's gpt-image-1.5 model."""

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
    ext = os.path.splitext(filename)[1].lower()
    if ext in (".jpg", ".jpeg"):
        return "jpeg"
    if ext == ".webp":
        return "webp"
    return "png"

def generate_image(prompt: str, output: str) -> int:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY not set", file=sys.stderr)
        return 1

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "n": 1,
        "size": "auto",
        "output_format": get_format_from_filename(output),
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
        print(f"API Error ({e.code})", file=sys.stderr)
        return 1

    b64 = data.get("data", [{}])[0].get("b64_json")
    if not b64:
        print("No image data in response", file=sys.stderr)
        return 1

    with open(output, "wb") as f:
        f.write(base64.b64decode(b64))
    print(f"Saved to {output}")
    return 0

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt")
    parser.add_argument("output", nargs="?", default="image.png")
    args = parser.parse_args()
    return generate_image(args.prompt, args.output)

if __name__ == "__main__":
    sys.exit(main())
```

### Installing a skill

Skills can be symlinked for easy development:

```bash
# Make skill available globally
ln -sf /path/to/your/skill ~/.claude/skills/skill-name

# Or project-specific
ln -sf /path/to/your/skill .claude/skills/skill-name
```

### How skills are loaded

Only the frontmatter (name, description) is loaded into context initially. The LLM sees all available skill descriptions and decides when to load and use a skill. The full SKILL.md content is loaded only when the LLM chooses to invoke that skill.

If you provide additional files like scripts and documents these will be loaded into the context only if needed.

This means:
- **Description matters** - it's how the LLM decides whether to use the skill
- **SKILL.md can be detailed** - it's not always in context, only when needed

### Tips

- Write a clear, specific description in frontmatter - the LLM uses it to decide when to load the skill
- Include "when to use" guidance in the body for when the skill is loaded
- Scripts should have proper exit codes (0 = success, non-zero = failure)
- Use standard tools (Python, bash) that are likely available

# Reference

- https://agentskills.io/
- https://code.claude.com/docs/en/skills
- https://github.com/heilcheng/awesome-agent-skills
- https://skills.sh
