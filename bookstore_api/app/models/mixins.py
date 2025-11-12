from sqlalchemy.exc import SQLAlchemyError

from bookstore_api.app.extensions import db

class TransactionMixin(db.Model):
    __abstract__ = True

    def save(self):
        """Saves an instance of the model to the database."""
        try:
            db.session.add(self)
            db.session.commit()

            return True
        except SQLAlchemyError as error:
            db.session.rollback()
            raise error
        
    def delete(self):
        """Delete an instance of the model from the database."""
        try:
            db.session.delete(self)
            db.session.commit()

            return True
        except SQLAlchemyError as error:
            db.session.rollback()
            return error
