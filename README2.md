# bookzilla
A book sharing web app written in Python / Django

###### Authors
* Ananth Murthy 
* Chandan Yeshwanth 

Bookzilla is a book-sharing application written in Python using the Django Framework. Before deploying, you need to install the prerequisites.

### Prerequisites

1. Python (version 2.7 or higher)

2. Git

3. Django (version 1.7 or higher)

4. Pip, the Python Package Manager 

5. SQLite 3 (using apt-get)

### Deploying

* Get the source from the repository using git pull

* Enter the source folder and run python manage.py migrate. You should see a list of SQL commands being applied.

* Install the required Django plugins by running pip install -r requirements.txt from the root of the source folder

* Create a superuser using python manage.py createsuperuser and follow the instructions on screen.

* Enter the administration interface with the account you just created at localhost:8000/admin, go to Groups and create a new group called Couriers.

* To start the local development server, run python manage.py runserver

	- You can now use the website on localhost:8000

	- The courier interface is at localhost:8000/courier/login

* To run the webserver on a specific IP and port, run python manage.py <IP>:<port>

* You can then stop the server using Ctrl+C
