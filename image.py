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
        (h, w, _) = self.img.shape
        return (w, h)

    def create_temp_image(self) -> str:
        file_name = "temp" + os.path.splitext(self.path)[1]
        if not cv.imwrite(file_name, self.img):
            raise Exception("ERROR: Can not create temp image")
        return file_name

    def add_logo(
        self,
        logo_path: str,
        width: int = -1,
        height: int = -1,
        offset: tuple[int, int] = (0, 0),
        min_image_size: int = 150,
        padding: tuple[int, int] = (50, 50),
        padding_size: bool = True,
    ):
        (w, _) = self.get_size()
        if w <= min_image_size:
            print("INFO: Can not add logo for small images > 150px")
            return
        logo_image = cv.imread(logo_path, cv.IMREAD_UNCHANGED)
        if logo_image is None:
            return
        logo_width = max(int(self.img.shape[1] * 0.2), 150) if width == -1 else width
        logo_height = (
            int(logo_image.shape[0] * (logo_width / logo_image.shape[1]))
            if height == -1
            else height
        )
        logo_image = cv.resize(
            logo_image, (logo_width, logo_height), interpolation=cv.INTER_AREA
        )
        offsetColumn = (
            offset[0] - (logo_width + padding[0]) if padding_size else offset[0]
        )
        offsetRow = (
            offset[1] - (logo_height + padding[1]) if padding_size else offset[0]
        )
        for i, row in enumerate(logo_image):
            for ii, column in enumerate(row):
                if column[3] != 0:
                    posX = offsetColumn + ii
                    posY = offsetRow + i
                    self.img[posY, posX] = column[0:3]
