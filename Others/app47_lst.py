if __name__ == '__main__':
    LST = []
    for _ in range(int(input())):
        name = input()
        score = float(input())
        LST.append([name, score])
    LST.sort()
    # print(LST)
    SECOND = sorted({s for _, s in LST})[1]
    for name, score in LST:
        if SECOND == score:
            print(name)

# 5
# Harry
# 37.21
# Berry
# 37.21
# Tina
# 37.2
# Akriti
# 41
# Harsh
# 39
