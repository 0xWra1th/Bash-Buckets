#!/bin/bash

# Setting up Django and Bash Buckets App

cd project
python3 manage.py migrate

echo ""
echo "You will now be prompted to create a new account: "
python3 manage.py createsuperuser

echo ""
echo "-------------------"
echo "| Setup complete! |"
echo "-------------------"
