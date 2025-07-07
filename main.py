from image import Image
from model import Model
from color import WHITE


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


def main():
    image = Image(1000, 1000)
    model = Model("head.obj")
    for tri in range(model.ntriangles):
        for i in range(3):
            va = model.triangle(tri)[i]
            vb = model.triangle(tri)[(i + 1) % 3]

            # convert vertex coordinates to image coordinates
            x0 = round((va.x + 1) * (image.width - 1) / 2)
            y0 = round((va.y + 1) * (image.height - 1) / 2)
            x1 = round((vb.x + 1) * (image.width - 1) / 2)
            y1 = round((vb.y + 1) * (image.height - 1) / 2)

            # connect the dots
            line(image, x0, y0, x1, y1, WHITE)

    with open("out.tga", "wb") as f:
        f.write(image.to_bytes())
    print("image rendered to out.tga")


if __name__ == "__main__":
    main()
