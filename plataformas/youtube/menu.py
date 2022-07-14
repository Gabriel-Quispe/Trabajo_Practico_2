import os
from time import sleep

from tekore import Spotify

from constantes.constantes import YOUTUBE, LISTA_OPCIONES
from plataformas.youtube.crud import listar_playlist_en_youtube, crear_playlist_en_youtube, buscar_cancion_en_youtube, \
    insertar_cancion_en_playlist_youtube
from playlist.playlist import buscar_playlist
from validar.input_platataforma import validar_input, validar_input_cancion
from vistas.vista import imprimir_lista_playlist, imprtimir_menu, linea_divisora


def menu_youtube(spotify: Spotify, youtube: any) -> None:
    iterable: int = 0
    volver: str
    nombre_playlist: str

    while iterable == 0:
        os.system("clear")
        imprtimir_menu(YOUTUBE)
        opcion: str = validar_input(LISTA_OPCIONES, "el numero de opcion")

        if opcion == LISTA_OPCIONES[0]:
            os.system("clear")
            print("Cargando playlist ................................")
            imprimir_lista_playlist(listar_playlist_en_youtube(youtube))
            print()
            volver = input("Escribir v para regresar al manu: ")

        elif opcion == LISTA_OPCIONES[1]:
            os.system("clear")
            nombre_playlist = input("Ingresar el nombre de la playlist: ")
            crear_playlist_en_youtube(youtube, nombre_playlist)
            playlist_youtube: dict = buscar_playlist(nombre_playlist, listar_playlist_en_youtube(youtube))
            linea_divisora()
            agregar_canciones_playlist(youtube, playlist_youtube["id"])
            volver = input("Escribir v para regresar al manu: ")


"""
        while Iterable == 0:
        os.system("cls")
        opcion = str()
        #spotify = SP.Generar_Servicio_Spotify()
        youtube = YT.Generar_Servicios_Youtube()

        while opcion != "1" and opcion != "2" and opcion != "3" and opcion != "4" and opcion != "5" and opcion != "6" and opcion != "Salir" and opcion != "Cambiar" :
            os.system("cls")
            print("Menu de Youtube:")
            imprtimir_menu()
            opcion = input("Ingrese que decea: ")

        if opcion == "1":
            os.system("cls")
            YT.Listar_Playlist_Youtube( youtube )
            return

        elif opcion == "2":
            os.system("cls")

            YT.Crear_Playlist_Youtube( youtube )
            return

        elif opcion =="3":
            palabra = YT.buscar_youtube(youtube)
            playlist_seleccionada = YT.seleccionar_playlist_youtube(youtube)
            YT.insertar_en_playlist_youtube(youtube, palabra, playlist_seleccionada)
            #canal, cancion = filtro.filtrar_palabras_titulo(nueva_track.artists[0].name, nueva_track.name)
            canal, cancion = filtro.filtrar_palabras_titulo(palabra['snippet']['channelTitle'], palabra['snippet']['title'])
            print(f"{canal}   {cancion}")
            letra = genius.genius_total(canal, cancion, True)

            os.system("cls")
            print(letra)
            return

        elif opcion == "4":
            os.system("cls")
            repes = {}
            playlist_seleccionada = YT.seleccionar_playlist_youtube(youtube)
            Datos_playlist = youtube.playlistItems().list( part = "snippet", playlistId = playlist_seleccionada['id'] , maxResults = 50).execute()
            print("Esto puede tradar.......")
            for j in range(Datos_playlist['pageInfo']['totalResults']):
                canal = Datos_playlist['items'][j]['snippet']['videoOwnerChannelTitle']
                cancion = Datos_playlist['items'][j]['snippet']['title']
                canal, cancion = filtro.filtrar_palabras_titulo(canal, cancion)

                letra = genius.genius_total(canal, cancion, False)
                filtro.diccionario_de_palabras(repes, letra)
                os.system("cls")
                print(f"letras calculadas {j} / {Datos_playlist['pageInfo']['totalResults']}")


            dic_a_lista:list = filtro.convertir_diccionario(repes)
            if(dic_a_lista == None):
                print("No se pudo encontrar ninguna letra en la playlist")
                return
            lista_cloud = []
            for i in range(len(dic_a_lista)):
                lista_cloud.append(str(dic_a_lista[i][0]))

            text = " ".join(lista_cloud)
            #borra las palabras comunes como articulos y pronombres
            wordcloud2 = wordcloud.WordCloud(stopwords = None, max_words = 10).generate(text)
            wordcloud2.to_file("cloud.png")
            return

        elif opcion == "5":

            spotify = SP.Generar_Servicio_Spotify()
            os.system("clear")
            print(" Lista de PlayList ")
            print("------------------------------")
            print()
            lista_playlist_spotify: list = SP.listar_playlist(spotify)
            lista_playlist_youtube: list = YT.listar_playlist(youtube)
            imprimir_titulos_playlist(lista_playlist_youtube)

            print()
            print("------------------------------")
            nombre_playlist: str = input("Ingresar el nombre de la playlist que desea sincronizar: ")
            sincronizar_youtube.sincronizar_playlist(nombre_playlist, lista_playlist_spotify, lista_playlist_youtube,
                                                     spotify)
            return


        elif opcion == "6":
            os.system("clear")
            print(" Lista de PlayList ")
            print("------------------------------")
            print()
            lista_playlist_csv: list = YT.listar_playlist(youtube)
            imprimir_titulos_playlist(lista_playlist_csv)
            print()
            nombre_de_la_playlist: str = input("Escriba el nombre de la playlist a exportar: ")
            playlist: dict = buscar_playlist(nombre_de_la_playlist, lista_playlist_csv)
            exportar_playlist.exportar(playlist, 'youtube')
            return

        if opcion == "Salir":
            Iterable = 1

        if opcion == "Cambiar":

            Menu_Spotify()

            Iterable = 1
"""


def agregar_canciones_playlist(youtube: any, id_playlist: str) -> None:
    contador: int = 0
    print("Agregar canciones en la playlist")
    print()
    while contador != -1:

        nombre_cancion: str = validar_input_cancion()

        if nombre_cancion != "-1":
            video: any = buscar_cancion_en_youtube(youtube, nombre_cancion.title())

            while video == -1:
                print("La cancion no existe ")
                nombre_cancion: str = validar_input_cancion()
                video = buscar_cancion_en_youtube(youtube, nombre_cancion.title())
                contador = contador + 1
                if contador == 4:
                    print("La cancion no se encuentra intente mas tarde")
                    contador = -1
                    sleep(4.0)

            if contador != -1:
                insertar_cancion_en_playlist_youtube(youtube, video, id_playlist)
                print("Ingresar -1 para terminar de agregar canciones")
                print()
        else:
            contador = -1
