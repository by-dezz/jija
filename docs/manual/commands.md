## How to call
All commands are called from the command line.

```bash
python main.py <command>
```

## Run
Default command to run the app in dev mode.
It will run the app in debug mode and will reload the app when the code changes.

```bash
python main.py run
```

## Runprocess
Command to run the app in production mode.
It will run the app in production mode and will not reload the app when the code changes.

```bash
python main.py runprocess
```

## Migrate
Command to create migrations for your models.

```bash
python main.py migrate
```

## Update
Command to update the database with migrations.

```bash
python main.py update
```

## Custom commands
If you want to create custom commands you need to create ``commands`` dir in any app 
and create ``<command name>.py`` in it.

    my_project
    ├── apps
    ├── commands
    │   └── <command name>.py

Then fill ``<command name>.py`` by `Command` class from `jija.commands.Command` and implement `handle` method. 
It can be async or sync. 
```python title="my_app/commands/<command name>.py"
from jija import commands

class Command(commands.Command):
    def handle(self):
        print('Hello world')
```

After that you can run your command with ``python main.py <command name>`` if you created it in core app 
else you can run it with ``python main.py my_app.<command name>``.