def definir_playlist()->dict:

  """
    Precondicion:
    Postcondicion: devuelve un diccionario del tipo playlist con sus propiedades sin datos
  """

  playlist:dict = {
      "id":"",
			"nombre_playlist":"",
			"lista_canciones":[]
	}

  return playlist

def buscar_playlist(nombre_playlist:str, lista_playlist)->dict:

  """
    Precondicion: Recibir el nombre de una playlist y una lista de playlist
    Postcondicion: Devuelve un dictionario del tipo playlist con sus propiedades con datos
  """

  playlist:dict = definir_playlist()

  for i in range(len(lista_playlist)):
      if(lista_playlist[i]["nombre_playlist"] == nombre_playlist):
        playlist['id'] = lista_playlist[i]['id']
        playlist["nombre_playlist"] = nombre_playlist
        for canciones in lista_playlist[i]["lista_canciones"]:
          playlist["lista_canciones"].append(canciones)              

  return playlist  


def esta_presente_playlist_en_la_lista(nombre_playlist:str, lista_playlist:list)->bool:

  """
    Precondicion: Recibir el nombre de una playlist y una lista de playlist
    Postcondicion: Devulve True si existe la plyalist en la lista caso contrario devuelve false
  """
  for i in range(len(lista_playlist)):
      if(lista_playlist[i]["nombre_playlist"] == nombre_playlist):
        return True

  return False