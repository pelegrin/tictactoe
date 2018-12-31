import random
import sys


class TicTacToe:
    def print_board(self):
        print('-------------')
        for y in range(3):
            bx = ''
            for x in range(3):
                r = y * 3
                v = self.board[r + x] if self.board[r + x] != '' else '   '
                bx = bx + '|' + v
            bx = bx + '|' + '\n' + '-------------'
            print(bx)

    # Return player score first/machine second
    def play(self):
        while not self.is_end_game():
            if self.is_user_first:
                self.print_board()
                self.user_move()
                self.print_board()
                if self.is_end_game():
                    break
                self.game_move()
            else:
                self.game_move()
                self.print_board()
                if self.is_end_game():
                    break
                self.user_move()
                self.print_board()
        return self.score

    # Smart move implementation
    def game_move(self):
        print('...thinking...')
        # finishing attack
        wining_weights = self.get_weights(self.game_symbol)
        defending_weights = self.get_weights(self.player_symbol)
        for w in wining_weights:
            if len(w) == 2:
                marked_position = get_next_index(w)
                if self.board[marked_position] != self.empty_symbol:
                    continue
                self.board[marked_position] = self.game_symbol
                return
        # defence move
        for w in defending_weights:
            if len(w) == 2:
                marked_position = get_next_index(w)
                if self.board[marked_position] != self.empty_symbol:
                    continue
                self.board[marked_position] = self.game_symbol
                return
        # light attacking move
        for w in wining_weights:
            if len(w) == 1:
                marked_position = get_next_index(w)
                if self.board[marked_position] != self.empty_symbol:
                    continue
                self.board[marked_position] = self.game_symbol
                return
        # useful move
        empty_index = []
        for i in range(len(self.board)):
            if self.board[i] == '':
                empty_index.append(i)
        if len(empty_index) == 0:
            print("Draw!")
            return
        preferred = []
        for i in preferred_index():
            if i in empty_index:
                preferred.append(i)
        if len(preferred) > 0:
            marked_position = random.randint(0, len(preferred) - 1)
            self.board[preferred[marked_position]] = self.game_symbol
        else:
            marked_position = random.randint(0, len(empty_index) - 1)
            self.board[empty_index[marked_position]] = self.game_symbol

    def is_end_game(self):
        if self.check_win(self.player_symbol):
            self.score = [1, 0]
            return True
        if self.check_win(self.game_symbol):
            self.score = [0, 1]
            return True
        if self.check_draw():
            return True
        return False

    def check_win(self, mark):
        for w in self.get_weights(mark):
            if len(w) == 3:
                return True
        return False

    def get_weights(self, mark):
        basket = ([], [], [], [], [], [], [], [])
        for i in range(len(self.board)):
            if self.board[i] == mark:
                pos = 0
                for one_basket in winning_basket():
                    if i in one_basket:
                        basket[pos].append(i)
                    pos += 1
        return basket

    def check_draw(self):
        empty_index = []
        for i in range(len(self.board)):
            if self.board[i] == '':
                empty_index.append(i)
        return True if len(empty_index) == 0 else False

    def user_move(self):
        marked_position = checked_user_move()
        while not self.board[marked_position] == '':
            print('Already marked! Enter different row and column!')
            self.print_board()
            marked_position = checked_user_move()
        self.board[marked_position] = self.player_symbol

    def __init__(self, question, player_symbol, game_symbol, is_user_first):
        self.player_symbol = player_symbol
        self.game_symbol = game_symbol
        self.question = question
        self.empty_symbol = ''
        self.is_user_first = is_user_first
        self.score = [0, 0]
        self.board = ['', '', '', '', '', '', '', '', '']


def get_next_index(w: list):
    small_list = set(w)
    for wb in winning_basket():
        winning_set = set(wb)
        if small_list.issubset(winning_set):
            remaining_set = winning_set - small_list
            for i in remaining_set:
                return i


def winning_basket():
    return [0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]


def preferred_index():
    return [0, 2, 4, 6, 8]


def checked_user_move():
    print("Your move!")
    row = input('Enter row (from 1 to 3)? ')
    while not check_input(row):
        print("Enter again...(from 1 to 3 only) ")
        row = input()
    col = input('Enter column (from 1 to 3)? ')
    while not check_input(col):
        print("Enter again...(from 1 to 3 only) ")
        col = input()
    r = (int(row) - 1) * 3
    c = int(col) - 1
    return r + c


def is_user_answers_yes(q):
    not_recognised = True
    ans = ''
    while not_recognised:
        ans = input(q)
        not_recognised = False if (ans == 'Y' or ans == 'n') else True
        if not_recognised:
            print('Pardon?!')
    return True if ans == 'Y' else False


def check_input(i):
    return True if i == '1' or i == '2' or i == '3' else False


question = 'Would you like to play? (Y/n)'
# Player/Machine
game_score = [0, 0]
draw_score = [0, 0]

while True:
    if not is_user_answers_yes(question):
        print('Bye. Have a good game next time!')
        sys.exit(0)
    is_user_first = is_user_answers_yes('Would you like to play first ? (Y/n)')
    if is_user_first:
        game_symbol = ' 0 '
        player_symbol = ' X '
    else:
        game_symbol = ' X '
        player_symbol = ' 0 '
    game = TicTacToe(question, player_symbol, game_symbol, is_user_first)
    score = game.play()
    if score == draw_score:
        print("Draw")
    if score[0] == 1:
        print("Player won")
    if score[1] == 1:
        print("Machine won")
    game_score[0] += score[0]
    game_score[1] += score[1]
    print("Score: Player " + str(game_score[0]) + " / " + str(game_score[1]) + " Machine")
    question = 'Would you like to play again? (Y/n)'
