a, b, c, d = map(int, [input(), input(), input(), input()])
if all(1 <= x <= 1000 for x in (a, b, c, d)):
    print(a**b+c**d)
