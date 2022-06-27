from os import system
import Youtube as YT
import Spotify as SP
from sincronizar import sincronizar


def Menu_Spotify() -> None:

	Iterable = 0

	while Iterable == 0 :

		system("cls")

		opcion = str()

		spotify = SP.Generar_Servicio_Spotify()
		youtube = YT.Generar_Servicios_Youtube()

		while opcion != "1" and opcion != "2" and opcion != "3" and opcion != "4" and opcion != "5" and opcion != "6" and opcion != "Salir" and opcion != "Cambiar" :

			system("cls")

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

			system("cls")

			SP.Listar_Playlist_Spotify( spotify )

			input()

		elif opcion == "2":

			system("cls")

			SP.Crear_Playlist_Spotify( spotify )

		elif opcion =="3":

			return

		elif opcion == "4":

			return

		elif opcion == "5":
			system("clear")
			print(" Lista de PlayList ")
			print("------------------------------")
			print()
			nombre_playlist:str = input("Ingresar el nombre de la playlist que desea sincronizar: ")
			sincronizar.sincronizar_playlist(nombre_playlist, SP.lista(spotify), youtube)
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

		system("cls")

		opcion = str()

		youtube = YT.Generar_Servicios_Youtube()

		while opcion != "1" and opcion != "2" and opcion != "3" and opcion != "4" and opcion != "5" and opcion != "6" and opcion != "Salir" and opcion != "Cambiar" :

			system("cls")

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

			system("cls")

			YT.Listar_Playlist_Youtube( youtube )

			input()

		elif opcion == "2":

			system("cls")

			YT.Crear_Playlist_Youtube( youtube )

		elif opcion =="3":

			return

		elif opcion == "4":

			return

		elif opcion == "5":

			return

		elif opcion == "6":

			return

		if opcion == "Salir":

			Iterable = 1

		if opcion == "Cambiar":

			Menu_Spotify()

			Iterable = 1

def main() -> None:

	Programa = str()

	while Programa != "Youtube" and Programa != "Spotify" and Programa != "SALIR" :

		print("Bienvendio su Aplicacion de Control de Playlist")

		Programa = input("Seleccione: | Youtube | o | Spotify | o | SALIR |: ")

		system("cls")

	if Programa == "Spotify":

		Menu_Spotify()

	elif Programa == "Youtube":

		Menu_Youtube()

	else:

		print("Gracias, vuelva pronto")

main()
