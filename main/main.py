from constantes.constantes import INICIO, SALIR
from login.login import login
from plataformas.plataforma import menu_plataformas
from vistas.vista import pantalla_inicio

if __name__ == '__main__':

    palabra_corte: str = INICIO

    while palabra_corte != SALIR:
        pantalla_inicio()
        usuario: dict = login()
        if bool(usuario):
            palabra_corte = menu_plataformas(usuario)
        else:
            palabra_corte = SALIR
