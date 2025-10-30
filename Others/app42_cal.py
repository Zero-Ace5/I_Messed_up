import calendar

# print(calendar.TextCalendar(firstweekday=6).formatyear(2015))
# print(calendar.isleap(2024))
# print(calendar.leapdays(2000, 2025))
MONTH, DAY, YEAR = map(int, input().split())
DAY = calendar.weekday(YEAR, MONTH, DAY)
print(calendar.day_name[DAY].upper())
