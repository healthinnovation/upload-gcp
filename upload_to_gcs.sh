#!/bin/bash

# Set the path to your GCS bucket
BUCKET_NAME=gs://inl-mvp-d-gcs-useast4-mvp-b2f455

# Set the path to the local folder containing the files to upload
LOCAL_FOLDER=./data

# Set the path to the remote folder where the files will be uploaded
REMOTE_FOLDER=harmonize/landing

# Set the path to your service account JSON key file
export GOOGLE_APPLICATION_CREDENTIALS=./credentials/service_account_key.json

# Upload each file in the local folder to the remote folder in the GCS bucket
cd "$LOCAL_FOLDER"
find . -type f | while read FILE; do
    gsutil cp -r "$FILE" "$BUCKET_NAME/$REMOTE_FOLDER/${FILE#./}"
done
