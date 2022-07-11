import os

import tekore as tk
from tekore import RefreshingToken
from tekore import Spotify


def generar_servicio_spotify(credenciales: dict) -> Spotify:
    """
    Precondicion: Tener CLIENT ID and SECRET y haber ingresado la URL
    Poscondicion: Haber dado acceso completo, copiando la URL en la consola
    """

    token: RefreshingToken = None
    id, secret, url, tekore_user = (credenciales["id"], credenciales["secret"], credenciales["url"], credenciales["tokere_user"])
    configuracion = (id, secret, url)
    if os.path.exists(tekore_user):

        configuracion: tuple = tk.config_from_file(tekore_user, return_refresh=True)
        token = tk.refresh_user_token(*configuracion[:2], configuracion[3])

    elif not token == True:

        token = tk.prompt_for_user_token(*configuracion, scope=tk.scope.every)
        tk.config_to_file(tekore_user, configuracion + (token.refresh_token,))

    return tk.Spotify(token)
