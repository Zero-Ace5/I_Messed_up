HIGH_INCOME = True
GOOD_CREDIT = False
STUDENT = False

# if HIGH_INCOME or GOOD_CREDIT:
# if not STUDENT:
# 1
# if (HIGH_INCOME or GOOD_CREDIT) and not STUDENT:
#     print("Eligible")
# else:
#     print("Not Eligible")

if HIGH_INCOME or GOOD_CREDIT or not STUDENT:
    print("A")
