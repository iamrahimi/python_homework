import math


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Equality check
    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    # String representation
    def __str__(self):
        return f"Point({self.x}, {self.y})"

    # Euclidean distance
    def distance_to(self, other):
        if isinstance(other, Point):
            return math.sqrt((self.x - other.x) ** 2 + (self.y - other.y) ** 2)
        raise TypeError("distance_to() requires a Point or Vector instance")


class Vector(Point):
    # Override string representation
    def __str__(self):
        return f"Vector<{self.x}, {self.y}>"

    # Vector addition
    def __add__(self, other):
        if isinstance(other, Vector):
            return Vector(self.x + other.x, self.y + other.y)
        raise TypeError("Can only add Vector to Vector")


if __name__ == "__main__":
    # Demonstrate Point
    p1 = Point(3, 4)
    p2 = Point(6, 8)
    print("p1:", p1)
    print("p2:", p2)
    print("p1 == p2?", p1 == p2)
    print("Distance between p1 and p2:", p1.distance_to(p2))

    # Demonstrate Vector
    v1 = Vector(1, 2)
    v2 = Vector(3, 4)
    print("v1:", v1)
    print("v2:", v2)
    v3 = v1 + v2
    print("v1 + v2 =", v3)
    print("Distance between v1 and v3:", v1.distance_to(v3))