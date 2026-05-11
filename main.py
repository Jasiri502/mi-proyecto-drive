import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Si cambias estos permisos, borra el archivo token.json
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def main():
    creds = None
    # El archivo token.json se crea automáticamente al iniciar sesión la primera vez
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # Si no hay credenciales válidas, inicia el flujo de inicio de sesión
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Guarda las credenciales para la siguiente ejecución
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Conexión con el servicio de Google Drive
    service = build('drive', 'v3', credentials=creds)

    # Solicitar la lista de los 10 archivos más recientes
    print("Conectando con Google Drive...")
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No se encontraron archivos en tu unidad.')
    else:
        print('--- Lista de Archivos ---')
        for item in items:
            print(f"Nombre: {item['name']} | ID: {item['id']}")

if __name__ == '__main__':
    main()