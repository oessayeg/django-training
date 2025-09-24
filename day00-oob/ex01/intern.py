class Intern:
    def __init__(self, name="My name? I’m nobody, an intern, I have no name."):
        self.name = name

    def __str__(self):
        return self.name

    def work(self):
        raise Exception("I’m just an intern, I can’t do that...")

    def make_coffee(self):
        return self.Coffee()

    class Coffee:
        def __str__(self):
            return "This is the worst coffee you ever tasted."


if __name__ == "__main__":
    no_name_intern = Intern()
    named_intern = Intern("Mark")

    print("No name intern: ", no_name_intern)
    print("Named intern: ", named_intern)

    coffee = named_intern.make_coffee()

    print(coffee)

    try:
        no_name_intern.work()
    except Exception as e:
        print(e)
