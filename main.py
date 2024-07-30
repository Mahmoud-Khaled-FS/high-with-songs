import sys

from video_maker import VideoMaker
from image import ImageFile
from audio import AudioFile


def main(argv):
    image = ImageFile("res/spider man.jpg")
    audio = AudioFile("res/audio.mp3")
    # audio.set_pos("00:01:57", "00:02:39")
    video_maker = VideoMaker(image=image, audio=audio)

    video_maker.build()


if __name__ == "__main__":
    main(sys.argv[1:])
