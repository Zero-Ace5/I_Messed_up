from itertools import product

print(list(product([1, 2, 3], repeat=2)))

A = [1, 2]
B = [3, 4]
print(*product(A, B))
