import os
from ffmpeg.ffprobe import FFprobe


class AudioFile:
    path: str
    data: dict[str, str]
    pos: tuple[str, str] = None

    def __init__(self, audio_path: str) -> None:
        if not os.path.isfile(audio_path):
            raise Exception("ERROR: Audio not found!")
        self.path = audio_path
        self.data = FFprobe.get_audio_info(audio_path)

    def get_duration(self) -> str:
        return self.data["format"]["duration"]
