def definir_playlist() -> dict:
    """
        Precondicion:
        Postcondicion: devuelve un diccionario del tipo playlist con sus propiedades sin datos
    """
    playlist: dict = {
        "id": "",
        "nombre_playlist": "",
        "creador_playlist": "",
        "tipo_playlist": False,
        "descripcion": "",
        "url": "",
        "cantidad_canciones": 0,
        "duracion_playlist": 0,
        "lista_canciones": [],
        "listar_artistas": []
    }
    return playlist


def buscar_playlist(nombre_playlist: str, lista_playlist) -> dict:
    """
    Precondicion: Recibir el nombre de una playlist y una lista de playlist
    Postcondicion: Devuelve un dictionario del tipo playlist con sus propiedades con datos
  """

    playlist: dict = definir_playlist()

    for i in range(len(lista_playlist)):
        if (lista_playlist[i]["nombre_playlist"] == nombre_playlist):
            playlist = lista_playlist[i]
            return playlist
    return playlist


def esta_presente_playlist_en_la_lista(nombre_playlist: str, lista_playlist: list) -> bool:
    """
    Precondicion: Recibir el nombre de una playlist y una lista de playlist
    Postcondicion: Devulve True si existe la plyalist en la lista caso contrario devuelve false
  """
    for i in range(len(lista_playlist)):
        if (lista_playlist[i]["nombre_playlist"] == nombre_playlist):
            return True

    return False


def esta_presente_la_cancion_en_la_playlist(nombre_cancion, lista_canciones: list) -> bool:
    for cancion in lista_canciones:
        if cancion.find(nombre_cancion):
            return True
    return False
