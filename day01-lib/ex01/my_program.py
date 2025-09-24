from local_lib.path import Path

def main():
    folder = Path("my_folder")
    folder.makedirs_p()

    file = folder / "my_file.txt"
    file.write_text("Hello, this is a test using path.py!")

    content = file.read_text()
    print("File content:")
    print(content)

if __name__ == "__main__":
    main()