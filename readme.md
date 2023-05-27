[![Build Status](https://travis-ci.org/NeverWalkAloner/async-blogs.svg?branch=master)](https://travis-ci.org/NeverWalkAloner/async-blogs)

# Asynchronous API implementation with Python and FastAPI

## How to run

Run

````
$ docker-compose up -d --build
````

and go to http://127.0.0.1:8000/docs

## How to run tests

````
$ docker-compose exec app python -m pytest app/tests
````

## Update

Starting from version 1.4 SQLAlchemy supports asyncio. This means you don't need externla tools like `encode/databases`. 
If you are interesting in new styled SQLAlchemy async example you can check [this repo](https://github.com/NeverWalkAloner/secureblogs).
