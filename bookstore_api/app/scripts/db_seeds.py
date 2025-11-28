import click

from flask.cli import AppGroup
from werkzeug.security import generate_password_hash
from bookstore_api.app.helpers import RoleType

from bookstore_api.app.extensions import db

db_cli = AppGroup('seed', help='Database related commands.')

# To see commands inside the 'db' group:
# poetry run my-cli seed --help

# This command remains a flat, top-level command: poetry run my-cli greet <name>
@click.command('greet')
@click.argument('name')
def greet_command(name):
    """Greets a user by their provided name."""
    
    click.echo(f"Hello {name}! Welcome to the custom Flask CLI.")

# To run the nested command:
# poetry run my-cli seed roles
@db_cli.command('roles')
@click.confirmation_option(
    prompt='Are you sure you want to seed the roles table? This will delete all existing roles.'
)
def seed_roles():
    """Seed roles table."""
    from bookstore_api.app.models import Role # pylint: disable=import-outside-toplevel

    click.echo('Creating admin user...')
    try:
        # Use query.delete() to perform a mass deletion without loading objects into memory.
        # synchronize_session='fetch' tells SQLAlchemy to fetch the affected rows
        # count from the database after the delete operation.
        rows_deleted = db.session.query(Role).delete(synchronize_session='fetch')

        # Commit the transaction to finalize the deletion in the database
        db.session.commit()

        click.echo(f"🔥 Successfully deleted {rows_deleted} rows from the Roles table.")
    except Exception as e:
        # Rollback the session in case of an error
        db.session.rollback()
        click.echo(f'❌ Error during deletion: {e}')
        return

    click.echo('Seeding roles table...')

    roles = [
        {'name': Role.ADMIN.value},
        {'name': Role.USER.value},
    ]

    for role in roles:
        db.session.add(Role(**role))

    try:
        db.session.commit()

        click.echo('🔥 Roles table seeded.')
    except Exception as error:
        # Rollback the session in case of an error
        db.session.rollback()
        click.echo(f'❌ Error creating roles table: {error}', err=True)

# To run the nested command:
# poetry run my-cli seed admin-user
@db_cli.command('admin-user')
@click.confirmation_option(
    prompt='Before seeding admin user, ensure the roles are already seeded.Are you sure you want to proceed?'
)
@click.option('--username', prompt="Enter Username", help='The username for authentication.')
@click.option('--email', prompt="Enter Admin Email", help='The email for authentication.')
@click.password_option(help='The password for authentication (input hidden).')
def create_admin_user(username, email, password):
    """Create admin user."""
    from bookstore_api.app.models import Role, User # pylint: disable=import-outside-toplevel

    click.echo('Creating admin user...')
    try:
        # fetch admin role
        admin_role = db.session.query(Role).filter(RoleType.name == 'admin').one_or_none()        
        if not admin_role:
            click.echo("❌ Admin role not found. Please seed roles first.")
            return

        # create admin user
        db.session.add(
            User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password),
                role_id=admin_role.id
            )
        )

        # Commit the transaction
        db.session.commit()

        click.echo('🔥 Successfully created admin user.')
    except Exception as e:
        # Rollback the session in case of an error
        db.session.rollback()
        click.echo(f'❌ Error creating admin user: {e}')
        return
