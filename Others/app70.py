from collections import defaultdict

if __name__ == "__main__":
    n, m = map(int, input().split())
    print(n, m)
    d = defaultdict(list)

    for i in range(1, n+1):
        word = input().strip()
        d[word].append(i)

    for i in range(m):
        word = input().strip()
        if word in d:
            print(*d[word])
        else:
            print(-1)

    for i in d.items():
        print(i)
