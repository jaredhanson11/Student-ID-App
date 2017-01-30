from sqlalchemy.exc import IntegrityError
import bcrypt

from . import db, login_manager
from ..utils import responses

class Admin(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)

    hashed_password = db.Column(db.String(200))
    is_super_admin = db.Column(db.Boolean, default=False)


    def __init__(self, email, first_name, last_name, plaintext_password):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.hashed_password = self._get_hashed_password(plaintext_password)


    def get_json(self):
        ret = {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name
        }
        return ret

    @staticmethod
    def login(email, plaintext_password):
        admin_obj = Admin.query.filter_by(email=email).first()
        if admin_obj is None:
            error_ret = {
                'error': 'This email is not registered',
                'error_code': 404
            }
            return error_ret

        passwords_match = Admin._check_password(plaintext_password, admin_obj.hashed_password)
        if not passwords_match:
            error_ret = {
                'error': 'The email/password combination is invalid',
                'error_code': 422
            }
            return error_ret

        ret = {'admin': admin_obj}
        return ret

    @staticmethod
    def register(email, plaintext_password, first_name, last_name):
        new_admin = Admin(
            email=email,
            first_name=first_name,
            last_name=last_name,
            plaintext_password=plaintext_password
        )

        try:
            db.session.add(new_admin)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            error_ret = {
                'error': 'There was a database error.',
                'error_code': 500
            }
            return error_ret

        ret = {'admin': new_admin}
        return ret


    ######################## Flask-Login #########################
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_annonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    @login_manager.user_loader
    def load_user(user_id):
            return Admin.query.get(int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        return responses.error('No admin user was logged in.', 401)

    ####################### End Flask-Login ######################

    @staticmethod
    def _get_hashed_password(plaintext_password):
        return bcrypt.hashpw(plaintext_password.encode('utf-8'), bcrypt.gensalt(12))

    @staticmethod
    def _check_password(plaintext_password, hashed_password):
        return bcrypt.checkpw(plaintext_password.encode('utf-8'), hashed_password.encode('utf-8'))

