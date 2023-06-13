#!/bin/bash
set -euo pipefail
# Set your Google Cloud Storage bucket name
bucket_name="inl-mvp-d-gcs-useast4-mvp-b2f455"

# `set -euox pipefail`

CLOUD_RUN_TASK_INDEX=${CLOUD_RUN_TASK_INDEX:=0}
CLOUD_RUN_TASK_ATTEMPT=${CLOUD_RUN_TASK_ATTEMPT:=0}

# Read the file line by line
while IFS= read -r line
do
    # Split the line into source and target paths
    source_path=$(echo "$line" | cut -d ' ' -f1)
    target_path=$(echo "$line" | cut -d ' ' -f2)
    # Remove the trailing slash from the source path
    source_path=$(echo "$source_path" | sed 's:/$::') # remove trailing slash
    # Remove the leading slash from the target path
    target_path=$(echo "$target_path" | sed 's:^/::') # remove leading slash
    # Copy the blob from source to target
    gsutil cp gs://${bucket_name}/${source_path} gs://${bucket_name}/${target_path}
    
done < results.txt

echo "Completed Task #${CLOUD_RUN_TASK_INDEX}."