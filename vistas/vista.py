import os


def imprimir_lista_playlist(lista_playlist: list) -> None:
    for i in range(len(lista_playlist)):
        print(lista_playlist[i]["nombre_playlist"] + ":")
        for canciones in lista_playlist[i]["lista_canciones"]:
            print(f"    {canciones}")


def imprimir_titulos_playlist(lista_playlist: list) -> None:
    for posicion_playlist in range(len(lista_playlist)):
        print("No. {1} - {0} ".format(lista_playlist[posicion_playlist]["nombre_playlist"], posicion_playlist))


def linea_divisora() -> None:
    linea: str = "-"
    print(linea * 60)

def pantalla_inicio() -> None:
    os.system("clear")
    print()
    print("Organizador de Plataformas TEAM - 7")
    linea_divisora()
    print("Youtube | Spotify")
    print()


def imprtimir_menu(nombre_plataforam: str) -> None:
    print("Menu {}".format(nombre_plataforam))
    print("------------------------------")
    print(" 1 | Listar Playlist ")
    print(" 2 | Crear Playlist ")
    print(" 3 | Añadir a Playlist ")
    print(" 4 | Analizar Playlist")
    print(" 5 | Sincronizar Playlist")
    print(" 6 | Exportar Playlist ")
    print(" 7 | Salir de Spotify ")
    print("_________________________")