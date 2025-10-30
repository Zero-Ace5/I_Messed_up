from collections import Counter
Num_Shoes = int(input())
myList = [2, 3, 4, 5, 6, 8, 7, 6, 5, 18]

Shoe = Counter(myList)
print(Shoe)
print(Shoe[6])

# Num_Cx = int(input())
# Money = 0
# for x in range(Num_Cx):
#     A, B = map(int, input().split())
#     if Shoe[A] > 0:
#         Money += B
#         Shoe[A] -=1

# print(Money)
