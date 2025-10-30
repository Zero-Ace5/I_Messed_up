import re

n = int(input())

for _ in range(n):
    regex = input().strip()
    try:
        if re.search(r'(\*|\+|\?){2,}', regex):
            print("False")
        else:
            re.compile(regex)
            print("True")
    except re.error:
        print("False")
