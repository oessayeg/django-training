#!/bin/sh

pip3 --version
rm -rf local_lib
pip3 install --target=local_lib git+https://github.com/jaraco/path > installation.log

python3 my_program.py