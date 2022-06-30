from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os

from playlist.playlist import definir_playlist
 
#Son los permisos que se le pediran al usuario
SCOPES = ['https://www.googleapis.com/auth/youtube',
		  "https://www.googleapis.com/auth/youtube.force-ssl",
          "https://www.googleapis.com/auth/youtube.readonly",
          "https://www.googleapis.com/auth/youtubepartner"]

#Para tener el archivo crdenciales.json se debe registrar una aplicacion en google
#darle acceso a la API de youtube v3, y obtener las credenciales,
#luego deben descargar el archivo json y llamarlo "credenciales"
ARCHIVO_SECRET_CLIENT = 'credenciales.json'

#Este es el nombre del archivo donde se almacenara el token para acceder al servicio
ARCHIVO_TOKEN = 'token.json'

#Permite acceder a los servicios de la API de youtube
def Generar_Servicios_Youtube() -> 'googleapiclient.discovery.Resource':

	#Precondicion: Tener las credenciales y una cuenta de google
	#Poscondicion: Haber dado acceso completo a esta app

    creds = None
    
    #Si existe un archivo con el token, lo usa
    if os.path.exists(ARCHIVO_TOKEN):

        creds = Credentials.from_authorized_user_file(ARCHIVO_TOKEN, SCOPES)
    
    #Si no existe o no es valido
    if not creds or not creds.valid:

    	#Si esta exipirado y puede refrescarse ("actualizarse"), lo ase
        if creds and creds.expired and creds.refresh_token:

            creds.refresh(Request())

        #Sino usas las credenciales y crea el token
        else:

            flow = InstalledAppFlow.from_client_secrets_file(ARCHIVO_SECRET_CLIENT, SCOPES)
            creds = flow.run_local_server(port=0)
        
        #Lo guarda en un archivo "token.json"
        with open(ARCHIVO_TOKEN, 'w') as token:

            token.write(creds.to_json())

    #usa el token y crea el acceso a la API de youtube
    return build('youtube', 'v3', credentials = creds)

#Lista las playlist con sus canciones de una cuenta de youtube
def Listar_Playlist_Youtube( youtube : 'googleapiclient.discovery.Resource' ) -> None:

	"""
	Precondicion: Tener acceso al servicio y tener alguna playlist
	Poscondicion: None
	"""

	#Obtiene la informacion de todas las playlist del usuario
	Info_playlist = youtube.playlists().list( part="snippet", mine=True).execute()

	#Ingresa a las playlist
	for playlists in range(len(Info_playlist['items'])):

		#Imprime su titulo
		print(Info_playlist['items'][playlists]['snippet']['title'])

		#Obtiene los datos que contiene la playlist
		Datos_playlist = youtube.playlistItems().list( part = "snippet", playlistId = Info_playlist['items'][playlists]['id'] , maxResults = 50).execute()

		#Ingresa a las canciones que contiene		
		for j in range(Datos_playlist['pageInfo']['totalResults']):

			#Imprime su titulo
			print(f"	{Datos_playlist['items'][j]['snippet']['title']}")

		print("-------------------------------")

def listar_playlist(youtube : 'googleapiclient.discovery.Resource')->dict:
	"""
		Precondicion: Tener acceso al servicio y tener alguna playlist
		Poscondicion: Devuelve una lista de playlist
	"""

	#Obtiene la informacion de todas las playlist del usuario
	info_playlist:any = youtube.playlists().list( part="snippet", mine=True).execute()
	lista_playlist:list = []

	#Ingresa a las playlist
	for playlists in range(len(info_playlist['items'])):

		playlist:dict = definir_playlist()
		playlist["id"] = info_playlist['items'][playlists]['id']
		playlist["nombre_playlist"] = info_playlist['items'][playlists]['snippet']['title']
		datos_playlist = youtube.playlistItems().list( part = "snippet", playlistId = info_playlist['items'][playlists]['id'] , maxResults = 50).execute()
		
		for j in range(datos_playlist['pageInfo']['totalResults']):
			playlist["lista_canciones"].append(datos_playlist['items'][j]['snippet']['title'])

		lista_playlist.append(playlist)

	return lista_playlist

def crear_playlist(youtube : 'googleapiclient.discovery.Resource', nombre_playlist:str):
	"""
		Precondicion: Tener acceso al servicio
		Poscondicion: None
	"""
	print("Ingrese alguna Descripcion:")
	Descripcion = input("")

	#Crea la playlist con los datos dados
	youtube.playlists().insert(part = "snippet", body = dict(snippet = dict(title = nombre_playlist, description = Descripcion))).execute()


#Crea una playlist para una cuenta de youtube
def Crear_Playlist_Youtube( youtube : 'googleapiclient.discovery.Resource' ) -> None:

	"""
	Precondicion: Tener acceso al servicio
	Poscondicion: None
	"""

	Nombre = input("Ingrese el Nombre de su Playlists: ")

	print("Ingrese alguna Descripcion:")
	Descripcion = input("")

	#Crea la playlist con los datos dados
	youtube.playlists().insert(part = "snippet", body = dict(snippet = dict(title = Nombre, description = Descripcion))).execute()


#Pre: hace falta que max sea un int
#Post: Le pide al usuario que ingrese un numero dentre 0 y el maximo dado
#	   luego, una vez que esté  dentro del rango devuelve ese numero
def pedir_centinela_int(max:int):
	centinela = int(input("Seleccione: "))
	while(centinela < 0 or centinela > max):
		centinela = int(input("ERROR: Seleccione nuevamente: "))
	return centinela


def seleccionar_playlist_youtube(youtube : 'googleapiclient.discovery.Resource'):
	Info_playlist = youtube.playlists().list( part="snippet", mine=True).execute()
	for playlists in range(len(Info_playlist['items'])):
		print(f" {playlists} - {Info_playlist['items'][playlists]['snippet']['title']}")

	centinela:int = pedir_centinela_int(len(Info_playlist['items']))
	
	return Info_playlist['items'][centinela]

#Pre: requiere que ya esté logueado en youtube
#Post: Devuelve el id de la cancion y de que no coincida con la busqueda devuelve -1
def buscar_cancion(youtube : 'googleapiclient.discovery.Resource', nombre_cancion:str):
	resultado = youtube.search().list(
				part = "id,snippet",
				q = nombre_cancion,
				maxResults = 5
	).execute()

	for i in range(len(resultado['items'])):
		nombre_cancion_youtube:str = resultado['items'][i]['snippet']['title']
		if(nombre_cancion_youtube.find(nombre_cancion) != -1):
			return resultado['items'][i]['id']['videoId']
		
	return -1

#Pre: Estar logueado en youtube, el objeto cancion y el objeto playlist
#Post: Agrega la cancion a la playlist
def insertar_cancion_en_playlist(youtube : 'googleapiclient.discovery.Resource', videoId:str, playlist_id):
	youtube.playlistItems().insert(part = "snippet",
	body = {
		'snippet': {
			'playlistId': playlist_id,
			'resourceId': {
					'kind': 'youtube#video',
				'videoId': videoId,
			}
		}
	}).execute()