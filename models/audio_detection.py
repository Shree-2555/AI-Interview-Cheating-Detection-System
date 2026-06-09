import pyaudio
import numpy as np

THRESHOLD = 500

def detect_audio():
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=44100,
                    input=True,
                    frames_per_buffer=1024)

    data = np.frombuffer(stream.read(1024), dtype=np.int16)

    volume = np.linalg.norm(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    if volume > THRESHOLD:
        return "Noise Detected"
    else:
        return "Silent"