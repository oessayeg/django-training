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


def get_capital_city(state):
    states = get_states_dict()
    capital_cities = get_capital_cities_dict()

    state_abbreviation = states.get(state)
    if state_abbreviation is None:
        print("Unknown state")
    else:
        print(capital_cities.get(state_abbreviation))


def main():
    if len(sys.argv) != 2:
        sys.exit()
    get_capital_city(sys.argv[1])


if __name__ == "__main__":
    main()
