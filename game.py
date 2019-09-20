# Python 3.5.2 :: Anaconda 4.2.0 (x86_64)

import sys
import numpy as np
# import keras as ke

import pdb


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

def main():
    gameover = False
    board = np.matrix([[0,0,0], [0,0,0], [0,0,0]])
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
    main()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
