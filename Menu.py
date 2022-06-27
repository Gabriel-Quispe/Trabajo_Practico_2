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

letra_aux= """"
Bohemian Rhapsody Lyrics[Intro]
Is this the real life? Is this just fantasy?
Caught in a landslide, no escape from reality
Open your eyes, look up to the skies and see
I'm just a poor boy, I need no sympathy
Because I'm easy come, easy go, little high, little low     
Any way the wind blows doesn't really matter to me, to me   

[Verse 1]
Mama, just killed a man
Put a gun against his head, pulled my trigger, now he's dead
Mama, life had just begun
But now I've gone and thrown it all away
Mama, ooh, didn't mean to make you cry
If I'm not back again this time tomorrow
Carry on, carry on as if nothing really matters
[Verse 2]
Too late, my time has come
Sends shivers down my spine, body's aching all the time
Goodbye, everybody, I've got to go
Gotta leave you all behind and face the truth
Mama, ooh (Any way the wind blows)
I don't wanna die
I sometimes wish I'd never been born at all

[Guitar Solo]

[Verse 3]
I see a little silhouetto of a man
Scaramouche, Scaramouche, will you do the Fandango?
Thunderbolt and lightning, very, very frightening me
(Galileo) Galileo, (Galileo) Galileo, Galileo Figaro magnifico
But I'm just a poor boy, nobody loves me
He's just a poor boy from a poor family
Spare him his life from this monstrosity
Easy come, easy go, will you let me go?
Bismillah! No, we will not let you go
(Let him go) Bismillah! We will not let you go
(Let him go) Bismillah! We will not let you go
(Let me go) Will not let you go
(Let me go) Will not let you go
(Never, never, never, never let me go) Ah
No, no, no, no, no, no, no
(Oh, mamma mia, mamma mia) Mamma mia, let me go
Beelzebub has a devil put aside for me, for me, for me!
[Verse 4]
So you think you can stone me and spit in my eye?
So you think you can love me and leave me to die?
Oh, baby, can't do this to me, baby!
Just gotta get out, just gotta get right outta here

[Outro]
(Ooh)
(Ooh, yeah, ooh, yeah)
Nothing really matters, anyone can see
Nothing really matters
Nothing really matters to me
Any way the wind blows679Embed
"""

def comparar_str_a_en_b(a:str, b:str) -> bool:
	a1:str = a.replace(" ","")
	b1:str = b.replace(" ","")
	if(a1.lower() in  b1.lower()):
		return True
	return False

def leer_archivo_sinc(nombre_archivo:str, diccionario:dict) -> None:
	archivo = open(nombre_archivo, "r")
	diccionario['nombre_playlist'] = archivo.readline()
	canciones_str = archivo.readline()
	diccionario['lista_canciones'] = canciones_str.split(",")
	archivo.close()

def genius_funcion(nueva_track, artista, imprimir_pantalla:bool) -> None:
	genius = lyricsgenius.Genius(CLIENTE_ACCESS_TOKE_GENIUS)
	genius_tack_artist = genius.search(artista.title(), type_='artist')
	if(len(genius_tack_artist['sections'][0]['hits']) == 0):
		if(imprimir_pantalla == True):
			print("No se encontró al artista")
		return
	export:int = 0
	for i in range(len(genius_tack_artist['sections'][0]['hits'])):
		if(genius_tack_artist['sections'][0]['hits'][i]['result']['name'].lower() == artista.lower()):
			export = i
	
	song_genius = genius.search_artist_songs(	artist_id = genius_tack_artist['sections'][0]['hits'][export]['result']['id'], 
												search_term = nueva_track,
												per_page = 2, 
												sort = artista )

	dict_final:dict = {}
	basta = False
	
	for i in range(len(song_genius['songs'])):
		#print(f"{song_genius['songs'][i]['title']} !!! {song_genius['songs'][i]['artist_names']}" )
		if((	comparar_str_a_en_b(nueva_track, song_genius['songs'][i]['title']) == True) and 
		   (	comparar_str_a_en_b(artista, song_genius['songs'][i]['artist_names']) == True)and
		   (	basta == False)):
			dict_final = song_genius['songs'][i]
			basta = True
	if(imprimir_pantalla == True):
		print("Esto puede tradar.......")
	if(len(dict_final) != 0):
		#letra = genius.lyrics(song_id = dict_final['id'], per_page = 2)
		letra = genius.lyrics(song_url = dict_final['url'])	
		if(imprimir_pantalla == True):
			print(letra)	
		return(letra)
	else:
		if(imprimir_pantalla == True):
			print("Nos se pudo encontrar la letra")
	return None

