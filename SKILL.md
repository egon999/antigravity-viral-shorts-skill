---
name: viral-shorts-engine
description: Autonomous AI viral shorts production engine for YouTube Shorts, Reels, and TikTok. Generates high-retention scripts, neural voiceover (edge-tts) with Faster-Whisper word alignment, kinetic animated pop captions, sound design, and 60 FPS 9:16 FFmpeg video assembly.
metadata:
  author: egon999
  version: 2.0.0
---

# 🚀 Viral Shorts Engine — Antigravity Agent Skill

An autonomous, end-to-end viral video production pipeline built specifically for Google Antigravity. It takes a raw topic or script, generates energetic neural voiceover, aligns exact word timestamps via Faster-Whisper, formats video footage into 9:16 vertical 60 FPS cuts, layers dynamic sound design (whooshes, impacts, pops), and burns kinetic animated captions (MrBeast / Hormozi style) directly into the video.

## ✨ Key Capabilities
- **Neural Voiceover**: Powered by `edge-tts` with vocal EQ mastering, silence clipping, and multi-band compression.
- **Word-Level Subtitle Sync**: Zero drift! Uses `faster-whisper` for millisecond-level word timing.
- **Kinetic Word-Pop Captions**: Generates `.ass` styling with custom bounce animations (`\fscx\fscy`) and colored keywords (Gold, Coral Red, Spring Green).
- **Automated Sound Design**: Places whooshes at clip transitions, impacts on hooks, and pops on punchlines.
- **Vertical 9:16 Auto-Crop**: Converts 16:9 or 4:3 footage into vertical 1080x1920 with high-contrast color grading and unsharp masks.
- **Top Hook Neon Banner**: Creates high-CTR top pill banners to retain mobile viewers.

---

## 🛠️ Installation & Setup

### 1. Install Requirements
Ensure you have `ffmpeg` installed on your machine and run:
```bash
pip install edge-tts faster-whisper pydub numpy pillow
```

### 2. Antigravity Skill Registration
Copy this directory into your Antigravity skills directory:
```powershell
Copy-Item -Path "viral-shorts-engine" -Destination "$HOME\.gemini\config\skills\viral-shorts-engine" -Recurse -Force
```

---

## 🎬 How to Use

### Option A: Direct CLI Execution
```bash
python scripts/orchestrator.py --config example_manifest.json
```

Or pass arguments directly:
```bash
python scripts/orchestrator.py \
  --title "TOP 3 SECRET HACKS" \
  --script "You won't believe what happens when you try this simple trick! Number one will blow your mind!" \
  --clips assets/clips/clip1.mp4 assets/clips/clip2.mp4 assets/clips/clip3.mp4 \
  --voice "en-US-ChristopherNeural" \
  --output ./Final_Shorts
```

### Option B: Antigravity Agent Trigger Prompt
Ask Antigravity in chat:
> *"Using the `viral-shorts-engine` skill, create a 30-second viral YouTube Short about the top 3 AI engineering breakthroughs this week. Synthesize high-energy voiceover, assemble real vertical footage, add kinetic captions and punchy sound design."*

---

## 📁 Repository Structure
- `scripts/orchestrator.py`: Master pipeline coordinator.
- `scripts/voice_engine.py`: Audio synthesis & Faster-Whisper word alignment.
- `scripts/caption_engine.py`: Kinetic pop caption generator (.ass format).
- `scripts/sound_designer.py`: Automated SFX placement & audio mastering.
- `scripts/editor_engine.py`: FFmpeg vertical cropping, banner overlay & 60 FPS renderer.
- `assets/Sound_Effects/`: High-impact royalty-free WAV sound effects.
