import os

from plataformas.youtube.crud import crear_playlist_en_youtube, buscar_cancion_en_youtube, listar_playlist_en_youtube, \
    insertar_cancion_en_playlist_youtube
from playlist.playlist import buscar_playlist, esta_presente_playlist_en_la_lista, \
    esta_presente_la_cancion_en_la_playlist


def sincronizar_playlist(nombre_playlist: str, lista_playlist_spotify: list, lista_playlist_youtube: list, youtube: any)-> None:
    """
        Precondicion: Recibir una nombre de la plyalist, lista_playlist y la plataforma con la se quiere sincronizar
        PostCondicion:
    """
    archivo = open("../csv/canciones/{1}/{0}.csv".format("cancionesNoExistenEnYoutube", 'spotify'), "w", newline="")

    if not esta_presente_playlist_en_la_lista(nombre_playlist, lista_playlist_youtube):

        crear_playlist_en_youtube(youtube, nombre_playlist)
        playlist_youtube: dict = buscar_playlist(nombre_playlist, listar_playlist_en_youtube(youtube))
        playlist_spotify: dict = buscar_playlist(nombre_playlist, lista_playlist_spotify)

        for cancion in playlist_spotify["lista_canciones"]:
            id_cancion = buscar_cancion_en_youtube(youtube, cancion)
            if id_cancion != -1:
                insertar_cancion_en_playlist_youtube(youtube, id_cancion, playlist_youtube['id'])
            else:
                archivo.write(cancion)

    else:
        playlist_youtube: dict = buscar_playlist(nombre_playlist, listar_playlist_en_youtube(youtube))
        playlist_spotify: dict = buscar_playlist(nombre_playlist, lista_playlist_spotify)
        if len(playlist_youtube["lista_canciones"]) == 0:
            for cancion in playlist_spotify["lista_canciones"]:
                insertar_cancion_en_playlist_youtube(youtube, buscar_cancion_en_youtube(youtube, cancion), playlist_youtube['id'])
        else:
            for cancion_spotify in playlist_spotify["lista_canciones"]:
                if not esta_presente_la_cancion_en_la_playlist(cancion_spotify, playlist_youtube["lista_canciones"]):
                    id = buscar_cancion_en_youtube(youtube, cancion_spotify)
                    if id != -1:
                        insertar_cancion_en_playlist_youtube(youtube, id, playlist_youtube['id'])
                    else:
                        archivo.write(cancion_spotify)

    archivo.close()

