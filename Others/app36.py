if __name__ == '__main__':
    n = int(input())
    arr = list(map(int, input().split()))
    if 2 <= n <= 10 and all(-100 <= x <= 100 for x in arr):
        SORTED = sorted(set(arr), reverse=True)
        if len(SORTED) >= 2:
            print(SORTED[1])
            print(*arr)
            print(*SORTED)
