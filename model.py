class Vector3:
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Vector3({self.x}, {self.y}, {self.z})"


class Model:
    def __init__(self, filename):
        self.vertices: list[Vector3] = []
        self._faces: list[int] = []

        with open(filename) as f:
            for line in f:
                if line == "\n":
                    continue

                tokens = line.split()

                if tokens[0] == "v":
                    x = float(tokens[1])
                    y = float(tokens[2])
                    z = float(tokens[3])
                    self.vertices.append(Vector3(x, y, z))

                if tokens[0] == "f":
                    v0 = int(tokens[1].split("/")[0]) - 1
                    v1 = int(tokens[2].split("/")[0]) - 1
                    v2 = int(tokens[3].split("/")[0]) - 1
                    self._faces.extend([v0, v1, v2])

    @property
    def ntriangles(self):
        return len(self._faces) // 3

    def triangle(self, index) -> tuple[Vector3]:
        offset = index * 3
        return tuple(self.vertices[self._faces[offset + i]] for i in range(3))
