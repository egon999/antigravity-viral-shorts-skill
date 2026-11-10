import os
import sys
import asyncio
import subprocess
import edge_tts
import numpy as np
from pathlib import Path

whisper_model = None

def get_whisper():
    global whisper_model
    if whisper_model is None:
        from faster_whisper import WhisperModel
        whisper_model = WhisperModel("base.en", device="cpu", compute_type="int8")
    return whisper_model

async def _synthesize_edge_tts(text, raw_output_path, voice="en-US-ChristopherNeural", rate="+6%", pitch="+2Hz"):
    communicate = edge_tts.Communicate(text, voice=voice, rate=rate, pitch=pitch)
    await communicate.save(raw_output_path)

def master_voice_audio(raw_path, mastered_path):
    filter_chain = (
        "silenceremove=stop_periods=-1:stop_duration=0.12:stop_threshold=-40dB,"
        "acompressor=threshold=-18dB:ratio=4:attack=5:release=50,"
        "equalizer=f=120:width_type=h:width=100:g=4,"
        "volume=1.25"
    )
    cmd = f'ffmpeg -y -i "{raw_path}" -af "{filter_chain}" -ar 44100 -ac 2 "{mastered_path}"'
    subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def generate_voice(short_id, script_text, voice="en-US-ChristopherNeural", temp_dir="./temp"):
    temp_path = Path(temp_dir)
    temp_path.mkdir(parents=True, exist_ok=True)
    raw_path = temp_path / f"{short_id}_raw.mp3"
    mastered_path = temp_path / f"{short_id}_voice.wav"

    asyncio.run(_synthesize_edge_tts(script_text, str(raw_path), voice=voice))
    master_voice_audio(str(raw_path), str(mastered_path))

    model = get_whisper()
    from pydub import AudioSegment
    seg = AudioSegment.from_file(str(mastered_path)).set_frame_rate(16000).set_channels(1)
    samples = np.array(seg.get_array_of_samples(), dtype=np.float32) / 32768.0

    segments, info = model.transcribe(
        samples,
        word_timestamps=True,
        language="en",
        condition_on_previous_text=False
    )

    all_words = []
    for segment in segments:
        for word in segment.words:
            all_words.append({
                "word": word.word.strip(),
                "start": float(word.start),
                "end": float(word.end),
                "probability": float(word.probability)
            })

    total_duration = len(seg) / 1000.0

    return {
        "audio_path": str(mastered_path),
        "duration": total_duration,
        "words": all_words
    }
