# Installation, Setup and Testing

This system is designed to be hosted on a Linux Debian 10 machine.

## Automatic Installation and Setup

1) Run the install.sh script -> ```./install.sh```

2) Run the setup.sh script -> ```./setup.sh``` 

3) You will be prompted to create a new admin account, provide required details.

4) To run the server use the start.sh script -> ```./start.sh```

## Manual Installation and Setup

1) Install dependencies for bash scripts:
   * Some or most of these packages may already be installed, just run the commands below and they will install if not installed already.
   * systemd -> ```sudo apt install systemd```
   * sysstat -> ```sudo apt install sysstat```
   * original-awk -> ```sudo apt install original-awk```
   * sqlite3 -> ```sudo apt install sqlite3```

2) Install Python and Modules:
   * Run the commands given within the Bash-Buckets directory
   * Python3 -> ```sudo apt install python3```
   * Pip -> ```sudo apt install python3-pip```
   * Modules -> ```pip3 install -r requirements.txt```

3) Setup and Run Django and the App:
   * Go to the root directory -> ```"Bash-Buckets"```
   * Go into 'project' where 'manage.py' is present -> ```"Bash-Buckets/project/manage.py"```
   * Run: ```python3 manage.py migrate```
   * Run: ```python3 manage.py runserver```
   * The server is now running and you can connect to it via localhost:8000
   * Run: ```python3 manage.py createsuperuser```
   * This will prompt you for details, provide account details for your new superuser account.

## Testing

   * Start the server by running the start script -> ```./start.sh```
   * Inside the root directory you will find a testing folder containing 'Tests.py' -> ```"Bash-Buckets/testing/Tests.py"```
   * Run: ```python3 Tests.py <superuser-username> <superuser-password>```
   * This will run the tests and confirm that the App if functioning correctly