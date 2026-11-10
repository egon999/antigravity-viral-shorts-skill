# 🚀 Antigravity Viral Shorts Production Skill

> **The Autonomous Agentic Video Pipeline for Google Antigravity & Content Creators.**  
> Create high-retention, viral vertical shorts (YouTube Shorts, Instagram Reels, TikTok) completely through AI.

[![Antigravity Compatible](https://img.shields.io/badge/Antigravity-Ready-6366f1?style=for-the-badge&logo=google)](https://github.com/egon999/antigravity-viral-shorts-skill)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776ab?style=for-the-badge&logo=python)](https://python.org)
[![FFmpeg Accelerated](https://img.shields.io/badge/FFmpeg-60fps%20Render-green?style=for-the-badge&logo=ffmpeg)](https://ffmpeg.org)

---

## ⚡ What is This?
This skill distills the automated video editing workflow developed inside Google Antigravity for producing viral short-form content. 

Unlike traditional "code-slides" or static presentations, this engine enforces **The Pure Real Hybrid Edit Standard**:
1. **Dynamic Multi-Cut Pacing**: Cuts every 1.5 to 3 seconds with smart 9:16 vertical re-framing.
2. **AI Voiceover & Perfect Word Sync**: High-energy `edge-tts` narration aligned to millisecond precision with `faster-whisper`.
3. **Kinetic Animated Captions**: Bouncy, popping words with color-coded psychological keyword highlighting (Gold, Coral Red, Spring Green) in SubStation Alpha (`.ass`) format.
4. **Tactile Sound Design**: Automated whooshes at scene cuts, heavy bass impacts on hooks, and comedic pops on punchlines.
5. **High-CTR Top Pill Banner**: Modern neon-bordered callout banner that locks mobile viewers in during the first 3 seconds.

---

## 📥 Quick Installation in Google Antigravity

Clone or download this skill into your Antigravity skills directory:

```bash
# In your terminal / command prompt:
git clone https://github.com/egon999/antigravity-viral-shorts-skill.git ~/.gemini/config/skills/viral-shorts-engine
```

Install dependencies:
```bash
pip install edge-tts faster-whisper pydub numpy pillow
```
*(Make sure `ffmpeg` is installed and available on your system PATH)*

---

## 🎯 How to Use with Antigravity

Once installed, simply prompt Antigravity in your conversation:

```text
@viral-shorts-engine Create a 45-second high-energy short about the wildest discoveries in deep space. 
Use ChristopherNeural voiceover, cut between dynamic space footage, add MrBeast-style bouncing captions, 
and layer tactical whooshes and impacts.
```

Antigravity will autonomously:
1. Script the video with hook-first retention structure.
2. Synthesize and master the vocal track.
3. Compute word-level timestamps using Whisper.
4. Format and slice video clips to 1080x1920 @ 60 FPS.
5. Mix the sound effects track.
6. Render the final MP4 ready for upload!

---

## 💻 Manual CLI Usage

You can also run the engine directly from your terminal:

```bash
# Using a JSON manifest
python scripts/orchestrator.py --config example_manifest.json

# Using CLI flags
python scripts/orchestrator.py \
  --title "UNBELIEVABLE MOMENTS! 😱" \
  --script "You won't believe what happens in this clip! Number three is completely illegal!" \
  --clips clip1.mp4 clip2.mp4 clip3.mp4 \
  --voice "en-US-ChristopherNeural" \
  --output ./Final_Shorts
```

---

## 📂 Architecture

```
viral-shorts-engine/
├── SKILL.md                 # Antigravity skill specification & instructions
├── scripts/
│   ├── orchestrator.py      # Master pipeline coordinator
│   ├── voice_engine.py      # Edge-TTS synthesis & Faster-Whisper alignment
│   ├── caption_engine.py    # Kinetic word-pop ASS subtitle builder
│   ├── sound_designer.py    # SFX overlay & multi-track audio mastering
│   └── editor_engine.py     # 9:16 vertical crop, top banner & 60fps FFmpeg render
├── assets/
│   ├── Sound_Effects/       # Royalty-free impacts, whooshes, pops, risers
│   └── Graphics/            # Visual badges and HUD reticles
├── requirements.txt         # Python dependencies
└── README.md                # Documentation & quickstart
```

---

## 🌟 Author & Community
- Built by **Ayushman ([@egon999](https://github.com/egon999))**
- Star ⭐ this repository if you find it helpful!
- Follow on Instagram for daily AI automation and agentic workflows.
