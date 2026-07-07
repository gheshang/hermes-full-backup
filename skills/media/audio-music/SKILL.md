---
name: audio-music
description: Audio and music workflow — visualization (spectrograms), songwriting craft, and AI music generation (Suno, HeartMuLa, AudioCraft/MusicGen).
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [audio, music, spectrogram, visualization, songwriting, suno, heartmula, audiocraft, musicgen, text-to-music]
    related_skills: []
---

# Audio & Music — Unified Guide

This umbrella skill consolidates all audio and music-related capabilities. Each tool serves a different purpose:

- **songsee**: Spectrogram and audio feature visualization
- **songwriting-and-ai-music**: Songwriting craft and Suno AI prompts
- **heartmula**: Open-source music generation (Suno-like, HeartMuLa model)
- **audiocraft-audio-generation**: Meta's AudioCraft (MusicGen, AudioGen)

**Choose your tool based on the task:**

| Task | Tool |
|------|------|
| Visualize audio (spectrogram, MFCC, etc.) | songsee |
| Write song lyrics / Suno prompts | songwriting-and-ai-music |
| Generate music locally (Suno-like) | heartmula |
| Generate music/sound with Meta models | audiocraft-audio-generation |

---

## 1. SongSee — Audio Visualization

### Overview

Generate spectrograms and multi-panel audio feature visualizations from audio files via CLI.

### Prerequisites

Requires Go:
```bash
go install github.com/steipete/songsee/cmd/songsee@latest
```

Optional: `ffmpeg` for formats beyond WAV/MP3.

### Quick Start

```bash
# Basic spectrogram
songsee track.mp3

# Save to specific file
songsee track.mp3 -o spectrogram.png

# Multi-panel visualization grid
songsee track.mp3 --viz spectrogram,mel,chroma,hpss,selfsim,loudness,tempogram,mfcc,flux

# Time slice (start at 12.5s, 8s duration)
songsee track.mp3 --start 12.5 --duration 8 -o slice.jpg

# From stdin
cat track.mp3 | songsee - --format png -o out.png
```

### Visualization Types

| Type | Description |
|------|-------------|
| `spectrogram` | Standard frequency spectrogram |
| `mel` | Mel-scaled spectrogram |
| `chroma` | Pitch class distribution |
| `hpss` | Harmonic/percussive separation |
| `selfsim` | Self-similarity matrix |
| `loudness` | Loudness over time |
| `tempogram` | Tempo estimation |
| `mfcc` | Mel-frequency cepstral coefficients |
| `flux` | Spectral flux (onset detection) |

### Common Flags

| Flag | Description |
|------|-------------|
| `--viz` | Visualization types (comma-separated) |
| `--style` | Color palette: `classic`, `magma`, `inferno`, `viridis`, `gray` |
| `--width` / `--height` | Output image dimensions |
| `--window` / `--hop` | FFT window and hop size |
| `--min-freq` / `--max-freq` | Frequency range filter |
| `--start` / `--duration` | Time slice of the audio |
| `--format` | Output format: `jpg` or `png` |
| `-o` | Output file path |

### Notes

- WAV and MP3 decoded natively; other formats require `ffmpeg`
- Output images can be inspected with `vision_analyze` for automated audio analysis
- Useful for comparing audio outputs, debugging synthesis, or documenting audio processing pipelines

---

## 2. Songwriting & AI Music (Suno)

### Overview

Songwriting craft, AI music generation prompts (Suno focus), parody/adaptation techniques, phonetic tricks, and lessons learned.

**Everything here is a GUIDELINE, not a rule. Art breaks rules on purpose.**

### Song Structure

Common skeletons:
```
ABABCB  Verse/Chorus/Verse/Chorus/Bridge/Chorus    (most pop/rock)
AABA    Verse/Verse/Bridge/Verse (refrain-based)    (jazz standards, ballads)
ABAB    Verse/Chorus alternating                    (simple, direct)
AAA     Verse/Verse/Verse (strophic, no chorus)     (folk, storytelling)
```

Building blocks:
- Intro — set the mood
- Verse — the story, details, world-building
- Pre-Chorus — optional tension ramp
- Chorus — emotional core, what people remember
- Bridge — detour, shift in perspective
- Outro — farewell, can echo or subvert

### Rhyme, Meter, and Sound

**Rhyme types** (tight to loose):
- Perfect: lean/mean
- Family: crate/braid
- Assonance: had/glass (same vowels, different endings)
- Consonance: scene/when (different vowels, similar endings)
- Near/slant: enough to suggest connection

