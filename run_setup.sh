#!/bin/bash

python -m venv .venv
source .venv/bin/activate
which python
python --version

pip install .

echo 'Setup complete!'
