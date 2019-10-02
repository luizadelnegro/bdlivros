import re
from django.shortcuts import render, redirect
from django.conf import settings
from django.shortcuts import HttpResponseRedirect
from registro.models import User
import jwt

class CookieMiddleware(object):
    def __init__(self,get_response):
    #One-time configuration and initialization
        self.get_response=get_response

    def __call__(self, request):
     #Code to be executed for ech request before the view(and latter middleware) are called
        if request.path in ['/', '/about/', '/login/', '/signup/' ]:
            return self.get_response(request)

        login = request.COOKIES.get('login')
        if login is None:
            return redirect('/')
        else:
            cookie_jwt = request.COOKIES.get('ultimate_token')
            decoded = jwt.decode(cookie_jwt,'secret',algorithms='HS256')
            obj_usuario = User.objects.get(login=login)
            id_usuario = obj_usuario.id
            login_usuario = obj_usuario.login
            dici={'sub':id_usuario, 'login':login_usuario}
            if dici==decoded:#ok
                response=self.get_response(request)
                return response
            else:#not ok
                return  redirect('/')
        response = self.get_response(request)
        return response
