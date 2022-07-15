import os

from playlist.playlist import definir_playlist


def Listar_Playlist_Youtube(youtube: 'googleapiclient.discovery.Resource') -> None:
    """
    Precondicion: Tener acceso al servicio y tener alguna playlist
    Poscondicion: None
    """

    # Obtiene la informacion de todas las playlist del usuario
    Info_playlist = youtube.playlists().list(part="snippet", mine=True).execute()

    # Ingresa a las playlist
    for playlists in range(len(Info_playlist['items'])):

        # Imprime su titulo
        print(Info_playlist['items'][playlists]['snippet']['title'])

        # Obtiene los datos que contiene la playlist
        Datos_playlist = youtube.playlistItems().list(part="snippet",
                                                      playlistId=Info_playlist['items'][playlists]['id'],
                                                      maxResults=50).execute()

        for j in range(Datos_playlist['pageInfo']['totalResults']):
            # Imprime su titulo
            print(f"	{Datos_playlist['items'][j]['snippet']['title']}")

        print("-------------------------------")


def listar_playlist_en_youtube(youtube: 'googleapiclient.discovery.Resource') -> list:
    """
        Precondicion: Tener acceso al servicio y tener alguna playlist
        Poscondicion: Devuelve una lista de playlist
    """

    # Obtiene la informacion de todas las playlist del usuario
    info_playlist: any = youtube.playlists().list(part="snippet", mine=True).execute()
    lista_playlist: list = []

    # Ingresa a las playlist
    for playlists in range(len(info_playlist['items'])):

        playlist: dict = definir_playlist()
        playlist["id"] = info_playlist['items'][playlists]['id']
        playlist["nombre_playlist"] = info_playlist['items'][playlists]['snippet']['title']
        playlist["descripcion"] = info_playlist['items'][playlists]['snippet']['description']

        datos_playlist = youtube.playlistItems().list(part="snippet",
                                                      playlistId=info_playlist['items'][playlists]['id'],
                                                      maxResults=50).execute()

        for j in range(datos_playlist['pageInfo']['totalResults']):
            playlist["lista_canciones"].append(datos_playlist['items'][j]['snippet']['title'])

        playlist["cantidad_canciones"] = len(playlist["lista_canciones"])
        lista_playlist.append(playlist)

    return lista_playlist


def crear_playlist_en_youtube(youtube: 'googleapiclient.discovery.Resource', nombre_playlist: str) -> None:
    """
        Precondicion: Tener acceso al servicio
        Poscondicion: None
    """
    print("Ingrese alguna Descripcion:")
    descripcion: str = input("")

    youtube.playlists().insert(part="snippet", body=dict(snippet=dict(title=nombre_playlist, description=descripcion))).execute()


def Crear_Playlist_Youtube(youtube: 'googleapiclient.discovery.Resource') -> None:
    """
    Precondicion: Tener acceso al servicio
    Poscondicion: None
    """

    Nombre = input("Ingrese el Nombre de su Playlists: ")

    print("Ingrese alguna Descripcion:")
    Descripcion = input("")

    # Crea la playlist con los datos dados
    youtube.playlists().insert(part="snippet", body=dict(snippet=dict(title=Nombre, description=Descripcion))).execute()


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


# Pre: requiere que ya esté logueado en youtube
# Post: le muestra al usuario todas las playlists que tiene y le da a elejir cual seleccionar, luego la devuelve
def seleccionar_playlist_youtube(youtube: 'googleapiclient.discovery.Resource'):
    Info_playlist = youtube.playlists().list(part="snippet", mine=True).execute()
    for playlists in range(len(Info_playlist['items'])):
        print(f" {playlists} - {Info_playlist['items'][playlists]['snippet']['title']}")

    centinela: int = pedir_centinela_int(len(Info_playlist['items']))

    return Info_playlist['items'][centinela]


# Pre: requiere que ya esté logueado en youtube
# Post: Pide al usuario una palabra clave y busca en youtube
# 	   imprime los 5 resultados de youtube, le pide al usuario cual desea y devuelve el objeto cancion elejida por el usuario
def buscar_youtube(youtube: 'googleapiclient.discovery.Resource'):
    palabra_clave = input("Ingrese que desea buscar en youtube: ")
    resultado = youtube.search().list(
        part="id,snippet",
        q=palabra_clave,
        maxResults=5
    ).execute()

    print("==========================================")
    for i in range(len(resultado['items'])):
        cancion: str = resultado['items'][i]['snippet']['title']
        canal: str = resultado['items'][i]['snippet']['channelTitle']
        print(f" {i} | {cancion} | {canal}")

    print("==========================================")
    centinela: int = pedir_centinela_int(len(resultado['items']))

    return resultado['items'][centinela]


# Pre: Estar logueado en youtube, el objeto cancion y el objeto playlist
# Post: Agrega la cancion a la playlist
def insertar_en_playlist_youtube(youtube: 'googleapiclient.discovery.Resource', resultado, playlist_seleccionada):
    youtube.playlistItems().insert(part="snippet",
                                   body={
                                       'snippet': {
                                           'playlistId': playlist_seleccionada['id'],
                                           'resourceId': {
                                               'kind': 'youtube#video',
                                               'videoId': resultado['id']['videoId']
                                           }
                                       }
                                   }).execute()


# Pre: requiere que ya esté logueado en youtube
# Post: Devuelve el id de la cancion y de que no coincida con la busqueda devuelve -1
def buscar_cancion_en_youtube(youtube: 'googleapiclient.discovery.Resource', nombre_cancion: str):
    resultado = youtube.search().list(
        part="id,snippet",
        q=nombre_cancion,
        maxResults=5
    ).execute()

    for i in range(len(resultado['items'])):
        nombre_cancion_youtube: str = resultado['items'][i]['snippet']['title']
        if nombre_cancion_youtube.find(nombre_cancion) != -1:
            return resultado['items'][i]['id']['videoId']

    return -1


#
#
def insertar_cancion_en_playlist_youtube(youtube: 'googleapiclient.discovery.Resource', videoId: str, playlist_id) -> None:

    """
        Pre: Estar logueado en youtube, el objeto cancion y el objeto playlist
        Post: None
    """
    youtube.playlistItems().insert(part="snippet",
                                   body={
                                       'snippet': {
                                           'playlistId': playlist_id,
                                           'resourceId': {
                                               'kind': 'youtube#video',
                                               'videoId': videoId,
                                           }
                                       }
                                   }).execute()
