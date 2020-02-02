# secretary
Manage my time, schedule, memory, etc...

**The Project Environment is managed by [Pipenv](https://pipenv.kennethreitz.org/)**

## Getting Started

### Requirements
Python 3.8+
MySQL 5.7

### Install Dependencies
$ pipenv install --dev
If occur mysql client error, link

### Setup Local Infrastructure

#### Startup
```bash
$ docker-compose up -d
```

#### Shutdown
```bash
$ docker-compose up down
```

### Database migration

#### Migrate Tables and Set Initial Data
```bash
$ pipenv shell

(secretary)$ python manage.py makemigrations
(secretary)$ python manage.py migrate
(secretary)$ python manage.py createsuperuser
```

### Run

#### Django Development Server
```bash
$ pipenv shell

(secretary)$ python manage.py runserver
```

If want to configure environment variables, edit .env after copy .env.example to .env.

## Appendix

### Mysqlclient Install Error

* [Prerequisites](https://pypi.org/project/mysqlclient/)

```shell script
$ export PATH="/usr/local/opt/openssl/bin:$PATH"
$ export LDFLAGS="-L/usr/local/opt/openssl/lib"
$ export CPPFLAGS="-I/usr/local/opt/openssl/include"

$ pipenv install
```
