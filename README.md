# BlogPost API

[![Build Status](https://travis-ci.com/flacode/drf_practice.svg?branch=ch-test-features)](https://travis-ci.com/flacode/drf_practice)
[![Coverage Status](https://coveralls.io/repos/github/flacode/drf_practice/badge.svg?branch=ch-test-features)](https://coveralls.io/github/flacode/drf_practice?branch=ch-test-features)
[![Maintainability](https://api.codeclimate.com/v1/badges/159c3d486314a760be7a/maintainability)](https://codeclimate.com/github/flacode/drf_practice/maintainability)

> BlogPost API is a simple application that allows users to write, read and comment on blogs. 

## Features
- Users can create accounts.
- Users can log in.
- Users can create, view, update and delete a blog post. 

## Running the tests
Within the project's root directory, run
```coverage run --source=posts manage.py test && coverage report -m```


## Getting Started
### Prerequisites
1. Install requirements, run 
```sh
     pip install -r requirements.txt
```
2. Database configuration.
   - Download and install postgres from [here](https://www.postgresql.org/download/)
   - Create database in terminal
   ```sh
      $ psql postgres;
      $ CREATE DATABASE database_name;
   ```
   - Store the database name under an environment variable called `DATABASE_URL` in the following format.
   ```sh
      $ export DATABASE_URL='postgres://USER:PASSWORD@HOST:PORT/NAME'
   ```
   
3. Switch to the project's root directory and run migrations to create database tables.
```sh 
    $ python manage.py makemigrations
    $ python manage.py migrate
 ```
 4. Then run the application.
 ```sh
    $ python manage.py runserver
 ```

## End points
### Endpoints to create a user account and login into the application
HTTP Method|End point | Public Access|Action
-----------|----------|--------------|------
POST | /entries/register/ | True | Create an account.
POST | /entries/login/  | True | Login a user.
GET  | /entries/useradmin/ | False | Return list of registered users to a super user.
GET or DELETE  | /entries/useradmin/<int:pk>/ | False | Allow super user to view user details and delete a user.
GET or PUT | /entries/user/<int:pk>/ | False | Allow a user to view their account details and update them.


## End points
### Endpoints for blog posts
HTTP Method|End point | Public Access|Action
-----------|----------|--------------|------
GET | /entries/ | True | Get all blog posts.
POST | /entries/  | False | Create a post.
GET  | /entries/<int:pk>/ | False | Retrieve a certain post.
PUT or DELETE | /entries/<int:pk>/ | Update or delete a certain post by the author.
