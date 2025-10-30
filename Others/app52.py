def print_rangoli(size):
    n = size
    letter = 96 + n
    max_len = 4*n-3
    strings = []

    for i in range(n):
        s = []
        for j in range(letter, letter-i-1, -1):
            s.append(chr(j))
        for k in range(letter-i+1, letter+1):
            s.append(chr(k))
        print(s)
        strings.append("-".join(s))
    print(strings)
    for string in strings:
        print(string.center(max_len, '-'))
    strings.reverse()
    for string in strings[1:]:
        print(string.center(max_len, '-'))


if __name__ == '__main__':
    num = int(input())
    print_rangoli(num)
