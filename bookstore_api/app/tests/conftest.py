import pytest
from bookstore_api.app import create_app
from bookstore_api.app.extensions import db
from bookstore_api.app.models import Role, User
from bookstore_api.app.helpers import RoleType
from werkzeug.security import generate_password_hash

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    with app.app_context():
        # Create all database tables (in-memory SQLite)
        db.create_all()

        yield app

        # Teardown: Clean up and close the database session
        db.session.remove()
        db.drop_all()

@pytest.fixture
def init_db(app):
    # Seed roles
    user_role = Role(name=RoleType.USER.value)
    admin_role = Role(name=RoleType.ADMIN.value)
    db.session.add(user_role)
    db.session.add(admin_role)
    db.session.commit()

    # Create admin user
    admin_user = User(
        username='admin',
        email='admin@example.com',
        password_hash=generate_password_hash('admin'),
        role_id=Role.query.filter_by(name=RoleType.ADMIN.value).first().id
    )
    # Create regular user
    regular_user = User(
        username='user',
        email='user@example.com',
        password_hash=generate_password_hash('user'),
        role_id=Role.query.filter_by(name=RoleType.USER.value).first().id
    )
    db.session.add(admin_user)
    db.session.add(regular_user)
    db.session.commit()

    yield db
