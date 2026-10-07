import math

# Indexing: xyzw, 1234, rThetaPhi, ijk
indexing_to_str = {
    "xyzw": "xyzwvutsrqponmlkjihgfedcba",
    "rThetaPhi": "rθϕ",
    "ijk": "ijk"
}

class PointND:

    # === CONSTRUCTORS === #
    def __init__(self, *coords, indexing = "1234"):
        self._coords = list(coords)
        self._dims = len(coords)

        self._validIndexing(indexing)

    @classmethod
    def origin(cls):
        raise NotImplementedError("Нет фиксированной размерности")

    @classmethod
    def clone(cls, point):
        return cls(*point._coords)

    # === PRIVATE ===
    def _validIndexing(self, indexing):

        self._indexing_chars = None
        if indexing == "1234":
            self._indexing = "1234"
            return

        indexing_chars = indexing_to_str[indexing]
        self._indexing = indexing
        if len(indexing_chars) < self._dims:
            print(
                f"Не получится проименовать все значения способом [ {indexing}... ] "
                f"для размерности dims={self._dims}! Используем способ [ 1234... ] по умолчанию."
            )
            self._indexing = "1234"
        else:
            self._indexing_chars = indexing_chars

    def _genCoordsInfoForRepr(self):

        if self._indexing == "1234":
            return ", ".join(f"x{i+1}={c:.2f}" for i, c in enumerate(self._coords))
        
        return ", ".join(f"{self._indexing_chars[i]}={c:.2f}" for i, c in enumerate(self._coords))

    # === MAGIC METHODS === #
    def __getitem__(self, index):

        if isinstance(index, int):
            return self._coords[index]
        
        if isinstance(index, str):
            try:
                idx = self._indexing_chars.index(index)
                return self._coords[idx]
            except ValueError:
                raise IndexError(f"Не найден символ \"{index}\" в обозначениях [ {self._indexing}... ]")
            except IndexError:
                raise IndexError(
                    f"Выход за пределы данного измерения (dims={self._dims})! "
                    f"Здесь нет обозначения \"{index}\""
                )

    def __str__(self):
        coords_str = ", ".join(f"{c:.2f}" for c in self._coords)
        return f"({coords_str})"

    def __repr__(self):
        coords_str = self._genCoordsInfoForRepr()
        return f"Point{self.dims}D({coords_str})"

    # === PROPERTIES === #
    @property
    def dims(self):
        return self._dims

    # === USING === #
    def distanceTo(self, other):
        return PointND.distanceBetween(self._coords, other._coords)
    
    @staticmethod
    def distanceBetween(p1, p2):
    
        if len(p1) != len(p2):
            raise ValueError(f"Разная размерность: p1.dims={len(p1)}, p2.dims={len(p2)}")
        
        sqrts_sum = sum((p2[i] - p1[i])**2 for i in range(len(p1)))
        return math.sqrt(sqrts_sum)


class Point2D(PointND):

    count = 0

    # === CONSTRUCTORS === #
    def __init__(self, x, y):
        super().__init__(x, y, indexing = "xyzw")

        Point2D.count += 1

    def __del__(self):
        Point2D.count -= 1

    @classmethod
    def fromPolar(cls, r, angle_degrees):
        
        theta = math.radians(angle_degrees)
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        return cls(x, y)

    @classmethod
    def origin(cls):
        return cls(0.0, 0.0)

    # === PROPERTIES === #
    @property
    def x(self):
        return self._coords[0]
    
    @x.setter
    def x(self, value):
        if not isinstance(value, int|float):
            raise ValueError("Неверный тип")
        self._coords[0] = value

    @property
    def y(self):
        return self._coords[1]

    @y.setter
    def y(self, value):
        if not isinstance(value, int|float):
            raise ValueError("Неверный тип")
        self._coords[1] = value


# === TEST === #
def pointsCountPrint():
    print(
        ("-" * 10) + "\n"
        f"Текущее количество: {Point2D.count}" +
        "\n" + ("-" * 10)
    )

if __name__ == "__main__":

    points = [Point2D(1 / i, 1 / i) for i in range(1, 11)]
    for i in range(len(points)):
        print(f"Point {i + 1} -> str: {points[i]}, repr: {repr(points[i])}")
    pointsCountPrint()

    origin = Point2D.origin()
    print(f"Origin -> str: {origin}, repr: {repr(origin)}")

    print("\nУдаление списка points...")
    del points
    pointsCountPrint()

    clone = Point2D.clone(origin)
    print("Изменение координат у clone...")
    clone.x = 10
    clone.y = 20
    print(
        f"Original -> str: {origin}, repr: {repr(origin)}\n"
        f"Clone -> str: {clone}, repr: {repr(clone)}"
    )
    pointsCountPrint()