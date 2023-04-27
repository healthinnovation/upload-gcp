import os
from google.cloud import storage
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request
from threading import Thread

# Set up GCS credentials
creds = Credentials.from_service_account_file('credentials/service-account.json')
creds = creds.with_scopes(['https://www.googleapis.com/auth/cloud-platform'])

# Set up GCS client
client = storage.Client(credentials=creds)

# Set up bucket name and directory
bucket_name = 'my-bucket-name'
directory = '/path/to/local/directory/'

# Define function to upload file to GCS using resumable uploads
def upload_file_to_gcs(filename):
    try:
        blob = client.bucket(bucket_name).blob(filename)
        chunk_size = 5 * 1024 * 1024 # 5 MB
        upload_url = blob.create_resumable_upload_session().get('session_url')
        with open(os.path.join(directory, filename), 'rb') as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break
                headers = {'Content-Type': 'application/octet-stream'}
                request = Request(upload_url, headers=headers, method='PUT', body=chunk)
                resp = request.run()
                if resp.status_code == 308:
                    offset = int(resp.headers['range'].split('-')[1]) + 1
                    request.headers['Content-Range'] = f'bytes {offset}-*/{os.path.getsize(os.path.join(directory, filename))}'
                else:
                    raise Exception(f"Failed to upload chunk: {resp.status_code} {resp.text}")
    except Exception as e:
        print(f"Error uploading file {filename}: {str(e)}")
        return False
    else:
        print(f"File {filename} uploaded successfully")
        return True

if __name__ == '__main__':
    # Get list of files in directory
    files = os.listdir(directory)
    # Filter list to include only files
    files = [f for f in files if os.path.isfile(os.path.join(directory, f))]
    # Sort list of files alphabetically
    files.sort()
    # Get last uploaded file (if any) from GCS bucket
    try:
        bucket = client.get_bucket(bucket_name)
        last_uploaded_file = bucket.get_blob('last_uploaded_file.txt').download_as_text().strip()
    except Exception:
        last_uploaded_file = None
    # Upload each file to GCS, starting with the last uploaded file (if any)
    for filename in files:
        if last_uploaded_file is None or filename > last_uploaded_file:
            if upload_file_to_gcs(filename):
                # Update last uploaded file in GCS bucket
                bucket.blob('last_uploaded_file.txt').upload_from_string(filename)
