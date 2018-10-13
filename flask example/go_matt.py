# Go Base Game Class
# Author: Matthew Bird
# date: 10/5/2018

from copy import deepcopy
from math import floor
from random import choice


class Game:
    def __init__(self, board_size=19, rules=None):
        """

        The Game class is for playing go. There is only one method for now, "play".

        :param board_size: int
        :param rules: {'suicide': False, 'komi': 6.5, 'superko': True, 'editmode': False}
        """
        self.board_size = board_size
        self.board = board_generate_empty(board_size)
        self.board_history = [deepcopy(self.board)]
        self.rules = rules if rules else {'suicide': False, 'komi': 6.5, 'superko': True, 'editmode': False}
        self.captures = {'w': [], 'b': []}
        self.turn = "b"
        self.latest_status = None

    def play(self, xy, color):
        """

        Place a stone at xy of the given color.
        All associated actions that normally take place when playing a stone are taken care of.

        :param xy: (int,int)
        :param color: 'b' or 'w'
        :return: N/A
        """
        validity = xy_is_valid(xy, color, self.board, self.rules, self.board_history)
        self.latest_status = validity
        self.latest_status['xy'] = xy
        self.latest_status['captured_stones'] = []
        if validity["status"] == "valid":
            self.board = xy_play_on_board(xy, self.board, color)
            new_captures = list(xy_to_captures(xy, color, self.board_history[-1]))
            self.captures[color] += new_captures
            self.board_history.append(deepcopy(self.board))
            self.latest_status['captured_stones'] = new_captures
            return True
        return False


def xy_is_valid(xy, color, board, rules, board_history):
    """

    Determines if a play at xy is valid for a given color, board, rules, and board_history.

    :param xy: tuple (x, y)
    :param color: 'w' or 'b'
    :param board: 2d list
    :param rules: dict
    :param board_history: 3d list
    :return: dict
    """
    response = {"status": "valid", "result": []}

    # =========CAN I PLACE IT==========

    # if xy is off the board
    if xy_off_board(xy, board):
        response["status"] = "invalid"
        response["result"].append("off_board")
    #
    # if location is occupied
    if xy_occupied(xy, board):
        response["status"] = "invalid"
        response["result"].append("occupied_location")

    # =========IF I PLACE IT==========

    if response["status"] == "valid":
        fictional_board = xy_play_on_board(xy, deepcopy(board), color)

        # if it violates suicide
        if not rules['suicide']:
            if xy_suicide(xy, fictional_board, color):
                response["status"] = "invalid"
                response["result"].append("suicide")

        # if it violates superko
        if rules['superko']:
            if not rule_superko(fictional_board, board_history):
                response["status"] = "invalid"
                response["result"].append("superko")
    return response


def xy_off_board(xy, board):
    """

    Return True if xy is off the board.

    :param xy: (int, int)
    :param board: 2d list
    :return: bool
    """
    return False if 0 <= xy[0] < len(board) and 0 <= xy[1] < len(board) else True


def xy_occupied(xy, board):
    """

    Returns True if xy is already occupied on the given board.

    :param xy: (int, int)
    :param board: 2d list
    :return: bool
    """
    return True if board[xy[0]][xy[1]] else False


def xy_play_on_board(xy, board, color):
    """

    Returns board after stone is played at xy.

    :param xy: (int, int)
    :param board: 2d list
    :param color: 'b' or 'w'
    :return: 2d list
    """
    board[xy[0]][xy[1]] = color
    potential_adjacent_captures = xy_adjacents(xy, board)
    opp_color = switch_color(color)
    p_a_p = filter(lambda xy_: board[xy_[0]][xy_[1]] == opp_color, potential_adjacent_captures)
    for xy_opp in p_a_p:
        group = xy_to_group(xy_opp, board)
        if group_is_surrounded(group, board):
            board = group_remove(group, board)
    return board


def xy_to_group(xy, board):
    """

    Returns the group of which the stone at xy is a member.

    :param xy: (int, int)
    :param board: 2d list
    :return: group {(int,int), (int,int), ...}
    """
    group = {xy}
    inspected = set([])
    to_inspect = group - inspected
    while to_inspect:
        for stone in to_inspect:
            inspected.add(stone)
            group |= xy_adjacents(stone, board, filter_by="friend")
        to_inspect = group - inspected
    return group


def xy_adjacents(xy, board=None, filter_by=None, color=None):
    """

    Returns locations neighboring xy.
    if color is given, it is preferred, otherwise it is inferred from the board.
    if filter_by == "friend" then friendly adjacents are returned.
    if filter_by == "foe" then opponents adjacents are returned.
    if filter_by == "None" then open liberties are returned.

    :param xy: (int, int)
    :param board: 2d list
    :param filter_by: None, "None", "friend", "foe"
    :param color: "b" or "w"
    :return: {(int,int), (int,int), ...}
    """
    color = board[xy[0]][xy[1]] if not color else color
    adjacents = {(xy[0] + 1, xy[1]), (xy[0] - 1, xy[1]), (xy[0], xy[1] + 1), (xy[0], xy[1] - 1)}
    legal_adjs = set(filter(lambda xy_: 0 <= xy_[0] <= len(board) - 1 and 0 <= xy_[1] <= len(board) - 1, adjacents))
    if filter_by == "friend":
        legal_adjs &= {xy_ for xy_ in legal_adjs if board[xy_[0]][xy_[1]] == color}
    elif filter_by == "foe":
        legal_adjs &= {xy_ for xy_ in legal_adjs if board[xy_[0]][xy_[1]] == switch_color(color)}
    elif filter_by == "None":
        legal_adjs &= {xy_ for xy_ in legal_adjs if not board[xy_[0]][xy_[1]]}
    return legal_adjs


