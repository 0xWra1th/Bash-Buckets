## Install, Setup and Run Bash Buckets

This systen is designed to be hosted on a Linux Debian 10 machine.

1) Install dependencies for bash scripts:
   * Some or most of these packages may already be installed, just run the commands below and they will install if not installed already.
   * systemd -> ```sudo apt-get install systemd```
   * sysstat -> ```sudo apt-get install sysstat```
   * original-awk -> ```sudo apt-get install original-awk```

2) Install Python and Modules:
   * Run the commands given within the Bash-Buckets directory
   * Python3 -> ```sudo apt-get install python3```
   * Modules -> ```pip3 install -r requirements.txt```

3) Setup and Run Django and the App:
   * Go to the root directory -> ```"Bash-Buckets"```
   * Go into 'project' where 'manage.py' is present -> ```"Bash-Buckets/project"```
   * Run: ```python3 manage.py createsuperuser```
   * This will prompt you for details, provide account details for your new superuser account.
   * Run: ```python3 manage.py makemigrations```
   * Run: ```python3 manage.py migrate```
   * Run: ```python3 manage.py runserver```
   * The server is now running and you can connect to it via localhost:8000

4) Testing:
   * Inside the main Bash-Buckets directory you will find a testing folder containing 'Tests.py' -> ```"Bash-Buckets/testing"```
   * While the server is running go to the admin page, login with you superuser credentials and get the superuser account token
   * Run: ```python3 Tests.py <superuser-token>```
   * This will run the tests and confirm that the App if functioning correctly