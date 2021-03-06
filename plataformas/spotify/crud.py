import os

from tekore import Spotify
from tekore._model import SimplePlaylist

from playlist.playlist import definir_playlist


def listar_playlist_en_spotify(spotify: Spotify) -> list:
    """
        Precondicion: Tener acceso al servicio
        Poscondicion: retorna una la lista de playlist
    """
    lista_playlist: list = []
    try:
        spotify_playlist: list = spotify.playlists(spotify.current_user().id).items
        for i in range(len(spotify_playlist)):

            playlist: dict = definir_playlist()
            playlist["id"] = spotify_playlist[i].id
            playlist["nombre_playlist"] = spotify_playlist[i].name
            playlist["descripcion"] = spotify_playlist[i].description
            playlist["creador_playlist"] = spotify_playlist[i].owner.display_name
            playlist["tipo_playlist"] = spotify_playlist[i].public
            playlist["url"] = spotify_playlist[i].owner.external_urls["spotify"]

            playlist_total: int = spotify.playlist_items(spotify.playlists(spotify.current_user().id).items[i].id).total
            for j in range(playlist_total):
                playlist["lista_canciones"].append(
                    spotify.playlist_items(spotify.playlists(spotify.current_user().id).items[i].id).items[j].track.name)

            playlist["cantidad_canciones"] = len(playlist["lista_canciones"])
            lista_playlist.append(playlist)
        return lista_playlist
    except:
        print("Spotify no responde")
        return lista_playlist



# Pre: hace falta que max sea un int
# Post: Le pide al usuario que ingrese un numero dentre 0 y el maximo dado
#	   luego, una vez que esté  dentro del rango devuelve ese numero
def pedir_centinela_int(max: int) -> int:
    centinela: int = input("Seleccione: ")
    validar: bool = True
    while (validar == True):
        if (centinela.isdecimal() == True):
            if (int(centinela) < 0 and int(centinela) > max):
                validar = False
        if (validar == True):
            centinela = input("ERROR: Seleccione nuevamente: ")

    return int(centinela)


# Pre: requiere que ya esté logueado en spotify
# Post: le muestra al usuario todas las playlists que tiene y le da a elejir cual seleccionar, luego la devuelve
def seleccionar_playlists_spotify(spotify: Spotify) -> SimplePlaylist:
    print(f"Playlists en spotify de {spotify.user(spotify.current_user().id).display_name}:")
    for i in range(spotify.playlists(spotify.current_user().id).total):
        print(f" {i} - {spotify.playlists(spotify.current_user().id).items[i].name}")

    centinela: int = pedir_centinela_int(spotify.playlists(spotify.current_user().id).total)
    # devuelvo el objeto entero despues se ulitiza .id .name .uri etc
    return spotify.playlists(spotify.current_user().id).items[centinela]


def crear_playlist_en_spotify(spotify: Spotify, nombre_playlist: str) -> dict:
    """
    Precondicion: Inicializar el objeto spotify y tener el nombre de la playlist que quiere crear
    Poscondicion: devuleve un diccionario del tipo playlist
    """
    playlist: dict = definir_playlist()
    playlist["id"] = spotify.playlist_create(spotify.current_user().id, nombre_playlist, public=True,
                                             description="musica").id
    return playlist


def buscar_cancion_en_spotify(spotify: Spotify, cancion: str) -> any :
    """
        Precondicion: Inicializar el objeto spotify y tener el  nombre de la playlist que quiere buscar
        Poscondicion: Devuelve la lista de url
    """
    RANGO_CANCIONES: int = 5
    track = spotify.search(cancion)
    uri_cancion: any

    if len(track[0].items) == 0:
        return -1
    else:
        for i in range(RANGO_CANCIONES):
            cancion_nombre: str = track[0].items[i].name
            if cancion_nombre.find(cancion) != -1:
                uri_cancion = track[0].items[i]
                return uri_cancion


def buscar_spotify(spotify: Spotify):
    rango_busqueda: int = 5
    buscador: str = input("ingrese que cancion quiere buscar: ")
    track: tuple = spotify.search(buscador)
    # track es una lista de los resultados devueltos por el search, oredeando por que tanto se asemeja la palabra clave
    if (len(track[0].items) == 0):
        print("no se encontro resultado")

    else:
        print("==========================================")
        for i in range(rango_busqueda):
            cancion: str = track[0].items[i].name
            artista: str = track[0].items[i].artists[0].name
            album: str = track[0].items[i].album.name
            print(f" {i} - nombre: {cancion}, artista: {artista}, album: {album}")

        print("==========================================")
        centinela: int = pedir_centinela_int(rango_busqueda)
        os.system("cls")

    # al momento de añadir la cancion a la playlist tiene que ser una lista
    return track[0].items[centinela]


def insertar_cancion_en_playlist_spotify(spotify: Spotify, id_playlist: str, url_cancion: list) -> None:
    """
        Precondicion: Inicializar el objeto spotify, id de la playlist y url de la cancion que se desea agregar
        Poscondicion: None
    """
    spotify.playlist_add(id_playlist, [url_cancion.uri])
