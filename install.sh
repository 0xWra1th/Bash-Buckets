#!/bin/bash

# Installing dependencies for Bash Buckets:
#   1) systemd 
#   2) sysstat 
#   3) original-awk 
#   4) sqlite3 python3 
#   5) python3-pip

sudo apt install systemd sysstat original-awk sqlite3 python3 python3-pip

# Installing python module requirements:
#   1) Django
#   2) Python-magic
#   3) Requests

pip3 install -r requirements.txt

echo ""
echo "--------------------------"
echo "| Installation complete! |"
echo "--------------------------"
