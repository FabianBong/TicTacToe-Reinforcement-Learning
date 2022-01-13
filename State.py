import numpy as np


class State:
    def __init__(self, p1, p2):
        self.board = np.zeros((3, 3))  # Board is 3x3 bc TicTacToe
        self.p1 = p1  # Player one init
        self.p2 = p2  # Player two init
        self.isEnd = False  # Game is not over
        self.boardHash = None  # No board hash yet
        self.playerSymbol = 1  # First player is playing first

    # Hashing the board state allows us to easily store the board state
    # One hash = one board configuration
    def get_hash(self):
        self.boardHash = str(self.board.reshape(9))  # Reshape into one column vector
        return self.boardHash

    # This function will return all positions that are available on the board
    def get_available_positions(self):
        return [(i, j) for i in range(3) for j in range(3) if self.board[i, j] == 0]

    # Add a symbol to the board
    def add_to_board(self, position):
        self.board[position] = self.playerSymbol  # add player symbol
        self.playerSymbol = self.playerSymbol * -1  # switch to 1 or -1

    def check_winner(self):
        # Non-Diagonal lines check
        for i in range(3):
            if sum(self.board[i, :]) == 3 or sum(self.board[:, i]) == 3:
                self.isEnd = True
                return 1
            if sum(self.board[i, :]) == -3 or sum(self.board[:, i]) == -3:
                self.isEnd = True
                return -1

        # Diagonal lines check
        if self.board[0, 0] == self.board[1, 1] == self.board[2, 2] and self.board[1, 1] != 0:
            self.isEnd = True
            return self.board[1, 1]
        if self.board[0, 2] == self.board[1, 1] == self.board[2, 0] and self.board[1, 1] != 0:
            self.isEnd = True
            return self.board[1, 1]

        # Tie
        if len(self.get_available_positions()) == 0:
            self.isEnd = True
            return 0

        self.isEnd = False
        return None

    def reward(self):
        result = self.check_winner()
        if result == 1:
            self.p1.reward(1)
            self.p2.reward(0)
        elif result == -1:
            self.p1.reward(0)
            self.p2.reward(1)
        else:
            self.p1.reward(0.1)
            self.p2.reward(0.5)

    def reset(self):
        self.board = np.zeros((3, 3))
        self.boardHash = None
        self.isEnd = False
        self.playerSymbol = 1

    ## REFACTOR
    def train(self, rounds=100):
        for i in range(rounds):
            print("Training Round " + str(i)) if i % 1000 == 0 else None
            while not self.isEnd:
                positions = self.get_available_positions()
                p1_action = self.p1.choose_action(positions, self.board, self.playerSymbol)
                self.add_to_board(p1_action)
                board_hash = self.get_hash()
                self.p1.addState(board_hash)

                win = self.check_winner()
                if win is not None:
                    self.reward()
                    self.p1.reset()
                    self.p2.reset()
                    self.reset()
                    break

                positions = self.get_available_positions()
                p2_action = self.p2.choose_action(positions, self.board, self.playerSymbol)
                self.add_to_board(p2_action)
                board_hash = self.get_hash()
                self.p2.addState(board_hash)

                win = self.check_winner()
                if win is not None:
                    self.reward()
                    self.p1.reset()
                    self.p2.reset()
                    self.reset()
                    break

    ## REFACTOR
    def showBoard(self):
        # p1: x  p2: o
        for i in range(0, 3):
            print('-------------')
            out = '| '
            for j in range(0, 3):
                if self.board[i, j] == 1:
                    token = 'x'
                if self.board[i, j] == -1:
                    token = 'o'
                if self.board[i, j] == 0:
                    token = ' '
                out += token + ' | '
            print(out)
        print('-------------')

    def play_human(self):
        while not self.isEnd:
            print("")
            print("It is " + self.p1.name + "'s turn!")
            print("")
            positions = self.get_available_positions()
            p1_action = self.p1.choose_action(positions, self.board, self.playerSymbol)
            self.add_to_board(p1_action)
            self.showBoard()
            win = self.check_winner()

            if win is not None:
                if win == 1:
                    print("")
                    print(self.p1.name, " has won!!")
                else:
                    print("tie!")
                self.reset()
                break

            print("")
            print("It is " + self.p2.name + "'s turn!")
            print("")
            position = self.get_available_positions()
            p2_action = self.p2.choose_action(positions)
            self.add_to_board(p2_action)
            self.showBoard()

            win = self.check_winner()
            if win is not None:
                if win == -1:
                    print("")
                    print(self.p2.name, " has won!!")
                else:
                    print("Tie!")
                self.reset()
                break
