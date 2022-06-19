import os
import tekore as tk
from tekore import RefreshingToken 
from tekore import Spotify

#Estos datos se obtienen en "https://developer.spotify.com/dashboard/login"
#solo creen una aplicacion con una cuenta de spotify y tendran
#arriba a la derecha acceso a estos datos
CLIENT_ID = '56aa6d858d4041b9bdf3a30facecd839'
CLIENT_SECRET = '71825c90b8aa464985acfe7e51822cd5'

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

#pide al usuario una palabra clave y busca en spotify canciones 
def buscar_sp(spotify: Spotify) -> str:
	rango_busqueda = 5
	aux:bool = True
	while(aux == True):
		buscador = input("ingrese que cancion quiere buscar: ")
		track = spotify.search(buscador)
		if(len(track[0].items) == 0):
			print("no se encontro resultado")
		else:
			print("==========================================")
			for i in range(rango_busqueda):
				print(f" {i} - nombre: {track[0].items[i].name}, artista: {track[0].items[i].artists[0].name}, album: {track[0].items[i].album.name}")
			print("==========================================")

			centinela = int(input("Ingrese cual cancion quiere añadir a la playlist o -1 para volver a buscar: "))
			while(centinela < -1 or centinela > rango_busqueda):
				centinela = int(input("ERROR: Ingrese cual cancion quiere añadir a la playlist o -1 para volver a buscar: "))
			if(centinela == -1):
				aux = True
			else:
				aux = False
			os.system("cls")

			
	#devuelvo una uri en str, pero al momento de añadir la cancion a la playlist tiene que ser una lista
	return track[0].items[centinela].uri

	#spotify.playlist_add(spotify.playlists(spotify.current_user().id).items[0].id, [track[0].items[centinela].uri])

def anadir_cancion(spotify : Spotify) -> None:

	#print(spotify.playlist_items(spotify.playlists(spotify.current_user().id).items[0].id).items[0].track.name)
	#print(spotify.playlist_items(spotify.playlists(spotify.current_user().id).items[0].id).items[0].track.id)
	#print(spotify.playlist_items(spotify.playlists(spotify.current_user().id).items[0].id).items[0].track.uri)
	
	uri_track_nueva = []
	#vas a la cancion-> tres puntitos -> compartit -> alt+ctrl ->copiar uri
	uri_track_nueva.append("spotify:track:7MeXwzhSDGfqNfuFANgzVC")
	uri_track_nueva.append("spotify:track:3AwLxSqo1jOOMpNsgxqRNE")
	id_playlist = spotify.playlists(spotify.current_user().id).items[0].id

	spotify.playlist_add(id_playlist, uri_track_nueva)


def sincronizar_lista_spotify(spotify : Spotify) -> None:
	print("Playlists en Spotify:")
	for i in range(spotify.playlists(spotify.current_user().id).total):
		print(f" {i} - {spotify.playlists(spotify.current_user().id).items[i].name}:")
	
	centinela = int(input("Ingrese que playlist quiere sincronizar: "))
	while(centinela < 0 or centinela > spotify.playlists(spotify.current_user().id).total):
		centinela = int(input("ERROR: Ingrese que playlist quiere sincronizar nuevamente: "))

	archivo = open("sync_sp.csv", "w", newline = "")
	archivo.write(spotify.playlists(spotify.current_user().id).items[centinela].name + '\n')
	for j in range(spotify.playlist_items(spotify.playlists(spotify.current_user().id).items[centinela].id).total):
		if(j != spotify.playlist_items(spotify.playlists(spotify.current_user().id).items[centinela].id).total - 1):
			archivo.write(spotify.playlist_items(spotify.playlists(spotify.current_user().id).items[centinela].id).items[j].track.name + ",")
		else:
			archivo.write(spotify.playlist_items(spotify.playlists(spotify.current_user().id).items[centinela].id).items[j].track.name)

	archivo.close()