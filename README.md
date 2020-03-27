# Book_Bay
## Requirements :
   * PyCharm Professional (only for development, not required for running the project)
   * Python environment
   * Django
   * mysql client and server

## Steps to follow (linux):
  * sudo pip install virtualenv
  * mkdir envs
  * virtualenv ./envs/
  * source envs/bin/activate
  * pip install Django
  * pip install mysql
  * git clone "https://github.com/Anshul718/Book_Bay.git"
  * open terminal in root directory of project
  * login to mysql account
  * run command 'source <path to schema.sql>' (this will create 'book_bay' database in your mysql)
  * open settings.py in bookbay folder and change the database setting according to your user account
  * python manage.py makemigrations
  * python manage.py migrate
  * python manage.py runserver
