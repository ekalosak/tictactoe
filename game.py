# Python 3.5.2 :: Anaconda 4.2.0 (x86_64)
# Python 3.7.4

import pdb

import sys
import logging
import argparse
import numpy as np

# TODO implement real logging

# TODO: implement save and load for model
def new_model():
    """Initialize new Keras model with fixed architecture"""
    from keras.models import Sequential
    from keras.layers import Dense
    from keras.optimizers import Adam
    from collections import deque
    model = Sequential()
    model.add(Dense(units=16, activation='relu', input_dim=9))
    model.add(Dense(units=16, activation='relu'))
    model.add(Dense(9, activation='linear'))
    model.compile(loss='mse', optimizer=Adam(lr=learningrate))
    return(model)

def new_memory():
    memory = deque(maxlen=2000)
    return(memory)

class Agent(object):
    def __init__(self):
        self.model = new_model()
        self.memory = new_memory()
        self.learningrate = 0.01
        self.discount = 0.95

    # model.fit(state, reward_value, epochs=1, verbose=0)
    # prediction = model.predict(state)
    # target = reward + gamma * np.amax(model.predict(next_state))
    #
    # def remember(state, action, reward, next_state, done):
    #     memory.append((state, action, reward, next_state, done))



def new_board():
    board = np.matrix([[0,0,0], [0,0,0], [0,0,0]])
    return(board)

def apply_move(x, y, wp, bd):
    bd[x,y] = wp
    return(bd)

def is_legal(x, y, bd):
    r = True
    if x > 2 or x < 0: r = False
    if y > 2 or y < 0: r = False
    if bd[x,y] != 0: r = False
    return(r)

def won(bd):
    r = False
    for x in range(3):
        # check rows, then columns
        if (bd[x,:] == 1).all() or (bd[x,:] == 2).all(): r = True
        if (bd[:,x] == 1).all() or (bd[:,x] == 2).all(): r = True
    # diags
    if (bd.diagonal() == 1).all() or (bd.diagonal() == 2).all(): r = True
    b2 = np.rot90(bd)
    if (b2.diagonal() == 1).all() or (b2.diagonal() == 2).all(): r = True
    return(r)

class Board(object):
    def __init__(self):
        self.state = new_board()
        self.gameover = False
        self.whichplayer = 1

    def __repr__(self):
        print("<BOARD>")
        print("It's player {}'s turn.".format(self.whichplayer))
        print(self.state)

    def _is_legal(self, x, y):
        r = True
        if x > 2 or x < 0: r = False
        if y > 2 or y < 0: r = False
        if self.state[x,y] != 0: r = False
        return(r)

    def _apply_move(self, x, y, wp):
        self.state[x,y] = wp

    def _next_player(self):
        self.whichplayer = (self.whichplayer % 2) + 1

    def move(self, x, y, wp):
        """If move is legal, apply it. Return reward."""
        if self._is_legal(x, y):
            r = 0.1 # small reward for legal move
            self._apply_move(x, y, wp)
            self._next_player()
        else:
            r = -0.1 # negative reward for illegal move
        if won # TODO: continue here

def train():
    """Play a fixed number of games
    In each game, agent moves and gets rewards.
    """
    epoch = 10
    agents = (Agent(), Agent())
    for ng in range(epoch):
        print("Starting game {}".format(ng))
        bd = Board()
        print(bd)
        while not bd.gameover:
            agent = agents[bd.whichplayer-1]
            pm = agent.propose_move()
            r = bd.move(pm)
            agent.apply_reward(r)

def game():
    """Interactive gameloop for playing 2 humans in cmdline"""
    # TODO: use Board
    gameover = False
    board = new_board()
    whichplayer = 1
    while not gameover:
        print(board)
        i = input("Player {}, please enter your move: ".format(whichplayer))
        mx = int(i[0])
        my = int(i[1])
        if is_legal(mx, my, board):
            board = apply_move(mx, my, whichplayer, board)
            if won(board): gameover = True
            else: whichplayer = (whichplayer % 2) + 1
        else:
            print("Illegal move!")
    print("Congrats player {}, you won!".format(whichplayer))
    return(whichplayer) # return who won

def main():
    parser = argparse.ArgumentParser(description='TicTacToe game')
    parser.add_argument('--train', help='Train the model',
        default=False, action='store_true')
    args = parser.parse_args()
    if not args.train: game()
    else: train()

def quit(): sys.exit(0)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: quit()
