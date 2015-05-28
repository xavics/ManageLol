from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from Manager.Forms import TeamForm, PlayerForm
from django.contrib.auth import authenticate, login, logout
from models import Team, Player, Rounds, Match, League, Notice, Resolution
import Riot
from Manager.prova import make_random_statistics
import json
from itertools import chain
from operator import attrgetter, itemgetter
from django.db.models import Q
from django.utils import timezone
import ast

def base(request):
    return render(request, 'prova.html', {})

def mainpage(request):
    team_form = TeamForm()
    player_form = PlayerForm()
    servers = Riot.get_servers_stats()
    notices = Notice.objects.all()
    return render(request, 'Main.html', {'team_form': team_form, 'player_form': player_form,'servers':servers,
                                         'notices': notices})

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
        Riot.is_top_team(team_name)
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
                return HttpResponseRedirect('/team/'+username)
            else:
                return HttpResponse("Your account is disabled")
        else:
            print "Invalid log details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid log details")
    # si la request no es un HTTP POST se mostre el loguin form.
    else:
        return render(request, 'Login.html', {})

def team(request, name):
    players = Player.objects.filter(team=request.user)
    league = sorted(request.user.league.get_teams(), key=itemgetter('points','dead'), reverse=True)
    all_matches = Match.objects.filter(Q(local_team=request.user) | Q(visitor_team=request.user))
    matches = sorted(all_matches, key=attrgetter('round.data'))
    options = Player.ROLES
    options_ = []
    for option in options:
        options_.append({'val':option[0],'txt':option[1]})
    player_form = PlayerForm()
    return render(request, 'pagina_team.html', {'players': players, 'classification': league, 'matches': matches,
                                                'player_form':player_form, 'options': options_})

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('')

def alert(request):
    return render(request, 'alert.html', {})

def game_ready(request):
    now = timezone.now()
    all_matches = Match.objects.filter(Q(local_team=request.user) | Q(visitor_team=request.user))
    matches = sorted(all_matches, key=attrgetter('round.data'))
    for match in matches:
        time = match.round.data
        if (time - now).days >= 0:
            match_p = match
            break
    return render(request, 'start_game.html', {'match':match_p})

def set_ip(request):
    if request.method == 'GET':
        match = request.GET.get('match')
        match_en = Match.objects.get(id=match)
        if match_en.have_ip() == False:
            ip = Riot.get_ip()
            match_en.set_ip(ip)
            match_en.save()
            make_random_statistics(match)
        else:
            ip = match_en.ip
        statisitcs = match_en.get_statistics()
        local = statisitcs[0].values('team', 'dead', 'killed')
        visitor = statisitcs[1].values('team', 'dead', 'killed')
        winner = match_en.winner
        print winner
        data = {'ip': ip, 'winner': winner, 'local': local[0], 'visitor': visitor[0]}
        return HttpResponse(json.dumps(data))
    else:
        return HttpResponse("Bad request!")

def reclamation(request):
    if request.method == 'POST':
        match_id = request.POST.get('match')
        description = request.POST.get('description')
        match = Match.objects.get(id=match_id)
        resolution = Resolution(match=match, description=description)
        resolution.save()
        HttpResponse('Correct')
    else:
        HttpResponse('Incorrect')


@csrf_exempt
def modify(request):
    if request.method == 'POST':
        print request.POST
        team_id = request.POST.get('team')
        data_email = request.POST.get('email')
        data_old = request.POST.get('old_players')
        data_new = request.POST.get('new_players')
        new_players = json.loads(data_new)
        old_players = json.loads(data_old)
        if new_players != 0:
            for player_ in new_players:
                player = json.loads(player_)
                if not Riot.is_riot_user(player['name'], player['email']):
                        return HttpResponse('Player '+player['name']+' incorrect name/email')
            team = Team.objects.get(id=team_id)
            for player_ in new_players:
                print "First"
                player = json.loads(player_)
                print player
                player_entry = Player(name=player['name'], email=player['email'], team=team, role=player['role'])
                player_entry.save()
        if old_players != 0:
            for player in old_players:
                player = Player.objects.get(id=player)
                print player.name
                player.delete()
        if data_email != '':
            team.email = data_email
            team.save()
        if data_email == '' and new_players == 0 and old_players == 0:
            return HttpResponse('Empty')
        else:
            return HttpResponse('Correct')
    else:
        return HttpResponse('Bad')
