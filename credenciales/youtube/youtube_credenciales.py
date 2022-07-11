SCOPES_GABI: list = [
    'https://www.googleapis.com/auth/youtube',
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/youtubepartner"
]

SECRET_CLIENT_GABY: str = '../credenciales/youtube/configuracion/credenciales.json'
TOKEN_GABI: str = '../credenciales/youtube/configuracion/token.json'

CREDENCIALES_GABRIEL_YOUTUBE: dict = {
    "scopes": SCOPES_GABI,
    "secret_client": SECRET_CLIENT_GABY,
    'token': TOKEN_GABI
}
