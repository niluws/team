from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from django.utils.decorators import method_decorator
from django.views import View

from .forms import SignUpForm, LoginForm, TeamForm
from .models import Team, Account


def home(request):
    teams = Team.objects.filter(account__username__iexact=request.user.username)
    return render(request, 'home.html', {'teams': teams})


class signup(View):

    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):

        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password1 = form.cleaned_data.get('password1')
            user: bool = Account.objects.filter(username__iexact=username).exists()

            if user:
                form.add_error('username', 'username is exist')
            else:

                new_user = Account(
                    username=username,
                    email=email,
                    password=password1,

                )
                new_user.set_password(password1)
                new_user.save()

        return render(request, 'signup.html', {'form': form})


class login_account(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = Account.objects.filter(username__iexact=username).first()
            if user is not None:
                is_password_correct = user.check_password(password)
                if is_password_correct:
                    login(request, user)
                    return redirect(reverse('home'))
                else:

                    return redirect(reverse('login'))

            else:

                return redirect(reverse('create'))

        return render(request, 'login.html', {'form': form})


def logout_account(request):
    logout(request)
    return redirect(reverse('home'))


@method_decorator(login_required, name='dispatch')
class joinoradd_team(View):
    def get(self, request):
        form = TeamForm()
        have_team: bool = Team.objects.filter(account__username__iexact=request.user.username).exists()
        if have_team == True:
            print('have team')
            return redirect(reverse('home'))
        return render(request, 'team.html', {'form': form})

    def post(self, request):
        form = TeamForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data.get('name')
            team_exist: bool = Team.objects.filter(name__iexact=name).exists()
            user = Account.objects.filter(username__iexact=request.user.username).first()
            if team_exist:
                form.add_error('name', ' team name is exist')
            else:

                new_team = Team(
                    name=name,
                    jitsi_url_path=F'http://meet.jit.si/{name}'

                )
                new_team.save()

                user.team_id = new_team.id
                user.save()
                return redirect(reverse('home'))

        return render(request, 'team.html', {'form': form})


class exit_team(View):
    def get(self,request):
        user = Account.objects.filter(username__iexact=request.user.username).first()
        user.team_id = ''
        user.save()
        return redirect(reverse('home'))
