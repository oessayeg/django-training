def get_musicians_list():
	d = [
		('Hendrix' , '1942'),
		('Allman' , '1946'),
		('King' , '1925'),
		('Clapton' , '1945'),
		('Johnson' , '1911'),
		('Berry' , '1926'),
		('Vaughan' , '1954'),
		('Cooder' , '1947'),
		('Page' , '1944'),
		('Richards' , '1943'),
		('Hammett' , '1962'),
		('Cobain' , '1967'),
		('Garcia' , '1942'),
		('Beck' , '1944'),
		('Santana' , '1947'),
		('Ramone' , '1948'),
		('White' , '1975'),
		('Frusciante', '1970'),
		('Thompson' , '1949'),
		('Burton' , '1939')
	]
	return d

def list_to_map(musicians_list):
	musicians_map = {}

	for musician_name, year in musicians_list:
		musicians_map[year] = musician_name
	return musicians_map

def print_musicians_map(musicians_map):
	for year, musician_name in musicians_map.items():
		print(f"{year}: {musician_name}")

if __name__ == "__main__":
	musicians_list = get_musicians_list()
	musicians_map = list_to_map(musicians_list)
	print_musicians_map(musicians_map)
