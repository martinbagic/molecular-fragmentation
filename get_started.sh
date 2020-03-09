#!/bin/bash
virtualenv .env --python=python3.6
source .env/bin/activate
pip install -r requirements.txt