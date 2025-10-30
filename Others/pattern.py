def pattern(n):
    for i in range(1, n+1):
        print(" "*(n-i) + "#" * i + "#" * (i-1))
    for i in range(n-1, 0, -1):
        print(" "*(n-i) + "#" * i + "#" * (i-1))


if __name__ == "__main__":
    n = 5
    pattern(n)
