python 3.7.5
channels==3.0.1
channels-redis==2.4.2
Django==3.1.4
mysqlclient==2.0.3

> Database files are in /database

To run:

    1. Install packages:
        `pip install requirements.txt`
    2. Configure settings:
        2.1. Find variable named `DATABASE`
            2.1.1. Modify `'name', 'user', 'password`' depending on your local mysql.
        2.2. Find variables named `EMAIL_HOST_USER, EMAIL_HOST_PASSWORD`
            2.2.1. Change it to your preferred email and password.
    3. Run server:
        Run the following commands:

        `conda activate [your_path_to_anaconda_libs]` (*optional*, if you use anaconda to manage your libraries)
        `env\scripts\activate` (enter virtual environment)\

```
     py manage.py runserver
```
