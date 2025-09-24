import sys

def get_capital_cities_dict():
	capital_cities = {
		"OR": "Salem",
		"AL": "Montgomery",
		"NJ": "Trenton",
		"CO": "Denver"
	}
	return capital_cities

def get_states_dict():
	states = {
		"Oregon" : "OR",
		"Alabama" : "AL",
		"New Jersey": "NJ",
		"Colorado" : "CO"
	}
	return states

def reverse_dict(dict_to_reverse):
	return {
		value: key for key, value in dict_to_reverse.items() 
	}

def get_state(capital_city):
	reversed_capital_cities_dict = reverse_dict(get_capital_cities_dict())
	reversed_states_dict = reverse_dict(get_states_dict())

	capital_city_abbreviation = lower_dictionnary_keys(reversed_capital_cities_dict).get(capital_city.lower())

	if capital_city_abbreviation is None:
		return None
	return reversed_states_dict.get(capital_city_abbreviation)

def lower_dictionnary_keys(dictionnary):
	return {
		key.lower(): value for key, value in dictionnary.items()
	}

def get_capital_city(state):
	states = lower_dictionnary_keys(get_states_dict())
	capital_cities = get_capital_cities_dict()

	state_abbreviation = states.get(state.lower())

	if state_abbreviation is None:
		return None
	return capital_cities.get(state_abbreviation)

def get_parsed_argument_as_list(script_arg):
	split_arg = script_arg.split(",")
	cleaned_list_from_spaces = [city_or_state.strip() for city_or_state in split_arg]
	cleaned_list_from_empty_strings = [city_or_state for city_or_state in cleaned_list_from_spaces if len(city_or_state) > 0]

	return cleaned_list_from_empty_strings

def print_is_capital_or_state(argument):
	capital_city = get_capital_city(argument)
	state = get_state(argument)
	
	if capital_city is None and state is None:
		print(f"{argument} is neither a capital city or state")
	if capital_city:
		print(f"{capital_city} is the capital of {argument}")
	if state:
		print(f"{argument} is the capital of {state}")
	
def all_in(argument):
	parsed_argument_as_list = get_parsed_argument_as_list(argument)
	for state_or_city in parsed_argument_as_list:
		print_is_capital_or_state(state_or_city)

if __name__ == "__main__":
	if len(sys.argv) != 2:
		sys.exit()
	all_in(sys.argv[1])
	