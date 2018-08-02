# BlogPost API

[![Build Status](https://travis-ci.com/flacode/drf_practice.svg?branch=develop)](https://travis-ci.com/flacode/drf_practice)
[![Coverage Status](https://coveralls.io/repos/github/flacode/drf_practice/badge.svg?branch=develop)](https://coveralls.io/github/flacode/drf_practice?branch=ch-test-features)
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

**Base url:** http://localhost:8000/api/v1/

## End points
### Endpoints to create a user account and login into the application
HTTP Method|End point | Public Access|Action
-----------|----------|--------------|------
POST | /posts/register/ | True | Create an account.
POST | /posts/login/  | True | Login a user.
GET  | /posts/admin/ | False | Return list of registered users to a super user.
GET or DELETE  | /posts/admin/<int:pk>/ | False | Allow super user to view user details and delete a user.
GET or PUT | /posts/user/<int:pk>/ | False | Allow a user to view their account details and update them.


## End points
### Endpoints for blog posts
HTTP Method|End point | Public Access|Action
-----------|----------|--------------|------
GET | /posts/ | True | Get all blog posts.
POST | /posts/  | False | Create a post.
GET  | /posts/<int:pk>/ | False | Retrieve a certain post.
PUT or DELETE | /posts/<int:pk>/ | False | Update or delete a certain post by the author.
