import csv
from datetime import datetime

from django.contrib.auth.models import User
from django.contrib.auth.views import LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View, generic

from .forms import RegisterForm, AuthForm, UpdateForm, CreateBlogForm, FileBlogForm
from .models import Profile, BlogModel, File
from django.contrib.auth import authenticate, login


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(
                user=user
            )
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('main')
    else:
        form = RegisterForm()
    return render(request, 'blog/register.html', context={'form': form})


def login_view(request):
    if request.method == 'POST':
        auth_form = AuthForm(request.POST)
        if auth_form.is_valid():
            username = auth_form.cleaned_data.get('username')
            password = auth_form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect('main')
                else:
                    auth_form.add_error('__all__', 'Ошибка! Учетная запись пользователя не активна!')
            else:
                auth_form.add_error('__all__', 'Ошибка! Проверьте правильность написания логина и пароля')
    else:
        auth_form = AuthForm()
    return render(request, 'blog/login.html', context={'form': auth_form})


class AnotherLogoutView(LogoutView):
    next_page = 'main'


class MainView(generic.ListView):
    model = BlogModel
    template_name = 'blog/main.html'
    context_object_name = 'blog'


class BlogDetail(generic.DetailView):
    model = BlogModel
    template_name = 'blog/detail.html'
    context_object_name = 'details'


class UpdateProfile(generic.UpdateView):
    model = User
    template_name = 'blog/profile.html'
    context_object_name = 'profile'
    success_url = reverse_lazy('main')

    form_class = UpdateForm


def create_to_blog(request):
    user = request.user
    form = CreateBlogForm(request.POST)
    file_form = FileBlogForm(request.POST, request.FILES)
    files = request.FILES.getlist('file')
    if request.method == 'POST':
        if form.is_valid() and file_form.is_valid():
            blog_instance = form.save(commit=False)
            blog_instance.user = user
            blog_instance.save()
            for f in files:
                file_instance = File(file=f, blog=blog_instance)
                file_instance.save()
            return redirect('main')
    else:
        form = CreateBlogForm()
        file_form = FileBlogForm()
    return render(request, 'blog/create_blog.html', context={'form': form, 'file_form': file_form})


def load_blog(request):
    if request.method == 'POST':
        upload_file_form = FileBlogForm(request.POST, request.FILES)
        if upload_file_form.is_valid():
            file_blog = upload_file_form.cleaned_data['file'].read().strip()
            file_blog_strip = file_blog.decode('cp1251').split('\n')
            csv_reader = csv.reader(file_blog_strip, delimiter=';')
            for row in csv_reader:
                convert_data = datetime.strptime(row[2], '%d.%m.%Y')
                blog = BlogModel.objects.create(title=row[0], content=row[1], created_at=convert_data,
                                                created_by=request.user)
                blog.save()
            return redirect('main')
    else:
        upload_file_form = FileBlogForm()
    return render(request, 'blog/load_csv.html', context={'form': upload_file_form})
