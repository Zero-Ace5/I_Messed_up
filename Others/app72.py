from collections import namedtuple
N, Record = int(input()), namedtuple('Record', input().split())
print(f"{(sum(int(Record._make(input().split()).MARKS) for _ in range(N)))/N:.2f}")
