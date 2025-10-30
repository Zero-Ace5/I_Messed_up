COUNT = 0
for NUMBER in range(1, 10):
    if NUMBER % 2 == 0:
        print(NUMBER)
        COUNT += 1
print(f"We have {COUNT} even numbers")
