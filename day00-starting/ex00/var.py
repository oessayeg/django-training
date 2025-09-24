def print_variable_and_its_type(variableToPrint):
	print(f"{variableToPrint} has a type {type(variableToPrint)}")

def my_var():
	int_var = 42
	str_var = "42"
	second_str_var = "quarante-deux"
	float_var = 42.0
	boolean_var = True
	list_var = [42]
	dict_var = {42: 42}
	tuple_var = (42,)
	set_var = set()

	print_variable_and_its_type(int_var)
	print_variable_and_its_type(str_var)
	print_variable_and_its_type(second_str_var)
	print_variable_and_its_type(float_var)
	print_variable_and_its_type(boolean_var)
	print_variable_and_its_type(list_var)
	print_variable_and_its_type(dict_var)
	print_variable_and_its_type(tuple_var)
	print_variable_and_its_type(set_var)

if __name__ == "__main__":
	my_var()