def filtrar_string(nueva_track:str, basura:str):
	final:str = nueva_track
	basura = basura.lower()
	nueva_track =  nueva_track.lower()
	if(comparar_str_a_en_b(basura, nueva_track) == True):
		final = nueva_track.replace(basura, "")
	return final

def filtrar_palabras_titulo(canal:str, cancion:str):

	canal = filtrar_string(canal, "vevo")
	canal = filtrar_string(canal, "official")
	canal = filtrar_string(canal, "oficial")
	canal = filtrar_string(canal, "channel")
	canal = filtrar_string(canal, "canal")
	canal = filtrar_string(canal, "(")
	canal = filtrar_string(canal, ")")
	canal = filtrar_string(canal, "-")
	canal = filtrar_string(canal, "-")

	while("  " in canal):
		canal = filtrar_string(canal, "  ")
	while(canal[len(canal) - 1] == " "):
		canal = canal[:-1]
	while(canal[0] == " "):
		canal = canal[1:]
	while(canal[len(canal) - 1].isalnum() == False):
		canal = canal[:-1]
	while(canal[0].isalnum() == False):
		canal = canal[1:]

	cancion = filtrar_string(cancion, canal)
	cancion = filtrar_string(cancion, "(")
	cancion = filtrar_string(cancion, ")")
	cancion = filtrar_string(cancion, "(")
	cancion = filtrar_string(cancion, ")")
	cancion = filtrar_string(cancion, "]")
	cancion = filtrar_string(cancion, "[")
	cancion = filtrar_string(cancion, "]")
	cancion = filtrar_string(cancion, "[")
	cancion = filtrar_string(cancion, "-")
	cancion = filtrar_string(cancion, "-")
	cancion = filtrar_string(cancion, "remastered")
	cancion = filtrar_string(cancion, "hd")
	cancion = filtrar_string(cancion, "hq")
	cancion = filtrar_string(cancion, "fullhd")
	cancion = filtrar_string(cancion, "music")
	cancion = filtrar_string(cancion, "4k")
	cancion = filtrar_string(cancion, "video")
	cancion = filtrar_string(cancion, "official")
	cancion = filtrar_string(cancion, "oficial")
	cancion = filtrar_string(cancion, "lyrics")
	cancion = filtrar_string(cancion, "con letra")
	for i in range(1900, 2022):
		cancion = filtrar_string(cancion, str(i))
	while(cancion[len(cancion) - 1] == " "):
		cancion = cancion[:-1]
	while(cancion[len(cancion) - 1].isalnum() == False):
		cancion = cancion[:-1]
	while(cancion[0] == " "):
		cancion = cancion[1:]
	while(cancion[0].isalnum() == False):
		cancion = cancion[1:]
	while("  " in cancion):
		cancion = filtrar_string(cancion, " ")
	cancion = filtrar_string(cancion, canal)

	return (canal, cancion)

def borrar_comentario(letra:str) -> str:
	if(letra == None):
		return None
	while("[" in letra):
		lista_aux1 = []
		lista_aux1.append(letra[0 : letra.index("[")])
		lista_aux1.append(letra[letra.index("]") + 1 :])
		letra = "".join(lista_aux1)
	letra = letra[letra.index("Lyrics") + 6:]
	letra = letra[0: len(letra) - 8]
	return letra

