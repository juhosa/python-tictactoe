import os
import readchar
import random


def draw_board(board: list[list[str]], cursor: tuple[int, int]):
    top_row = "/-----\\"
    print(top_row)

    for i, row in enumerate(board):
        r = ["|"]

        for j, c in enumerate(row):
            if i == cursor[0] and j == cursor[1]:
                r.append(f"\033[4m{c}\033[0m")
            else:
                r.append(c)
            r.append("|")
        print("".join(r))

    bottom_row = "\\-----/"
    print(bottom_row)


def place_tick(board, cursor_index, player_char="x"):
    row = cursor_index[0]
    col = cursor_index[1]

    if board[row][col] == " ":
        board[row][col] = player_char


def play_robot_turn(board):
    # find empty slots
    emptys = []
    for i, row in enumerate(board):
        for j, c in enumerate(row):
            if c == " ":
                emptys.append((i, j))

    # pick one at random
    if len(emptys) > 0:
        rando = random.choice(emptys)
        place_tick(board, rando, "o")


def check_win(board) -> tuple[bool, str]:
    # horizontal
    for row in board:
        if "".join(row) == "xxx":
            return (True, "x")
        elif "".join(row) == "ooo":
            return (True, "o")

    # vertical
    for i in range(0, 3):
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != " ":
            return (True, board[0][i])

    # diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != " ":
        return (True, board[0][0])

    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != " ":
        return (True, board[0][2])

    return (False, "")


def render(board, cursor_index):
    # TODO: Make multiplatform compatible
    os.system("clear")

    print("Move with h/j/k/l. space places the tick. q quits")

    draw_board(board, cursor_index)
    print(f"cursor: {cursor_index}")


def main():
    board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
    cursor_index = (0, 0)
    while True:
        render(board, cursor_index)

        # TODO: readchar possibly isn't multiplatfrom?
        char = readchar.readchar()

        if char == "j":
            cursor_index = (min(cursor_index[0] + 1, 2), cursor_index[1])
        elif char == "k":
            cursor_index = (max(cursor_index[0] - 1, 0), cursor_index[1])
        elif char == "l":
            cursor_index = (cursor_index[0], min(cursor_index[1] + 1, 2))
        elif char == "h":
            cursor_index = (cursor_index[0], max(cursor_index[1] - 1, 0))
        elif char == " ":
            place_tick(board, cursor_index, "x")
            render(board, cursor_index)

            win, winner = check_win(board)
            if win:
                print(f"{winner} won!")
                break

            play_robot_turn(board)
            render(board, cursor_index)
            win, winner = check_win(board)
            if win:
                print(f"{winner} won!")
                break

        elif char == "q":
            break


if __name__ == "__main__":
    main()
