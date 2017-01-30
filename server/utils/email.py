from flask_mail import Message
from .. import mail

set_password_url_template = 'http://127.0.0.1:5000/auth/reset/%s'
reset_password_url_template = 'http://127.0.0.1:5000/auth/reset/%s'

set_password_msg_body_template = \
    '''
    %s %s, please visit <a href='%s'>%s<a> to confirm your email and set a password for your BHS Student ID Mobile account.
    '''

reset_password_msg_body_template = \
    '''
    %s %s, please visit <a href='%s'>%s<a> to change your BHS Student ID Mobile password. If you did not request your password
    '''

def set_password(student_obj):
    first_name = student_obj.first_name
    last_name = student_obj.last_name
    set_password_url = set_password_url_template % (student_obj.reset_token)

    msg_body = set_password_msg_body_template % (first_name, last_name, set_password_url, set_password_url)
    msg_subject = 'Confirm your Benicia High School student ID account!'
    msg_recipients = [student_obj.email]
    msg = Message(subject=msg_subject, recipients=msg_recipients, body=msg_body)
    mail.send(msg)

def reset_password(student_obj):
    first_name = student_obj.first_name
    last_name = student_obj.last_name
    reset_password_url = reset_password_url_template % (student_obj.reset_token)

    msg_body = reset_password_msg_body_template % (first_name, last_name, reset_password_url, reset_password_url)
    msg_subject = 'Confirm your Benicia High School student ID account!'
    msg_recipients = [student_obj.email]
    msg = Message(subject=msg_subject, recipients=msg_recipients, body=msg_body)
    mail.send(msg)
