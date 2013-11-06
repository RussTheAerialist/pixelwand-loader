from PIL import Image

class Loader(object):
    def __init__(self, filename):
        self.image = Image.open(filename)
        self.resized = None

    def _calculate_width(self, pixels):
        width, height = self.image.size
        new_height = pixels
        new_width = width * new_height / height

        return new_width

    def get_image_pixels(self, width):
        pass

    def send_to(self, wand):
        wand.start_upload()
        pixels = wand.number_pixels()

	width = self._calculate_width(pixels)
        wand.set_width(width)

        bytes = self.get_image_pixels(width)
        wand.send_bytes(bytes)
