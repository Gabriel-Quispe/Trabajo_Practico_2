import os
import filtro
import genius
import wordcloud

from tekore import Spotify
from constantes.constantes import SPOTIFY, LISTA_OPCIONES
from exportar_playlist import exportar_playlist
from plataformas.spotify.crud import listar_playlist_en_spotify, crear_playlist_en_spotify, buscar_cancion_en_spotify, insertar_cancion_en_playlist_spotify, \
    seleccionar_playlists_spotify, buscar_spotify

from plataformas.youtube.crud import listar_playlist_en_youtube
from playlist.playlist import buscar_playlist
from sincronizar import sincronizar_spotify
from validar.input_platataforma import validar_input, validar_input_cancion, validar_input_titulo_playlist
from vistas.vista import imprtimir_menu, imprimir_lista_playlist, linea_divisora, imprimir_titulos_playlist


def menu_spotify(spotify: Spotify, youtube: any) -> None:
    iterable: int = 0
    volver: str
    nombre_playlist: str

    while iterable == 0:
        os.system("clear")
        imprtimir_menu(SPOTIFY)
        opcion: str = validar_input(LISTA_OPCIONES, "el numero de opcion")

        if opcion == LISTA_OPCIONES[0]:
            os.system("clear")
            print("Cargando playlist ................................")
            imprimir_lista_playlist(listar_playlist_en_spotify(spotify))
            volver = input("Escribir v para regresar al manu: ")

        elif opcion == LISTA_OPCIONES[1]:
            os.system("clear")
            nombre_playlist = input("Ingresar el nombre de la playlist: ")
            playlist_creada: dict = crear_playlist_en_spotify(spotify, nombre_playlist)
            linea_divisora()
            agregar_canciones_playlist(spotify, playlist_creada["id"])
            volver = input("Escribir v para regresar al manu: ")

        elif opcion == LISTA_OPCIONES[2]:

            os.system("cls")

            nueva_track = buscar_spotify(spotify)
            canal, cancion = filtro.filtrar_palabras_titulo(nueva_track.artists[0].name, nueva_track.name)

            playlist_agregar = seleccionar_playlists_spotify(spotify)
            insertar_cancion_en_playlist_spotify(spotify, playlist_agregar.id, nueva_track)
            print(f"canal: {canal}   cancion:{cancion}")
            letra = genius.genius_total(canal, cancion, True)

            # letra = borrar_comentario(letra)

            os.system("cls")
            print(letra)

            volver = input("Escribir v para regresar al manu: ")

        elif opcion == LISTA_OPCIONES[3]:
            os.system("cls")
            repes = {}
            playlist_seleccionada = seleccionar_playlists_spotify(spotify)

            print("Esto puede tradar.......")
            for j in range(spotify.playlist_items(playlist_seleccionada.id).total):
                canal = spotify.playlist_items(playlist_seleccionada.id).items[j].track.artists[0].name
                cancion = spotify.playlist_items(playlist_seleccionada.id).items[j].track.name
                canal, cancion = filtro.filtrar_palabras_titulo(canal, cancion)

                letra = genius.genius_total(canal, cancion, False)
                filtro.diccionario_de_palabras(repes, letra)

                os.system("cls")
                print(f"letras calculadas {j} / {spotify.playlist_items(playlist_seleccionada.id).total}")

            dic_a_lista: list = filtro.convertir_diccionario(repes)
            if (dic_a_lista == None):
                print("No se pudo encontrar ninguna letra en la playlist")
                return
            lista_cloud = []
            for i in range(len(dic_a_lista)):
                lista_cloud.append(str(dic_a_lista[i][0]))

            text = " ".join(lista_cloud)
            # borra las palabras comunes como articulos y pronombres
            wordcloud2 = wordcloud.WordCloud(stopwords=None, max_words=10).generate(text)
            wordcloud2.to_file("cloud.png")

            volver = input("Escribir v para regresar al manu: ")

        elif opcion == LISTA_OPCIONES[4]:
            os.system("clear")
            print(" Lista de PlayList ")
            print("------------------------------")
            print()

            lista_playlist_spotify: list = listar_playlist_en_spotify(spotify)
            lista_playlist_youtube: list = listar_playlist_en_youtube(youtube)
            imprimir_titulos_playlist(lista_playlist_spotify)
            print()
            print("------------------------------")
            nombre_playlist: str = validar_input_titulo_playlist(lista_playlist_spotify)
            sincronizar_spotify.sincronizar_playlist(nombre_playlist, lista_playlist_spotify, lista_playlist_youtube,
                                                     youtube)
            volver = input("Escribir v para regresar al manu: ")

        elif opcion == LISTA_OPCIONES[5]:
            os.system("clear")
            print(" Lista de PlayList ")
            print("------------------------------")
            print()
            lista_playlist_csv: list = listar_playlist_en_spotify(spotify)
            imprimir_titulos_playlist(lista_playlist_csv)
            print()
            nombre_de_la_playlist: str = validar_input_titulo_playlist(lista_playlist_csv)
            playlist: dict = buscar_playlist(nombre_de_la_playlist, lista_playlist_csv)
            exportar_playlist.exportar(playlist, 'spotify')

            volver = input("Escribir v para regresar al manu: ")

        elif opcion == LISTA_OPCIONES[6]:
            iterable = -1


def agregar_canciones_playlist(spotify: Spotify, id_playlist: str) -> None:
    contador: int = 0
    print("Agregar canciones en la playlist")
    print()
    while contador != -1:

        nombre_cancion: str = validar_input_cancion()

        if nombre_cancion != "-1":
            uri_cancion: any = buscar_cancion_en_spotify(spotify, nombre_cancion)

            while uri_cancion == -1:
                print("La cancion no existe ")
                nombre_cancion: str = validar_input_cancion()
                uri_cancion = buscar_cancion_en_spotify(spotify, nombre_cancion)

            insertar_cancion_en_playlist_spotify(spotify, id_playlist, uri_cancion)
            print("Ingresar -1 para terminar de agregar canciones")
            print()
        else:
            contador = -1
