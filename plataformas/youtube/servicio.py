from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import os.path
import os


def generar_servicios_youtube(credenciales: dict) -> 'googleapiclient.discovery.Resource':

    # Precondicion: Tener las credenciales y una cuenta de google
    # Poscondicion: Haber dado acceso completo a esta app

    creds = None

    if os.path.exists(credenciales['token']):
        creds = Credentials.from_authorized_user_file(credenciales['token'], credenciales['scopes'])

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:

            creds.refresh(Request())

        else:

            flow = InstalledAppFlow.from_client_secrets_file(credenciales['secret_client'], credenciales['scopes'])
            creds = flow.run_local_server(port=0)

        # Lo guarda en un archivo "token.json"
        with open(credenciales['token'], 'w') as token:

            token.write(creds.to_json())

    # usa el token y crea el acceso a la API de youtube
    return build('youtube', 'v3', credentials=creds)