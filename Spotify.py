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

#Pre: hace falta que max sea un int
#Post: Le pide al usuario que ingrese un numero dentre 0 y el maximo dado
#	   luego, una vez que esté  dentro del rango devuelve ese numero
def pedir_centinela_int(max:int):
	centinela:int = int(input("Seleccione: "))
	while(centinela < 0 and centinela > max):
		centinela = int(input("ERROR: Seleccione nuevamente: "))

	return centinela

#Pre: requiere que ya esté logueado en spotify
#Post: le muestra al usuario todas las playlists que tiene y le da a elejir cual seleccionar, luego la devuelve
def seleccionar_playlists_spotify(spotify: Spotify):
	print(f"Playlists en spotify de {spotify.user(spotify.current_user().id).display_name}:")
	for i in range(spotify.playlists(spotify.current_user().id).total):
		print(f" {i} - {spotify.playlists(spotify.current_user().id).items[i].name}")

	centinela:int = pedir_centinela_int(spotify.playlists(spotify.current_user().id).total)
	#devuelvo el objeto entero despues se ulitiza .id .name .uri etc
	return spotify.playlists(spotify.current_user().id).items[centinela]

#Pre: Estar logueado en spotify 
#Post: Pide al usuario una palabra clave y busca en spotify 
# 	   imprime los 5 resultados de spotify, le pide al usuario cual desea y devuelve el objeto cancion elejida por el usuario
def buscar_spotify(spotify: Spotify):
	rango_busqueda:int = 5
	buscador:str = input("ingrese que cancion quiere buscar: ")
	track = spotify.search(buscador)
	#track es una lista de los resultados devueltos por el search, oredeando por que tanto se asemeja la palabra clave
	if(len(track[0].items) == 0):
		print("no se encontro resultado")

	else:
		print("==========================================")
		for i in range(rango_busqueda):
			cancion:str = track[0].items[i].name
			artista:str = track[0].items[i].artists[0].name
			album:str = track[0].items[i].album.name
			print(f" {i} - nombre: {cancion}, artista: {artista}, album: {album}")

		print("==========================================")
		centinela:int = pedir_centinela_int(rango_busqueda)
		os.system("cls")

	#al momento de añadir la cancion a la playlist tiene que ser una lista
	return track[0].items[centinela]


#Pre: Estar loguado, el objeto de playlist y de la cancion a agregar
def insertar_en_playlist_spotify(spotify : Spotify, playlist_destino, track_a_agregar ) -> None:
	#vas a la cancion-> tres puntitos -> compartit -> alt+ctrl ->copiar uri
	spotify.playlist_add(playlist_destino.id, [track_a_agregar.uri])

def sincronizar_lista_spotify(spotify : Spotify) -> None:
	print("Playlists en Spotify:")
	for i in range(spotify.playlists(spotify.current_user().id).total):
		print(f" {i} - {spotify.playlists(spotify.current_user().id).items[i].name}")
	
	centinela:int = pedir_centinela_int(spotify.playlists(spotify.current_user().id).total)

	archivo = open("sync_sp.csv", "w", newline = "")
	archivo.write(spotify.playlists(spotify.current_user().id).items[centinela].name + '\n')
	for j in range(spotify.playlist_items(spotify.playlists(spotify.current_user().id).items[centinela].id).total):
		if(j != spotify.playlist_items(spotify.playlists(spotify.current_user().id).items[centinela].id).total - 1):
			archivo.write(spotify.playlist_items(spotify.playlists(spotify.current_user().id).items[centinela].id).items[j].track.name + ",")
		else:
			archivo.write(spotify.playlist_items(spotify.playlists(spotify.current_user().id).items[centinela].id).items[j].track.name)

	archivo.close()