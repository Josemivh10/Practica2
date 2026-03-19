import threading
import time
class Game:
    def __init__(self, game_id):
        self.game_id = game_id

        # jugadores
        self.players = []
        # sockets asociados a jugadores
        self.player_sockets = {}
        # estado partida
        self.state = "waiting"  # waiting, playing, finished
        # letra actual
        self.letter = None
        # tiempo
        self.start_time = None
        self.time_limit = 60  # segundos
        # lock concurrencia
        self.lock = threading.Lock()
        # tablero
        self.board = self.init_board()
    def init_board(self):
        categories = ["Marca", "Comida", "Lugar", "Animal"]
        board = {}
        for cat in categories:
            board[cat] = {
                "word": "",
                "locked_by": None,
                "locked_until": 0
            }
        return board
    def add_player(self, player_name):
        with self.lock:
            if player_name not in self.players:
                self.players.append(player_name)
                return True
            return False
    def remove_player(self, player_name):
        with self.lock:
            if player_name in self.players:
                self.players.remove(player_name)
            if player_name in self.player_sockets:
                del self.player_sockets[player_name]
