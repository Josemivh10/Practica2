from bottle import route, run
from juego import Game
partidas = {}
siguiente_id = 8000
@route('/stop/nueva')
def nueva_partida():
    global siguiente_id
    id_partida = str(siguiente_id)
    siguiente_id += 1
    partida = Game(id_partida)
    partidas[id_partida] = partida
    return {
        "id_partida": id_partida,
        "estado": "creada"
    }
@route('/stop/<id_partida>')
def obtener_partida(id_partida):
    if id_partida in partidas:
        return partidas[id_partida].to_dict()
    return {"error": "Partida no encontrada"}
run(host='0.0.0.0', port=8080, debug=False, reloader=False)
