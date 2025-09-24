from beverages import Cappuccino, Chocolate, Coffee, HotBeverage, Tea
import random


class CoffeeMachine:
    class EmptyCup(HotBeverage):
        def __init__(self):
            super().__init__("empty cup", 0.90)

        def description(self):
            return "An empty cup?! Gimme my money back!"

    class BrokenMachineException(Exception):
        def __init__(self):
            super().__init__("This coffee machine has to be repaired.")

    def __init__(self):
        self.remaining_servings = 10

    def repair(self):
        self.remaining_servings = 10

    def serve(self, beverage):
        if self.remaining_servings <= 0:
            raise self.BrokenMachineException()

        self.remaining_servings -= 1
        random_number = random.randint(0, 1)

        if random_number == 0:
            return self.EmptyCup()
        return beverage()


if __name__ == "__main__":
    machine = CoffeeMachine()
    wanted_beverage = [Coffee, Tea, Chocolate, Cappuccino]

    try:
        for i in range(15):
            print(f"Drink {i+1}: {machine.serve(random.choice(wanted_beverage))}")
    except CoffeeMachine.BrokenMachineException as e:
        print(f"Exception caught: {e}")
        print("Repairing machine...")
        machine.repair()

    try:
        for i in range(15):
            print(f"Drink {i+1}: {machine.serve(random.choice(wanted_beverage))}")
    except CoffeeMachine.BrokenMachineException as e:
        print(f"Exception caught: {e}")
        print("Repairing machine...")
