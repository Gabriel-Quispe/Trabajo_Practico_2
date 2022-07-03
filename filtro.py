#Pre:  que ambas variables seans strings
#Post: La funcion compara si a se encuentra dentro de b, devuelve True si es ese el caso o False de lo contrario
def comparar_str_a_en_b(a:str, b:str) -> bool:
	a1:str = a.replace(" ","")
	b1:str = b.replace(" ","")
	if(a1.lower() in  b1.lower()):
		return True
	return False

#Pre:  Recibe dos strings
#Post: Si la duncion encuentra basura en nueva track, la borra, luego devuelve el string modificado, 
# 	   si no encuentra nada lo devuelve como lo recibió
def filtrar_string(nueva_track:str, basura:str) -> str:
	final:str = nueva_track
	basura:str = basura.lower()
	nueva_track =  nueva_track.lower()
	if(comparar_str_a_en_b(basura, nueva_track) == True):
		final = nueva_track.replace(basura, "")
	return final

#Pre:  Recibe dos string, uno del artista, y la cancion
#Post: la funcion filtra palabras que podrian aparecer en ambos string las cuales perjudicarian el programa
#      al momento de compara string, esto se encuentra m,çucho mas presente en youtube, 
#      pero tambien lo aplicamosa para spotify
def filtrar_palabras_titulo(canal:str, cancion:str) -> tuple:
	canal = filtrar_string(canal, "vevo")
	canal = filtrar_string(canal, "official")
	canal = filtrar_string(canal, "oficial")
	canal = filtrar_string(canal, "channel")
	canal = filtrar_string(canal, "canal")
	canal = filtrar_string(canal, "music")
	canal = filtrar_string(canal, "musica")
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
	cancion = filtrar_string(cancion, "español")
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

#Pre:  Recibe el string de la letra de la cancion
#Post: La funcion borra los comentarios que pone genius en la letra como la numeracion de versos
def borrar_comentario(letra:str) -> str:
	if(letra == None):
		return None
	while("[" in letra):
		lista_aux1:list = []
		lista_aux1.append(letra[0 : letra.index("[")])
		lista_aux1.append(letra[letra.index("]") + 1 :])
		letra = "".join(lista_aux1)
	letra = letra[letra.index("Lyrics") + 6:]
	letra = letra[0: len(letra) - 8]
	return letra

#Pre:  Recibe un dicciorio que tiene como claves las palabras y valor la cantidad de veces que se dice 
#      hace falta que el diccionario esté creado pero no pasa nada si está vacio
#Post: La funcion primero reemplaza algunos de los caracretes mas comunes lso cuales se encuentran inmediatamnte
#      al lado de la plabra por lo que al momento de hacer split con espacio puede haber errores al momento de comaprar
#      por ejemplo "casa" y "casa," las tomaria como dos pàlabras diferentes.
#      Luego las separa y mete en el diccionario dado.
def diccionario_de_palabras(dicc:dict, letra:str) -> None:
	if(letra == None):
		return
	lista_palabras:list = []
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

def convertir_diccionario(repes:dict) -> list:
	dic_a_lista:list = []
	dic_a_lista = list(repes.items())
	dic_a_lista.sort(key = lambda x:x[1] , reverse = True)
	for i in range(10):
		print(f"Top {i}:  {dic_a_lista[i][0]} con {dic_a_lista[i][1]} ocurrencias")
	#print(json.dumps(repes, indent = 3))
	return dic_a_lista