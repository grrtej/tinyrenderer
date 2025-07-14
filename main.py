from image import Image
from model import Model, Vector3
from color import Color


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
    """
    for each y, connect left and right sides of triangle using a line.
    handling flat top and flat bottom triangles separately makes this easier.
    """

    def top(a, b, c):
        b, c = sorted((b, c), key=lambda v: v.x)
        xl = a.x
        xr = a.x
        xl_delta = (b.x - a.x) / (b.y - a.y)
        xr_delta = (c.x - a.x) / (c.y - a.y)
        for y in range(a.y, b.y + 1):
            for x in range(round(xl), round(xr) + 1):
                image.set(x, y, color)
            xl += xl_delta
            xr += xr_delta

    def bottom(a, b, c):
        a, b = sorted((a, b), key=lambda v: v.x)
        xl = c.x
        xr = c.x
        xl_delta = (c.x - a.x) / (c.y - a.y)
        xr_delta = (c.x - b.x) / (c.y - b.y)
        for y in range(c.y, a.y - 1, -1):
            for x in range(round(xl), round(xr) + 1):
                image.set(x, y, color)
            xl -= xl_delta
            xr -= xr_delta

    a, b, c = sorted((a, b, c), key=lambda v: v.y)
    if c.y - a.y == 0:
        return  # collinear points, not a triangle

    if a.y == b.y:
        bottom(a, b, c)
    elif b.y == c.y:
        top(a, b, c)
    else:
        # interpolate point D on longest side AC, to split triangle
        # into flat top and flat bottom triangles
        dx = c.x - a.x
        dy = c.y - a.y
        alpha = (b.y - a.y) / dy
        new_x = a.x + alpha * dx
        d = Vector3(new_x, b.y)
        top(a, b, d)
        bottom(b, d, c)


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
        print(f"tri: {i}/{model.ntriangles}", end="\r")
        a, b, c = to_screen_space(model.triangle(i), image.width, image.height)
        triangle(image, a, b, c, Color.random_color())

    with open("out.tga", "wb") as f:
        f.write(image.to_bytes())
    print("image rendered to out.tga")


if __name__ == "__main__":
    main()
