from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db

migrate = Migrate(app, db)
manager = Manager(app)

# create a migration utility command
manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    """
    Creates the database tables
    """
    db.create_all()


@manager.command
def drop_db():
    """
    Drops the database tables
    """
    db.drop_all()


if __name__ == '__main__':
    manager.run()
