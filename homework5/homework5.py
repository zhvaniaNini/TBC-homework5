import multiprocessing
import random
import time


# ტრაპეციის კლასი
class Trapezoid:
    def __init__(self, top_base, bottom_base, height):
        self.top_base = top_base
        self.bottom_base = bottom_base
        self.height = height

    def area(self):
        return ((self.top_base + self.bottom_base) / 2) * self.height

    def __add__(self, other):
        return self.area() + other.area()

    def __sub__(self, other):
        return abs(self.area() - other.area())

    def __mod__(self, other):
        return self.area() % other.area()


# მართკუთხედის კლასი, რომელიც ტრაპეციის შვილობილია
class Rectangle(Trapezoid):
    def __init__(self, length, width):
        super().__init__(length, length, width)
        self.length = length
        self.width = width

    def __str__(self):
        return "მართკუთხედის სიგრძე {} და მართკუთხედის სიგანე {}".format(self.length, self.width)

    def area(self):
        return self.length * self.width

    def __add__(self, other):
        return self.area() + other.area()

    def __sub__(self, other):
        return abs(self.area() - other.area())

    def __mod__(self, other):
        return self.area() % other.area()


# კვადრატის კლასი, რომელიც მართკუთხედის შვილობილია
class Square(Rectangle):
    def __init__(self, side_length):
        super().__init__(side_length, side_length)


# ტრაპეციის ფართობს გამოსათვლელი ფუნქცია
def trapezoid_area(arr):
    for i in arr:
        T = Trapezoid(i)
        T.area()


# მართკუთხედის ფართობს გამოსათვლელი ფუნქცია
def rectangle_area(arr):
    for i in arr:
        R = Rectangle(i)
        R.area()


# კვადრატის ფართობს გამოსათვლელი ფუნქცია
def square_area(arr):
    for i in arr:
        S = Square(i)
        S.area()


# ფიგურების მიხედვით, შესაბამისი ფიგურის ფართობის გამოთვლა და ლისტში დამატება
def calculate_areas(constructor, args_list):
    areas = []
    for args in args_list:
        shape = constructor(*args)
        areas.append(shape.area())
    return areas


"""
# მაგალითი, სრედების და პროცესების გარეშე ფართობების გამოთვლა
trapezoid_args = [(2, 4, 3), (3, 5, 4), (4, 6, 5)]
rectangle_args = [(2, 4), (3, 5), (4, 6)]
square_args = [(2,), (3,), (4,)]

start = time.perf_counter()
trapezoid_areas = calculate_areas(Trapezoid, trapezoid_args)
rectangle_areas = calculate_areas(Rectangle, rectangle_args)
square_areas = calculate_areas(Square, square_args)
end = time.perf_counter()

print(f"ტრაპეციებისს ფართობები: {trapezoid_areas}")
print(f"მართკუთხედის ფართობები: {rectangle_areas}")
print(f"კვადრატის ფართობები: {square_areas}")
print(end - start)
"""


# სრედების და პროცესების დახმარებით ფართობების გამოთვლა რენდომულად აღებული ზომებით
def process_task(constructor, args_list, areas):
    areas.extend(calculate_areas(constructor, args_list))
    return areas


if __name__ == "__main__":
    start = time.perf_counter()

    trapezoid_args = [(random.randint(1, 10), random.randint(1, 10), random.randint(1, 10)) for _ in range(1000)]
    rectangle_args = [(random.randint(1, 10), random.randint(1, 10)) for _ in range(1000)]
    square_args = [(random.randint(1, 10),) for _ in range(1000)]

    manager = multiprocessing.Manager()
    areas = manager.list()

    processes = []

    for shape_cls, args_list in [(Trapezoid, trapezoid_args), (Rectangle, rectangle_args), (Square, square_args)]:
        process = multiprocessing.Process(target=process_task, args=(shape_cls, args_list, areas))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    areas = list(areas)

    print("ტრაპეციის ფართობები:", areas[:1000])
    print("მართკუთხედის ფართობები:", areas[1000:2000])
    print("კვადრატის ფართობები:", areas[2000:])

    finish = time.perf_counter()
    print('დასრულდა', round(finish - start, 2), 'წამში')
    print(len(areas))
