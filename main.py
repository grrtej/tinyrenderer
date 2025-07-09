from image import Image
from model import Model, Vector3
from color import COLORS


def line(image, x0, y0, x1, y1, color):
    """
    https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
    https://ics.uci.edu/~gopi/CS112/web/handouts/OldFiles/Bresenham.pdf

    Bresenham's algorithm is a line drawing technique based on the implicit
    equation of a line. Its main advantage is that it only uses integer math.

    Implicit equation of a line:
    F(x, y) = ∆y*x - ∆x*y + ∆x*y0 - ∆y*x0

    If F(x, y) = 0, (x, y) is on the line defined by (x0, y0), (x1, y1).
    If < 0, it is on one side of the line.
    If > 0, it is on the other side of the line.

    For horizontal lines and +y axis up:
    x++ always
    y++ when F(x + 1, y + 0.5) >= 0
        Explanation:
            If line at x + 1 passes over the midpoint of y and y + 1 (y + 0.5),
            then move y up. In other words, midpoint is below line which is
            what the equation is checking.

    For vertical lines (slope > 1), decisions are made for x++ (whether to go
    right or stay).

    Bresenham's algorithm accumulates F (or "error") instead of calculating it
    from scratch for each x, y. Refer to the articles linked above to see how
    it does this.
    """

    def horizontal(x0, y0, x1, y1):
        dx = x1 - x0
        dy = y1 - y0
        dir = -1 if dy < 0 else 1
        dy *= dir
        e = 2 * dy - dx
        y = y0
        for x in range(x0, x1 + 1):
            image.set(x, y, color)
            if e >= 0:
                y += dir
                e -= 2 * dx
            e += 2 * dy

    def vertical(x0, y0, x1, y1):
        dx = x1 - x0
        dy = y1 - y0
        dir = -1 if dx < 0 else 1
        dx *= dir
        e = 2 * dx - dy
        x = x0
        for y in range(y0, y1 + 1):
            image.set(x, y, color)
            if e >= 0:
                x += dir
                e -= 2 * dy
            e += 2 * dx

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
