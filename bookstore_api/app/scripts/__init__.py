from .db_seeds import db_cli, greet_command

def init_app_commands(app):
    app.cli.add_command(db_cli)
    app.cli.add_command(greet_command)
