#!/bin/python3

n = int(input())

# VAL = int(input("Enter a number b/w 1 & 100:"))

if 1 <= n <= 100:
    if n % 2 == 0:
        if 2 <= n <= 5:
            print("Not Weird")
        elif 6 <= n <= 20:
            print("Weird")
        elif n > 20:
            print("Not Weird")
        else:
            print("Error")
    else:
        print("Weird")
else:
    print("Invalid Input")
