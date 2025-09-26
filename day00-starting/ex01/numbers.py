#!/usr/bin/env python3

def read_and_get_file_content(filename):
    with open(filename, "r") as file_to_read:
        file_content = file_to_read.read()
        return file_content


def print_all_numbers_each_per_line(file_content):
    split_numbers = file_content.split(",")
    for number in split_numbers:
        print(f"{number}")


def read_and_print():
    file_content = read_and_get_file_content("numbers.txt")
    print_all_numbers_each_per_line(file_content)


if __name__ == "__main__":
    try:
        read_and_print()
    except Exception as exception:
        print(f"There was an error reading the file, error {exception}")
