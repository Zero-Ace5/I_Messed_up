if __name__ == '__main__':
    N = int(input())
    if 1 <= N <= 150:
        NUM = 1
        while NUM <= N:
            print(NUM, end="\n")
            NUM += 1
    else:
        print("Invalid Input")
