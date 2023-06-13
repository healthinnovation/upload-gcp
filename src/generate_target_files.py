import os
import re
from datetime import datetime
from google.cloud import storage
from google.oauth2.service_account import Credentials

# Set up GCS credentials
creds = Credentials.from_service_account_file('../credentials/service-account.json')
creds = creds.with_scopes(['https://www.googleapis.com/auth/cloud-platform'])

# Set up GCS client
def generate_target_folder(filepath):
    # Extract information from the source file path
    # pattern = r'harmonize/landing/(\d+)-(\d{2}\.\d{2}\.\d{2})/DCIM/DJI_(\d{8})(\d{4})_\d{3}_(.*)/DJI_(\d{8})(\d{2})_(\d+)_(.*).JPG'
    pattern = r'harmonize/landing/(?:\d+-)?(\d{2}\.\d{2}\.\d{2})/DCIM/DJI_(\d{8})(\d{4})_\d{3}_(.*)/DJI_(\d{8})(\d{6})_(\d+)_(.*).JPG'

    match = re.match(pattern, filepath)
    
    if not match:
        return None
        # raise ValueError('Invalid file format: ' + filepath)

    if len(match.groups()) == 8:
        _, _, _, village, yyyymmdd2, hhmm2, sequential_id, file_type = match.groups()
    else:
        _, _, _, _, village, yyyymmdd2, hhmm2, sequential_id, file_type = match.groups()

    # Convert date and time components to datetime object
    # source_datetime = datetime.strptime(yyyymmdd2 + hhmm2, '%Y%m%d%H%M')

    # Generate the target folder structure
    target_folder = f'harmonize/raw/drone-imagery/{yyyymmdd2}/{file_type}/{village}/{yyyymmdd2}{hhmm2}_{sequential_id}.JPG'
    
    return target_folder

def generate_target_files(bucket_name, file_list_path):
    # Instantiate a GCS client
    client = storage.Client(credentials=creds)
    
    # Get the bucket and list all blobs (files) in the bucket
    bucket = client.get_bucket(bucket_name)
    blobs = bucket.list_blobs(prefix='harmonize/landing/')
    
    # Iterate through each blob in the bucket
    target_names = []
    for blob in blobs:
        # Extract the filename from the blob path
        filename = blob.name
        
        # Generate the target folder path
        target_folder = generate_target_folder(filename)
        if target_folder is None:
            with open('invalid_files.txt', 'a') as file:
                file.write(filename + '\n')
            continue
        target_name = os.path.join(filename,' ', target_folder)
        target_names.append(target_name)
    
    # Write the target names to a file
    with open(file_list_path, 'w') as file:
        file.write('\n'.join(target_names))
    
    print(f'Target file list created successfully: {file_list_path}')

# Example usage
bucket_name = 'inl-mvp-d-gcs-useast4-mvp-b2f455'
file_list_path = './results.txt'

generate_target_files(bucket_name, file_list_path)
