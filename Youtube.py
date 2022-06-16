from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

import os
 
SCOPES = ['https://www.googleapis.com/auth/youtube',
		  "https://www.googleapis.com/auth/youtube.force-ssl",
          "https://www.googleapis.com/auth/youtube.readonly",
          "https://www.googleapis.com/auth/youtubepartner"]

ARCHIVO_SECRET_CLIENT = 'credenciales.json'
ARCHIVO_TOKEN = 'token.json'

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


def generar_servicio()->None:

    creds = None
    
    if os.path.exists(ARCHIVO_TOKEN):

        creds = Credentials.from_authorized_user_file(ARCHIVO_TOKEN, SCOPES)
    
    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:

            creds.refresh(Request())

        else:

            flow = InstalledAppFlow.from_client_secrets_file(ARCHIVO_SECRET_CLIENT, SCOPES)
            creds = flow.run_local_server(port=0)
        

        with open(ARCHIVO_TOKEN, 'w') as token:

            token.write(creds.to_json())

    return build('youtube', 'v3', credentials = creds)
