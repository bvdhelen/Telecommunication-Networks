import sys

def is_leap_year(year):
    if year % 4 != 0:
        return False
    if year % 100 == 0:
        if year % 400 == 0:
            return True
        return False
    return True

if len(sys.argv) < 2:
    raise Exception("Usage: python leap.py [year]")

year = int(sys.argv[1])

if is_leap_year(year):
    print(f"{year} is a leap year")
else:
    print(f"{year} is NOT a leap year")