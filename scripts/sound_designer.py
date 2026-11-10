import os
import subprocess
from pathlib import Path
from pydub import AudioSegment

class SoundDesigner:
    def __init__(self, assets_dir=None):
        if assets_dir is None:
            self.assets_dir = Path(__file__).resolve().parent.parent / "assets" / "Sound_Effects"
        else:
            self.assets_dir = Path(assets_dir)

    def load_sfx(self, name):
        p = self.assets_dir / f"{name}.wav"
        if not p.exists():
            p = self.assets_dir / f"{name}.mp3"
        if p.exists():
            return AudioSegment.from_file(str(p))
        return None

    def design_soundtrack(self, voice_path, segments, out_path, bgm_path=None, bgm_volume=-18):
        voice = AudioSegment.from_file(voice_path)
        total_duration_ms = len(voice)

        # Base mix with voice
        mix = voice

        # Add transition whoosh at each segment cut
        whoosh = self.load_sfx("whoosh")
        impact = self.load_sfx("impact")
        pop = self.load_sfx("pop")

        # Initial hook impact
        if impact:
            imp = impact - 4
            mix = mix.overlay(imp, position=50)

        # Overlay SFX at cuts
        cumulative_ms = 0
        for idx, seg in enumerate(segments):
            seg_dur_ms = int(seg.get("duration", 3.0) * 1000)
            if idx > 0 and cumulative_ms < total_duration_ms:
                if whoosh:
                    w = whoosh - 6
                    pos = max(0, cumulative_ms - 150)
                    mix = mix.overlay(w, position=pos)
                if idx % 2 == 1 and pop:
                    p = pop - 8
                    mix = mix.overlay(p, position=min(total_duration_ms, cumulative_ms + 100))
            cumulative_ms += seg_dur_ms

        # Optional background music bed (ducked)
        if bgm_path and Path(bgm_path).exists():
            bgm = AudioSegment.from_file(bgm_path)
            bgm = bgm + bgm_volume
            # Loop bgm to fit duration
            while len(bgm) < total_duration_ms + 1000:
                bgm = bgm + bgm
            bgm = bgm[:total_duration_ms].fade_in(500).fade_out(800)
            mix = bgm.overlay(mix)

        out_path = Path(out_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        mix.export(str(out_path), format="wav")
        return str(out_path), total_duration_ms / 1000.0
