from math import *
import random
from copy import deepcopy
from pandas import Series, DataFrame

def read_cities(file_name):
    city_tuples = []
    stream = open(file_name)
    data = stream.readlines()
    stream.close()
    for line in data:
        line_list = []
        for entry in line.split('\t'): # tab seperated
            entry = str(entry)
            entry = entry.replace('\n','') # remove new line character
            if any(character.isdigit() for character in entry):
                entry = float(entry) # if entry is formatted as a number, convert to float
                # https://stackoverflow.com/questions/19859282/check-if-a-string-contains-a-number
            line_list.append(entry)
        line_list = tuple(line_list)
        city_tuples.append(line_list)
    return city_tuples

def print_cities(road_map):
    for city in road_map:
        print(city[1] + ' (' + str(round(city[2],2)) + ',' + str(round(city[3],2)) + ')')

def distance(lat1degrees, long1degrees, lat2degrees, long2degrees):
    earth_radius = 3956  # miles
    lat1 = radians(lat1degrees)
    long1 = radians(long1degrees)
    lat2 = radians(lat2degrees)
    long2 = radians(long2degrees)
    lat_difference = lat2 - lat1
    long_difference = long2 - long1
    sin_half_lat = sin(lat_difference / 2)
    sin_half_long = sin(long_difference / 2)
    a = sin_half_lat ** 2 + cos(lat1) * cos(lat2) * sin_half_long ** 2
    c = 2 * atan2(sqrt(a), sqrt(1.0 - a))
    return earth_radius * c

def compute_total_distance(road_map):
    total_distance = 0
    for i in range(0, len(road_map)):
        x1 = road_map[i][2]
        x2 = road_map[(i + 1) % len(road_map)][2]
        y1 = road_map[i][3]
        y2 = road_map[(i + 1) % len(road_map)][3]
        #euclidean_distance = sqrt(((x1-x2)**2) + ((y1-y2)**2))
        total_distance = total_distance + distance(x1,y1,x2,y2)

    return total_distance

def swap_adjacent_cities(road_map, index):
    new_road_map = deepcopy(road_map)
    if index == len(road_map) - 1: # if index refers to last element in list
        new_road_map[index], new_road_map[0] = new_road_map[0], new_road_map[index]
    else:
        new_road_map[index], new_road_map[index+1] = new_road_map[index+1], new_road_map[index]
    new_total_distance = compute_total_distance(new_road_map)
    return (new_road_map, new_total_distance)

def swap_cities(road_map, index1, index2):
    new_road_map = deepcopy(road_map)
    new_road_map[index1], new_road_map[index2] = new_road_map[index2], new_road_map[index1]
    new_total_distance = compute_total_distance(new_road_map)
    return(new_road_map, new_total_distance)

def find_best_cycle(road_map):
    best_cycle = (road_map, compute_total_distance(road_map))
    best_distance = best_cycle[1]
    new_cycle = ()
    swaps = 10000
    for i in range(1,swaps):
        swap_to_perform  = random.choice(['swap_cities', 'swap_adjacent_cities'])
        if swap_to_perform == 'swap_cities':
            index1 = random.randint(0, len(road_map) - 1)
            index2 = random.randint(0, len(road_map) - 1)
            new_cycle = swap_cities(best_cycle[0], index1, index2)
        elif swap_to_perform == 'swap_adjacent_cities':
            index = random.randint(0, len(road_map) - 1)
            new_cycle = swap_adjacent_cities(best_cycle[0], index)
        if new_cycle[1] < best_distance:
                best_cycle = new_cycle
                best_distance = new_cycle[1]     
    return best_cycle[0]

def print_map(road_map):
    map = DataFrame()
    cities = []
    x = []
    y = []
    connections = []
    distances = []
    for city in (road_map):
        cities.append(city[1])
        x.append(city[2])
        y.append(city[3])
    for i in range(len(cities)):
        if i == len(cities)-1:
            connections.append(cities[0])
        else:
            connections.append(cities[i+1])
    for i in range(len(cities)):
        if i == 0:
            distances.append(distance(x[i], y[i], x[i+1], y[i+1]))
        elif i == len(cities)-1:
            distances.append(distance(x[i], y[i], x[0], y[0]))
        else:
            distances.append(distance(x[i], y[i], x[i+1], y[i+1]))
    
    map['City'] = Series(cities)
    map['Connection'] = Series(connections)
    map['Distance (Miles)'] = Series(distances)
    map['Distance (Miles)'] = map['Distance (Miles)'].round(2)
    map['Total Distance (Miles)'] = map['Distance (Miles)'].cumsum()
    print(map)
    
def main():
    valid_file = False
    while not valid_file:
        try:
            cities_file = input('Please enter the name of a file containg the cities to travel: ') or 'city-data.txt'
            road_map = read_cities(cities_file)
            valid_file = True
        except FileNotFoundError:
            print('File not found. Please try again')
    print('')
    print('The cities to be travelled between are: ')
    print('')
    print_cities(road_map)
    print('')
    print('The shortest route between these cities that can be found is: ')
    print('')
    print_map(find_best_cycle(road_map))

if __name__ == "__main__":
    