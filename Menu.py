#from os import systeminstall
import lyricsgenius
import os
import Youtube as YT
import Spotify as SP
import csv
import json

#algo1team7
CLIENTE_ID_GENIUS = '0aTUJE7lllfO1eWN_Ccbxw7v6ryfPsMxdG4Q7W7LP1wM1ZXEhKZ9v4nwNVBiE7nq'
CLIENTE_SECRET_GENIUS = 'jdLpCzyEhsbakzcv44OfkHxnGtvEs93Vjrv02uSgsKzURtMEZ-g-S3cREkvYqDpQ7eFgyCkseHEK-wbVctCe-g'
CLIENTE_ACCESS_TOKE_GENIUS = 'LJdoBgeVh5a90i4Svo-DeMhiSgO2Y9hdgb2ZqyejhGHgdC-qj4RLcWNPdiXn6ZSP'


def leer_archivo_sinc(nombre_archivo:str, diccionario:dict) -> None:
	archivo = open(nombre_archivo, "r")
	diccionario['nombre_playlist'] = archivo.readline()
	canciones_str = archivo.readline()
	diccionario['lista_canciones'] = canciones_str.split(",")
	archivo.close()

def Menu_Spotify() -> None:

	Iterable = 0

	while Iterable == 0 :

		os.system("cls")

		opcion = str()

		spotify = SP.Generar_Servicio_Spotify()

		while opcion != "1" and opcion != "2" and opcion != "3" and opcion != "4" and opcion != "5" and opcion != "6" and opcion != "Salir" and opcion != "Cambiar" :

			os.system("cls")

			print("Menu de Spotify:")
			print("------------------------------")
			print(" 1 | Listar Playlist ")
			print(" 2 | Crear Playlist ")
			print(" 3 | Añadir a Playlist ")
			print(" 4 | Analizar Playlist")
			print(" 5 | Sincronizar Playlist")
			print(" 6 | Exportar Playlist ")	
			print(" Cambiar | Ingresara a Youtube")
			print(" Salir | Cerrara el Programa")
			print("_________________________")
			opcion = input("Ingrese que decea: ")

		if opcion == "1":

			os.system("cls")
			SP.Listar_Playlist_Spotify( spotify )

			input()

		elif opcion == "2":

			os.system("cls")

			SP.Crear_Playlist_Spotify( spotify )

		elif opcion =="3":
			os.system("cls")
			genius = lyricsgenius.Genius(CLIENTE_ACCESS_TOKE_GENIUS)

			nueva_track = SP.buscar_sp(spotify)
			genius_tack_artist = genius.search(nueva_track.artists[0].name, type_='artist')
			genius_artist_id =  genius_tack_artist['sections'][0]['hits'][0]['result']['id']

			song_genius = genius.search_artist_songs(	artist_id = genius_artist_id, 
														search_term = nueva_track.name,
														per_page = 2, 
														sort =nueva_track.artists[0].name )
			dict_final = {}
			for i in range(len(song_genius['songs'])):
				if(		(nueva_track.name == song_genius['songs'][i]['title']) 
						and (nueva_track.artists[0].name == song_genius['songs'][i]['artist_names']) 
						):
					dict_final = song_genius['songs'][i]
			if(len(dict_final) != 0):
				print(f"La letra de {dict_final['title']} se exporto exitosamente al archivo letra_aux.txt")
				letra = genius.lyrics(song_id = dict_final['id'])
				if(letra != None):
					letra_aux = open("letra_aux.txt", "w")
					letra_aux.write(letra)
					letra_aux.close()
			else:
				print("Nos se pudo encontrar la letra")
			playlist_agregar = SP.seleccionar_playlists(spotify)
			SP.anadir_cancion(spotify, playlist_agregar, nueva_track)

			return

		elif opcion == "4":


			return

		elif opcion == "5":
			youtube = YT.Generar_Servicios_Youtube()
			SP.sincronizar_lista_spotify(spotify)

			diccionario_sinc_sp:dict = {}
			leer_archivo_sinc("sync_sp.csv", diccionario_sinc_sp)

			return

		elif opcion == "6":

			return

		if opcion == "Salir":

			Iterable = 1

		if opcion == "Cambiar":

			Menu_Youtube()

			Iterable = 1

def Menu_Youtube() -> None:

	Iterable = 0

	while Iterable == 0 :

		os.system("cls")

		opcion = str()

		youtube = YT.Generar_Servicios_Youtube()

		while opcion != "1" and opcion != "2" and opcion != "3" and opcion != "4" and opcion != "5" and opcion != "6" and opcion != "Salir" and opcion != "Cambiar" :

			os.system("cls")

			print("Menu de Youtube:")
			print("------------------------------")
			print(" 1 | Listar Playlist ")
			print(" 2 | Crear Playlist ")
			print(" 3 | Añadir a Playlist ")
			print(" 4 | Analizar Playlist")
			print(" 5 | Sincronizar Playlist")
			print(" 6 | Exportar Playlist ")	
			print(" Cambiar | Ingresara a Spotify")	
			print(" Salir | Cerrara el Programa")
			print("_________________________")
			opcion = input("Ingrese que decea: ")

		if opcion == "1":

			os.system("cls")

			YT.Listar_Playlist_Youtube( youtube )

			input()

		elif opcion == "2":

			os.system("cls")

			YT.Crear_Playlist_Youtube( youtube )

		elif opcion =="3":

			return

		elif opcion == "4":

			return

		elif opcion == "5": 
			spotify = SP.Generar_Servicio_Spotify()
			YT.sincronizar_lista_youtube(youtube)

			diccionario_sinc_yt:dict = {}
			leer_archivo_sinc("sync_yt.csv", diccionario_sinc_yt)
			

			#crear playlist de yt en spotify
			#agregar las canciones de la lista de diccionarios_sinc_yt en la lista recien creada en sp

			return


		elif opcion == "6":

			return

		if opcion == "Salir":

			Iterable = 1

		if opcion == "Cambiar":

			Menu_Spotify()

			Iterable = 1

def main() -> None:

	os.system("cls")
	Programa = str()

	while Programa != "Youtube" and Programa != "Spotify" and Programa != "SALIR" and Programa != "y" and Programa != "s":

		print("Bienvendio su Aplicacion de Control de Playlist")

		Programa = input("Seleccione: | Youtube | o | Spotify | o | SALIR |: ")

		os.system("cls")

	if Programa == "Spotify" or Programa == "s":

		Menu_Spotify()

	elif Programa == "Youtube" or Programa == "y":				

		Menu_Youtube()

	else:

		print("Gracias, vuelva pronto")

main()
