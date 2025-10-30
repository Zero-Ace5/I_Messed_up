from itertools import product

A = [24, 48, 96]
B = [24, 48, 96, 24]

PRODUCT = 0
for X in product(A, B):
    TOTAL = sum(x**2 for x in X) % int(24)
    PRODUCT = max(TOTAL, PRODUCT)
    print(TOTAL, PRODUCT)
print(PRODUCT)
