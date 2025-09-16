import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_file_to_gdrive(local_file_path, drive_folder_id=None, credentials_path='credentials.json'):
    """
    Uploads a file to Google Drive using a service account.
    Args:
        local_file_path (str): Path to the file to upload.
        drive_folder_id (str): Optional. Google Drive folder ID to upload into.
        credentials_path (str): Path to service account credentials JSON.
    Returns:
        file_id (str): The ID of the uploaded file on Google Drive.
    """
    SCOPES = ['https://www.googleapis.com/auth/drive.file']
    creds = service_account.Credentials.from_service_account_file(credentials_path, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)

    file_metadata = {'name': os.path.basename(local_file_path)}
    if drive_folder_id:
        file_metadata['parents'] = [drive_folder_id]

    media = MediaFileUpload(local_file_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    return file.get('id')

# Example usage:
# file_id = upload_file_to_gdrive('uploads/BILL.xlsx', drive_folder_id='your_folder_id')
# print('Uploaded file ID:', file_id)
