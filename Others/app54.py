def print_formatted(N):
    CNT = 1
    while CNT <= N:
        print(str(CNT).rjust(len(bin(N))-2), end=" ")
        print(oct(CNT)[2:].rjust(len(bin(N))-2), end=" ")
        print(hex(CNT)[2:].upper().rjust(len(bin(N))-2), end=" ")
        print(bin(CNT)[2:].rjust(len(bin(N))-2), end="\n")
        CNT += 1


if __name__ == '__main__':
    n = int(input())
    print_formatted(n)
