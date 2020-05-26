import abc

PLAYER1 = "X"
PLAYER2 = "O"
EMPTY = "-"
SIZE = 3



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
        row = [EMPTY] * SIZE # <-- OK
        result.append(row) 
    return result
            

def set_board_value(plansza, położenie, player):
    x = położenie[0]
    y = położenie[1]
    plansza[x][y]=player



#def utworz_historie():
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
    index = human_number -1
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
    return (    
        # POZIOME
        (board[0][0] == symbol and board[0][1] == symbol and board[0][2] == symbol) or
        (board[1][0] == symbol and board[1][1] == symbol and board[1][2] == symbol) or
        (board[2][0] == symbol and board[2][1] == symbol and board[2][2] == symbol) or
        # PIONOWE
        (board[0][0] == symbol and board[0][1] == symbol and board[0][2] == symbol) or
        (board[1][0] == symbol and board[1][1] == symbol and board[1][2] == symbol) or
        (board[2][0] == symbol and board[2][1] == symbol and board[2][2] == symbol) or
        # 2 UKOS
        (board[0][0] == symbol and board[1][1] == symbol and board[2][2] == symbol) or
        (board[0][2] == symbol and board[1][1] == symbol and board[2][0] == symbol)
    )


def is_end(game): 
    return (
        not has_free_field(game['board']) or
        has_line(game['board'], get_player(game))
    )
    
    
def update_game(game):
    wyswietl(game['board'])
    
    print('Ruch wykonuje', get_player(game)) # <---
    position = game['user'].get_position('Podaj pozycję ', game['board'])
    set_board_value(game['board'], position, get_player(game)) 
    
    game['running'] = not is_end(game)
    
    if not game['running']:
        print("KONIEC GRY!! Wygrał gracz ", get_player(game))
        wyswietl(game['board'])
    
    update_queue(game['queue'])
    

def ask_for_history():
    print("czy chcesz odtworzyć grę ??")
    answer = input()
    if answer == "y":
        return True
    else:
        return False
    
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
    
def display_hist(game):
    print("hidtoria gry")
    print(str(game['history']))

def main():
    user = DevUser(['1', '6', '2', '9', '3'])
    #user = RealUser()
    game = make_game(user)
    run_game(game)
    
    display_hist(game)
    answer = ask_for_history()
    
    if answer:
        hist_user = DevUser(game['history'])    
        hist_game = make_game(hist_user)
        run_game(hist_game) 
    

# for _ in range(5):
    # print(user.get_position())
    
main()


# Bibliotka: requests

# requests.get('')

# I) OBSŁUGA HISTORII:
# po grze pada pytanie do użytkownika
# czy chce odtworzyć tą historię

# II) Gra na większej planszy

# Na kolejnym spotkaniu ruszamy testy.
