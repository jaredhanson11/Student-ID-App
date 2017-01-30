from flask import request
from flask_restful import Resource
from flask_login import current_user, login_required, login_user, logout_user
from ..models import admin

from ..utils import responses

class AdminLogin(Resource):
    '''
    URL Endpoint: `/student/login`
    Allowed methods: POST, DELETE
    '''
    def post(self):
        try:
            login_json = request.get_json()
            email = str(login_json['email'])
            password = str(login_json['password'])

        except:
            return responses.error('Invalid form data')

        login_response = admin.Admin.login(email, password)
        if 'error' in login_response:
            error_status_code = login_response.pop('error_code')
            error_message = login_response.pop('error')
            return responses.error(error_message, error_status_code)

        admin_obj = login_response['admin']
        login_user(admin_obj)

        ret = {'admin': admin_obj.get_json()}
        return responses.success(ret, 200)

    @login_required
    def delete(self):
        logout_user()
        ret = {'message': 'Successfully logged out.'}
        return responses.success(ret, 200)
