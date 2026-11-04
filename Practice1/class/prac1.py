import sys
import json

mylist = []
i = 0
while i <= 10:
    mylist.append(i**2)
    i += 1
    #i++
    #++i
    #i--
print(mylist)
print("=====")

for i in mylist:
    print(i)

print("=====")
for i in range(5, 3, -1):
    print(i)
mylist = []
for i in range(11):
    mylist.append(i**2)
print(mylist)

mylist = [x**2 for x in range(11) if x % 2 == 0]
print(mylist)

print("=====")
def is_even(num):
    if num % 2 == 0:
        return True
    else:
        return False

for i in range(1, 10):
    if is_even(i):
        print("Num: " + str(i))
        print(f"Num: {i}")

print("=====")
mylist = [1,2,3]
[a,b,c] = mylist
print(a)
print(b)
print(c)
mytuple = (10,20)
a,b = mytuple
print(a)
print(b)

print("=====")
def complex(x):
    return (x**2, x**3, x**4)
print(complex(5))
a, b, c = complex(10)
print(a)
print(b)
print(c)
_, b, _ = complex(122)
print(b)

print("=====")
team = {
    91: "Bob",
    13: "Adam",
    3: "Ryan",
    54: "Ann",
    22: "Ross"
}
print(team)
print(team[3])
print(team[22])
team[22] = "Elena"
print(team[22])
print(team.keys())
print(team.values())
for (key, value) in team.items():
    print(f"{key} -> {value}")
for key in team:
    print(f"{key} -> {team[key]}")

print("=====")
mydict = {x : x**2 for x in range(10)}
print(mydict)
team_inv = {name: num for (num, name) in team.items()}
print(team_inv)
print(team_inv["Bob"])

print("=====")
is_even = lambda num: (num % 2) == 0
print(is_even(4))

is_even2 = lambda num: True if (num % 2) == 0 else False
print([x if is_even(x) else x*2 for x in range(10)])
print(is_even2(4))

print("=====")
def fahrenheit(T):
    return T * 9 / 5 + 32
def celsius(T):
    return (T - 32) * 5 / 9
temperature = (36.5, 37, 37.5, 38, 39)
F = list(map(fahrenheit, temperature))
C = list(map(celsius, F))
print(F)
print(C)

print("=====")
fibonacci = [0,1,1,2,3,5,8,13,21,34,55]
is_odd = lambda x : x % 2 == 1
print(list(filter(is_odd, fibonacci)))
print(list(filter(lambda x : x % 2 == 1, fibonacci)))

print("=====")
f = open("demofile.txt", "r")
#data = f.read()
#data = f.readline()
for x in f:
    print("==", x.strip())
f.close()

with open("demofile.txt", "r") as f:
    for line in f:
        print(line.strip())
with open("demofile2.txt", "w") as f:
    f.write("lorem ipsum")

print("=====")
#x = input("Please enter a number!\n")
#print("Number entered is", x)
#print(int(x)*2)

print(sys.argv)

print("=====")
class Student:
    name = ''
    testpoint = 0
    def __init__(self, _name, _point):
        #this
        self.name = _name
        self.testpoint = _point
    def __str__(self):
        return f"{self.name}: {self.testpoint}"
    def __repr__(self):
        return f"{self.name}({self.testpoint})"

p = Student("Bob", 50)
print(p)
print([p])

print("=====")
data = {
    "president": {
        "name": "Zaphod Beeblerox",
        "species": "Betelgeusian"
    }
}
print(json.dumps(data))
with open("data_file.json", "w") as f:
    #f.write(json.dumps(data))
    json.dump(data, f)