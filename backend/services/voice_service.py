from google import genai
from google.genai import types
import wave
import os

def save_wave(filename, pcm, channels=1, rate=24000, sample_width=2):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(pcm)

def generate_voice(script, output_path="output/audio.wav"):
    if not script or script.strip() == "":
        raise ValueError("Script is empty")

    client = genai.Client()  # ✅ NO api_version override

    response = client.models.generate_content(
        model="gemini-3.1-flash-tts-preview",  # ✅ correct model
        contents=[script],  # ✅ must be list
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],  # ✅ correct for this method
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name="Puck"   # 🔥 best voice
                    )
                )
            )
        )
    )

    # ✅ Extract audio safely
    try:
        audio_data = response.candidates[0].content.parts[0].inline_data.data
    except Exception as e:
        print("❌ Full response:", response)
        raise RuntimeError("Audio extraction failed") from e

    os.makedirs("output", exist_ok=True)
    save_wave(output_path, audio_data)

    print(f"🎧 Saved: {output_path}")
    return output_path