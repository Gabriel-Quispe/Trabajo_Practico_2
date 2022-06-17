import os
import tekore as tk
from tekore import RefreshingToken 
from tekore import Spotify

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
