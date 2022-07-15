from credenciales.spotify.spotify_credenciales import CREDENCIALES_GABRIEL_SPOTIFY, CREDENCIALES_FEDE_SPOTIFY
from credenciales.youtube.youtube_credenciales import CREDENCIALES_GABRIEL_YOUTUBE

USUARIOS: list = [
            {
                'user': "gabi",
                'password': "1234",
                'plataformas': [
                    {
                        "nombre": "spotify",
                        "credenciales": CREDENCIALES_GABRIEL_SPOTIFY
                    },
                    {
                        "nombre": "youtube",
                        "credenciales": CREDENCIALES_GABRIEL_YOUTUBE
                    },
                ]
            },
            {
                'user': "fede",
                'password': "1234",
                'plataformas': [
                    {
                        "nombre": "spotify",
                        "credenciales": CREDENCIALES_FEDE_SPOTIFY
                    }
                ]
            }
        ]
