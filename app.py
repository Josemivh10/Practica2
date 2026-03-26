from bottle import get, post, run
from juego import Partida

partidas = {}
siguiente_id = 8000

@post('/stop/nueva')
def nueva_partida():
    global siguiente_id
    id_partida = str(siguiente_id)
    siguiente_id += 1
    partida = Partida(id_partida)
    partidas[id_partida] = partida
    return {
        "id_partida": id_partida,
        "estado": "creada"
    }

@get('/stop/<id_partida>')
def obtener_partida(id_partida):
    if id_partida in partidas:
        return partidas[id_partida].a_diccionario()
    return {"error": "Partida no encontrada"}


@post('/stop/<id_partida>/join/<jugador>')
def unir_jugador(id_partida, jugador):
    if id_partida not in partidas:
        return {"error": "Partida no encontrada"}
    ok = partidas[id_partida].anadir_jugador(jugador)
    if ok:
        return {
            "estado": "jugador anadido",
            "jugador": jugador
        }
    return {"error": "Jugador repetido"}

@post('/stop/<id_partida>/start')
def iniciar_partida(id_partida):
    if id_partida not in partidas:
        return {"error": "Partida no encontrada"}
    ok = partidas[id_partida].iniciar_partida()
    if ok:
        return {
            "estado": "partida iniciada",
            "letra": partidas[id_partida].letra
        }
    return {"error": "No se puede iniciar la partida"}

@post('/stop/<id_partida>/bloquear/<categoria>/<jugador>')
def bloquear_categoria(id_partida, categoria, jugador):
    if id_partida not in partidas:
        return {"error": "Partida no encontrada"}
    ok = partidas[id_partida].bloquear_categoria(categoria, jugador)
    if ok:
        return {
            "estado": "categoria bloqueada",
            "categoria": categoria,
            "jugador": jugador
        }
    return {"error": "No se pudo bloquear la categoria"}

@post('/stop/<id_partida>/enviar/<categoria>/<jugador>/<palabra>')
def enviar_palabra(id_partida, categoria, jugador, palabra):
    if id_partida not in partidas:
        return {"error": "Partida no encontrada"}
    ok = partidas[id_partida].enviar_palabra(categoria, jugador, palabra)
    if ok:
        if partidas[id_partida].tablero_completo():
            partidas[id_partida].finalizar_partida()
            return {
                "estado": "palabra enviada y partida finalizada",
                "categoria": categoria,
                "jugador": jugador,
                "palabra": palabra
            }
        return {
            "estado": "palabra enviada",
            "categoria": categoria,
            "jugador": jugador,
            "palabra": palabra
        }
    return {"error": "No se pudo enviar la palabra"}

run(host='0.0.0.0', port=8080, debug=False, reloader=False)
