## Why struct is important
You should follow this struct because it is important for jija.
Jija uses this struct to find apps and models.
If you don't follow this struct, jija will not work properly.
If u want to change this struct, you can do it in ``settings.py``.

## What is core app
Core app is a special app, definition of this app is optional.
If you want to create some middleware or something else that will be used in all apps, you should create it in core app.

## Default struct
    my_project
    │
    ├── apps
    │   ├── first_app
    │   │   ├── app.py (defenition of app if you need else you can only create file)
    │   │   ├── models.py (database models if you need)
    │   │   ├── routes.py
    │   │   └── views.py
    │   └── seecnd_app
    │       ├── app.py
    │       ├── models.py
    │       ├── routes.py
    │       ├── views.py
    │       └── sub_app  
    │           ├── app.py
    │           ├── models.py
    │           ├── routes.py
    │           └── views.py
    ├── core (if you need)
    │   ├── app.py
    │   ├── models.py
    │   ├── routes.py
    │   └── views.py
    ├── main.py
    ├── settings.py
    └── requirements.txt
