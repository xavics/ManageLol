from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from Manager.Forms import TeamForm, PlayerForm
from django.contrib.auth import authenticate, login, logout
from models import Player, Team
import Riot
import json

def base(request):
    return render(request, 'prova.html', {})

def mainpage(request):
    team_form = TeamForm()
    player_form = PlayerForm()
    return render(request, 'base.html', {'team_form': team_form, 'player_form': player_form})

def register(request):
    if request.method == 'POST':
        data = request.POST
        print data
        myDict = dict(data.iterlists())
        players = []
        for n in range(5):
            name = myDict['name'][n]
            email = myDict['email'][n]
            print name, email
            if not Riot.is_riot_user(name, email):
                return HttpResponseRedirect('/alert/')
            role = myDict['role'][n]
            print role
            player = Player(name=name, email=email, role=role)
            players.append(player)
        team_name = myDict['team_name'][0]
        team_email = myDict['team_email'][0]
        team = Team(name= team_name, email= team_email)
        team.save()
        team.set_password(myDict['password'][0])
        team.save()
        for player in players:
            player.set_team(team)
            player.save()
        data_email = {'team':team_name, 'players':players}
        Riot.send_confimation_email(team_email, data_email)
        #log in
        team = authenticate(username=team_name, password=myDict['password'][0])
        if team:
            if team.is_active:
                login(request, team)
                return HttpResponseRedirect('/team/')
            else:
                return HttpResponse("Your account is disabled")
        else:
            print "Invalid log details: {0}, {1}".format(team_name, myDict['password'][0])
            return HttpResponse("Invalid log details")
    else:
        team_form = TeamForm()
        player_form = PlayerForm()
        return render(request, 'Register.html', {'team_form': team_form, 'player_form': player_form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        team = authenticate(username=username, password=password)
        # User exist in our database
        if team:
            # Is active
            if team.is_active:
                login(request, team)
                # return HttpResponseRedirect('/base/')
                return HttpResponseRedirect('/team/')
            else:
                return HttpResponse("Your account is disabled")
        else:
            print "Invalid log details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid log details")
    # si la request no es un HTTP POST se mostre el loguin form.
    else:
        return render(request, 'Login.html', {})

def team(request):
    players = Player.objects.filter(team=request.user)
    return render(request, 'pagina_team.html', {'players': players})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('')

def alert(request):
    return render(request, 'alert.html', {})