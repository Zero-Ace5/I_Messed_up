def multiply(*numbers):
    print(numbers)
    total = 1
    for number in numbers:
        print(number)
        total *= number
    return total


print(multiply(2, 3, 4, 5))
