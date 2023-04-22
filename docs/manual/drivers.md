## About it
Drivers is a addons for jija.
For config, you can use `jija.config.DriversConfig` in `settings.py`.

You can create your own drivers and use them in the project.

By default, jija has `jija.contrib.jija_orm.driver.JinjaORMDriver` for database
and `jija.contrib.swagger.driver.SwaggerDriver` for docs.

## Include
If you want to include drivers to your project, you need to init `jija.config.DriversConfig` in `settings.py`.

```python
from jija import config

config.DriversConfig(
    database=my_drivers.MyDatabaseDriver(),
    docs=my_drivers.DocDriver(),
)
```

## Docs driver
You need to init the docs config if you want to use the docs.
You can change the url of the docs.

```python
from jija.contrib.swagger.driver import SwaggerDriver

config.DriversConfig(
    docs=SwaggerDriver(url='/custom-docs')
)
``` 


## Database driver
By default, jija has driver only for `jija-orm`, it located in
`jija.contrib.jija_orm.driver.JinjaORMDriver` for database.

```python
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