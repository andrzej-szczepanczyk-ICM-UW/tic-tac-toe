import abc


PLAYER1 = "X"
PLAYER2 = "O"
EMPTY = "-"
SIZE = 3


# MODEL GRY

# LOGIKA GRY

# WYŚWIETLANIE

# INTERAKCJA Z UŻYTKOWNIKIEM
 
# KOD, KTÓRY URUCHAMIA GRĘ

#pycharm - skroty
#Ctrl+Shift+MINUS
#Ctrl+Shift+PLUS


def wyswietl(plansza):
    for linia in plansza:
        for pole in linia:
            print(pole, ", ", end='')
        print()
    print()


# utworz_plansze
def rozpocznij(SIZE):
    result = []
    for _ in range(SIZE):
        row = [EMPTY] * SIZE  # <-- OK
        result.append(row)
    return result


def set_board_value(plansza, położenie, player):
    x = położenie[0]
    y = położenie[1]
    plansza[x][y] = player


# def utworz_historie():
#   return []


def get_valid_number(message):
    while True:
        try:
            return int(input(message))
        except ValueError:
            print('podaj jeszcze raz')


def get_valid_number_from_range(message, from_value, to_value):
    while True:
        number = get_valid_number(message)
        if from_value <= number <= to_value:
            return number
        else:
            print('Wymagana liczba od {} do {}'.format(from_value, to_value))


def is_free_position(board, position):
    row, col = position
    return board[row][col] == EMPTY


USER_MIN_VALUE = 1
USER_MAX_VALUE = 9


def make_position(human_number, size):
    index = human_number - 1
    return [index // size, index % size]


def get_position(message, board):
    while True:
        human_number = get_valid_number_from_range(
            message, from_value=USER_MIN_VALUE, to_value=USER_MAX_VALUE)

        position = make_position(human_number, size=len(board))
        if is_free_position(board, position):
            return position
        print('To jest pole jest już zajęte')


# def pobierz_położenie(plansza):
#     while True:
#         try:
#             number = int(input())
#         except ValueError:
#             print('podaj jeszcze raz')
#             continue

#         if not (number<1 or number>9):
#             print('podaj jeszcze raz')
#             continue

#         # number = number - 1 # !!!
#         index = number - 1
#         położenie = [index // 3, index %3] # <--

#         if plansza[położenie[0], położenie[1]] == puste:
#             return położenie


def make_queue():
    return [PLAYER1, PLAYER2]


def update_queue(queue):
    first, second = queue
    queue[0] = second
    queue[1] = first


def make_game(user):
    return {
        'board': rozpocznij(SIZE),
        'queue': make_queue(),
        'running': True,
        'user': user,
        'history': []
    }


def get_player(game):
    return game['queue'][0]


def has_free_field(board):
    for row in board:
        if EMPTY in row:
            return True
    return False



def has_line(board, symbol):
    def horizontal(n):
        if (board[n][0] == symbol and board[n][1] == symbol and board[n][2] == symbol):
            return True
        else:
            return False

    def vertical(n):
        if (board[0][n] == symbol and board[1][n] == symbol and board[2][n] == symbol):
            return True
        else:
            return False

    def cross1():
        if (board[0][0] == symbol and board[1][1] == symbol and board[2][2] == symbol):
            return True
        else:
            return False

    def cross2():
        if (board[0][2] == symbol and board[1][1] == symbol and board[2][0] == symbol):
            return True
        else:
            return False

    answer = horizontal(0) or horizontal(1) or horizontal(2) or vertical(0) or vertical(1) or vertical(2) or\
        cross1() or cross2()

    return answer


def is_end(game):
    return (
            not has_free_field(game['board']) or
            has_line(game['board'], get_player(game))
    )


def update_game(game):
    wyswietl(game['board'])

    print('Ruch wykonuje', get_player(game))  # <---
    position = game['user'].get_position('Podaj pozycję ', game['board'])
    set_board_value(game['board'], position, get_player(game))
    
    # update_history(game['history'], position)
    game['history'].append(position)

    game['running'] = not is_end(game)

    if not game['running']:
        print("KONIEC GRY!! Wygrał gracz ", get_player(game))
        wyswietl(game['board'])

    update_queue(game['queue'])

ANSWER_YES = "y"
ANSWER_NO = "n"

def is_answer(s):
    return s in [ANSWER_YES, ANSWER_NO]

def ask_for_history():
    while True:
        print("czy chcesz odtworzyć grę ?? [y/n]")
        line = input() # 
        answer = line.lower().strip()
        if is_answer(answer):
            return answer == ANSWER_YES

def run_game(game):
    while game['running']:
        update_game(game)


class BaseUser(abc.ABC):

    @abc.abstractmethod
    def get_position(self, message, board):
        pass


class RealUser(BaseUser):

    def get_position(self, message, board):
        return get_position(message, board)


class DevUser(BaseUser):

    def __init__(self, seq):
        self.seq = seq
        self.index = 0 if seq else -1

    def get_position(self, message, board):
        if self.index < len(self.seq):
            value = self.seq[self.index]
            self.index += 1
            return make_position(int(value), size=len(board))
        raise Exception('Illegal state')


# TODO:
# dopisz klasę użytkownika pod historię (żeby obsługiwał kliknięcie)

# TODO: 
# napisz testy do najważniejszych fragmentów kodu

#pogrupowa : logika, developerski, wywietlanie, interakcja 
        
def display_hist(game):
    print("hidtoria gry")
    print(str(game['history']))

def main():
    #user = DevUser(['1', '6', '2', '9', '3'])
    user = RealUser()
    game = make_game(user)
    run_game(game)

    display_hist(game) # Pokazywanie na potrzeby developerskie
    answer = ask_for_history() 

    if answer == ANSWER_YES:
        hist_user = DevUser(game['history'])  # <-- BRAWO!
        hist_game = make_game(hist_user)
        run_game(hist_game)

    # for _ in range(5):
    # print(user.get_position())


# UNCOMMENT:
# main()

# Bibliotka: requests

# requests.get('')

# I) OBSŁUGA HISTORII:
# po grze pada pytanie do użytkownika
# czy chce odtworzyć tą historię

# II) Gra na większej planszy

# Na kolejnym spotkaniu ruszamy testy.

# indeksy mamy od zero

# to co człowiek widzi to on liczy od 1

# 0, 0 -> 1


# 1, 1 (gdy size 3) -> 5

# row,col



def make_human_position(position, size):
    row, col = position
    return row * size + col + 1
        
# tests.py

import unittest


class HumanPositionTests(unittest.TestCase):
    
    def test_when_size_equals_1(self):
        self._run_mini_tests(size=1)
    
    def test_when_size_equals_2(self):
        self._run_mini_tests(size=2)
    
    def test_when_size_equals_3(self):
        self._run_mini_tests(size=3)
    
    def _run_mini_tests(self, size):
        last_number = size * size   
        for number in range(1, last_number + 1):
            pos = make_position(number, size)
            human_pos = make_human_position(pos, size)
            self.assertEquals(number, human_pos, 'when size={}'.format(size))
            
unittest.main()

