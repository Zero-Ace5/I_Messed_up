STRING = "1 2 2 3 4 5 6 7 8  9"
STRING_2 = STRING.split(" ")
print(STRING_2)
LENGTH = len(STRING_2)
LOOP = 0
NEO = ""
while LOOP < LENGTH:
    if STRING_2[LOOP].isalpha():
        NEO += STRING_2[LOOP].title()
    else:
        NEO += STRING_2[LOOP]

    if LOOP < LENGTH-1:
        NEO += " "

    LOOP += 1

print(NEO)
