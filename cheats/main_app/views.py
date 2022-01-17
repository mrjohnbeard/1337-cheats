from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from .models import Cheatsheet
from django.views.generic.edit import CreateView
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required


# Create your views here.


def home(request):
    return render(request, 'home.html')


def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in via code
            login(request, user)
            return redirect('menu')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/sign_up.html', context)


def menu(request):
    return render(request, 'menu.html')


def cheatsheets_index(request):
    cheatsheets = Cheatsheet.objects.all()
    return render(request, 'cheatsheets/index.html', {'cheatsheets': cheatsheets})


class CheatsheetCreate(CreateView):
    model = Cheatsheet
    fields = ['title', 'topic']
    success_url = '/cheatsheets/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def cheatsheets_detail(request, cheatsheet_id):
    cheatsheet = Cheatsheet.objects.get(id=cheatsheet_id)
    return render(request, 'cheatsheets/detail.html', {'cheatsheet': cheatsheet})
