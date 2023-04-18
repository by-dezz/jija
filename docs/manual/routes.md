## How it works
In jija routes collect automatically from all apps and core app from `routes.py` in each app,
`routes.py` should contain a variable `routes` that is a list of endpoints.
Core app routes will starts with `/` and my_app routes will starts with `/my_app/`.

```python
from jija import router

routes = [
    router.Endpoint('/', MyView),
    router.Endpoint('/hi/', HiJija),
]
```

You can redefine url of app by add config to `apps/my_app/app.py`:

```python
from jija import app

class MyApp(app.App):
    CUSTOM_URL_PATH = '/custom-url'
```

## Endpoint
Endpoint is a class that contains information about path and view.
It automatically adds all methods of view to router.

```python
router.Endpoint('/', MyView)
```

## Include
If you want to create some group in your routes, you can use `Include` class instead of creating a subapp.

```python
from jija import router

routes = [
    router.Endpoint('/', MyView),
    router.Include('/i_dont_want_to_create_some_subapp_for_this/', [
        router.Endpoint('/', MyAnotherView),
        router.Endpoint('/hi/', HiJija),
    ])
]
```
