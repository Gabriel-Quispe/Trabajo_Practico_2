import time

from usuario.usuario import USUARIOS
from vistas.vista import linea_divisora


def login() -> dict:

    TIME: float = 5.0
    contador: int = 0
    user_input: str = input("Ingresar el usuario: ")
    password_input: str = input("Ingresar contraseña: ")

    while contador != 3:
        for user in USUARIOS:
            if user["user"] == user_input and user["password"] == password_input:
                return user
        print("El usuario no existe, ingresar nuevamente el usuario y contraseña: ")
        linea_divisora()
        user_input: str = input("Ingresar el usuario: ")
        password_input: str = input("Ingresar contraseña: ")
        contador = contador + 1
        if contador == 3:
            print("Si no recuerdas tu usuario y contraseña comunicarse con el equipo TEAM 7")
            time.sleep(TIME)
    return {}

