N, M = map(int, input().split())
for i in range(1, N, 2):
    PATTERN = (".|." * i).center(M, "-")
    print(PATTERN)

print(("WELCOME").center(M, "-"))

for i in range(N-2, 0, -2):
    PATTERN = (".|." * i).center(M, "-")
    print(PATTERN)
