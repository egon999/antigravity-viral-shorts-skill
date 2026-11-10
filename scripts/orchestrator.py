import os
import sys
import json
import argparse
import time
from pathlib import Path

# Add current scripts directory to path
SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS_DIR))

from voice_engine import generate_voice
from caption_engine import generate_captions
from sound_designer import SoundDesigner
from editor_engine import EditorEngine

def produce_short(config, out_dir="./output"):
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    temp_dir = Path("./temp")
    temp_dir.mkdir(parents=True, exist_ok=True)

    short_id = config.get("id", f"short_{int(time.time())}")
    title = config.get("title", "VIRAL AI SHORT")
    hook = config.get("hook", title)
    script_text = config.get("script", "")
    voice_name = config.get("voice", "en-US-ChristopherNeural")
    segments = config.get("segments", [])
    bgm_path = config.get("bgm_path", None)

    print(f"🎬 [1/5] Synthesizing high-energy voiceover for '{title}'...")
    voice_data = generate_voice(short_id, script_text, voice=voice_name, temp_dir=temp_dir)
    print(f"   -> Voice generated: {voice_data['duration']:.2f}s, {len(voice_data['words'])} aligned words.")

    print(f"🎨 [2/5] Generating kinetic MrBeast-style word-pop captions...")
    ass_path = generate_captions(short_id, voice_data["words"], out_dir=temp_dir)

    print(f"🔊 [3/5] Designing layered SFX soundscape (whooshes, impacts, pops)...")
    designer = SoundDesigner()
    mastered_audio, audio_duration = designer.design_soundtrack(
        voice_path=voice_data["audio_path"],
        segments=segments,
        out_path=temp_dir / f"{short_id}_mastered_mix.wav",
        bgm_path=bgm_path
    )

    print(f"⚡ [4/5] Cutting B-Roll, cropping to 9:16 vertical 60 FPS, burning animated subtitles...")
    editor = EditorEngine(temp_dir=temp_dir)
    final_output_file = out_path / f"{short_id}.mp4"
    editor.render_final_short(
        segments=segments,
        voice_dur=voice_data["duration"],
        audio_path=mastered_audio,
        ass_caption_path=ass_path,
        hook_title=hook,
        out_video_path=final_output_file
    )

    print(f"✅ [5/5] Render complete! File saved at: {final_output_file.resolve()}")
    return str(final_output_file.resolve())

def main():
    parser = argparse.ArgumentParser(description="Antigravity Viral Shorts Production Engine")
    parser.add_argument("--config", type=str, help="Path to JSON manifest configuration")
    parser.add_argument("--script", type=str, help="Script text for narration")
    parser.add_argument("--title", type=str, default="VIRAL HOOK", help="Hook title for top banner")
    parser.add_argument("--voice", type=str, default="en-US-ChristopherNeural", help="Edge-TTS voice name")
    parser.add_argument("--clips", nargs="+", help="Paths to B-roll MP4 clips")
    parser.add_argument("--output", type=str, default="./output", help="Output directory")

    args = parser.parse_args()

    if args.config:
        with open(args.config, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        produce_short(cfg, out_dir=args.output)
    elif args.script and args.clips:
        # Build segments automatically dividing duration across clips
        segments = []
        clip_dur = 3.0
        for c in args.clips:
            segments.append({
                "file": c,
                "start": 0.0,
                "duration": clip_dur
            })
        cfg = {
            "title": args.title,
            "hook": args.title,
            "script": args.script,
            "voice": args.voice,
            "segments": segments
        }
        produce_short(cfg, out_dir=args.output)
    else:
        print("Usage: python orchestrator.py --config manifest.json OR python orchestrator.py --script '...' --clips clip1.mp4 clip2.mp4")

if __name__ == "__main__":
    main()
