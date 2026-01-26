---
name: generate-image
description: Generate images using OpenAI's gpt-image-1.5 model
---

# Generate Image

Create images from text prompts using the `scripts/generate-image.py` script.

## Usage

```bash
./scripts/generate-image.py "prompt" [output_file]
```

## Parameters

- **prompt** (required): Description of the image to generate
- **output_file** (optional): Output path. Defaults to `image.png`
  - Use `.png` for images needing transparency (icons, logos)
  - Use `.jpg` for photos
  - Use `.webp` for smaller file size

## When to use

- User asks for an image, icon, logo, illustration
- Visual content would help explain something
- User explicitly requests image generation

## Requirements

`OPENAI_API_KEY` environment variable must be set.
