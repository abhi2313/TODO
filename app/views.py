from wsgiref.util import request_uri
import django
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login as loginuser, logout
from matplotlib.style import context
from requests import Request

from sqlalchemy import null
from app.forms import TODOForm
from app.models import TODO
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required(login_url='login')
def home(request):
    form = TODOForm()
    if request.user.is_authenticated:
        user = request.user
        todos = TODO.objects.filter(user=user).order_by('priority')
        return render(request, 'index.html', context={'form': form, 'todos': todos})


def login(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        context = {
            'form': form
        }

        return render(request, 'login.html', context)
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            print(user)
            if user is not None:
                loginuser(request, user)
                return redirect('home')
            else:
                return redirect('login')
        else:
            context = {
                'form': form
            }

            return render(request, 'login.html', context)


def signup(request):
    if(request.method == 'GET'):
        form = UserCreationForm()
        context = {
            "form": form
        }

        return render(request, 'signup.html', context=context)
    else:
        # print(request.POST)
        # print('checking ----')
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            if user is not None:

                return redirect('home')

        else:
            print("fails")
            for key, value in form.errors.items():

                print(key, '->', value)
                context = {
                    "form": form
                }
                return render(request, 'signup.html', context=context)


@login_required(login_url='login')
def addtodo(request):
    if(request.user.is_authenticated):
        user = request.user
        # print(user)
        form = TODOForm(request.POST)
        if(form.is_valid()):
            # print(form.cleaned_data)
            todo = form.save(commit=False)
            todo.user = user
            todo.save()
            return redirect('home')
        else:
            return render(request, 'index.html', context={'form': form})


@login_required(login_url='login')
def signout(request):
    logout(request)
    return redirect('login')


def delete_todo(request,id):
    # print(id)
    TODO.objects.get(pk=id).delete()
    return redirect('home')

def change_todo(request,id,status):
    todo=TODO.objects.get(pk=id)
    todo.status=status
    todo.save()
    return redirect('home')




