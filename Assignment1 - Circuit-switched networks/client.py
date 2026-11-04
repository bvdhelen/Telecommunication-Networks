#Elena Sol Díaz Contreras
#Assignment1 - Circuit-switched networks

# Task:
    # Write a program which simulates the allocation and deallocation of resources according to the topology, capacities and demands outlined in the given JSON file!

import json
import sys

# AUXILIARY FUNCTION 1: Find a route between two endpoints
def find_path(u, v, possible_circuits):
    """
    Devuelve la primera ruta de 'possible_circuits' que empiece en u y termine en v.
    Si no encuentra ninguna, devuelve None.
    """
    for circuit in possible_circuits:
        if circuit[0] == u and circuit[-1] == v:
            return circuit
    return None

# AUXILIARY FUNCTION 2: Check if a route has capacity
def has_capacity(path, demand, remaining):
    """
    Devuelve True si TODOS los enlaces de 'path' tiene al menos 'demand' de capacidad libre.
    Si alguno no la tiene, duvuelve False.
    """
    for i in range(len(path) - 1):
        a = path[i]
        b = path[i + 1]
        key = tuple(sorted((a, b)))
        if remaining[key] < demand:
            return False
    return True

# AUXILIARY FUNCTION 3: Reserve (subtract) capacity on a route
def reserve_capacity(path, demand, remaining):
    for i in range(len(path) - 1):
        a = path[i]
        b = path[i + 1]
        key = tuple(sorted((a, b)))
        remaining[key] -= demand

# AUXILIARY FUNCTION 4: Free up (add) capacity on a route
def release_capacity(path, demand, remaining):
    for i in range(len(path) - 1):
        a = path[i]
        b = path[i + 1]
        key = tuple(sorted((a, b)))
        remaining[key] += demand

# MAIN PROGRAM
def main():
    if len(sys.argv) != 2:
        print("Usage: py .\\client.py <json_file>")
        return

    json_file = sys.argv[1]
    
    # 1. Read the JSON file
    with open(json_file, 'r') as file:
        data = json.load(file)
    #print(f"\nJSON '{json_file}' read succesfully!\n")

    #print("\n=== Data ===\n")
	#end_points = data['end-points']
    #switches = data['switches']
    links = data['links']
    possible_circuits = data['possible-circuits']
    duration = data['simulation']['duration']
    demands = data['simulation']['demands']

    #print(f"Available keys: {list(data.keys())}")
    #print(f"End-points: {end_points}")
    #print(f"Switches: {switches}")
    #print(f"Number of links: {len(links)}")
    #print(f"Number of possible circuits: {len(possible_circuits)}")
    #print(f"Number of demands: {len(demands)}")
    #print(f"Duration: {duration}")

    # 2. Store the initial capacity of each link
        # Since the network is undirected, I use an ordered key (nodeA, nodeB)
    remaining = {} #dictionary: key=(nodeA, nodeB) -> available capacity
    for link in links:
        a, b = link['points']
        capacity = float(link['capacity'])
        key = tuple(sorted((a, b)))
        remaining[key] = capacity
        #print(f"\tLink saved: {key} -> capacity = {capacity}")

    # 3. Add 'path' field to each demand (None = unassigned)
    for dem in demands:
        dem['path'] = None
    
    # 4. Event counter
    event_num = 1

    # 5. Time loop
    #print("\n=== Simulation ===")
    for t in range(1, duration + 1):
        #print(f"\n--- t = {t} ---")

        # 5.a RELEASE the demands that end in that 't'
        for dem in demands:
            if dem['end-time'] == t and dem['path'] is not None:
                release_capacity(dem['path'], dem['demand'], remaining)
                
                u, v = dem['end-points']
                #print(f"\t[FIN] Demand #{i}: {u} <-> {v}")
                print(f"{event_num}. demand deallocation: {u}<->{v} st:{t}")
                
                event_num += 1
                dem['path'] = None

        # 5.b ASSIGN the demands that begin at that 't'
        for dem in demands:
            if dem['start-time'] == t:
                u, v = dem['end-points']
                demand_value = dem['demand']
                #print(f"\t[INICIO] Demand #{i}: {u} <-> {v} (needs {demand_value})")

                path = find_path(u, v, possible_circuits)

                # Find route and check capacity
                if path is not None and has_capacity(path, demand_value, remaining):
                    reserve_capacity(path, demand_value, remaining)
                    dem['path'] = path
                    print(f"{event_num}. demand allocation: {u}<->{v} st:{t} - successful")
                else:
                    print(f"{event_num}. demand allocation: {u}<->{v} st:{t} - unsuccessful")
                
                event_num += 1

if __name__ == "__main__":
    main()

# Submission:
    # Send it to the TMS in .zip file which should contain one and only one file called client.py!
