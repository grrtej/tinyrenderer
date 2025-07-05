from color import Color


class Image:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self._data = [Color()] * (width * height)

    def get(self, x, y) -> Color:
        return self._data[y * self.width + x]

    def set(self, x, y, color: Color):
        self._data[y * self.width + x] = color

    def to_bytes(self, vflip=False) -> bytes:
        header = bytearray(18)
        header[2] = 2
        header[12] = self.width & 0xFF
        header[13] = (self.width >> 8) & 0xFF
        header[14] = self.height & 0xFF
        header[15] = (self.height >> 8) & 0xFF
        header[16] = 32
        header[17] = 0x28 if vflip else 0x08

        data = bytearray()
        for y in range(self.height):
            for x in range(self.width):
                data.extend(self.get(x, y).bgra)

        return bytes(header + data)
