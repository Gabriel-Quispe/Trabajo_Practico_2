from functools import total_ordering
import os

import wordcloud

import Spotify as SP
import Youtube as YT
import filtro
import genius
from playlist.playlist import buscar_playlist
from sincronizar import sincronizar_spotify, sincronizar_youtube
from vistas.vista_playlist import imprimir_lista_playlist, imprimir_titulos_playlist
from exportar_playlist import exportar_playlist


def imprtimir_menu():
    print("------------------------------")
    print(" 1 | Listar Playlist ")
    print(" 2 | Crear Playlist ")
    print(" 3 | Añadir a Playlist ")
    print(" 4 | Analizar Playlist")
    print(" 5 | Sincronizar Playlist")
    print(" 6 | Exportar Playlist ")
    print(" Cambiar | Ingresara a Youtube")
    print(" Salir | Cerrara el Programa")
    print("_________________________")

def Menu_Spotify() -> None:
    Iterable = 0
    try:
        spotify = SP.Generar_Servicio_Spotify()
        #youtube = YT.Generar_Servicios_Youtube()
    except Exception:
        print(" Error en conexion de plataformas")
        return

    while Iterable == 0 :
        os.system("cls")
        opcion = str()

        while opcion != "1" and opcion != "2" and opcion != "3" and opcion != "4" and opcion != "5" and opcion != "6" and opcion != "Salir" and opcion != "Cambiar" :
            os.system("cls")
            print("Menu de Spotify:")
            imprtimir_menu()
            opcion = input("Ingrese que decea: ")

        if opcion == "1":
            os.system("cls")
            SP.Listar_Playlist_Spotify(spotify)
            return

        elif opcion == "2":
            os.system("cls")
            SP.Crear_Playlist_Spotify( spotify )
            return

        elif opcion =="3":
            os.system("cls")

            nueva_track = SP.buscar_spotify(spotify)
            canal, cancion = filtro.filtrar_palabras_titulo(nueva_track.artists[0].name, nueva_track.name)

            playlist_agregar = SP.seleccionar_playlists_spotify(spotify)
            SP.insertar_en_playlist_spotify(spotify, playlist_agregar, nueva_track)
            print(f"canal: {canal}   cancion:{cancion}")
            letra = genius.genius_total(canal, cancion, True)

            #letra = borrar_comentario(letra)

            os.system("cls")
            print(letra)
            return

        elif opcion == "4":

            os.system("cls")
            repes = {}
            playlist_seleccionada = SP.seleccionar_playlists_spotify(spotify)

            print("Esto puede tradar.......")
            for j in range(spotify.playlist_items(playlist_seleccionada.id).total):
                canal = spotify.playlist_items(playlist_seleccionada.id).items[j].track.artists[0].name
                cancion = spotify.playlist_items(playlist_seleccionada.id).items[j].track.name
                canal, cancion = filtro.filtrar_palabras_titulo(canal, cancion)

                letra = genius.genius_total(canal, cancion, False)
                filtro.diccionario_de_palabras(repes, letra)

                os.system("cls")
                print(f"letras calculadas {j} / {spotify.playlist_items(playlist_seleccionada.id).total}")

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
            youtube = YT.Generar_Servicios_Youtube()
            os.system("clear")
            print(" Lista de PlayList ")
            print("------------------------------")
            print()

            lista_playlist_spotify: list = SP.listar_playlist(spotify)
            lista_playlist_youtube: list = YT.listar_playlist(youtube)
            imprimir_titulos_playlist(lista_playlist_spotify)
            print()
            print("------------------------------")
            nombre_playlist: str = input("Ingresar el nombre de la playlist que desea sincronizar: ")

            sincronizar_spotify.sincronizar_playlist(nombre_playlist, lista_playlist_spotify, lista_playlist_youtube,
                                                     youtube)
            return

        elif opcion == "6":
            os.system("clear")
            print(" Lista de PlayList ")
            print("------------------------------")
            print()
            try:
                lista_playlist_csv: list = SP.listar_playlist(spotify)
                imprimir_titulos_playlist(lista_playlist_csv)
                print()
                nombre_de_la_playlist: str = input("Escriba el nombre de la playlist a exportar: ")
                playlist: dict = buscar_playlist(nombre_de_la_playlist, lista_playlist_csv)
                exportar_playlist.exportar(playlist, 'spotify')
            except Exception:
                print("error en conexion de spotify")
            return

        if opcion == "Salir":
            Iterable = 1

        if opcion == "Cambiar":
            Menu_Youtube()

            Iterable = 1

def Menu_Youtube() -> None:
    Iterable = 0

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

def main() -> None:

    os.system("cls")
    Programa = str()

    while Programa != "Youtube" and Programa != "Spotify" and Programa != "SALIR" and Programa != "y" and Programa != "s":
        print("Bienvendio su Aplicacion de Control de Playlist")
        Programa = input("Seleccione: | Youtube | o | Spotify | o | SALIR |: ")
        os.system("cls")

    if Programa == "Spotify" or Programa == "s":
        Menu_Spotify()

    elif Programa == "Youtube" or Programa == "y":
        Menu_Youtube()

    else:
        print("Gracias, vuelva pronto")

main()

