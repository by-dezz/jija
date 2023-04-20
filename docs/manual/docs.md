## Include
You need to add `jija.conf.DriversConf` 
and add `jija.contrib.swagger.driver.SwaggerDriver` to it in ``settings.py``.

```python
from jija.contrib.swagger.driver import SwaggerDriver
...
config.DriversConfig(
    docs=SwaggerDriver()
)
```

Then add ``jija.views.DocMixin`` to view in ``apps/my_app/views.py``.

```python
class MyView(views.View, views.DocMixin): ...
```

After that you can open docs on ``http://127.0.0.1:8080/docs/``.
Only views with ``jija.views.DocMixin`` will be included to docs.

## Custom url
If you want to change url of docs,
you need to provide ``url`` arg to ``jija.contrib.swagger.driver.Swagger``.

```python
from jija.contrib.swagger.driver import SwaggerDriver
...
config.DriversConfig(
    docs=SwaggerDriver(url='/custom-docs')
)
```

## Adding fields
Fields will be added to the docs automatically if you add serializer to the view.
