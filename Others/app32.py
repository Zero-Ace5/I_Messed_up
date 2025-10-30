if __name__ == '__main__':
    n = int(input())
    if n > 0:
        num = 0
        while n > num:
            print(num*num)
            num += 1
    elif n < 0:
        print("Negative")
    else:
        print(0)
