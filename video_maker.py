import subprocess
import numpy as np
import os

from image import ImageFile
from audio import AudioFile


class VideoMaker:
    image: ImageFile
    audio: AudioFile

    ffmpeg_command: str = "ffmpeg"

    def __init__(self, image: ImageFile, audio: AudioFile) -> None:
        self.image = image
        self.audio = audio

    def build(self):
        init_command = [self.ffmpeg_command, "-y"]

        width, height = self.image.get_size()
        out_command = [
            "-c:v",
            "libx264",
            "-c:a",
            "aac",
            "-shortest",
            "-vf",
            f"scale='{width}:{height}',format=yuv420p",
            "-movflags",
            "+faststart",
            "out.mp4",
        ]
        temp_image_path = self.image.create_temp_image()
        command = (
            init_command
            + self.image_args_ffmpeg(temp_image_path)
            + self.audio_args_ffmpeg()
            + out_command
        )
        print(" ".join(command))
        proc = subprocess.Popen(command, stderr=subprocess.PIPE)
        proc.communicate()
        os.remove(path=temp_image_path)

    def image_args_ffmpeg(self, image_path: str) -> list[str]:
        return [
            "-loop",
            "1",
            "-r",
            "24",
            "-i",
            image_path,
        ]

    def audio_args_ffmpeg(self) -> list[str]:
        audio_prams = ["-i", self.audio.path]
        if self.audio.pos is not None:
            audio_prams = [
                "-ss",
                self.audio.pos[0],
                "-to",
                self.audio.pos[1],
            ] + audio_prams
        return audio_prams
