import settings
import re
import sys

def get_defined_variables_in_settings():
	all_magic_and_defined_variables = vars(settings)
	user_defined_global_variables = {
		variable: value
		for variable, value
		in all_magic_and_defined_variables.items()
		if not variable.startswith("__")
	}
	return user_defined_global_variables

def is_valid_extension(templateFile):
	pattern = re.compile(r"\.template$")
	return bool(pattern.search(templateFile))

def read_and_get_template_content(templateFile):
	if not is_valid_extension(templateFile):
		raise Exception("File does not end with '.template' extension")
	with open(templateFile, 'r') as template:
		return template.read()

def read_and_generate_html_file(templateFile):
	template_content = read_and_get_template_content(templateFile)
	settings_global_variables = get_defined_variables_in_settings()
	newly_generate_file_name = templateFile.replace(".template", "")

	with open(f"{newly_generate_file_name}.html", 'w') as html_file:
		formatted_template = template_content.format(**settings_global_variables)
		html_file.write(formatted_template)

if __name__ == "__main__":
	try:
		if (len(sys.argv) != 2):
			raise Exception("Usage: python render.py <file.template>")
		read_and_generate_html_file(sys.argv[1])
	except Exception as e:
		print(f"Error generating html template, {e}")
