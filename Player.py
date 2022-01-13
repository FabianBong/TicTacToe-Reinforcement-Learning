import numpy as np
import pickle

class Player:
    def __init__(self, name, e_val = 0.4):
        self.name = name
        self.states = []
        self.learning_rate = 0.2
        self.e_val = e_val
        self.decay_gamma = 0.9
        self.states_value = {}

    # Function to choose player action
    def choose_action(self, positions, cur_board, symbol):
        if np.random.uniform(0, 1) <= self.e_val:  # In this case we will perform a random action
            index = np.random.choice(len(positions))  # get random position
            action = positions[index]
        else:
            max_val = -999
            for p in positions:
                next_board = cur_board.copy()
                next_board[p] = symbol
                next_board_hash = self.get_hash(next_board)
                value = 0 if self.states_value.get(next_board_hash) is None else self.states_value.get(next_board_hash)
                if value >= max_val:
                    max_val = value
                    action = p
        return action

    def reward(self, reward):
        for state in reversed(self.states):
            if self.states_value.get(state) is None:
                self.states_value[state] = 0
            self.states_value[state] += self.learning_rate * (self.decay_gamma * reward - self.states_value[state])
            reward = self.states_value[state]

    def addState(self, state):
        self.states.append(state)

    def reset(self):
        self.states = []

    def savePolicy(self):
        fw = open('policy_' + str(self.name), 'wb')
        pickle.dump(self.states_value, fw)
        fw.close()

    def loadPolicy(self, file):
        fr = open(file, 'rb')
        self.states_value = pickle.load(fr)
        fr.close()

    def get_hash(self, board):
        boardHash = str(board.reshape(9))
        return boardHash