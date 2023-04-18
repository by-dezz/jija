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