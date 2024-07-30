import subprocess
import json


class FFprobe:
    def get_audio_info(audio_path: str):
        out = subprocess.run(
            [
                "ffprobe",
                "-v",
                "quiet",
                "-print_format",
                "json",
                # "-sexagesimal",
                "-show_format",
                "-show_streams",
                audio_path,
            ],
            stdout=subprocess.PIPE,
        )
        if out.returncode != 0:
            raise Exception("ERROR: Invalid audio!")

        output = out.stdout.decode("utf-8")
        result = json.loads(output)
        return result
