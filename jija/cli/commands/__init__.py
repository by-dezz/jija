from jija.cli.commands.run import Run
from jija.cli.commands.migrate import Migrate
from jija.cli.commands.upgrade import Upgrade
from jija.cli.commands.create_app import CreateApp


COMMANDS = {
    'run': Run,
    'migrate': Migrate,
    'update': Upgrade,
    'create-app': CreateApp
}
