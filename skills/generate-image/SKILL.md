---
name: generate-image
description: Generate images using OpenAI's gpt-image-2 model, or the codex CLI's built-in image_gen when no OpenAI API key is set
---

# Generate Image

Create images from text prompts using the `scripts/generate-image.py` script.

## Usage

```bash
./scripts/generate-image.py "prompt" [output_file]
./scripts/generate-image.py --backend codex "prompt" [output_file]
./scripts/generate-image.py -i photo1.png -i photo2.jpg "prompt" [output_file]
```

## Parameters

- **prompt** (required): Description of the image to generate
- **output_file** (optional): Output path. Defaults to `image.png`
  - Use `.png` for images needing transparency (icons, logos)
  - Use `.jpg` for photos
  - Use `.webp` for smaller file size
- **-i / --image** (optional, repeatable): a reference image to base the result on, e.g. profile photos to turn into illustrated characters. The codex backend passes each one to `codex exec -i` and sends the prompt on stdin, because `-i` takes several values and would swallow a positional prompt as one more image path. The API backend switches to the `images/edits` endpoint and uploads them as multipart `image[]` fields.
- **--backend** (optional): `auto` (default), `api`, or `codex`

## When to use

- User asks for an image, icon, logo, illustration
- Visual content would help explain something
- User explicitly requests image generation

## Backends

The script picks a backend automatically, preferring codex:

| Backend | Selected when | Notes |
| --- | --- | --- |
| `codex` | **Default**, whenever `codex` is on `PATH` | Runs `codex exec` and lets codex's built-in `image_gen` tool do the work. Codex uses its own credentials, so it keeps working when the OpenAI account has no credits. Takes ~30s because it's a full agent turn. |
| `api` | Fallback, when `codex` isn't installed | Direct call to the OpenAI Images API with `gpt-image-2`. Honors `.png`/`.jpg`/`.webp` natively. Takes a few seconds, but returns a 429 once the account is out of credits. |

Codex is primary because the OpenAI key hit `You have no credits remaining` mid-task, which turned one image into two runs. Codex bills through its own auth and didn't care.

Force either one with `--backend api` / `--backend codex`.

### How the codex fallback works

1. Snapshots `$CODEX_HOME/generated_images` (default `~/.codex`).
2. Runs `codex exec --sandbox read-only` with a prompt that pins codex to its
   built-in `image_gen` tool and forbids the `OPENAI_API_KEY`-dependent CLI
   fallback described in `$CODEX_HOME/skills/.system/imagegen/SKILL.md`.
   Read-only is enough — `image_gen` writes into `$CODEX_HOME` itself, not
   through the shell.
3. Diffs the snapshot and copies the newest new file to `output_file`. The
   filesystem diff is the source of truth, not the path codex prints.
4. `image_gen` always returns PNG, so a `.jpg` destination is re-encoded with
   `sips` and `.webp` with `cwebp`. If `cwebp` isn't installed the PNG bytes
   are copied as-is and the script warns.

## Requirements

Either:

- `OPENAI_API_KEY` (or `OPENAI_API_KEY_IG`) set — uses the API directly, or
- the `codex` CLI on `PATH`, authenticated, with the `image_generation` feature
  enabled (`codex features list | grep image_generation` → `stable true`).

If neither is available the script exits 1 and says so. Runs on Python 3.9+
(macOS system Python included).