def xy_suicide(xy, board, color):
    """

    Return True if xy is a suicide move.

    :param xy: (int, int)
    :param board: 2d list
    :param color: 'b' or 'w'
    :return: bool
    """
    group = xy_to_group(xy, board)

    if group_adjacents(group, board, color) == group_adjacents(group, board, filter_by="foe"):
        for xy_adj in xy_adjacents(xy, board, filter_by="foe", color=color):
            group_adj = xy_to_group(xy_adj,board)
            if group_is_surrounded(group_adj,board):
                return False
        return True
    else:
        return False


def xy_to_captures(xy, color, board):

    """

    Returns the number of captures the move at xy produces.

    :param xy: (int, int)
    :param color: 'b' or 'w'
    :param board: 2d list
    :return: int
    """
    captures = set([])
    for adj in xy_adjacents(xy, board, "foe", color):
        potential_captured_group = xy_to_group(adj, board)
        captured_groups_adjacents = group_adjacents(potential_captured_group, board, filter_by="None")
        if len(captured_groups_adjacents) <= 1:
            captures |= potential_captured_group
    return captures


def group_adjacents(group, board, filter_by=None):
    """

    Returns what the adjacent locations are for a group.
      if filter_by == "None" then returns open liberties.
      if filter_by == "friend" then returns friendly neighbors.
      if filter_by == "foe" then returns opponents neighbors.

    :param group: {(int,int), (int,int), ...}
    :param board: 2d list
    :param filter_by: None, "None", "friend", "foe"
    :return: {(int,int), (int,int), ...}
    """
    liberties = set([])
    for location in group:
        if filter_by == "None":
            liberties |= xy_adjacents(location, board, filter_by="None")
        elif filter_by == "friend":
            liberties |= xy_adjacents(location, board, filter_by="friend")
        elif filter_by == "foe":
            liberties |= xy_adjacents(location, board, filter_by="foe")
        else:
            liberties |= xy_adjacents(location, board)
    liberties -= group
    return liberties


def group_is_surrounded(group, board):
    """

    Returns True if a group is surrounded.

    :param group: {(int,int), (int,int), ...}
    :param board: 2d list
    :return: bool
    """
    if group_adjacents(group, board, filter_by="None"):
        return False
    else:
        return True


def group_remove(group, board):
    """

    Removes the group from the board and returns the new board.

    :param group: {(int,int), (int,int), ...}
    :param board: 2d list
    :return: 2d list
    """
    for xy in group:
        board[xy[0]][xy[1]] = None
    return deepcopy(board)


def rule_superko(board, board_history):
    """

    Returns True is board position is not in the history.
            False if it is.

    :param board: 2d list
    :param board_history: 3d list
    :return: bool
    """
    if board in board_history:
        return False
    return True


def board_generate_empty(size: 'board size'):
    """

    Generates an empty board.

    :param size: int
    :return: 2d list
    """
    empty_board = [[None] * size for _ in range(size)]
    return empty_board


def switch_color(color):
    """

    Returns 'w' if 'b'.
    Returns 'b' if 'w'.

    :param color: 'w' or 'b'
    :return: 'w' or 'b'
    """
    return "b" if color == "w" else "w"


def flatten(list_of_lists):
    """

    Turns a 2d list into a 1d list by means of unraveling it.

    :param list_of_lists: 2d list
    :return: list
    """
    flattened_list = [y for x in list_of_lists for y in x]
    return flattened_list


def get_int_width(integer):
    """

    Quite literally tells you the length of an integer (cast as a string).

    :param integer: int
    :return: int
    """
    return len(str(integer))


def render_board(board, empty=' '):
    """

    Generates a 2d ascii image of the board.

    :param board: 2d list
    :param empty: char which will represent how empties are shown
    :return: ascii image of board
    """
    board_image = ''

    size_list = list(range(len(board[0])))

    first_digit = [floor(x1 / 10.) for x1 in size_list]
    second_digit = [x2 % 10 for x2 in size_list]

    largest_int_width = get_int_width(size_list[-1])

    print_row = ' ' * (largest_int_width + 2)
    for ix in range(len(size_list)):
        if first_digit[ix]:
            print_row += str(first_digit[ix]) + " "
        else:
            print_row += "  "
    board_image += print_row + "\n"  # print(print_row)

    print_row = ' ' * (largest_int_width + 2)
    for ix in range(len(size_list)):
        print_row += str(second_digit[ix]) + " "
    board_image += print_row + "\n"  # print(print_row)
    board_image += "\n"  # print()

    for i, row in enumerate(board):
        int_width = get_int_width(i)
        blank_spaces = largest_int_width - int_width
        print_row = ''
        for b_s in range(blank_spaces):
            print_row += " "
        print_row += str(i) + " " * 2

        for element in row:
            if not element:
                print_row += empty + ' '
            else:
                print_row += element + ' '
        board_image += print_row + "\n"  # print(print_row)
    return board_image


if __name__ == "__main__":
    # Initialize
    player = 'b'
    b_size = 19
    g = Game(b_size)

    # Test Moves

    for _ in range(100):
        open_spaces = []
        for i in range(len(g.board)):
            for j in range(len(g.board)):
                if not g.board[i][j]:
                    open_spaces.append((i, j))

        chosen = choice(open_spaces)
        g.play(chosen, player)
        player = switch_color(player)

    print(render_board(g.board, "."))
    print("captures: ", g.captures)
    print("rules: ", g.rules)
