# Book_Bay
## Requirements :
   * Python 2.7
   * Django version 1.7
   * SQLite 3 (using apt-get)

## Steps to follow:
  * sudo pip install virtualenv
  * mkdir envs
  * virtualenv ./envs/
  * source envs/bin/activate
  * pip install Django==1.7.11
  * sudo apt-get install sqlite3 libsqlite3-dev
  * git clone "https://github.com/Anshul718/Book_Bay.git"
  * python manage.py migrate
  * go to root directory of project
  * pip install -r requirements.txt 
  * python manage.py createsuperuser
  * now create superuser to login into book sharing system
  * Enter the administration interface with the account you just created at localhost:8000/admin, go to Groups and create a new group called Couriers
  * run python manage.py runserver
  * open http://localhost:8000/
