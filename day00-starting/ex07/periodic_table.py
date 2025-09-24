class Element:
	def __init__(self):
		self.name = None
		self.position = None
		self.number = None
		self.abbreviation = None
		self.molar = None
		self.electrons = None

def get_periodic_table_html_template(table_rows_content) -> str:
    return f"""<!DOCTYPE html>
			<html lang="en">
			<head>
				<meta charset="utf-8">
				<meta name="viewport" content="width=device-width, initial-scale=1">
				<title>Periodic Table</title>
			</head>
			<body>
				<main>
					<h1>Periodic Table</h1>
					<table id="periodic-table" style="border-collapse: collapse; table-layout: fixed; width: 100%;">
						<tbody>
							{table_rows_content}
						</tbody>
					</table>
				</main>
			</body>
		</html>"""

def get_html_empty_table_row():
	return """\n			<td style="width: 200px;"></td>\n"""

def get_html_table_row(element):
	return f"""
			<td style="border: 1px solid black; width: 200px;">
				<h4>{element.name}</h4>
				<ul>
					<li>No {element.number}</li>
					<li>{element.abbreviation}</li>
					<li>{element.molar}</li>
					<li>{element.electrons} electron</li>
				</ul>
			</td>
	"""

def parse_value(key_and_value_as_string):
	split_string = key_and_value_as_string.split(":")
	stripped_key_and_values = [key_and_value.strip() for key_and_value in split_string]

	value = stripped_key_and_values[1]
	return value

def get_name_and_position(name_and_position_as_string):
	split_name_and_position = name_and_position_as_string.split("=")
	stripped_name_and_position = [name_and_position.strip() for name_and_position in split_name_and_position]
	
	return stripped_name_and_position[0], parse_value(stripped_name_and_position[1])

def parse_and_get_element(data):
    element = Element()

    field_map = {
        1: lambda attr: setattr(element, "number", int(parse_value(attr))),
        2: lambda attr: setattr(element, "abbreviation", parse_value(attr)),
        3: lambda attr: setattr(element, "molar", parse_value(attr)),
        4: lambda attr: setattr(element, "electrons", parse_value(attr)),
    }

    for index, attribute in enumerate(data):
        if index == 0:
            name, position = get_name_and_position(attribute)
            element.name = name
            element.position = int(position)
        elif index in field_map:
            field_map[index](attribute)

    return element

def read_periodic_table_file_and_get_stripped_data():
	array_with_stripped_data = []
	file_name = "periodic_table.txt"

	with open(file_name, 'r') as periodic_table_file:
		for element in periodic_table_file:
			split_data = element.split(", ")
			array_with_stripped_data.append([element.strip() for element in split_data])
	return array_with_stripped_data

def parse_stripped_data_and_get_elements(array_with_stripped_data):
	elements = []

	for data in array_with_stripped_data:
		elements.append(parse_and_get_element(data))	
	return elements

def generate_periodic_table_in_html_file(formatted_html_table):
	with open("test.html", "w") as html:
		html.write(formatted_html_table)	

def has_gap_after_element(element, elements, element_index):
    if element_index + 1 >= len(elements):
        return False
    
    next_element = elements[element_index + 1]
    return (next_element.position != 0 and next_element.position - 1 != element.position)

def generate_empty_cells(element, elements, element_index):
    next_element = elements[element_index + 1]
    empty_cells = []
    
    current_pos = element.position
    target_pos = next_element.position
    
    while current_pos + 1 < target_pos:
        empty_cells.append(get_html_empty_table_row())
        current_pos += 1
    
    return "".join(empty_cells)

def build_row_element(element, elements, element_index):
	LAST_POSITION = 17

	row_element = ''
	if element.position == 0:
		row_element += '\n			<tr>\n'
	row_element += get_html_table_row(element)
	if has_gap_after_element(element, elements, element_index):
		row_element += generate_empty_cells(element, elements, element_index)
	if element.position == LAST_POSITION:
		row_element += '\n			</tr>\n'
	return row_element

def generate_periodic_table():
	array_with_stripped_data = read_periodic_table_file_and_get_stripped_data()
	elements = parse_stripped_data_and_get_elements(array_with_stripped_data)
	all_in = ""

	for element_index, element in enumerate(elements):
		template = build_row_element(element, elements, element_index)
		all_in += template
	final_template = get_periodic_table_html_template(all_in)
	generate_periodic_table_in_html_file(final_template)

if __name__ == "__main__":
	try:
		generate_periodic_table()
	except Exception as exception:
		print(f"There was an error generating the periodic table, error {exception}")
	
