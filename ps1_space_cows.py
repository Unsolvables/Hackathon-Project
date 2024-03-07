###########################
# 6.0002 Problem Set 1a: Space Cows 
# Name:
# Collaborators:
# Time:

from ps1_partition import get_partitions
import time
import timeit
import matplotlib.pyplot as plt


# ================================
# Part A: Transporting Space Cows
# ================================

# Problem 1
def load_cows(filename):
    """
    Read the contents of the given file.  Assumes the file contents contain
    data in the form of comma-separated cow name, weight pairs, and return a
    dictionary containing cow names as keys and corresponding weights as values.

    Parameters:
    filename - the name of the data file as a string

    Returns:
    a dictionary of cow name (string), weight (int) pairs
    """
    # TODO: Your code here
    cow_data = {}
    with open(filename, "r") as data:
        for i in data:
            name, weight = i.strip().split(",")
            if name not in cow_data:
                cow_data[name] = int(weight)
            else:
                cow_data[name] = int(weight)
    return cow_data


# Problem 2
def greedy_cow_transport(cows, limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    sorted_cows = sorted(cows.items(), key=lambda x: x[1], reverse=True)

    trips = []
    while sorted_cows:
        trip = []
        trip_weight = 0
        i = 0
        while i < len(sorted_cows):
            cow, weight = sorted_cows[i]
            if trip_weight + weight <= limit:
                trip.append(cow)
                trip_weight += weight
                del sorted_cows[i]
            else:
                i += 1
        trips.append(trip)
    return trips


# Problem 3
def brute_force_cow_transport(cows, limit=10):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips 
        Use the given get_partitions function in ps1_partition.py to help you!
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation
            
    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)
    
    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    # TODO: Your code here
    from ps1_partition import partitions, get_partitions
    best_partition = None
    min_trips = float('inf')
    for partition in get_partitions(cows):
        if all(sum(cows[name] for name in trip) <= limit for trip in partition):
            if len(partition) < min_trips:
                best_partition = partition
                min_trips = len(partition)

    return best_partition


# Problem 4
def compare_cow_transport_algorithms():
    """
    Using the data from ps1_cow_data.txt and the specified weight limit, run your
    greedy_cow_transport and brute_force_cow_transport functions here. Use the
    default weight limits of 10 for both greedy_cow_transport and
    brute_force_cow_transport.

    Print out the number of trips returned by each method, and how long each
    method takes to run in seconds.

    Returns:
    Does not return anything.
    """
    # TODO: Your code here
    results_greedy = []
    results_brute_force = []
    cow_data = load_cows("ps1_cow_data_mine")
    subset_cow_data = {}
    a = len(list(cow_data.items()))
    for num_cows in range(1, a + 1):
        # Limit the subset cow data to the current number of cows
        count = 0
        for key, value in cow_data.items():
            if count < num_cows:
                subset_cow_data[key] = value
                count += 1
        # Greedy algorithm
        time_greedy = timeit.timeit(lambda: greedy_cow_transport(subset_cow_data, 10), number=1) * 1000 * 1000
        results_greedy.append(time_greedy)

        # Brute force algorithm

        if count < 12:
            time_brute_force = timeit.timeit(lambda: brute_force_cow_transport(subset_cow_data, 10), number=1) * 1000 * 1000
            results_brute_force.append(time_brute_force)
        else:
            time_brute_force = 3 * 1000 * 1000
            results_brute_force.append(time_brute_force)
    return results_greedy, results_brute_force


results_greedy, results_brute_force = compare_cow_transport_algorithms()
print("Greedy Algorithm Times (ms):", results_greedy)
print("Brute Force Algorithm Times (ms):", results_brute_force)


# Number of cows
cow_data = load_cows("ps1_cow_data_mine")
num_cows = list(range(1, 101))
# Plotting the results
plt.figure(figsize=(10, 6))
plt.plot(num_cows, results_greedy, marker='o', markersize=1, label='Greedy Algorithm', color='blue')
plt.plot(num_cows, results_brute_force, marker='s', markersize=1, label='Brute Force Algorithm (10 Cows)', color='red')
plt.xlabel('Number of Cows')
plt.xlabel('Number of Cows')
plt.ylabel('Time (μs)')
plt.title('Comparison of Greedy and Brute Force Algorithms')
plt.legend()
plt.grid(True)
plt.xticks(range(0, max(num_cows) + 1, 10))
plt.ylim(0, 200)
plt.xlim(0, 100)
plt.tight_layout()
plt.show()
