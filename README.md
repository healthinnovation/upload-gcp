# upload-gcp

This is a Python script for uploading files to Google Cloud Storage (GCS). It includes support for multi-threaded uploads, and can automatically resume uploading from the last successful upload in case of a failure.

## Getting Started

To use this script, you'll need:

* Python 3.10
* A Google Cloud Storage bucket
* Google Cloud Storage credentials with access to the bucket


## Usage

### Uploading Files to GCS

To upload files to GCS, run the `run_upload_to_gcs.sh` script with the following arguments:

* `--bucket`: the name of the GCS bucket to upload the files to
* `--directory`: the path to the directory containing the files to upload
* `--credentials`: the path to the GCS credentials file

For example, to upload files in the `data` directory to a GCS bucket named `my-bucket`, run the following command:

```
./run_upload_to_gcs.sh --bucket my-bucket --directory data --credentials path/to/credentials.json
```


### Running Unit Tests

To run the unit tests for the script, run the `run_tests.sh` script:

```
$ chmod +x run_tests.sh
$ ./run_tests.sh
```