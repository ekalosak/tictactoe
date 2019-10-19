# Python 3.5.2 :: Anaconda 4.2.0 (x86_64)
# Python 3.7.4

import pdb

from abc import ABC, abstractmethod
import sys
import argparse
from inspect import cleandoc
import numpy as np

from utils import new_logger
log = new_logger()

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

class Agent(ABC):
    # TODO actually maked this an abstract class
    # TODO make the RandomAgent class

    def __init__(self, value):
        self.value = value
        super().__init__()

    @abstractmethod
    def do_something(self):
        pass

    def __init__(self, tp):
        validagenttypes = ['random', 'nnrl']
        assert tp in validagenttypes, "Got agent type <{}>, must be in".format(
            tp, validagenttypes)

        if tp == 'nnrl':
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

class RandomAgent(Agent):
    

def new_board():
    board = np.matrix([[0,0,0], [0,0,0], [0,0,0]])
    return(board)

# def apply_move(x, y, wp, bd):
#     bd[x,y] = wp
#     return(bd)

# def is_legal(x, y, bd):
#     if x > 2 or x < 0: return(False)
#     if y > 2 or y < 0: return(False)
#     if bd[x,y] != 0: return(False)
#     return(True)

# def won(bd):
#     r = False
#     for x in range(3):
#         # check rows, then columns
#         if (bd[x,:] == 1).all() or (bd[x,:] == 2).all(): r = True
#         if (bd[:,x] == 1).all() or (bd[:,x] == 2).all(): r = True
#     # diags
#     if (bd.diagonal() == 1).all() or (bd.diagonal() == 2).all(): r = True
#     b2 = np.rot90(bd)
#     if (b2.diagonal() == 1).all() or (b2.diagonal() == 2).all(): r = True
#     return(r)

class Board(object):

    def __init__(self):
        self.state = new_board()
        self.gameover = False
        self.whichplayer = 1

    def __repr__(self):
        msg = """<BOARD>\nIt's player {}'s turn.\n{}""".format(
            self.whichplayer, self.state)
        return(cleandoc(msg))

    def _is_legal(self, x, y):
        if x > 2 or x < 0: return(False)
        if y > 2 or y < 0: return(False)
        if self.state[x,y] != 0: return(False)
        return(True)

    def _apply_move(self, x, y, wp):
        self.state[x,y] = wp

    def _next_player(self):
        self.whichplayer = (self.whichplayer % 2) + 1

    def _won(self):
        """Using current state, return whether anyone has won"""
        # TODO: program ties
        bd = self.state
        for x in range(3):
            # check rows, then columns
            if (bd[x,:] == 1).all() or (bd[x,:] == 2).all(): return(True)
            if (bd[:,x] == 1).all() or (bd[:,x] == 2).all(): return(True)
        # diags
        if (bd.diagonal() == 1).all() or (bd.diagonal() == 2).all(): return(True)
        b2 = np.rot90(bd)
        if (b2.diagonal() == 1).all() or (b2.diagonal() == 2).all(): return(True)
        return(False)

    def move(self, x, y):
        """If move is legal, apply it and switch players. Return reward."""
        if self._is_legal(x, y):
            log.debug("Legal move {} {}, applying to board for player {}".format(
                x, y, self.whichplayer))
            self._apply_move(x, y, self.whichplayer)
            log.debug("Applied moved to board")
            switchplayer = True
            r = 0.1 # small reward for legal move
        else:
            log.debug("Illegal move {} {}".format(x, y))
            switchplayer = False
            r = -0.1 # negative reward for illegal move
        if self._won():
            log.debug("Player {} won".format(self.whichplayer))
            self.gameover = True
            switchplayer = False
            r = 1 # big reward for winning
        if switchplayer:
            log.debug("Switching player, currently {}".format(self.whichplayer))
            self._next_player()
            log.debug("Player is now {}".format(self.whichplayer))
        return(r)

def train():
    """Play a fixed number of games
    In each game, agent moves and gets rewards.
    """
    epoch = 10
    agents = (Agent('random'), Agent('random'))
    for ng in range(epoch):
        log.info("Starting game {}".format(ng))
        bd = Board()
        log.info(bd)
        while not bd.gameover:
            # TODO: make random policy agent
            # TODO: make nnrl agent
            agent = agents[bd.whichplayer-1]
            pm = agent.propose_move()
            r = bd.move(pm)
            agent.apply_reward(r)

def game():
    """Interactive gameloop for playing 2 humans in cmdline"""
    board = Board()
    while not board.gameover: # get move from player, apply game logic
        log.info(board)
        i = input("Player {}, please enter your move 'yx': ".format( board.whichplayer))
        mx, my = tuple(map(lambda x: int(x), i))
        log.debug("Got move {} {}".format(mx,my))
        _ = board.move(mx, my) # discard reward
    log.info("Congrats player {}, you won!".format(board.whichplayer))

def main():
    parser = argparse.ArgumentParser(description='TicTacToe game')
    parser.add_argument('--train', help='Train the model',
        default=False, action='store_true')
    args = parser.parse_args()
    if not args.train: game()
    else: train()

def quit():
    log.info("\nQuitting...")
    sys.exit(0)

if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: quit()
