N = '1222311'

count = 1
for i in range(1, len(N)):
    if N[i] == N[i-1]:
        count += 1
    else:
        print((count, int(N[i-1])), end=" ")
        count = 1

# Don't forget the last group
print((count, int(N[-1])), end=" ")
