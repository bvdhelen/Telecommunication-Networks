def is_leap_year(year):
    if year % 4 != 0:
        return False
    if year % 100 == 0:
        if year % 400 == 0:
            return True
        return False
    return True

with open("years.txt", "r") as file:
    for line in file:
        line = line.strip()
        if line == "":
            continue
        year = int(line)
        result = is_leap_year(year)
        print(f"{year}: {result}")