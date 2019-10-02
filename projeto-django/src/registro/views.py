from django.shortcuts import render, redirect
from registro.forms import UserRegistrationForm 
from .models import User 
from django.contrib import messages
import jwt
import hmac, base64
from django.contrib.auth.hashers import make_password, check_password
import logging





def RegisterUser(request): 
	if request.method=='POST':
		new_user_form=UserRegistrationForm(request.POST)
		if new_user_form.is_valid():
			logging.info('form registro valido')
			new_user = new_user_form.save()
			new_user.password=make_password(new_user.password)
			new_user.save()
			logging.info('form registro salvo')
			return redirect('/login/')
	else:
		logging.error('form registro invalido')
		new_user_form=UserRegistrationForm()
		messages.info(request,'Erro ao cadastrar! Refaça o formulário')
	return render(request, 'signup.html',{'form':new_user_form})

def LoginUser(request): 
	if request.method=='POST':
		login = request.POST.get('login')
		password = request.POST.get('password')
		
		try:
			get_user = User.objects.get(login__iexact=login)
		except:
			if get_user.DoesNotExist:
				logging.error('usuario nao existe')
				return redirect('/signup/')
		logging.info('usuario existe')
		if check_password(password,get_user.password):		
			logging.info('senha valida')
			response = redirect('/meumenu/')
			response.set_cookie('login',login)
			obj_usuario = User.objects.get(login=login)
			id_usuario = obj_usuario.id
			login_usuario = obj_usuario.login
			token=jwt.encode({'sub':id_usuario, 'login':login_usuario}, 'secret', algorithm='HS256').decode('utf-8')
			response.set_cookie('ultimate_token',token)
			return response
		else:
			logging.error('senha invalida')
			return render(request, 'login.html')	
	else:
		return render(request, 'login.html')


def LogOut(request):
	login=request.COOKIES.get('login')
	if login is None:
		logging.error('nenhum usuario logado')
		return render(request,'home.html')
	else:
		response=redirect ('/meumenu/')
		response.delete_cookie('login')
		response.delete_cookie('ultimate_token')
		logging.info('cookie do usuario logado sendo apagado')
		return response

def UserHome(request):
	login=request.COOKIES.get('login')
	if login is None:
		return render(request,'home.html')
	else:
		logging.info('usuario logado')
		return redirect('/meumenu/' )

def About(request):
		return render(request,'about.html')


