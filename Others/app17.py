SUCCESSFUL = True
for NUMBER in range(3):
    print("Attempt")
    if SUCCESSFUL:
        print("Successful")
        break
else:
    print(f"Failed after {NUMBER + 1} times.")
