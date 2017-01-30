from datetime import datetime, timedelta

from sqlalchemy.exc import IntegrityError
import bcrypt


from . import db

class Student(db.Model):
    __tablename__ = 'students'

    student_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)

    hashed_password = db.Column(db.String(200))
    is_confirmed = db.Column(db.Boolean, default=False)
    reset_token = db.Column(db.String(200))
    reset_token_expires = db.Column(db.DateTime)

    def __init__(self, email, student_id, first_name, last_name):
        self.email = email
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.is_confirmed = False
        self._set_new_token()


    def get_json(self):
        ret = {
            'student_id': self.student_id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'is_confirmed': self.is_confirmed,
        }
        return ret


    @staticmethod
    def login(email, plaintext_password):
        student_obj = Student.query.filter_by(email=email).first()
        if student_obj is None:
            error_ret = {
                'error': 'This email is not registered',
                'error_code': 404
            }
            return error_ret

        if not student_obj.is_confirmed:
            error_ret = {
                'error': 'Your password is not properly set.',
                'error_code': 403
            }
            return error_ret


        passwords_match = Student._check_password(plaintext_password, student_obj.hashed_password)
        if not passwords_match:
            error_ret = {
                'error': 'The email/password combination is invalid',
                'error_code': 422
            }
            return error_ret

        ret = {'student': student_obj}
        return ret


    @staticmethod
    def register(email, student_id, first_name, last_name):
        new_student = Student(
            email=email,
            student_id=student_id,
            first_name=first_name,
            last_name=last_name
        )

        try:
            db.session.add(new_student)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            error_ret = {
                'error': 'There was a database error.',
                'error_code': 500
            }
            return error_ret

        ret = {'student': new_student}
        return ret


    @staticmethod
    def is_account_available(email, student_id=None):
        email_exists = Student.query.filter_by(email=email).first()
        if student_id is None:
            student_id_exists = None
        else:
            student_id_exists = Student.query.get(student_id)

        if email_exists != None or student_id_exists != None:
            return False
        return True

    def _set_new_token(self, hours_valid=24):
        new_token = self._get_new_token(self.email)
        self.is_confirmed = False
        self.reset_token = new_token
        self.reset_token_expires = datetime.utcnow() + timedelta(hours=hours_valid)

        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            ## TODO return error
            db.session.rollback()
            pass
        return new_token

    @staticmethod
    def _get_new_token(email):
        new_token = bcrypt.hashpw(email, bcrypt.gensalt(2))
        return new_token

    @staticmethod
    def _get_hashed_password(plaintext_password):
        return bcrypt.hashpw(plaintext_password.encode('utf-8'), bcrypt.gensalt(12))

    @staticmethod
    def _check_password(plaintext_password, hashed_password):
        return bcrypt.checkpw(plaintext_password.encode('utf-8'), hashed_password.encode('utf-8'))
