#!/bin/bash

# create virtual environment if it does not exist
if [ ! -d "venv" ]
then
    python -m venv venv
fi

# activate virtual environment
source venv/bin/activate

# install/update requirements
pip install -r requirements.txt

# run script
python src/upload_to_gcs.py "$@"
