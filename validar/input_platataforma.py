def validar_input(lista: list, contexto: str) -> str:
    valor_corte: int = 1
    dato: str = input("Ingresar {0}: ".format(contexto))

    while valor_corte != -1:
        for item in lista:
            if item == dato.lower():
                valor_corte = -1
        if valor_corte == 1:
            print("El dato ingresao es inconrrecto")
            dato = input("Vuelva a ingresar {0} ".format(contexto))

    return dato.lower()


def validar_input_cancion() -> str:
    nombre_cancion: str = input("Ingresar nombre de la cancion: ")
    contador: int = 0
    while contador != -1:
        if len(nombre_cancion) == 0:
            print("Los campos no pueden ser nulos ")
            nombre_cancion: str = input("Ingresar nombre de la cancion: ")
        else:
            contador = -1

    return nombre_cancion


def validar_input_titulo_playlist(lista_playlist: list) -> str:
    valor_corte: int = 1
    dato: str = input("Ingresar nombre de la playlist : ")
    while valor_corte != -1:
        for playlist in lista_playlist:
            if playlist["nombre_playlist"].find(dato) != -1:
                return dato
        if valor_corte == 1:
            print("La playlist no existe")
            dato: str = input("Ingresar nombre de la playlist a sincronizar: ")
    return dato
