from collections import namedtuple

if __name__ == "__main__":
    POINT = namedtuple('POINT', 'x,y')
    pt1 = POINT(1, 2)
    pt2 = POINT(3, 4)
    dot_product = (pt1.x * pt2.x) + (pt1.y * pt2.y)
    print(dot_product)
    print(pt1, pt2)

    CAR = namedtuple('CAR', 'Price Mileage Color Class')
    C1 = CAR(Price=10, Mileage=100, Class="S", Color='Red')
    print(C1)
    print(C1.Class)
