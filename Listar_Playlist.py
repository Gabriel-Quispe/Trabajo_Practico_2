import Spotify as sp

def Listar_Playlist() -> None:

	spotify = sp.acceder_al_servicio()
	user = spotify.current_user()

	total_playlist = spotify.playlists(user.id).total

	for i in range(total_playlist):

		titulo = spotify.playlists(user.id).items[i].name
		print(f"{titulo}:")

		playlist_id = spotify.playlists(user.id).items[i].id
		total_canciones =  spotify.playlist_items(playlist_id).total

		for j in range(total_canciones):

			nombre_cancion = spotify.playlist_items(playlist_id).items[j].track.name 
			print(f"	{nombre_cancion}")

		print("-------------------------------")