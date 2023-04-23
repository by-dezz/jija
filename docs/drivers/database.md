## Jija-ORM
Jija-ORM is a new async ORM for python. 
It located in `jija.contrib.jija_orm.driver.JinjaORMDriver`.

???+ warning
    This driver is included in jija by default, but in next updates it will be moved to separate package.

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

For more details check [Database driver](/manual/drivers/#database-driver).


## SQLAlchemy
There is sqlalchemy driver for jija framework. It based on default jija database driver.
For more details check [jija_sqlalchemy driver](https://gitlab.com/by_dezz/jija-sqlalchemy).