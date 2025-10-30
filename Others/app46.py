N = int(input())
LST = []
for _ in range(N):
    LST.append(input())
t = tuple(LST)
print(hash(t))
