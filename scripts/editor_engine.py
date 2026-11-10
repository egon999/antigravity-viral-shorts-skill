import os
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

class EditorEngine:
    def __init__(self, temp_dir="./temp"):
        self.temp_dir = Path(temp_dir)
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    def create_hook_banner(self, banner_text, color_accent_hex="#00FFCC", out_path=None):
        width, height = 960, 110
        img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        hex_clean = color_accent_hex.lstrip("#")
        r, g, b = tuple(int(hex_clean[i:i+2], 16) for i in (0, 2, 4))
        border_rgba = (r, g, b, 255)
        bg_rgba = (12, 12, 18, 235)

        draw.rounded_rectangle([(0, 0), (width, height)], radius=24, fill=bg_rgba, outline=border_rgba, width=5)

        try:
            font = ImageFont.truetype(r"C:\Windows\Fonts\arialbd.ttf", 40)
        except Exception:
            font = ImageFont.load_default()

        # Sanitize text
        clean_text = "".join([c for c in banner_text if ord(c) < 128]).strip()
        bbox = draw.textbbox((0, 0), clean_text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]

        draw.text(((width - tw) / 2, (height - th) / 2 - 3), clean_text, font=font, fill=(255, 255, 255, 255))
        
        if out_path is None:
            out_path = self.temp_dir / "hook_banner.png"
        img.save(str(out_path))
        return str(out_path)

    def slice_and_format_segment(self, in_video, start_sec, dur_sec, out_segment):
        vf = (
            "fps=60,setpts=PTS-STARTPTS,"
            "scale=1080:1920:force_original_aspect_ratio=increase,"
            "crop=1080:1920:(in_w-1080)/2:(in_h-1920)/2,"
            "eq=contrast=1.06:brightness=0.01:saturation=1.12,"
            "unsharp=3:3:0.5:3:3:0.2"
        )
        cmd = [
            "ffmpeg", "-y",
            "-ss", str(start_sec),
            "-i", str(in_video),
            "-t", str(dur_sec),
            "-vf", vf,
            "-an",
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            str(out_segment)
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return str(out_segment)

    def render_final_short(self, segments, voice_dur, audio_path, ass_caption_path, hook_title, out_video_path):
        out_video_path = Path(out_video_path)
        out_video_path.parent.mkdir(parents=True, exist_ok=True)

        # 1. Process clips
        sliced_files = []
        for idx, seg in enumerate(segments):
            dur = seg.get("duration", 3.0)
            start_s = seg.get("start", 0.0)
            in_file = seg.get("file")
            seg_out = self.temp_dir / f"slice_{idx}.mp4"
            self.slice_and_format_segment(in_file, start_s, dur, seg_out)
            sliced_files.append(seg_out)

        # 2. Concat list
        concat_txt = self.temp_dir / "concat_list.txt"
        with open(concat_txt, "w", encoding="utf-8") as f:
            for s in sliced_files:
                f.write(f"file '{Path(s).resolve().as_posix()}'\n")

        stitched_raw = self.temp_dir / "stitched_raw.mp4"
        cmd_concat = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0",
            "-i", str(concat_txt),
            "-c", "copy",
            str(stitched_raw)
        ]
        subprocess.run(cmd_concat, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # 3. Create hook banner
        banner_png = self.create_hook_banner(hook_title, "#FFCC00")

        # 4. Final render with captions and banner overlay
        escaped_ass = Path(ass_caption_path).resolve().as_posix().replace(":", "\\:")
        escaped_banner = Path(banner_png).resolve().as_posix()

        filter_complex = (
            f"[0:v]subtitles='{escaped_ass}'[vsub];"
            f"[1:v]scale=960:110[vban];"
            f"[vsub][vban]overlay=60:120:shortest=1[vout]"
        )

        cmd_final = [
            "ffmpeg", "-y",
            "-i", str(stitched_raw),
            "-loop", "1", "-i", escaped_banner,
            "-i", str(audio_path),
            "-filter_complex", filter_complex,
            "-map", "[vout]",
            "-map", "2:a",
            "-t", str(voice_dur),
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "19",
            "-r", "60",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "256k",
            "-ar", "48000",
            "-movflags", "+faststart",
            str(out_video_path)
        ]
        subprocess.run(cmd_final, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return str(out_video_path)
