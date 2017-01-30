from flask import request
from flask_restful import Resource
from flask_login import login_required
from ..models import student
from ..utils import responses, email

class Login(Resource):
    '''
    URL Endpoint: `/student/login`
    Allowed methods: POST
    '''
    def post(self):
        try:
            login_json = request.get_json()
            email = str(login_json['email'])
            password = str(login_json['password'])

        except:
            return responses.error('Invalid form data')

        login_response = student.Student.login(email, password)
        if 'error' in login_response:
            error_status_code = login_response.pop('error_code')
            error_message = login_response.pop('error')
            return responses.error(error_message, error_status_code)

        student_obj = login_response['student']
        ret = {'student': student_obj.get_json()}
        return ret

class Register(Resource):
    '''
    URL Endpoint: `/student/register`
    Allowed methods: POST
    '''
    @login_required
    def post(self):
        try:
            login_json = request.get_json()

            email = str(login_json['email'])
            student_id = int(login_json['student_id'])
            first_name = str(login_json['first_name'])
            last_name = str(login_json['last_name'])

            no_photo_param = str(request.args.get('no_photo'))

        except:
            return responses.error('Invalid form data')

        account_is_available = student.Student.is_account_available(email, student_id)
        if not account_is_available:
            return responses.error('Account already in use', 409)


        # Upload photo unless explicity told not to upload photo
        if no_photo_param.lower() != 'true':
            try:
                student_img = request.files.get('student_img')
                if student_img == None:
                    return responses.error('You did not include an image or set the no_photo parameter to true')
                student_img_filename = secure_filename('%s.jpg' % (student_id))
                student_img_base_path = app.config('STUDENT_IMG_BASE_PATH')
                student_img_path = os.path.join(student_img_base_path, student_img_filename)
                student_img.save(student_img_path)

            except Exception, e:
                return responses.error('There was an error uploading your image', 500)


        register_response = student.Student.register(email, student_id, first_name, last_name)
        if 'error' in register_response:
            error_status_code = register_response.pop('error_code')
            error_message = register_response.pop('error')
            return responses.error(error_message, error_status_code)

        new_student_obj = register_response['student']
        email.set_password(new_student_obj)

        ret = {'student': new_student_obj.get_json()}
        return responses.success(ret, 201)
