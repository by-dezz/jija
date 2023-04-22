# Getting started

## Install
    pip install jija

## Simple layout
    my_project
    │
    ├── apps
    │   └── my_app
    │       ├── app.py
    │       ├── routes.py
    │       └── views.py
    ├── main.py
    ├── settings.py
    └── requirements.txt

## Fill main.py
That is entry point of your project.
```python title="main.py"
from jija.apps import Apps

if __name__ == '__main__':
    import settings
    Apps.run_command()
```

1.  :man_raising_hand: I'm a code annotation! I can contain `code`, __formatted
    text__, images, ... basically anything that can be written in Markdown.

## Fill settings.py
That is settings file of your project.
    
```python title="settings.py"
from pathlib import Path
from jija import config

config.StructureConfig(
    project_path=Path(__file__).parent
)

config.NetworkConfig(
    host='localhost',
)
```

If you are using virtual environment, you should add it to reloader excludes in `settings.py`.

```python title="settings.py"
...

config.DevConfig(
    reloader_excluded={'venv'}
)
```

## Fill apps/my_app/routes.py
That are paths to your views.
    
```python title="apps/my_app/routes.py"
from jija import router
from .views import *

routes = [
    router.Endpoint('/', MyView),
]
```

## Start project
After that you can start project with command ``python main.py run`` 
and go to ``http://127.0.0.1:8080/my_app/`` there u will see ``{"status": "ok"}``.

## Include docs
If you want to include docs to your project, you need to add
`jija.conf.DriversConf` and add `jija.contrib.swagger.driver.SwaggerDriver` to it in ``settings.py``.

```python title="settings.py"
from jija.contrib.swagger.driver import SwaggerDriver
...
config.DriversConfig(
    docs=SwaggerDriver()
)
```

Then add ``jija.views.DocMixin`` to view in ``apps/my_app/views.py``.

```python title="apps/my_app/views.py"
...
class MyView(views.View, views.DocMixin):
... 
```

After that you can open docs on ``http://127.0.0.1:8080/docs/``.
Only views with ``jija.views.DocMixin`` will be included to docs.

## Add serializers
If you want to add serializers to your project, you can change parent class of your view to ``jija.views.SerializedView`` 
and annotate serializer class to your method. 

```python title="apps/my_app/views.py"
from jija import views, serializers

class MySerializer(serializers.Serializer):
    name = serializers.CharField()
    age = serializers.IntegerField()

class MyView(views.SerializedView):
    def get(self, data: MySerializer):
        ...
```

## Include ORM
If you want to include ORM to your project, you need to install ``jija-orm``
```
pip install jija-orm
```

Then init database driver ``jija.contrib.jija_orm.driver.JijaOrmDriver`` in ``settings.py``.

```python title="settings.py"
from jija.contrib.jija_orm.driver import JijaOrmDriver
...

config.DriversConfig(
    ...,
    database=JijaOrmDriver(
        database='postgres',
        password='0000',
    )
)
```

Then you need to create ``models.py`` in ``apps/my_app`` and create models.

```python title="apps/my_app/models.py"
from jija_orm import models, fields

class MyModel(models.Model):
    name = fields.CharField(max_length=28)
```

After that you can create migrations by ``python main.py migrate`` and apply them by ``python main.py update``. 


## Include auth
Auth is using external lib for more info see [aiohttp_session](https://aiohttp-session.readthedocs.io/en/stable/).

If you want to include auth to your project, you need to init 'auth_config.AuthConfig' in 'settings.py'.

```python title="settings.py"
from jija.contrib.auth import config as auth_config
...

auth_config.AuthConfig(
    secret_key=b'*' * 32 # 32 bytes secret key
)

...
```

If you want to use auth in all project you need to create core app in root level of project 
else you can create it in any app.

    my_project
    ├── apps
    ├── core
    │   ├── app.py
    │   └── middlewares.py

And fill ``core/middlewares.py``

```python title="core/middlewares.py"
import aiohttp_session
from aiohttp import web
from jija import middleware
from jija import response

class Session(middleware.Middleware):
    async def handler(self, request: web.Request, handler):
        http_session = await aiohttp_session.get_session(request)
        request.session = http_session

        user = await self.get_user(request)
        if not user:
            return response.JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=401)

        request.user = user
        return await handler(request)

    async def get_user(self, request):
        # add your logic here
```


## Create custom commands
If you want to create custom commands you need to create ``commands`` dir in any app 
and create ``<command name>.py`` in it.

    my_project
    ├── apps
    ├── commands
    │   └── <command name>.py

And fill ``<command name>.py``
```python title="my_app/commands/<command name>.py"
from jija import commands

class Command(commands.Command):
    def handle(self):
        print('Hello world')
```

After that you can run your command with ``python main.py <command name>`` if you created it in core app 
else you can run it with ``python main.py my_app.<command name>``.


## Advanced layout
Actually you can create core app and models.py in any app and sub apps in any app except core app.

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
