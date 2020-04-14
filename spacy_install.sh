#!/usr/bin/env bash

# Run this script to install necessary language packages for spaCy
if [[ "$VIRTUAL_ENV" == "" ]]; then
    source ./venv/bin/activate
fi
python -m spacy download en
