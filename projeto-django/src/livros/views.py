from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Book
from .forms import BookForm
from django.contrib.auth.forms import UserCreationForm
from registro.models import User
from django.http import HttpResponse
import logging
import jwt, base64


def RedirectLoginToMenu(request):
	login = request.COOKIES.get('login')
	usuario=User.objects.get(login=login)
	nome_usuario=usuario.nome 
	return render (request,'user_menu.html',{'nome':'nome_usuario'})


def AllBooks(request):
	queryset = Book.objects.all()
	AddBookToList(request)
	context = { "books_list":queryset }
	return render(request, 'books_list.html',context)



def MyBooks(request):
	login = request.COOKIES.get('login')
	usuario = User.objects.get(login=login).mybooks.all()
	RemoveBookFromList(request)
	context = { "my_books":usuario }
	return  render(request, 'my_books.html',context)

 

def RegisterBook(request):
	if request.method=='POST':
		new_book_form = BookForm(request.POST)
		if new_book_form.is_valid():
			book = new_book_form.save()
			book.save()
			logging.info('livro criado')
			return redirect( '/lista/')
	else:
		new_book_form = BookForm()
		return render(request,"new_book.html",{ 'form':new_book_form})


def AddBookToList(request):
	if request.method=='POST':
		login = request.COOKIES['login']
		book = request.POST.get('book')
		usuario = User.objects.get(login=login)
		try:
			temlivro = usuario.mybooks.get(id=book) 
			if temlivro.exists():
				logging.info('livro ja esta na sua lista')
				return 
		except:
			book_obj = Book.objects.get(id=book)
			usuario = User.objects.get(login=login)
			usuario.mybooks.add(book_obj)
			logging.info('livro adicionado a sua lista')
			messages.info(request,'O livro foi adicionado!')
			return 

	else:
		return
		


def RemoveBookFromList(request):
	if request.method=='POST':
		login = request.COOKIES['login']
		book = request.POST.get('book')
		usuario = User.objects.get(login=login)
		book_obj = Book.objects.get(id=book)
		usuario.mybooks.remove(book_obj)
		logging.info('livro removido da sua lista')
		messages.info(request,'O livro foi removido!')
		return 

