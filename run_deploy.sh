#!/bin/bash
source venv/bin/activate
pip install --upgrade langchain-google-vertexai cloudpickle langchain-core
python3 deploy.py
