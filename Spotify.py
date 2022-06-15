import os
import tekore as tk
from tekore import RefreshingToken 
from tekore import Spotify

CLIENT_ID = '9446fa59f25043cda0f3162443491415'
CLIENT_SECRET = 'ddb6635b0f8b4d999e499172db01d5f6'

def acceder_al_servicio()->Spotify:

	token: RefreshingToken = None
	configuracion = (CLIENT_ID,CLIENT_SECRET,'https://example.com/callback')

	if os.path.exists('tekore.cfg'):

		configuracion: tuple = tk.config_from_file('tekore.cfg', return_refresh=True)
		token = tk.refresh_user_token(*configuracion[:2], configuracion[3])

	elif(not token == True):

		token = tk.prompt_for_user_token(*configuracion, scope=tk.scope.every)
		tk.config_to_file('tekore.cfg', configuracion + (token.refresh_token,))

	return tk.Spotify(token)