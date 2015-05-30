from copy import deepcopy
import datetime
from random import randint, getrandbits
import json
from ManageLol import settings
from Manager.models import Team, League, Rounds, Match, Statistics, Player, Reclamation
from rest_framework_xml.renderers import XMLRenderer
from xml.dom.minidom import parseString
from Riot import send_confimation_email
from django.contrib.auth.models import Group
# import copy
import dicttoxml

def distribucio(num):
    list = []
    div = num / 24
    falten = num - (div * 24)
    for i in range(div):
        list.append(24)
    if (falten != 0):
        list.append(falten)
    equit = False;
    i = len(list) - 1
    if (i != 0):
        while equit == False:
            if (i == 0):
                i = len(list) - 1
            newnum = (list[i] + list[i - 1]) / 2
            if (((list[i] + list[i - 1]) % 2) == 1):
                list[i] = newnum
                list[i - 1] = newnum + 1
            else:
                list[i] = newnum
                list[i - 1] = newnum
            if (allnumequal(list) == True):
                equit = True
            i -= 1
        # print "old:", list
        makepairs(list)
    return deepcopy(list)


def makepairs(list):
    for i in range(len(list) - 1, 0, -1):
        if ((list[i] % 2) != 0):
            pos = nextodd(list, i)
            if (pos == -1):
                break;
            list[pos] -= 1;
            list[i] += 1;
            # print "new:", list


def nextodd(list, i):
    for i in range(i - 1, -1, -1):
        if ((list[i] % 2) != 0):
            return i
    return -1


def allnumequal(list):
    i = len(list) - 1
    while i != 0:
        if (list[i] == list[i - 1] or list[i] + 1 == list[i - 1] or list[i] - 1 == list[i - 1]):
            pass
        else:
            return False
        i -= 1
    return True


def fillleagues(names, distr):
    dict = {}
    teams = []
    for n in range(len(distr)):
        while (distr[n] != len(teams)):
            teams.append(names.pop())
        dict[n+1] = deepcopy(teams)
        del teams[:]
    return deepcopy(dict)


def genhorari(leagues):
    timetable = {}

    for elem in leagues:

        horari = {}
        teamshour = []
        # numero equips
        tope = len(leagues[elem])

        clubes = leagues[elem]
        #for i in range(tope):
        #	clubes.append(i)
        auxT = len(clubes)
        impar = (auxT % 2 != 0)
        if (impar):
            auxT += 1
        #total partits ronda
        totalP = (auxT * (auxT - 1)) / 2
        local = [None] * totalP
        visita = [None] * totalP
        #per fer mod cada inici data
        modIF = auxT / 2
        indiceInverso = auxT - 2

        for i in range(totalP):
            if ((i % modIF) == 0):  #partit inicial de cada data
                if (impar):  #la primera data es borra si son impars
                    local[i] = "null"
                    visita[i] = "null"
                else:  #es fqe un local otro visita al ultim equip
                    if (i % 2 == 0):
                        local[i] = clubes[i % (auxT - 1)]
                        visita[i] = clubes[auxT - 1]
                    else:
                        local[i] = clubes[auxT - 1]
                        visita[i] = clubes[i % (auxT - 1)]
            else:
                local[i] = clubes[i % (auxT - 1)]
                visita[i] = clubes[indiceInverso]
                indiceInverso -= 1
                if (indiceInverso < 0):
                    indiceInverso = auxT - 2
        j = -2
        cont = 0
        if(impar):
            partits_jornada = (len(clubes) / 2)+1
        else:
            partits_jornada = (len(clubes) / 2)
        for i in range(totalP):
            if (i % partits_jornada == 0):
                hour = str(j) + ":00"
                #print hour
                j += 2
                cont = 1
            if (local[i] != "null"):
                #print local[i] + " vs " + visita[i]
                teamshour.append([deepcopy(local[i]), deepcopy(visita[i])])
                if (cont == partits_jornada):
                    horari[j] = deepcopy(teamshour)
                    del teamshour[:]
            cont += 1
        timetable[elem] = deepcopy(horari)
    return timetable


# print horari

def generate_leagues():
    num = Team.objects.count()
    distr = distribucio(num)
    teams = Team.objects.all().values_list('name', flat=True)
    team_list = []
    for team in teams:
        team_list.append(team)
    leagues = fillleagues(team_list, distr)
    for league in leagues:
        entry_league = League(id=league)
        entry_league.save()
        for team in leagues[league]:
            team_entry = Team.objects.get(name=team)
            team_entry.set_league(entry_league)
            team_entry.save()
    return leagues