**Internal rhyme**: Rhyming within a line
> "We pruned the lies from bleeding trees / Distilled the storm from entropy"

**Meter**: Stressed vs unstressed syllables
- Match syllable counts between parallel lines for singability
- Stressed syllables matter more than total count
- Say it out loud. If you stumble, meter needs work.
- Intentionally breaking meter can create emphasis

### Emotional Arc and Dynamics

**Energy mapping**:
```
Intro: 2-3  |  Verse: 5-6  |  Pre-Chorus: 7
Chorus: 8-9  |  Bridge: varies  |  Final Chorus: 9-10
```

**Contrast is the most powerful dynamic trick:**
- Whisper before a scream hits harder
- Sparse before dense. Slow before fast. Low before high.
- "Whisper to roar to whisper" — start intimate, build to power, strip back

### Writing Lyrics That Work

**Show, don't tell** (usually):
- "I was sad" = flat
- "Your hoodie's still on the hook by the door" = alive

**The hook**: Line people remember, hum, repeat. Usually title or core phrase.

**Prosody** — lyrics and music supporting each other:
- Stable feelings → settled melodies, perfect rhymes, resolved chords
- Unstable feelings → wandering melodies, near-rhymes, unresolved chords
- Verse melody typically lower, chorus higher

**Avoid** (unless on purpose):
- Cliches on autopilot
- Forcing word order to hit a rhyme ("Yoda-speak")
- Same energy in every section (flat dynamics)

### Parody and Adaptation

**The skeleton**: Map original's structure first
- Count syllables per line
- Mark rhyme scheme (ABAB, AABB, etc.)
- Identify stressed syllables
- Note where held/sustained notes fall

**Fitting new words**:
- Match stressed syllables to same beats
- Total syllable count can flex by 1-2 unstressed
- On long held notes, match vowel sound of original
- Monosyllabic swaps in key spots keep rhythm intact
- Sing new words over original — if you stumble, revise

**Keep some originals**: Leaving a few original lines intact adds recognizability.

### Suno AI Prompt Engineering

**Style/Genre field formula**:
```
Genre + Mood + Era + Instruments + Vocal Style + Production + Dynamics
```

**Bad**: "sad rock song"
**Good**: "Cinematic orchestral spy thriller, 1960s Cold War era, smoky sultry female vocalist, big band jazz, brass section with trumpets and french horns, sweeping strings, minor key, vintage analog warmth"

**Describe the journey**, not just genre:
```
"Begins as haunting whisper over sparse piano. Gradually layers in muted brass. Builds through chorus with full orchestra. Second verse erupts with raw belting intensity. Outro strips back to lone piano and fragile whisper fading to silence."
```

**Tips**:
- V4.5+ supports up to 1,000 chars in Style field — use them
- NO artist names or trademarks. Describe the sound instead.
- Specify BPM and key when you have preference
- Use Exclude Styles field for what you DON'T want
- Unexpected genre combos can be gold: "bossa nova trap", "Appalachian gothic"
- Build a vocal PERSONA, not just gender

**Metatags** (place in [brackets] inside lyrics):

Structure: `[Intro] [Verse] [Verse 1] [Pre-Chorus] [Chorus] [Post-Chorus] [Hook] [Bridge] [Interlude] [Instrumental] [Guitar Solo] [Breakdown] [Build-up] [Outro] [Silence] [End]`

Vocal performance: `[Whispered] [Spoken Word] [Belted] [Falsetto] [Powerful] [Soulful] [Raspy] [Breathy] [Smooth] [Gritty] [Staccato] [Legato] [Vibrato] [Melismatic] [Harmonies] [Choir]`

Dynamics: `[High Energy] [Low Energy] [Building Energy] [Explosive] [Emotional Climax] [Gradual swell] [Orchestral swell] [Quiet arrangement] [Falling tension] [Slow Down]`

Gender: `[Female Vocals] [Male Vocals]`

Atmosphere: `[Melancholic] [Euphoric] [Nostalgic] [Aggressive] [Dreamy] [Intimate] [Dark Atmosphere]`

SFX: `[Vinyl Crackle] [Rain] [Applause] [Static] [Thunder]`

**Keep to 5-8 tags per section max**. Don't contradict yourself.

**Custom Mode**: Always use for serious work (separate Style + Lyrics). Lyrics field limit: ~3,000 chars (~40-60 lines).

### Phonetic Tricks for AI Singers

AI vocalists don't read — they pronounce.

