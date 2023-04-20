## StructureConfig
    class jija.config.StructureConfig(
        *,
        project_path: pathlib.Path,
        core_dir: str = 'core',
        apps_dir: str = 'apps',
        python_path: str = None
    )


#### Parameters
`project_path`
    The path to the project root directory.

`core_dir`
    The name of the directory containing the core app.

`apps_dir`
    The name of the directory containing project apps.

`python_path`
    Default: current python executable. The path to the python executable.

#### Attributes
`PROJECT_PATH: pathlib.Path`
    The path to the project root directory.

`CORE_PATH: pathlib.Path`
    The path to the core app directory.

`APPS_PATH: pathlib.Path`
    The path to the apps directory.

`PYTHON_PATH: str`
    The path to the python executable.


## NetworkConfig
    class jija.config.NetworkConfig(
        *,
        host: str = '0.0.0.0',
        port: int = 8080,
    )

#### Parameters
`host`
    Host to bind to.

`port`
    Port to bind to.

#### Attributes
`HOST: str`
    Host to bind to.

`PORT: int`
    Port to bind to.


## DatabaseConfig
    class jija.config.DatabaseConfig(
        *,
        user: str = 'postgres',
        password: str,
        host: str = 'localhost',
        port: int = 5432,
        database: str,
    )

#### Parameters
`user`
    The user to connect as.

`password`
    The password to use.

`host`
    The host to connect to.

`port`
    The port to connect to.

`database`
    The database to connect to.

#### Attributes
`USER: str`
    The user to connect as.

`PASSWORD: str`
    The password to use.

`HOST: str`
    The host to connect to.

`PORT: int`
    The port to connect to.

`DATABASE: str`
    The database to connect to.


## DriversConfig
    class jija.config.DriversConfig(
        *,
        docs: jija.drivers.DocsDriver = jija.drivers.DocsDriver,
        database: drivers.DatabaseDriver = drivers.DatabaseDriver,
    )

#### Parameters
`docs`
    The docs driver to use.

`database`
    The database driver to use.

#### Attributes
`DOCS: jija.drivers.DocsDriver`
    The docs driver to use.

`DATABASE: drivers.DatabaseDriver`
    The database driver to use.


## DocksConfig
    class jija.config.DocsConfig(
        *,
        url='/docs',
    )

#### Parameters
`url`
    The url to serve the docs on.

#### Attributes
`URL: str`
    The url to serve the docs on.


## DevConfig
    class jija.config.DevConfig(
        *,
        reloader_excluded: list[str] = [],
    )

#### Parameters
`reloader_excluded`
    A list of paths to exclude from the reloader. Paths are relative to the project root.

#### Attributes
`RELOADER_EXCLUDED: set[str]`
    A list of paths to exclude from the reloader. Paths are absolute.
