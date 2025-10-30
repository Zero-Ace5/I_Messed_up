from itertools import combinations
S = 'a a c d'
S = S.split()
print(S)
# cnt = 0
# for tup in combinations(S, r=2):
#     if any(elem == 'a' for elem in tup):
#         cnt += 1

cnt = sum(1 for tup in combinations(S, r=2) if 'a' in tup)
comb = list(combinations(S, 2))
print(cnt)
res = cnt/len(comb)
print(f"{res:.4f}")
print(round(res, 3))
print("{:.3f}".format(res))
