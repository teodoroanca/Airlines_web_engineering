# Airlines api README

**For course: Web engineering**

## Installation

Install python
```shell
$ sudo apt-get update
$ sudo apt-get install python3.6
```

Install virtualenv
```shell
$ pip install --user virtualenv
```

## Configuration and running

Create a virtual environment for this project
```shell
virtualenv airlines_api
```

Activate the virtual environment for this project
```shell
source <path-of-the-newly-created-environment>/bin/activate
```

Navigate into the root folder of the project
```shell
cd  <project-path>/airlines_api
```

Install requirements of the project
```shell
pip install -r requirements.txt
```

Start the development server
```shell
./manage.py runserver
```

**In case a fresh database is desired:**

Delete "db.sqlite3" file

```shell
./manage.py migrate
```
Now import the data from the json
```shell
./manage.py import_json
```

Start the development server
```shell
./manage.py runserver
```
