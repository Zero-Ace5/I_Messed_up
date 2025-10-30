def countResponseTimeRegressions(responseTimes):
    total = 0
    result = 0
    for i, rt in enumerate(responseTimes):
        total += rt
        avg = total//(i+1)
        if rt > avg:
            result += 1
    return result


if __name__ == '__main__':

    responseTimes = [100, 200, 150, 300]

    result = countResponseTimeRegressions(responseTimes)

    print(result)