def generate_competition(leagues):
    timetable = genhorari(leagues)
    print show_correct(timetable)
    partial = 0
    for league in timetable:
        partial = partial + 1
        partial_league = 0
        for horari in timetable[league]:
            partial_league += 1
            # data = ""
            # hora = ""
            # hora_mod = horari
            if horari >= 24:
                # data = "Diumenge"
                if horari != 24:
                    hora_mod = horari-24-1
                else:
                    hora_mod = horari-24
                data = datetime.datetime(2015, 5, 30, hora_mod)
            else:
                # data = "Dissabte"
                data = datetime.datetime(2015, 5, 31, horari)
            # if horari < 10:
            #     hora = "0"+str(hora_mod)+":00"
            # else:
            #     hora = str(hora_mod)+":00"
            if not Rounds.objects.filter(data=data).exists():
                entry_round = Rounds(data=data)
                entry_round.save()
            else:
                entry_round = Rounds.objects.get(data=data)
            for match in timetable[league][horari]:
                local_team = Team.objects.get(name=match[0])
                visitor_team = Team.objects.get(name=match[1])
                entry_match = Match(local_team=local_team,visitor_team=visitor_team,round=entry_round)
                entry_match.save()
                match_statistic_l = Statistics(team=local_team, match=entry_match)
                match_statistic_v = Statistics(team=visitor_team, match=entry_match)
                match_statistic_l.save()
                match_statistic_v.save()
            print partial_league/float(len(timetable[league]))*100,"% \r",
        print partial/len(timetable)*100,"% \r",
    return timetable

def show_correct(data):
    print json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

def make_random_statistics(match_id):
    match = Match.objects.get(id=match_id)
    statistics_local = Statistics.objects.get(match=match, team=match.local_team)
    statistics_visitor = Statistics.objects.get(match=match, team=match.visitor_team)
    if bool(getrandbits(1)):
        winner = match.local_team.id
        local = Team.objects.get(id=match.local_team.id)
        local.points += 1
        local.save()
    else:
        winner = match.visitor_team.id
        visitor = Team.objects.get(id=match.visitor_team.id)
        visitor.points += 1
        visitor.save()
    match.winner = winner
    match.save()
    statistics_local.set_attributes(randint(1,12),randint(1,12))
    statistics_visitor.set_attributes(randint(1,12),randint(1,12))
    statistics_visitor.save()
    statistics_local.save()

def resoldre_reclamacio(id):
    reclamation = Reclamation.objects.get(id=id)
    # if bool(getrandbits(1)):
    #     winner = match.local_team.id
    #     local = Team.objects.get(id=match.local_team.id)
    #     local.points += 1
    #     local.save()
    # else:
    #     winner = match.visitor_team.id
    #     visitor = Team.objects.get(id=match.visitor_team.id)
    #     visitor.points += 1
    #     visitor.save()
    # recl


def round_statistics(id):
    structure_en = Rounds.objects.get(id=id)
    structure = structure_en.get_as_dict()
    xml = dicttoxml.dicttoxml(structure)
    dom = parseString(xml)
    data = {'type':"xml", 'id':id, 'text':dom.toprettyxml() }
    send_confimation_email("xacosa@gmail.com", data)
    return dom.toprettyxml()

def make_admin():
    team = Team(name='admin', is_admin=True)
    team.save()
    team.set_password('admin')
    team.save()

def make_referee(name, password):
    team = Team(name=name, is_referee=True)
    team.save()
    team.set_password(password)
    team.save()
    referee_g = Group.objects.get(name='Referee')
    team.group.add(referee_g)


def close_registers():
    leagues = generate_leagues()
    generate_competition(leagues)


def make_enable_team(team):
    team = Team.objects.get(name=team)
    team.set_password("xxx")
    team.save()

def create_groups():
    team_g = Group.objects.create(name='Team')
    referee_g = Group.objects.create(name='Referee')
    auth_g = Group.objects.create(name='Admin')

if __name__ == '__main__':
    # close_registers()
    # create_groups()
    # make_referee("ref1","xxx")
    team = Team.objects.get(id=1)
    print team.group
    referee_g = Group.objects.get(name='Referee')
    referee_g.team_set.add(team)
    team.group.add(referee_g)
    team.save()
    # make_admin()
    # make_enable_team("t1")
