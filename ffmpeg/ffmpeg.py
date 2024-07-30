import subprocess


class FFmpeg:
    common_output_options = [
        "-c:v",
        "libx264",
        "-c:a",
        "aac",
        "-shortest",
        "-movflags",
        "+faststart",
    ]

    def __init__(self):
        self.ffmpeg_command = "ffmpeg"
        self.common_options = []
        self.inputs = []
        self.output = []

    def add_global_option(self, option: str):
        self.common_options.append(option)
        return self

    def add_input(self, input: str) -> int:
        index = len(self.inputs)
        self.inputs.append(["-i", input])
        return index

    def add_option(self, input_index: int, *option: list[str]):
        self.inputs[input_index] = list(option) + self.inputs[input_index]
        return self

    def add_output(self, output: str, *options: list[str]):
        options = list(options)
        options.append(output)
        self.output = options
        return self

    def run(self):
        command = [self.ffmpeg_command] + self.common_options
        for input in self.inputs:
            command += input
        command += self.output
        # print(command)
        proc = subprocess.Popen(command, stderr=subprocess.PIPE)
        print(proc.args)
        proc.communicate()
