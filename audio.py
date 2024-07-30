import os
import subprocess
import json


class AudioFile:
    path: str
    data: dict[str, str]
    pos: tuple[str, str] = None

    def __init__(self, audio_path: str) -> None:
        if not os.path.isfile(audio_path):
            raise Exception("ERROR: Audio not found!")
        self.path = audio_path
        out = subprocess.run(
            [
                "ffprobe",
                "-v",
                "quiet",
                "-print_format",
                "json",
                "-sexagesimal",
                "-show_format",
                "-show_streams",
                audio_path,
            ],
            stdout=subprocess.PIPE,
        )
        if out.returncode != 0:
            raise Exception("ERROR: Invalid audio!")

        output = out.stdout.decode("utf-8")
        self.data = json.loads(output)

    def set_pos(self, start: str, end: str):
        self.pos = (start, end)
