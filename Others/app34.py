def is_leap(year):
    leap = False

    # Write your logic here
    if 1900 <= year <= 10 ** 5:
        if year % 4 == 0:
            if year % 100 == 0:
                if year % 400 == 0:
                    leap = True
            else:
                leap = True

    return leap
# return (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0))


YEAR = int(input())
print(is_leap(YEAR))
