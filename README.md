# Book_Bay

Please refer readme from gihub https://github.com/Anshul718/Book_Bay/ for details.

## Requirements :
   * Python environment
   * Django
   * mysql client and server

## Steps to follow (linux):
  * option1:
    * sudo pip install virtualenv
    * mkdir envs
    * virtualenv ./envs/
    * source envs/bin/activate
  * option2:
    * any python environment (eg. anaconda, virtualenv (as shown above), etc.)
    
  * pip install Django
  * pip install mysql
  * pip install isbnlib==3.6.1
  * git clone "https://github.com/Anshul718/Book_Bay.git"
  * open terminal in root directory of project
  * login to mysql account
  * run command 'source <path_to_schema.sql>' (this will create 'book_bay' database in your mysql)
  * open settings.py in bookbay folder and change the database setting according to your user account
  * open terminal in Book_Bay directory and run following commands
  * python manage.py makemigrations
  * python manage.py migrate
  * python manage.py runserver
