## Defining the configuration file
Configuration file is a python file `settings.py` that contains the configuration of the project.
In this file you should call constructor of the `jija.config` classes and pass the configuration to it.

## Structure
Structure is the most important part of the configuration file.
It contains name of core dir name, apps dir name, project path and python path for hot reloader.

```python
config.StructureConfig(
    project_path=Path(__file__).parent
    core_dir='custom_core',
    apps_dir='custom_apps',
    python_path='pypy'    
)
```

## Network
Network contains the host and port of the server.

```python
config.NetworkConfig(
    host='1.2.3.4',
    port=8000
)
```

## Drivers
The drivers config contains the drivers that will be used in the project.
It contains the database driver, the cache driver and the session driver.
You can create your own drivers and use them in the project.

By default, jija has `jija.contrib.jija_orm.driver.JijaOrmDriver` and `jija.contrib.swagger.driver.SwaggerDriver`.

```python
config.DriversConfig(
    database=my_drivers.MyDatabaseDriver(),
    docs=my_drivers.DocDriver(),
)
```

## Dev
Dev config contains the reloader excludes.
If you are using virtual environment, you should add it to reloader excludes in `settings.py`.

```python
config.DevConfig(
    reloader_excluded={'venv'}
)
```