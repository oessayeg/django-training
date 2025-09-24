#!/bin/sh

pip --version
rm -rf local_lib
pip install --target=local_lib git+https://github.com/jaraco/path > installation.log

python3 my_program.py