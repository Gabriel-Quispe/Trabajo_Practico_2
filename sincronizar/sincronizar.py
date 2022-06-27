
def sincronizar_playlist(nombre_playlist:str, lista_playlist:list, platform:any)->None:
    """
        Precondicion: Recibir una playlist
        PostCondicion:
    """
    buscar_playlist(nombre_playlist, lista_playlist)

def buscar_playlist(nombre_playlist:str, lista_playlist)->None:

    for i in range(len(lista_playlist)):
        if(lista_playlist[i]["nombre_playlist"] == nombre_playlist):
            for canciones in lista_playlist[i]["lista_canciones"]:
                print(canciones)


