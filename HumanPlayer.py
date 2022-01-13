class HumanPlayer:
    def __init__(self, name):
        self.name = name

    def choose_action(self, positions):
        while True:
            row = int(input("Input your action row: "))
            col = int(input("Input your action col: "))
            action = (row-1, col-1)
            if action in positions:
                return action
            else:
                print("This position is already taken.")

    def addState(self, state):
        pass

    def reward(self, reward):
        pass

    def reset(self):
        pass
