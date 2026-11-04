import json

with open("points.json", "r") as file:
    data = json.load(file)

homework_max = data["homework"]["max"]
homework_point = data["homework"]["point"]
homework_min_percent = data["homework"]["min_percent"]

socket_max = data["socket"]["max"]
socket_point = data["socket"]["point"]
socket_min_percent = data["socket"]["min_percent"]

kathara_max = data["kathara"]["max"]
kathara_min_percent = data["kathara"]["min_percent"]

homework_percent = homework_point / homework_max
socket_percent = socket_point / socket_max

minimum_points = {}

for point in range(kathara_max + 1):
    kathara_percent = point / kathara_max
    if kathara_percent < kathara_min_percent:
        continue

    final_percent = (homework_percent + socket_percent + kathara_percent) / 3
    #print(point, final_percent)

    if final_percent >= 0.85:
        grade = 5
    elif final_percent >= 0.75:
        grade = 4
    elif final_percent >= 0.60:
        grade = 3
    elif final_percent >= 0.50:
        grade = 2
    else:
        grade = 1

    if grade not in minimum_points:
        minimum_points[grade] = point

for grade in range(2, 6):
    if grade in minimum_points:
        print(f"{grade}: {minimum_points[grade]}")
    else:
        print(f"{grade}: Nope")
