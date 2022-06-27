import filtro
import lyricsgenius
#algo1team7
CLIENTE_ID_GENIUS = '0aTUJE7lllfO1eWN_Ccbxw7v6ryfPsMxdG4Q7W7LP1wM1ZXEhKZ9v4nwNVBiE7nq'
CLIENTE_SECRET_GENIUS = 'jdLpCzyEhsbakzcv44OfkHxnGtvEs93Vjrv02uSgsKzURtMEZ-g-S3cREkvYqDpQ7eFgyCkseHEK-wbVctCe-g'
CLIENTE_ACCESS_TOKE_GENIUS = 'LJdoBgeVh5a90i4Svo-DeMhiSgO2Y9hdgb2ZqyejhGHgdC-qj4RLcWNPdiXn6ZSP'




#Pre:  Estar logueado en genius, el nombre de la cancion y el artista en string, y el bool de si se imprime en pantalla
#Post: Busca en genius primero al artista y luego busca entre las canciones del artista la cancion pedida,
# 	   para de esa manera evitar enviar una cancion que se llame igual pero se de otro artista,
#      luego devuelve el objeto cancion
def buscar_genius(nueva_track:str, artista:str, imprimir_pantalla:bool, genius):
	genius_tack_artist = genius.search(artista, type_='artist')
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
	return song_genius

#Pre:  Estar logueado en genius, el nombre de la cancion y el artista en string
#Post: Recorre la lista de resultados que mandó genius y compara cual es el que corrresponde con el nombre y artista
#      luego guarda el diccionario del resultado y lo develve
def filtrar_resultado_genius(nueva_track:str, artista:str, song_genius) -> dict:
    if(song_genius == None):
        return None
        
    dict_final:dict = {}
    basta:bool = False
    for i in range(len(song_genius['songs'])):
		#print(f"{song_genius['songs'][i]['title']} !!! {song_genius['songs'][i]['artist_names']}" )
        if((	filtro.comparar_str_a_en_b(nueva_track, song_genius['songs'][i]['title']) == True) and 
        (	filtro.comparar_str_a_en_b(artista, song_genius['songs'][i]['artist_names']) == True)and
        (	basta == False)):
            dict_final = song_genius['songs'][i]
            basta = True
    return dict_final

#Pre:  El diccinario con el resultado de genius e imprimir pantalla
#Post: Con el dicionario de genius podemos buscar direcctamente la url de la cancion, se podria buscar por id
#      pero nuestras pruebas muestran que la url es mas rápido, y en caso de encontrala la devuelve como string sino NULL
def buscar_letra_url(dict_final:dict, imprimir_pantalla:bool, genius):
    if(dict_final == None):
        if(imprimir_pantalla == True):
            print("No se encontró la letra")
        return None

    if(len(dict_final) != 0):
        if(imprimir_pantalla == True):
            print("Esto puede tradar.......")
        #letra = genius.lyrics(song_id = dict_final['id'], per_page = 2)
        letra = genius.lyrics(song_url = dict_final['url'])	
        if(imprimir_pantalla == True):
            print(letra)	
        return(letra)
    else:
        if(imprimir_pantalla == True):
            print("Nos se pudo encontrar la letra")
    return None

#Pre:  Recibe el artista, la cancion en string y un bool si hace falta imprimir
#Post: la funcion buscar con la api de genius la letra de una cancion pedida y devuelve la letra 
def genius_total(artista:str, nueva_track:str, imprimir_pantalla:bool):
	genius = lyricsgenius.Genius(CLIENTE_ACCESS_TOKE_GENIUS)
	song_genius = buscar_genius(nueva_track, artista, imprimir_pantalla, genius)
	resultado: dict = filtrar_resultado_genius(nueva_track, artista, song_genius)
	letra = buscar_letra_url(resultado, imprimir_pantalla, genius)
	letra = filtro.borrar_comentario(letra)
	return letra
