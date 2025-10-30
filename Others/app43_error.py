TIMES = int(input())
# while TIMES > 0:
for _ in range(TIMES):
    try:
        TIMES -= 1
        a, b = map(int, input().split())
        RESULT = a//b
        if RESULT.is_integer():
            print(int(RESULT))
        else:
            print(RESULT)
    except ZeroDivisionError as e:
        print(f"Error Code: {e}")
    except ValueError as e:
        print(f"Error Code: {e}")
    else:
        pass
