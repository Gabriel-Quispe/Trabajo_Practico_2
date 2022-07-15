from plataformas.spotify.crud import buscar_cancion_en_spotify, crear_playlist_en_spotify, listar_playlist_en_spotify, \
    insertar_cancion_en_playlist_spotify
from playlist.playlist import buscar_playlist, esta_presente_playlist_en_la_lista, \
    esta_presente_la_cancion_en_la_playlist


def sincronizar_playlist(nombre_playlist: str, lista_playlist_spotify: list, lista_playlist_youtube: list,
                         spotify: any) -> None:
    """
        Precondicion: Recibir una nombre de la plyalist, lista_playlist y la plataforma con la se quiere sincronizar
        PostCondicion:
    """
    archivo = open("../csv/canciones/{1}/{0}.csv".format("cancionesNoExistenEnSpotify", 'youtube'), "w", newline="")
    playlist_youtube: dict = buscar_playlist(nombre_playlist, lista_playlist_youtube)
    playlist_spotify: dict = buscar_playlist(nombre_playlist, listar_playlist_en_spotify(spotify))

    if not esta_presente_playlist_en_la_lista(nombre_playlist, lista_playlist_spotify):

        crear_playlist_en_spotify(spotify, nombre_playlist)
        for cancion in playlist_youtube["lista_canciones"]:
            url_cancion = buscar_cancion_en_spotify(spotify, cancion)
            if url_cancion != -1:
                insertar_cancion_en_playlist_spotify(spotify, playlist_spotify['id'], url_cancion)
            else:
                archivo.write(cancion)

    else:
        if len(playlist_spotify["lista_canciones"]) == 0:
            for cancion in playlist_youtube["lista_canciones"]:
                url_cancion = buscar_cancion_en_spotify(spotify, cancion)
                if url_cancion != -1:
                    insertar_cancion_en_playlist_spotify(spotify, playlist_spotify['id'], url_cancion)
                else:
                    archivo.write(cancion)
        else:
            for cancion_youtube in playlist_youtube["lista_canciones"]:
                if not esta_presente_la_cancion_en_la_playlist(cancion_youtube, playlist_spotify["lista_canciones"]):
                    id = buscar_cancion_en_spotify(spotify, cancion_youtube)
                    if id != -1:
                        insertar_cancion_en_playlist_spotify(spotify, playlist_spotify['id'], id)
                    else:
                        archivo.write(cancion_youtube)

    archivo.close()
