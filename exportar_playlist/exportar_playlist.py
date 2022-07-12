def exportar(playlist: dict, plataforma) -> None:
    archivo = open("../csv/playlist/{1}/{0}.csv".format(playlist['nombre_playlist'], plataforma), "w", newline="")
    archivo.write("Id : {0}\r\n".format(playlist['id']))
    archivo.write("Nombre : {0}\r\n".format(playlist['nombre_playlist']))
    archivo.write("Creador de la Playlist  : {0}\r\n".format(playlist['creador_playlist']))
    if(playlist["tipo_playlist"]):
        archivo.write("Tipo Playlis : Publico\r\n")
    else:
        archivo.write("Tipo Playlis : Privado\r\n")
    archivo.write("Descripcion  : {0}\r\n".format(playlist['descripcion']))
    archivo.write("URl  : {0}\r\n".format(playlist['url']))
    archivo.write("Cantidad de Canciones  : {0}\r\n".format(playlist['cantidad_canciones']))
    archivo.write("Duracion Playlist  : {0}\r\n".format(playlist['duracion_playlist']))
    archivo.write("Lista de Artistas  : {0}\r\n".format(playlist['listar_artistas']))
    archivo.write("Lista de Canciones  : {0}\r\n".format(playlist['lista_canciones']))

    archivo.close()

