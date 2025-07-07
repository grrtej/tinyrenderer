class Color:
    def __init__(self, r=0.0, g=0.0, b=0.0, a=0.0):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    @classmethod
    def from_hex(cls, hex: int, alpha: int = 0xFF):
        r = ((hex >> 16) & 0xFF) / 255
        g = ((hex >> 8) & 0xFF) / 255
        b = (hex & 0xFF) / 255
        a = alpha / 255
        return cls(r, g, b, a)

    @property
    def bgra(self):
        r = int(self.r * 255)
        g = int(self.g * 255)
        b = int(self.b * 255)
        a = int(self.a * 255)
        return bytes((b, g, r, a))


COLORS = {
    "white": Color.from_hex(0xFFFFFF),
    "red": Color.from_hex(0xFF0000),
    "green": Color.from_hex(0x00FF00),
    "blue": Color.from_hex(0x0000FF),
}
