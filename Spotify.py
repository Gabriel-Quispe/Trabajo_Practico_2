import os
import tekore as tk
from tekore import RefreshingToken 
from tekore import Spotify

from playlist.playlist import definir_playlist

#Estos datos se obtienen en "https://developer.spotify.com/dashboard/login"
#solo creen una aplicacion con una cuenta de spotify y tendran
#arriba a la derecha acceso a estos datos
CLIENT_ID = '9446fa59f25043cda0f3162443491415'
CLIENT_SECRET = 'ddb6635b0f8b4d999e499172db01d5f6'

#En el apartado de "EDIT SETTINGS" ingresen 
#en "Redirect URIs" esta URL:
URL = "https://example.com/callback"

#Permite acceder a los servicios de la API de spotify
def Generar_Servicio_Spotify()->Spotify:

	"""
	Precondicion: Tener CLIENT ID and SECRET y haber ingresado la URL 
	Poscondicion: Haber dado acceso completo, copiando la URL en la consola
	"""

	token: RefreshingToken = None
	configuracion = (CLIENT_ID, CLIENT_SECRET, URL)

	#Si existe el archivo con el token, lo refresca ("actualiza") y lo utiliza
	if os.path.exists('tekore.cfg'):

		configuracion: tuple = tk.config_from_file('tekore.cfg', return_refresh=True)
		token = tk.refresh_user_token(*configuracion[:2], configuracion[3])

	#Si no existe lo crea
	elif(not token == True):

		token = tk.prompt_for_user_token(*configuracion, scope=tk.scope.every)
		tk.config_to_file('tekore.cfg', configuracion + (token.refresh_token,))

	#Utiliza el token y retorna el acceso a la API de spotify
	return tk.Spotify(token)

#Lista las playlist con sus canciones de una cuenta de spotify
def Listar_Playlist_Spotify( spotify : Spotify) -> None:

	"""
	Precondicion: Tener acceso al servicio y tener alguna playlist
	Poscondicion: None
	"""

	#Ingresa a las playlist
	for i in range(spotify.playlists(spotify.current_user().id).total):

		#Imprime el titulo
		print(f"{spotify.playlists(spotify.current_user().id).items[i].name}:")

		#Ingresa a las canciones
		for j in range(spotify.playlist_items(spotify.playlists(spotify.current_user().id).items[i].id).total):

			#Imprime el titulo
			print(f"	{spotify.playlist_items(spotify.playlists(spotify.current_user().id).items[i].id).items[j].track.name}")

		print("-------------------------------")

def listar_playlist(spotify : Spotify)->list:

	lista_playlist:list = []
	cantidad_de_playlist:int = spotify.playlists(spotify.current_user().id).total

	for i in range(cantidad_de_playlist):

		playlist:dict = definir_playlist()
		playlist["id"] = spotify.playlists(spotify.current_user().id).items[i].id
		playlist["nombre_playlist"] = spotify.playlists(spotify.current_user().id).items[i].name
		
		prueba= spotify.playlists(spotify.current_user().id).items[i]

		for j in range(spotify.playlist_items(spotify.playlists(spotify.current_user().id).items[i].id).total):
			playlist["lista_canciones"].append(spotify.playlist_items(spotify.playlists(spotify.current_user().id).items[i].id).items[j].track.name)

		lista_playlist.append(playlist)

	return lista_playlist	
	

#Crea una playlist para una cuenta de spotify
def Crear_Playlist_Spotify( spotify: Spotify) -> None:
	
	"""
	Precondicion: Tener acceso al servicio
	Poscondicion: None
	"""
	Nombre = input("Ingrese el Nombre de su Playlists: ")

	print("Ingrese alguna Descripcion:")
	Descripcion = input("")

	#Crea la playlist con los datos dados
	spotify.playlist_create(spotify.current_user().id, Nombre, public = True, description = Descripcion)

def crear_playlist( spotify: Spotify, nombre_playlist:str) -> None:
	
	"""
	Precondicion: Inicializar el objeto spotify y el nombre de la playlist que quiere crear
	Poscondicion: None
	"""
	spotify.playlist_create(spotify.current_user().id, nombre_playlist, public = True, description = "musica")

def buscar_cancion(spotify: Spotify, cancion:str):

	RANGO_CANCIONES:int = 5
	track = spotify.search(cancion)

	if(len(track[0].items) == 0):
		return -1
	else:
		for i in range(RANGO_CANCIONES):
			cancion_nombre:str = track[0].items[i].name
			if(cancion_nombre.find(cancion) !=-1):
				return track[0].items[i]

	return -1

def insertar_cancion_en_playlist(spotify : Spotify, id_playlist, url_cancion) -> None:
	"""
		Precondicion: Inicializar el objeto spotify, id de la playlist y url de la cancion que se desea agregar
		Poscondicion: None
	"""
	spotify.playlist_add(id_playlist, [url_cancion.uri])