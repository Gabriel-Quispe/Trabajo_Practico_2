def imprimir_lista_playlist(lista_playlist:list)-> None:
   for i in range(len(lista_playlist)):
      print(lista_playlist[i]["nombre_playlist"] + ":")
      for canciones in lista_playlist[i]["lista_canciones"]:
        print(f"    {canciones}")

def imprimir_titulos_playlist(lista_playlist:list)-> None:
    for posicion_playlist in range(len(lista_playlist)):
        print("No. {1} - {0} ".format(lista_playlist[posicion_playlist]["nombre_playlist"], posicion_playlist))