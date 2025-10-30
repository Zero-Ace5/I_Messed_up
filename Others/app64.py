from itertools import permutations
A, B = input().split()
A = sorted(A)
B = int(B)
print(A)
perms = permutations(A, B)

for p, q in perms:
    print(f"{p}{q}")
