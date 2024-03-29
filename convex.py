from deq import Deq
from r2point import R2Point


class Figure:
    """ Абстрактная фигура """

    def perimeter(self):
        return 0.0

    def area(self):
        return 0.0

    def min_dlin(self):
        return 0.0


class Void(Figure):
    """ "Hульугольник" """

    def add(self, p):
        return Point(p)


class Point(Figure):
    """ "Одноугольник" """

    def __init__(self, p):
        self.p = p

    def add(self, q):
        return self if self.p == q else Segment(self.p, q)


class Segment(Figure):
    """ "Двуугольник" """

    def __init__(self, p, q):
        self.p, self.q = p, q

    def perimeter(self):
        return 2.0 * self.p.dist(self.q)

    def min_dlin(self):
        return self.p.dist(self.q)

    def add(self, r):
        if R2Point.is_triangle(self.p, self.q, r):
            return Polygon(self.p, self.q, r)
        elif self.q.is_inside(self.p, r):
            return Segment(self.p, r)
        elif self.p.is_inside(r, self.q):
            return Segment(r, self.q)
        else:
            return self


class Polygon(Figure):
    """ Многоугольник """

    def __init__(self, a, b, c):
        self.points = Deq()
        self.points.push_first(b)
        self.dlina = []
        if b.is_light(a, c):
            self.points.push_first(a)
            self.points.push_last(c)
        else:
            self.points.push_last(a)
            self.points.push_first(c)
        self._perimeter = a.dist(b) + b.dist(c) + c.dist(a)
        self._area = abs(R2Point.area(a, b, c))
        if a.dist(b) >= b.dist(c) >= c.dist(a):
            self.dlina.append(c.dist(a))
            self.dlina.append(b.dist(c))
            self.dlina.append(a.dist(b))
        elif c.dist(a) >= b.dist(c) >= a.dist(b):
            self.dlina.append(a.dist(b))
            self.dlina.append(b.dist(c))
            self.dlina.append(c.dist(a))
        elif b.dist(c) >= c.dist(a) >= a.dist(b):
            self.dlina.append(a.dist(b))
            self.dlina.append(c.dist(a))
            self.dlina.append(b.dist(c))
        elif a.dist(b) >= c.dist(a) >= b.dist(c):
            self.dlina.append(b.dist(c))
            self.dlina.append(c.dist(a))
            self.dlina.append(a.dist(b))
        elif c.dist(a) >= a.dist(b) >= b.dist(c):
            self.dlina.append(b.dist(c))
            self.dlina.append(a.dist(b))
            self.dlina.append(c.dist(a))
        else:
            self.dlina.append(c.dist(a))
            self.dlina.append(a.dist(b))
            self.dlina.append(b.dist(c))

    def perimeter(self):
        return self._perimeter

    def area(self):
        return self._area

    def min_dlin(self):
        return self.dlina[0]

    # добавление новой точки
    def add(self, t):

        # поиск освещённого ребра
        for n in range(self.points.size()):
            if t.is_light(self.points.last(), self.points.first()):
                break
            self.points.push_last(self.points.pop_first())

        # хотя бы одно освещённое ребро есть
        if t.is_light(self.points.last(), self.points.first()):

            # учёт удаления ребра, соединяющего конец и начало дека
            self._perimeter -= self.points.first().dist(self.points.last())
            self._area += abs(R2Point.area(t,
                                           self.points.last(),
                                           self.points.first()))
            self.dlina.remove(self.points.first().dist(self.points.last()))

            # удаление освещённых рёбер из начала дека
            p = self.points.pop_first()
            while t.is_light(p, self.points.first()):
                self._perimeter -= p.dist(self.points.first())
                self._area += abs(R2Point.area(t, p, self.points.first()))
                self.dlina.remove(p.dist(self.points.first()))
                p = self.points.pop_first()
            self.points.push_first(p)

            # удаление освещённых рёбер из конца дека
            p = self.points.pop_last()
            while t.is_light(self.points.last(), p):
                self._perimeter -= p.dist(self.points.last())
                self._area += abs(R2Point.area(t, p, self.points.last()))
                self.dlina.remove(p.dist(self.points.last()))
                p = self.points.pop_last()
            self.points.push_last(p)

            # добавление двух новых рёбер
            self._perimeter += t.dist(self.points.first()) + \
                t.dist(self.points.last())
            low = 0
            high = len(self.dlina) - 1
            while (low < high):
                mid = (low + high) // 2
                if t.dist(self.points.last()) >= self.dlina[mid]:
                    low = mid + 1
                else:
                    high = mid - 1
            if t.dist(self.points.last()) <= self.dlina[low]:
                self.dlina.insert(low, t.dist(self.points.last()))
            else:
                self.dlina.insert(low + 1, t.dist(self.points.last()))
            low = 0
            high = len(self.dlina) - 1
            while (low < high):
                mid = (low + high) // 2
                if t.dist(self.points.first()) >= self.dlina[mid]:
                    low = mid + 1
                else:
                    high = mid - 1
            if t.dist(self.points.first()) <= self.dlina[low]:
                self.dlina.insert(low, t.dist(self.points.first()))
            else:
                self.dlina.insert(low + 1, t.dist(self.points.first()))

            self.points.push_first(t)

        return self


if __name__ == "__main__":
    f = Void()
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(1.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 1.0))
    print(type(f), f.__dict__)
