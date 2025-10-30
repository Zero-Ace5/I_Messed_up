if __name__ == '__main__':
    N = int(input())
    LIST = []
    for _ in range(N):
        ACTION = input().split()
        METHOD = ACTION[0]
        if METHOD == "insert":
            i = int(ACTION[1])
            e = int(ACTION[2])
            LIST.insert(i, e)
        elif METHOD == "remove":
            e = int(ACTION[1])
            LIST.remove(e)
        elif METHOD == "append":
            e = int(ACTION[1])
            LIST.append(e)
        elif METHOD == "sort":
            LIST.sort()
        elif METHOD == "pop":
            LIST.pop()
        elif METHOD == "reverse":
            LIST.reverse()
        elif METHOD == "print":
            print(LIST)
