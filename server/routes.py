from . import api
from controllers import student, admin

def make_routes():

    api.add_resource(student.Login, '/student/login')
    api.add_resource(student.Register, '/student/register')

    api.add_resource(admin.AdminLogin, '/admin/login')
