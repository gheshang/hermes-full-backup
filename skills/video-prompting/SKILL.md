---
name: video-prompting
description: Draft and refine prompts for video generation models (text-to-video and image-to-video), and create character-sheet prompts for image models when the goal is character consistency before image-to-video. Use when a user asks for a "video prompt", a model-specific prompt such as Seedance 2.0, Ovi, Sora, Veo 3, Wan 2.2, LTX-2, or LTX-2.3, or a consistent-character prompt such as "character sheet prompt", "character turnaround", "character reference sheet", or "photographic identity sheet".
---

# Video Prompting

## Overview

Turn a user’s intent into either:

- a strong, model-compliant video prompt, or
- a strong image-model prompt for a character sheet that will later support image-to-video consistency.

Model-specific video guidance lives in `references/models/`. Character-sheet guidance lives in `references/workflows/character-sheets.md`.
This file is the entry point: route to the right path, ask the minimum clarifying questions, then draft the prompt in the expected format.

## Model Index

- Ovi: `references/models/ovi/prompting.md`
- Sora (Sora 2): `references/models/sora/prompting.md`
- Veo 3 / 3.1: `references/models/veo3/prompting.md`
- Wan 2.2: `references/models/wan22/prompting.md`
- Seedance 2.0: `references/models/seedance2/prompting.md`
- LTX-2: `references/models/ltx2/prompting.md`
- LTX-2.3: `references/models/ltx2-3/prompting.md`

## Workflow Index

- Character sheets for consistent characters: `references/workflows/character-sheets.md`

To add a new model later: create `references/models/<model>/prompting.md`, then add it to this index.

To add a new workflow later: create `references/workflows/<workflow>.md`, then add it to the Workflow Index.

## Workflow

### Step 1 — Route the request

Decide whether the user wants:

- a video-generation prompt, or
- a character-sheet prompt for an image model

Route to the character-sheet workflow when the user wants a reusable reference sheet, turnaround, expression sheet, costume sheet, photographic identity sheet, or a consistent-character starting point for a longer image-to-video project.

If the user is asking for both, do them in this order:

1. Character sheet
2. Scene still / anchor frame
3. Video prompt

### Step 2 — If it is a video prompt, identify the model and input mode

If the user did not name a model, ask which model they are using (or offer supported options from the Model Index).

Then confirm the input mode:

- Text-to-video (t2v), or
- Image-to-video (i2v)

If i2v: ask the user to share the image (optional, but it will help you generate a better prompt). Use the image as an anchor according to the chosen model’s guidance (e.g., keep identity/wardrobe/composition stable; focus your text on motion/camera/what changes).

If the chosen model has versions, duration constraints, or required parameters, ask the minimum questions needed to select the right format (see the model guide).
For LTX-2.3 specifically: default to a 10-second clip when duration is missing, ask if the user wants shorter or longer, and scale motion complexity to match that duration.

### Step 3 — Load the correct reference and follow its format

For video prompts: open the model’s `prompting.md` from the Model Index and follow its rules strictly.

For character sheets: open `references/workflows/character-sheets.md` and follow its structure strictly. Treat this as an image-model prompt, not a video-model prompt.

### Step 4 — Draft the prompt in the right form

Draft the prompt using the structure and constraints from the markdown file you selected in Step 3.

For video prompts: follow the chosen model’s `prompting.md` exactly, including its preferred section order, dialogue/audio format, and any shot-structure guidance.

For character sheets: follow `references/workflows/character-sheets.md` exactly, including layout, consistency constraints, and expression-row guidance.

### Step 5 — Output

Default: output only the final prompt text.
Default formatting: output prompts as a single line with no line breaks unless the user explicitly requests multiline formatting.

If the user asks for options: provide 2–3 distinct prompt variants, each fully self-contained and compliant with the model’s formatting.

If the model uses required API parameters (e.g., duration/size), include a short “Recommended parameters” line only when the user has specified them or explicitly asks for them.

If the user wants the full consistency workflow, after the character-sheet prompt also provide:

- one prompt for a first scene still that uses the character sheet as reference, and
- one prompt for the follow-on image-to-video shot

## Multi-scene project workflow (minimize generation count)

When a user has a multi-scene script (e.g. 10+ scenes) and limited generation quota, merge scenes into longer clips using Extend rather than generating each scene independently.

### Strategy: pair adjacent scenes per video, use Extend to chain them

1. **Initial generation**: 8-second clip covering Scene N (full detail, no compression)
2. **Extend**: Continue the video for another 8 seconds covering Scene N+1 (Veo 3.1 generates from the last frame, natural transition)
3. Each "video unit" = 1 initial generation + 1 Extend = 2 scenes, 16 seconds

### Key rules
- **Never compress scene content to fit fewer generations** — users will notice and object
- Extend costs credits in Google Flow (≈same as a new generation), so it doesn't save quota — what it saves is **manual assembly effort** (7 clips vs 14 clips to stitch)
- Pair scenes by visual continuity: scenes with the same location/character/mood go together
- For Gemini App (3 videos/day on Pro): a 14-scene project at 7 clips takes 3 days
- For Google Flow (1000 credits/month on Pro): Veo 3 Fast = 10 credits/gen, 7 initial + 6 extend = 130 credits — doable in 1 day

### Quota reference (Google AI Pro, $19.99/month)

| Channel | Limit | Veo 3 Fast cost |
|---------|-------|-----------------|
| Gemini App | 3 videos/day | 1 generation |
| Google Flow | ~100 credits/month (Veo 3 with audio ≈50/gen) | Veo 3 Fast ≈10 credits/gen |
| Google AI Studio API | pay-per-second | $0.35/sec |