def diccionario_de_palabras(dicc:dict, letra:str):
	if(letra == None):
		return
	lista_palabras = []
	aux = letra.lower()
	aux = aux.replace("\n", " ")
	aux = aux.replace(",", "")
	aux = aux.replace(".", "")
	aux = aux.replace("(", "")
	aux = aux.replace(")", "")
	aux = aux.replace('\"', "")
	aux = aux.replace('?', "")
	aux = aux.replace('¡', "")
	aux = aux.replace('!', "")
	aux = aux.replace('¡', "")

	lista_palabras = aux.split(" ")

	for i in range(len(lista_palabras)):
		if(lista_palabras[i] != ""):
			if(lista_palabras[i] in dicc):
				dicc[lista_palabras[i]] += 1
			else:
				dicc[lista_palabras[i]] = 1

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

			nueva_track = SP.buscar_sp(spotify)
			
			canal, cancion = filtrar_palabras_titulo(nueva_track.artists[0].name, nueva_track.name)
			genius_funcion(cancion, canal, True)

			playlist_agregar = SP.seleccionar_playlists(spotify)
			SP.anadir_cancion(spotify, playlist_agregar, nueva_track)

			letra = genius_funcion(cancion, canal, True)
			letra = borrar_comentario(letra)

			os.system("cls")
			print(letra)
			return

		elif opcion == "4":
			os.system("cls")
			repes = {}
			playlist_seleccionada = SP.seleccionar_playlists(spotify)
			print("Esto puede tradar.......")
			for j in range(spotify.playlist_items(playlist_seleccionada.id).total):
				canal = spotify.playlist_items(playlist_seleccionada.id).items[j].track.artists[0].name
				cancion = spotify.playlist_items(playlist_seleccionada.id).items[j].track.name
				canal, cancion = filtrar_palabras_titulo(canal, cancion)

				letra = genius_funcion(cancion, canal, False)
				letra = borrar_comentario(letra)
				diccionario_de_palabras(repes, letra)
				os.system("cls")
				print(f"letras calculadas {j} / {spotify.playlist_items(playlist_seleccionada.id).total}")

			dic_a_lista:list = []
			if(len(repes) != 0):
				dic_a_lista = list(repes.items())
				dic_a_lista.sort(key = lambda x:x[1] , reverse = True)
				for i in range(10):
					print(f"Top {i}:  {dic_a_lista[i][0]} con {dic_a_lista[i][1]} ocurrencias")
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
			palabra = YT.buscar(youtube)
			playlist_seleccionada = YT.seleccionar_playlist_yt(youtube)
			YT.insertar_en_playlist_yt(youtube, palabra, playlist_seleccionada)

			canal, cancion = filtrar_palabras_titulo(palabra['snippet']['channelTitle'], palabra['snippet']['title'])
			letra = genius_funcion(cancion, canal, True)
			letra = borrar_comentario(letra)

			os.system("cls")
			print(letra)

			return

		elif opcion == "4":
			os.system("cls")
			repes = {}
			playlist_seleccionada = YT.seleccionar_playlist_yt(youtube)
			Datos_playlist = youtube.playlistItems().list( part = "snippet", playlistId = playlist_seleccionada['id'] , maxResults = 50).execute()
			print("Esto puede tradar.......")
			for j in range(Datos_playlist['pageInfo']['totalResults']):
				canal = Datos_playlist['items'][j]['snippet']['videoOwnerChannelTitle'] 
				cancion = Datos_playlist['items'][j]['snippet']['title']
				canal, cancion = filtrar_palabras_titulo(canal, cancion)
				letra = genius_funcion(cancion, canal, False)
				letra = borrar_comentario(letra)
				diccionario_de_palabras(repes, letra)

			dic_a_lista:list = []
			dic_a_lista = list(repes.items())
			dic_a_lista.sort(key = lambda x:x[1] , reverse = True)
			for i in range(10):
				print(f"Top {i}:  {dic_a_lista[i][0]} con {dic_a_lista[i][1]} ocurrencias")
			#print(json.dumps(repes, indent = 3))
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
