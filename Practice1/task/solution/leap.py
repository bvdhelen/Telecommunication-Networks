#!/usr/bin/env python

def is_leapyear(year):
  if year % 4 == 0:
    if year % 100 == 0:
      if year % 400 ==0:
        return True
      else:
        return False
    else:
      return True
  else:
    return False

with open('years.txt') as f:
  for year in f:
    year = year.strip()
    print(year, ':', is_leapyear(int(year)))
