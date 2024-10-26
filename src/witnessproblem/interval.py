

class Interval:

    def __init__(self, ini: int, fin: int):
        self.a = ini
        self.b = fin

    def __lt__(self, other):
        return self.a < other.a

    def are_intervals_disjoint(I1, I2):
        return I1.b < I2.a or I2.b < I1.a