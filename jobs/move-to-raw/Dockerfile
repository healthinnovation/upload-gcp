# Use the official Google Cloud SDK base image
FROM google/cloud-sdk:alpine

# Install necessary dependencies
RUN apk add --no-cache bash

# Set the working directory in the container
WORKDIR /app

# Copy the script and results.txt file to the container
COPY copy_blobs.sh .
COPY results.txt .

# Set the script as executable
RUN chmod +x copy_blobs.sh

# Set the command to run the script
CMD ["./copy_blobs.sh"]