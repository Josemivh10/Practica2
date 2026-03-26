import threading
import time
import random

class Partida:
    def __init__(self, id_partida):
        self.id_partida = id_partida
        # jugadores
        self.jugadores = []
        # sockets asociados a jugadores
        self.sockets_jugadores = {}
        # estado de la partida
        self.estado = "waiting"   # waiting, playing, finished
        # letra actual
        self.letra = None
        # tiempo
        self.tiempo_inicio = None
        self.tiempo_limite = 60
        # lock para concurrencia
        self.lock = threading.Lock()
        # tablero
        self.tablero = self.inicializar_tablero()

    def inicializar_tablero(self):
        categorias = ["Marca", "Comida", "Lugar", "Animal"]
        tablero = {}
        for cat in categorias:
            tablero[cat] = {
                "palabra": "",
                "bloqueado_por": None,
                "bloqueado_hasta": 0
            }
        return tablero

    def anadir_jugador(self, nombre_jugador):
        with self.lock:
            if nombre_jugador not in self.jugadores:
                self.jugadores.append(nombre_jugador)
                return True
            return False

    def eliminar_jugador(self, nombre_jugador):
        with self.lock:
            if nombre_jugador in self.jugadores:
                self.jugadores.remove(nombre_jugador)
            if nombre_jugador in self.sockets_jugadores:
                del self.sockets_jugadores[nombre_jugador]

    def iniciar_partida(self):
        with self.lock:
            if self.estado == "waiting" and len(self.jugadores) > 0:
                self.estado = "playing"
                self.letra = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
                self.tiempo_inicio = time.time()
                self.tablero = self.inicializar_tablero()
                return True
            return False

    def tiempo_agotado(self):
        with self.lock:
            if self.tiempo_inicio is None:
                return False
            return (time.time() - self.tiempo_inicio) >= self.tiempo_limite

    def bloquear_categoria(self, categoria, nombre_jugador, segundos=10):
        with self.lock:
            if self.estado != "playing":
                return False
            if categoria not in self.tablero:
                return False
            if self.tablero[categoria]["palabra"] != "":
                return False
            ahora = time.time()
            bloqueado_hasta = self.tablero[categoria]["bloqueado_hasta"]
            if bloqueado_hasta > ahora and self.tablero[categoria]["bloqueado_por"] != nombre_jugador:
                return False
            self.tablero[categoria]["bloqueado_por"] = nombre_jugador
            self.tablero[categoria]["bloqueado_hasta"] = ahora + segundos
            return True

    def enviar_palabra(self, categoria, nombre_jugador, palabra):
        with self.lock:
            if self.estado != "playing":
                return False
            if categoria not in self.tablero:
                return False
            if self.tablero[categoria]["bloqueado_por"] != nombre_jugador:
                return False
            if not palabra or palabra[0].upper() != self.letra:
                return False
            self.tablero[categoria]["palabra"] = palabra
            self.tablero[categoria]["bloqueado_por"] = None
            self.tablero[categoria]["bloqueado_hasta"] = 0
            return True

    def tablero_completo(self):
        with self.lock:
            for categoria in self.tablero:
                if self.tablero[categoria]["palabra"] == "":
                    return False
            return True

    def finalizar_partida(self):
        with self.lock:
            self.estado = "finished"

    def a_diccionario(self):
        with self.lock:
            return {
                "id_partida": self.id_partida,
                "jugadores": self.jugadores.copy(),
                "estado": self.estado,
                "letra": self.letra,
                "tiempo_inicio": self.tiempo_inicio,
                "tiempo_limite": self.tiempo_limite,
                "tablero": self.tablero.copy()
            }
        
