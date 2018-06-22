import pytest
from cities import *

def test_compute_total_distance_circular():
    # Simplified Three City Trip
    road_map = [('Alabama', 'Montgomery', 32.361538, -86.279118),
    ('Alaska', 'Juneau', 58.301935, -134.41974),
    ('Arizona',	'Phoenix', 33.448457, -112.073844)]
    montgomery_to_junea = distance(32.361538, -86.279118, 58.301935, -134.41974)
    juneau_to_phoenix = distance(58.301935, -134.41974, 33.448457, -112.073844)
    phoenix_to_montgomery = distance(33.448457, -112.073844, 32.361538, -86.279118) # route must be circular (return to original city)
    # check total distance for the circular route, to 2 decimal places, is correct
    assert round(compute_total_distance(road_map),2) == round(montgomery_to_junea +
                                                             juneau_to_phoenix + 
                                                             phoenix_to_montgomery,2)
def test_compute_total_distance_zero_distance():    
    # Test when there is zero distance between the cities                                                          
    road_map = [('Alabama', 'Montgomery', 32.361538, -86.279118),
    ('Alaska', 'Juneau', 32.361538, -86.279118)]
    assert compute_total_distance(road_map) == 0

def test_compute_total_distance_zero_input():
    # Test for inputs zero
    road_map = [('Alabama', 'Montgomery', 0, 0),
    ('Alaska', 'Juneau', 0, 0)]
    assert compute_total_distance(road_map) == 0

def test_swap_adjacent_cities():
    # Simplified Three City Trip
    road_map = [('Alabama', 'Montgomery', 32.361538, -86.279118),
    ('Alaska', 'Juneau', 58.301935, -134.41974),
    ('Arizona',	'Phoenix', 33.448457, -112.073844)]
    # Test Swap
    new_distance = compute_total_distance(road_map)
    assert swap_adjacent_cities(road_map, 1) == ([('Alabama', 'Montgomery', 32.361538, -86.279118), 
    ('Arizona', 'Phoenix', 33.448457, -112.073844), 
    ('Alaska', 'Juneau', 58.301935, -134.41974)], new_distance)

def test_swap_adjacent_cities_last():
    # Simplified Three City Trip
    road_map = [('Alabama', 'Montgomery', 32.361538, -86.279118),
    ('Alaska', 'Juneau', 58.301935, -134.41974),
    ('Arizona',	'Phoenix', 33.448457, -112.073844)]
    # Test Swap with last index in list
    new_distance = compute_total_distance(road_map)
    assert swap_adjacent_cities(road_map, 2) == ([('Arizona', 'Phoenix', 33.448457, -112.073844),
    ('Alaska', 'Juneau', 58.301935, -134.41974),
    ('Alabama', 'Montgomery', 32.361538, -86.279118) 
    ], new_distance)


def test_swap_cities():
    # Simplified Three City Trip
    road_map = [('Alabama', 'Montgomery', 32.361538, -86.279118),
    ('Alaska', 'Juneau', 58.301935, -134.41974),
    ('Arizona',	'Phoenix', 33.448457, -112.073844)]
    # Test Swap
    new_distance = compute_total_distance([('Alabama', 'Montgomery', 32.361538, -86.279118),
    ('Arizona', 'Phoenix', 33.448457, -112.073844),
    ('Alaska', 'Juneau', 58.301935, -134.41974)])
    assert swap_cities(road_map, 1, 2) == ([('Alabama', 'Montgomery', 32.361538, -86.279118),
    ('Arizona', 'Phoenix', 33.448457, -112.073844),
    ('Alaska', 'Juneau', 58.301935, -134.41974)], new_distance)

def test_find_best_cycle():
    # best cycle should find a distance less than the original
    assert find_best_cycle(read_cities('city-data.txt'))[1] < compute_total_distance(read_cities('city-data.txt'))