# SUMMARY
A simple APP built using `django-restframework` for a bookshop library.

## Functions
The app have the following functions
#### Views
 - Users
   - Anonymous Users can `GET` all users information also have the ability to create accounts
   - Other users functions are being controlled by the permissions assigned to users
   - Default user have no permissions assigned to them on `User` models
 - Groups
   - `Library-admin` group have the permissions `add-change-view` on all models `Book, Author, Publisher and Borrowed`
   - `Authors` group can view all other `authors` and change their own object, can `ADD` books and `CHANGE` their own books
   - `Library-users` group is a very basic user where he can `CHANGE` his own `user/profile` object.
#### Models
 - User: the hold user accounts
 - UserProfile: to store non-authentication user info
 - Books: to store Books
 - Authors: Authors should be registered users
 - Publisher: to store Publishers info.
 - Genre: to store Books genres
 - Borrowed: to store user rented books


## Notes for developer
### Writing Code
The code is organized by environment, as detailed below. Refer heavily to the Terraform docs for the specifics of each data source, resource, providers, and more.

Ensure you have activated the pre-commit hooks by [installing pre-commit](http://pre-commit.com/#install "pre-commit install")
```bash
pre-commit install
```
from the root of the repo. Now, every commit will be tested for a few easily-fixable errors and formatting.

### Steps to clone
 -  git clone `https://github.com/ahaffar/bookshop.git`
 - install the required packages
```bash
 sudo apt install python3 python3-dev git libmysqlclient-dev
 sudo apt-get install python3-venv
 sudo apt install build-essential
 ```
 - cd the new created directory by Step 1
 - python3 -m venv venv `this would create a new virtual-env called venv in a subdirectory venv, the venv name is added to .gitignore file`
 - modify the database settings on the `settings.py` file
 - run `python manage.py server`

 ### DB Diagram
 The DB diagram had been created using dbdiagram.io `A free, simple tool to draw ER diagrams by just writing code.
Designed for developers and data analysts. `

 Full example can be [found on](https://dbdiagram.io/d/5efee7800425da461f043365)

![alt text](https://ipolls-assets.s3.us-east-2.amazonaws.com/bookshop_db_2.png "Bookshop db diagram")
