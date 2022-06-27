from __future__ import print_function
from ast import keyword

import os.path
import os
import json
import csv
from textwrap import indent

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

#AIzaSyB618jeO2G8thgQTjiQnOR5mX6J1IaQQQ8
 
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
	
		for j in range(Datos_playlist['pageInfo']['totalResults']):

			#Imprime su titulo
			print(f"	{Datos_playlist['items'][j]['snippet']['title']}")


		print("-------------------------------")

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

def pedir_centinela_int(max:int):
	centinela = int(input("Seleccione: "))
	while(centinela < 0 or centinela > max):
		centinela = int(input("ERROR: Seleccione nuevamente: "))
	return centinela

def sincronizar_lista_youtube(youtube : 'googleapiclient.discovery.Resource') -> None:

	os.system('cls')
	Info_playlist = youtube.playlists().list( part="snippet", mine=True).execute()
	print("Playlists en Youtube:")
	for playlists in range(len(Info_playlist['items'])):

		print(f" {playlists} - {Info_playlist['items'][playlists]['snippet']['title']}")

	centinela:int = pedir_centinela_int(len(Info_playlist['items']))

	Datos_playlist = youtube.playlistItems().list( part = "snippet", playlistId = Info_playlist['items'][centinela]['id'] , maxResults = 50).execute()
	
	archivo = open("sync_yt.csv", "w", newline = "")
	archivo.write(Info_playlist['items'][centinela]['snippet']['title'] + '\n')
	for i in range(Datos_playlist['pageInfo']['totalResults']):
		if(i != Datos_playlist['pageInfo']['totalResults'] - 1):
			archivo.write(Datos_playlist['items'][i]['snippet']['title'] + ",")
		else:
			archivo.write(Datos_playlist['items'][i]['snippet']['title'])

	archivo.close()

def seleccionar_playlist_yt(youtube : 'googleapiclient.discovery.Resource'):
	Info_playlist = youtube.playlists().list( part="snippet", mine=True).execute()
	for playlists in range(len(Info_playlist['items'])):
		print(f" {playlists} - {Info_playlist['items'][playlists]['snippet']['title']}")

	centinela:int = pedir_centinela_int(len(Info_playlist['items']))

	return Info_playlist['items'][centinela]

def buscar(youtube : 'googleapiclient.discovery.Resource'):
	palabra_clave = input("Ingrese que desea buscar en youtube: ")
	resultado = youtube.search().list(
			part = "id,snippet",
			q = palabra_clave,
			maxResults = 5
	).execute()
	print("============================================================")
	print("Resultados: ")

	for i in range(len(resultado['items'])):
		print(f" {i} | {resultado['items'][i]['snippet']['title']} | {resultado['items'][i]['snippet']['channelTitle']}")

	centinela:int = pedir_centinela_int(len(resultado['items']))
		
	#playlist_seleccionada = seleccionar_playlist_yt(youtube)

	return resultado['items'][centinela]

def insertar_en_playlist_yt(youtube : 'googleapiclient.discovery.Resource', resultado, playlist_seleccionada):
	youtube.playlistItems().insert(part = "snippet",
	body = {
		'snippet': {
			'playlistId': playlist_seleccionada['id'],
			'resourceId': {
					'kind': 'youtube#video',
				'videoId': resultado['id']['videoId']
			}
		}
	}).execute()
