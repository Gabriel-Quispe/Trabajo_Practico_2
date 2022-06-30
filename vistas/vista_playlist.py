def imprimir_lista_playlist(lista_playlist:list)-> None:
   for i in range(len(lista_playlist)):
      print(lista_playlist[i]["nombre_playlist"] + ":")
      for canciones in lista_playlist[i]["lista_canciones"]:
        print(f"    {canciones}")