**Phonetic respelling**:
- Spell words as they SOUND: "through" -> "thru"
- Proper nouns highest failure rate — test early
- "Nous" -> "Noose" (forces correct pronunciation)
- Hyphenate to guide syllables: "Re-search", "bio-engineering"

**Delivery control**:
- ALL CAPS = louder, more intense
- Vowel extension: "lo-o-o-ove" = sustained/melisma
- Ellipses: "I... need... you" = dramatic pauses
- Hyphenated stretch: "ne-e-ed" = emotional stretch

**Always**:
- Spell out numbers: "24/7" -> "twenty four seven"
- Space acronyms: "AI" -> "A I" or "A-I"
- Test proper nouns in short 30-second clip first
- Once generated, pronunciation is baked in — fix BEFORE

### Workflow

1. Write concept/hook first — emotional core
2. If adapting, map original structure (syllables, rhyme, stress)
3. Generate raw material — brainstorm freely before structuring
4. Draft lyrics into structure
5. Read/sing aloud — catch stumbles, fix meter
6. Build Suno style description — paint dynamic journey
7. Add metatags to lyrics for performance direction
8. Generate 3-5 variations minimum — like recording takes
9. Pick best, use Extend/Continue to build on promising sections
10. If something great happens by accident, keep it

**Expect**: ~3-5 generations per 1 good result. Revision is normal.

### Lessons Learned

- Describing dynamic ARC in style field matters more than just listing genres
- Keeping some original lines intact in parody adds recognizability
- Bridge slot is where you can transform imagery
- Monosyllabic word swaps in hooks/tags are cleanest way to maintain rhythm
- Strong vocal persona description makes bigger difference than any single metatag
- Don't be precious about rules. If a line breaks meter but hits harder, keep it.

---

## 3. HeartMuLa — Open-Source Music Generation

### Overview

HeartMuLa is a family of open-source music foundation models (Apache-2.0) that generates music conditioned on lyrics and tags. Comparable to Suno for open-source.

Components:
- **HeartMuLa** — Music language model (3B/7B) for generation from lyrics + tags
- **HeartCodec** — 12.5Hz music codec for high-fidelity audio reconstruction
- **HeartTranscriptor** — Whisper-based lyrics transcription
- **HeartCLAP** — Audio-text alignment model

### When to Use

- User wants to generate music/songs from text descriptions
- User wants open-source Suno alternative
- User wants local/offline music generation

### Hardware Requirements

- **Minimum**: 8GB VRAM with `--lazy_load true`
- **Recommended**: 16GB+ VRAM for comfortable single-GPU
- **Multi-GPU**: Use `--mula_device cuda:0 --codec_device cuda:1`
- 3B model with lazy_load peaks at ~6.2GB VRAM

### Installation

```bash
# Clone
cd ~/
git clone https://github.com/HeartMuLa/heartlib.git
cd heartlib

# Create virtual environment (Python 3.10 required)
uv venv --python 3.10 .venv
. .venv/bin/activate
uv pip install -e .

# Upgrade dependencies (required for compatibility)
uv pip install --upgrade datasets
uv pip install --upgrade transformers
```

### Required Patches

**Patch 1** — RoPE cache fix in `src/heartlib/heartmula/modeling_heartmula.py`:
```python
# In setup_caches method, add after reset_caches try/except:
from torchtune.models.llama3_1._position_embeddings import Llama3ScaledRoPE
for module in self.modules():
    if isinstance(module, Llama3ScaledRoPE) and not module.is_cache_built:
        module.rope_init()
        module.to(device)
```

**Patch 2** — HeartCodec loading fix in `src/heartlib/pipelines/music_generation.py`:
Add `ignore_mismatched_sizes=True` to ALL `HeartCodec.from_pretrained()` calls.

### Download Models

```bash
cd heartlib
hf download --local-dir './ckpt' 'HeartMuLa/HeartMuLaGen'
hf download --local-dir './ckpt/HeartMuLa-oss-3B' 'HeartMuLa/HeartMuLa-oss-3B-happy-new-year'
hf download --local-dir './ckpt/HeartCodec-oss' 'HeartMuLa/HeartCodec-oss-20260123'
```

### Usage

```bash
cd heartlib
. .venv/bin/activate
python ./examples/run_music_generation.py \
  --model_path=./ckpt \
  --version="3B" \
  --lyrics="./assets/lyrics.txt" \
  --tags="./assets/tags.txt" \
  --save_path="./assets/output.mp3" \
  --lazy_load true
```

