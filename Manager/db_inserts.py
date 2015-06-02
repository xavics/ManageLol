import django
import datetime
import json
# from Manager.Riot import is_riot_user, is_top_team
from django.contrib.auth.models import Group
from Manager.models import Team, Player, Competition

# For debugging
with open('riotdatabase.json') as data_file:
    data = json.load(data_file)

def make_referee(name, password):
    team = Team(name=name, is_referee=True)
    team.save()
    team.set_password(password)
    team.save()
    referee_g = Group.objects.get(name='Referee')
    team.group.add(referee_g)
    team.save()


def make_enable_team(team):
    team = Team.objects.get(name=team)
    team.set_password("xxx")
    team.save()

def create_groups():
    team_g = Group.objects.create(name='Team')
    referee_g = Group.objects.create(name='Referee')
    auth_g = Group.objects.create(name='Admin')


def make_admin():
    team = Team(name='admin', is_admin=True)
    team.save()
    referee_g = Group.objects.get(name='Admin')
    team.group.add(referee_g)
    team.save()
    team.set_password("admin")
    team.save()


def make_db_inserts():
    f = open('db_in','w+')
    for x in range(24):
        if x != 0:
            st_x = str(x)
            data = str(datetime.datetime.now())
            team_name = "t"+st_x
            values = "'"+st_x+"','xxx','"+data+"','"+team_name+"',0,'mailo','','False','False'"
            f.write("insert into Manager_team values("+values+");\n")
            x_p = (x-1)*5
            for y in range(6):
                if y != 0:
                    p_id = str(x_p+y)
                    player_n = "p"+p_id
                    mail_p = player_n+"@mail.com"
                    values_p = "'"+p_id+"','"+player_n+"','"+mail_p+"','False','SU','"+st_x+"'"
                    f.write("insert into Manager_player values("+values_p+");\n")

def nmake_db_inserts():
    x = 0
    t = 0
    for player in data['players']:
        if x == 0:
            t += 1
            st_x = str(t)
            team_name = "team"+st_x
            team_email = team_name+"@gmail.com"
            team = Team(name=team_name, email=team_email)
            team.save()
            team.set_password("xxx")
            team.save()
            referee_g = Group.objects.get(name='Team')
            team.group.add(referee_g)
            team.save()
        if x < 5:
            n_player = Player(name=player['name'], email=player['email'], role='Support', team=team)
            n_player.save()
        x += 1
        if x == 5:
            x = 0
    competition = Competition(state="Open")
    competition.save()


if __name__ == '__main__':
    django.setup()
    create_groups()
    nmake_db_inserts()
    make_referee("referee","xxx")
    make_admin()