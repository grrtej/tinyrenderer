from image import Image
from model import Model, Vector3
from color import COLORS


def line(image, x0, y0, x1, y1, color):
    """
    https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
    """

    def horizontal(x0, y0, x1, y1):
        dx = x1 - x0
        dy = y1 - y0
        dir = -1 if dy < 0 else 1
        dy *= dir
        p = 2 * dy - dx
        y = y0
        for x in range(x0, x1 + 1):
            image.set(x, y, color)
            if p >= 0:
                y += dir
                p -= 2 * dx
            p += 2 * dy

    def vertical(x0, y0, x1, y1):
        dx = x1 - x0
        dy = y1 - y0
        dir = -1 if dx < 0 else 1
        dx *= dir
        p = 2 * dx - dy
        x = x0
        for y in range(y0, y1 + 1):
            image.set(x, y, color)
            if p >= 0:
                x += dir
                p -= 2 * dy
            p += 2 * dx

    if abs(y1 - y0) < abs(x1 - x0):
        if x0 < x1:
            horizontal(x0, y0, x1, y1)
        else:
            horizontal(x1, y1, x0, y0)
    else:
        if y0 < y1:
            vertical(x0, y0, x1, y1)
        else:
            vertical(x1, y1, x0, y0)


def triangle(image, a, b, c, color):
    line(image, a.x, a.y, b.x, b.y, color)
    line(image, b.x, b.y, c.x, c.y, color)
    line(image, c.x, c.y, a.x, a.y, color)


def to_screen_space(vectors, screen_width, screen_height):
    def convert(v):
        return Vector3(
            x=round((v.x + 1) * (screen_width - 1) / 2),
            y=round((v.y + 1) * (screen_height - 1) / 2),
            z=v.z,
        )

    if isinstance(vectors, Vector3):
        return convert(vectors)

    return type(vectors)(convert(v) for v in vectors)


def main():
    image = Image(1000, 1000)
    model = Model("head.obj")
    for i in range(model.ntriangles):
        a, b, c = to_screen_space(model.triangle(i), image.width, image.height)
        triangle(image, a, b, c, COLORS["white"])

    with open("out.tga", "wb") as f:
        f.write(image.to_bytes())
    print("image rendered to out.tga")


if __name__ == "__main__":
    main()
