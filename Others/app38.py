import cmath

z = complex(input().strip())
print(z)

r = abs(z)
theta = cmath.phase(z)
print(f"{r}, {theta}")

print(r)
print(theta)
