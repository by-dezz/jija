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


## DriversConfig
    class jija.config.DriversConfig(
        *,
        docs: jija.drivers.DocsDriver,
        database: jija.drivers.DatabaseDriver,
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
