import os

from tekore import Spotify

from constantes.constantes import SALIR, INICIO
from plataformas.spotify.menu import menu_spotify
from plataformas.spotify.servicio import generar_servicio_spotify
from plataformas.youtube.servicio import generar_servicios_youtube
from validar.input_platataforma import validar_input
from vistas.vista import linea_divisora

PLATAFORMAS: list = ["youtube", "spotify"]


def menu_plataformas(usuario: dict) -> str:

    spotify: Spotify = generar_servicio_spotify(usuario["plataformas"][0]["credenciales"])
    youtube = generar_servicios_youtube(usuario["plataformas"][1]["credenciales"])

    os.system("clear")
    print("PLATAFORMAS: Youtube | Spotify ")
    linea_divisora()
    nombre_plataforma: str = validar_input(PLATAFORMAS, "Plataforma")

    if nombre_plataforma == usuario["plataformas"][0]["nombre"]:
        menu_spotify(spotify, youtube)
    else:
        print("hola")
    salir_plataforma: str = input("Si desea Salir del organizador de paltaformas oprima? Si/No: ")
    if salir_plataforma == "Si":
        return SALIR
    else:
        return INICIO