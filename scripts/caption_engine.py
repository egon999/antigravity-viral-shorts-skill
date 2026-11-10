import os
import re
from pathlib import Path

HIGHLIGHT_GOLD = {
    "ELEVATOR", "DROPPED", "NOWHERE", "SURVIVAL", "INSTINCT", "CABLES",
    "BATTERY", "PERCENT", "CONCRETE", "RESCUE", "NIGHTMARE", "STAIRS",
    "SPLASH", "GRAVITY", "UNDEFEATED", "NINJA", "WARRIOR", "TARZAN",
    "BELLY", "FLOP", "NEVER", "SUPERCAR", "SKYSCRAPER", "PHYSICS",
    "DELETED", "CHEESEBURGERS", "BOWLING", "MODDERS", "DIFFERENT", "SPEEDRUN",
    "INSANE", "MONEY", "SECRET", "HACK", "CRAZY", "EPIC", "MILLION", "BILLION"
}

HIGHLIGHT_CORAL = {
    "PRAY", "SMASHING", "CRACK", "PANIC", "ZERO", "DEAD",
    "GIVE", "OUT", "SAVAGE", "LUNGES", "STUCK", "BURNS",
    "CRUSHED", "IMPOSSIBLE", "RIDICULOUS", "ILLEGAL", "DANGEROUS", "HIM",
    "FAIL", "CRASH", "EXPLODE", "LOST", "DESTROYED", "DEATH", "WARNING"
}

HIGHLIGHT_GREEN = {
    "CHEF", "LUCK", "HERO", "LANDS", "SAFETY", "WIN", "CLEAN", "FAST",
    "WINNER", "PRO", "GOD", "PERFECT", "RECORD", "BEAT", "GENIUS"
}

def format_ass_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    cs = int(round((sec - int(sec)) * 100))
    if cs >= 100: cs = 99
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

def generate_captions(short_id, words, out_dir="./temp", font_name="Arial Black", font_size=80):
    out_path = Path(out_dir) / f"{short_id}_captions.ass"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    header = f"""[Script Info]
Title: Antigravity Viral Shorts Dynamic Captions
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: ViralPop,{font_name},{font_size},&H00FFFFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,6,3,2,60,60,520,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    events = []
    chunk_size = 2
    i = 0
    clean_words = [w for w in words if w["word"].strip()]

    while i < len(clean_words):
        chunk = clean_words[i:i + chunk_size]
        i += chunk_size
        if not chunk:
            continue

        c_start = chunk[0]["start"]
        c_end = chunk[-1]["end"]
        if c_end <= c_start:
            c_end = c_start + 0.5

        for active_idx, target_word in enumerate(chunk):
            w_start = target_word["start"]
            w_end = target_word["end"]
            if w_end <= w_start:
                w_end = w_start + 0.35

            formatted_tokens = []
            for idx, w in enumerate(chunk):
                raw = w["word"].strip().upper()
                alphanumeric = re.sub(r'[^A-Z0-9]', '', raw)

                if idx == active_idx:
                    color = "&H0000FFFF"  # Yellow default
                    if alphanumeric in HIGHLIGHT_GOLD:
                        color = "&H0000D7FF"  # Bright Gold
                    elif alphanumeric in HIGHLIGHT_CORAL:
                        color = "&H004554FF"  # Coral Red
                    elif alphanumeric in HIGHLIGHT_GREEN:
                        color = "&H0000FF7F"  # Spring Green

                    token_str = (
                        r"{\t(0,70,\fscx120\fscy120)}"
                        r"{\t(70,160,\fscx100\fscy100)}"
                        f"{{\\c{color}\\bord8\\shad4}}"
                        f"{raw}"
                        r"{\c&H00FFFFFF&\bord6\shad3}"
                    )
                else:
                    token_str = f"{{\\c&H00FFFFFF&\\bord6\\shad3}}{raw}"

                formatted_tokens.append(token_str)

            text_payload = " ".join(formatted_tokens)
            line = f"Dialogue: 0,{format_ass_time(w_start)},{format_ass_time(w_end)},ViralPop,,0,0,0,,{text_payload}"
            events.append(line)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events) + "\n")

    return str(out_path)
