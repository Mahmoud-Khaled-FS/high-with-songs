import os

from image import ImageFile
from audio import AudioFile
from ffmpeg.ffmpeg import FFmpeg


class VideoMaker:
    image: ImageFile
    audio: AudioFile

    ffmpeg_command: str = "ffmpeg"

    def __init__(self, image: ImageFile, audio: AudioFile) -> None:
        self.image = image
        self.audio = audio

    def build(self):
        temp_image = self.image.create_temp_image()
        ffmpeg = FFmpeg()
        ffmpeg.add_global_option("-y")
        audio_input = ffmpeg.add_input(self.audio.path)
        ffmpeg.add_option(audio_input, "-ss", "00:10")
        ffmpeg.add_option(audio_input, "-to", "00:30")
        image_input = ffmpeg.add_input(temp_image)
        ffmpeg.add_option(image_input, "-to", "00:30")
        ffmpeg.add_option(image_input, "-loop", "1")
        # width, height = self.image.get_size()
        ffmpeg.add_output(
            "res/out.mp4",
            *FFmpeg.common_output_options,
            # "-vf",
            # f"scale='{width}:{height}',format=yuv420p",
        )
        ffmpeg.run()
        # os.remove(path=temp_image)

    def build_ffmpeg(self):
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
        command = (
            init_command
            + self.image_args_ffmpeg(temp_image_path)
            + self.audio_args_ffmpeg()
            + out_command
        )
        print(" ".join(command))
        temp_image_path = self.image.create_temp_image()

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
