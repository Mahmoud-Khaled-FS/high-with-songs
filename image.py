import os
import cv2 as cv
import numpy as np
import numpy.typing as npt

# TODO: Read image and get width and height


class ImageFile:
    path: str
    img: cv.typing.MatLike

    def __init__(self, image_path: str) -> None:
        if not os.path.isfile(image_path):
            raise Exception("ERROR: Image not found!")
        self.path = image_path
        self.img = cv.imread(image_path)
        if self.img is None:
            raise Exception("ERROR: Invalid image!")

    def set_size(self, width: int, height: int, respect_ratio: bool = False):
        self.img = cv.resize(self.img, (width, height), interpolation=cv.INTER_CUBIC)

    def get_jpg_bytes(self) -> bytes:
        return cv.imencode(".jpg", self.img)[1].tobytes()

    def get_size(self) -> tuple[int, int]:
        size = self.img.shape
        return (size[0], size[1])

    def create_temp_image(self) -> str:
        file_name = "temp" + os.path.splitext(self.path)[1]
        if not cv.imwrite(file_name, self.img):
            raise Exception("ERROR: Can not create temp image")
        return file_name
