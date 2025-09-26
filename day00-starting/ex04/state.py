#!/usr/bin/env python3

import sys


def get_capital_cities_dict():
    capital_cities = {
        "OR": "Salem",
        "AL": "Montgomery",
        "NJ": "Trenton",
        "CO": "Denver",
    }
    return capital_cities


def get_states_dict():
    states = {"Oregon": "OR", "Alabama": "AL", "New Jersey": "NJ", "Colorado": "CO"}
    return states


def reverse_dict(dict_to_reverse):
    return {value: key for key, value in dict_to_reverse.items()}


def print_matching_state(capital_city):
    reversed_capital_cities_dict = reverse_dict(get_capital_cities_dict())
    reversed_states_dict = reverse_dict(get_states_dict())

    capital_city_abbreviation = reversed_capital_cities_dict.get(capital_city)

    if capital_city_abbreviation is None:
        print("Unknown capital city")
    else:
        print(reversed_states_dict.get(capital_city_abbreviation))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit()
    print_matching_state(sys.argv[1])