**Tags** (comma-separated, no spaces):
```
piano,happy,wedding,synthesizer,romantic
```

**Lyrics** (use bracketed structural tags):
```
[Intro]

[Verse]
Your lyrics here...

[Chorus]
Chorus lyrics...

[Bridge]
Bridge lyrics...

[Outro]
```

### Key Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--max_audio_length_ms` | 240000 | Max length in ms (240s = 4 min) |
| `--topk` | 50 | Top-k sampling |
| `--temperature` | 1.0 | Sampling temperature |
| `--cfg_scale` | 1.5 | Classifier-free guidance scale |
| `--lazy_load` | false | Load/unload models on demand |
| `--mula_dtype` | bfloat16 | Dtype for HeartMuLa |
| `--codec_dtype` | float32 | Dtype for HeartCodec |

### Performance

- RTF ≈ 1.0 — a 4-minute song takes ~4 minutes to generate
- Output: MP3, 48kHz stereo, 128kbps

### Pitfalls

1. **Do NOT use bf16 for HeartCodec** — degrades audio quality. Use fp32.
2. **Tags may be ignored** — known issue (#90). Lyrics tend to dominate.
3. **Triton not available on macOS** — Linux/CUDA only for GPU.
4. **RTX 5080 incompatibility** reported in upstream issues.

### Links

- Repo: https://github.com/HeartMuLa/heartlib
- Models: https://huggingface.co/HeartMuLa
- Paper: https://arxiv.org/abs/2601.10547
- License: Apache-2.0

---

## 4. AudioCraft (Meta MusicGen/AudioGen)

### Overview

Meta's AudioCraft for text-to-music (MusicGen) and text-to-sound (AudioGen) generation.

### When to Use

- Generate music from text descriptions
- Create sound effects and environmental audio
- Melody-conditioned music generation
- Stereo audio output
- Style conditioning (reference-based generation)

### Installation

```bash
# From PyPI
pip install audiocraft

# From GitHub (latest)
pip install git+https://github.com/facebookresearch/audiocraft.git

# Or use HuggingFace Transformers
pip install transformers torch torchaudio
```

### Basic Text-to-Music

```python
import torchaudio
from audiocraft.models import MusicGen

# Load model
model = MusicGen.get_pretrained('facebook/musicgen-small')

# Set generation parameters
model.set_generation_params(
    duration=8,  # seconds
    top_k=250,
    temperature=1.0
)

# Generate from text
descriptions = ["happy upbeat electronic dance music with synths"]
wav = model.generate(descriptions)

# Save audio
torchaudio.save("output.wav", wav[0].cpu(), sample_rate=32000)
```

### Using HuggingFace Transformers

```python
from transformers import AutoProcessor, MusicgenForConditionalGeneration
import scipy

# Load model and processor
processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
model.to("cuda")

# Generate music
inputs = processor(
    text=["80s pop track with bassy drums and synth"],
    padding=True,
    return_tensors="pt"
).to("cuda")

audio_values = model.generate(
    **inputs,
    do_sample=True,
    guidance_scale=3,
    max_new_tokens=256
)

# Save
sampling_rate = model.config.audio_encoder.sampling_rate
scipy.io.wavfile.write("output.wav", rate=sampling_rate, data=audio_values[0, 0].cpu().numpy())
```

### Text-to-Sound (AudioGen)

```python
from audiocraft.models import AudioGen

# Load AudioGen
model = AudioGen.get_pretrained('facebook/audiogen-medium')
model.set_generation_params(duration=5)

# Generate sound effects
descriptions = ["dog barking in a park with birds chirping"]
wav = model.generate(descriptions)

torchaudio.save("sound.wav", wav[0].cpu(), sample_rate=16000)
```

### Model Variants

| Model | Size | Description | Use Case |
|-------|------|-------------|----------|
| `musicgen-small` | 300M | Text-to-music | Quick generation |
| `musicgen-medium` | 1.5B | Text-to-music | Balanced |
| `musicgen-large` | 3.3B | Text-to-music | Best quality |
| `musicgen-melody` | 1.5B | Text + melody | Melody conditioning |
| `musicgen-melody-large` | 3.3B | Text + melody | Best melody |
| `musicgen-stereo-*` | Varies | Stereo output | Stereo generation |
| `musicgen-style` | 1.5B | Style transfer | Reference-based |
| `audiogen-medium` | 1.5B | Text-to-sound | Sound effects |

### Generation Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `duration` | 8.0 | Length in seconds (1-120) |
| `top_k` | 250 | Top-k sampling |
| `top_p` | 0.0 | Nucleus sampling (0 = disabled) |
| `temperature` | 1.0 | Sampling temperature |
| `cfg_coef` | 3.0 | Classifier-free guidance |

### Melody-Conditioned Generation

```python
from audiocraft.models import MusicGen
import torchaudio

# Load melody model
model = MusicGen.get_pretrained('facebook/musicgen-melody')
model.set_generation_params(duration=30)

# Load melody audio
melody, sr = torchaudio.load("melody.wav")

# Generate with melody conditioning
descriptions = ["acoustic guitar folk song"]
wav = model.generate_with_chroma(descriptions, melody, sr)

torchaudio.save("melody_conditioned.wav", wav[0].cpu(), sample_rate=32000)
```

### Stereo Generation

```python
from audiocraft.models import MusicGen

# Load stereo model
model = MusicGen.get_pretrained('facebook/musicgen-stereo-medium')
model.set_generation_params(duration=15)

descriptions = ["ambient electronic music with wide stereo panning"]
wav = model.generate(descriptions)

# wav shape: [batch, 2, samples] for stereo
torchaudio.save("stereo.wav", wav[0].cpu(), sample_rate=32000)
```

### Audio Continuation

```python
from transformers import AutoProcessor, MusicgenForConditionalGeneration

processor = AutoProcessor.from_pretrained("facebook/musicgen-medium")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-medium")

# Load audio to continue
audio, sr = torchaudio.load("intro.wav")

# Process with text and audio
inputs = processor(
    audio=audio.squeeze().numpy(),
    sampling_rate=sr,
    text=["continue with a epic chorus"],
    padding=True,
    return_tensors="pt"
)

# Generate continuation
audio_values = model.generate(**inputs, do_sample=True, guidance_scale=3, max_new_tokens=512)
```

### Style-Conditioned Generation (MusicGen-Style)

```python
from audiocraft.models import MusicGen

# Load style model
model = MusicGen.get_pretrained('facebook/musicgen-style')

# Configure generation with style
model.set_generation_params(
    duration=30,
    cfg_coef=3.0,
    cfg_coef_beta=5.0  # Style influence
)

# Configure style conditioner
model.set_style_conditioner_params(
    eval_q=3,          # RVQ quantizers (1-6)
    excerpt_length=3.0  # Style excerpt length
)

# Load style reference
style_audio, sr = torchaudio.load("reference_style.wav")

# Generate with text + style
descriptions = ["upbeat dance track"]
wav = model.generate_with_style(descriptions, style_audio, sr)
```

### GPU Memory Requirements

| Model | FP32 VRAM | FP16 VRAM |
|-------|-----------|-----------|
| musicgen-small | ~4GB | ~2GB |
| musicgen-medium | ~8GB | ~4GB |
| musicgen-large | ~16GB | ~8GB |

### Common Issues

| Issue | Solution |
|-------|----------|
| CUDA OOM | Use smaller model, reduce duration |
| Poor quality | Increase cfg_coef, better prompts |
| Generation too short | Check max duration setting |
| Audio artifacts | Try different temperature |
| Stereo not working | Use stereo model variant |

### Alternatives

- **Stable Audio**: For longer commercial music generation
- **Bark**: For text-to-speech with music/sound effects
- **Riffusion**: For spectrogram-based music generation
- **OpenAI Jukebox**: For raw audio generation with lyrics

---

## Quick Reference

| Task | Tool | Install | Key Command |
|------|------|---------|-------------|
| Audio visualization | songsee | `go install github.com/steipete/songsee/cmd/songsee@latest` | `songsee track.mp3 --viz spectrogram,mel,chroma` |
| Suno prompts | songwriting-and-ai-music | — | See Suno prompt engineering section |
| Music generation (Suno-like) | heartmula | `pip install -e .` (from heartlib) | `python ./examples/run_music_generation.py` |
| Music/sound generation | audiocraft | `pip install audiocraft` | `MusicGen.get_pretrained('facebook/musicgen-small')` |

---

## Pitfalls Summary

1. **songsee**: Requires Go. WAV/MP3 native; other formats need ffmpeg.
2. **Songwriting**: Rules are guidelines. Art breaks rules. Focus on emotion, not perfection.
3. **HeartMuLa**: Requires patches for transformers 5.x compatibility. Do NOT use bf16 for HeartCodec.
4. **AudioCraft**: GPU memory scales with model size. Use smaller models for quick tests.