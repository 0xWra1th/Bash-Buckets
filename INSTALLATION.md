## Install, Setup and Run Bash Buckets

This systen is designed to be hosted on a Linux Debian 10 machine.

1) Install dependencies for bash scripts:
   * Some or most of these packages may already be installed, just run the commands below and they will install if not installed already.
   * systemd -> ```sudo apt-get install systemd```
   * sysstat -> ```sudo apt-get install sysstat```
   * original-awk -> ```sudo apt-get install original-awk```

2) Install Python and Modules:
   * Run the commands given
   * Python3 -> ```sudo apt-get install python3```
   * Django -> ```pip3 install django```
   * python-magic -> ```pip3 install python-magic```
   * requests -> ```pip3 install requests```

3) Setup and Run Django and the App:
   * Go to the directory where you have all the files -> ```"Bash-Buckets"```
   * Go into 'project' where 'manage.py' is present -> ```"Bash-Buckets/project"```
   * Run: ```python3 manage.py createsuperuser```
   * This is prompt you for details, provide account details for the superuser account you wish to create.
   * Run: ```python3 manage.py makemigrations```
   * Run: ```python3 manage.py migrate```
   * Run: ```python3 manage.py runserver```
   * The server is now running and you can connect to it via localhost:8000

4) Testing:
   * Inside the main Bash-Buckets directory you will find a testing folder containing 'Tests.py' -> ```"Bash-Buckets/testing"```
   * While the server is running go to the admin page, login with you superuser credentials and get the superuser account token
   * Run: ```python3 Tests.py <superuser-token>```
   * This will run the tests and confirm that the App if functioning correctly