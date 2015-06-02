from copy import deepcopy
import datetime
from random import randint, getrandbits
import json
from ManageLol import settings
from Manager.models import Team, League, Rounds, Match, Statistics, Player, Reclamation, Competition
from rest_framework_xml.renderers import XMLRenderer
from xml.dom.minidom import parseString
from Riot import send_confimation_email
import dicttoxml


time_competition = datetime.datetime.now()


def set_time_closing_inscriptions(y, m, d, h, min, s):
    time_limit = datetime.datetime(y, m, d, h, min, s)
    if time_limit < datetime.datetime.now():
        return "Incorrect time"
    global time_competition
    time_competition = time_limit


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
    num = Team.objects.filter(is_admin=False, is_referee=False).count()
    distr = distribucio(num)
    teams = Team.objects.filter(is_admin=False, is_referee=False).values_list('name', flat=True)
    print teams
    if len(teams) <= 1:
        return "Insuficient number of teams"
    team_list = []
    for team in teams:
        team_list.append(team)
        print team_list
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
                data = datetime.datetime(2015, 6, 2, hora_mod)
            else:
                # data = "Dissabte"
                data = datetime.datetime(2015, 6, 2, horari)
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

def round_statistics(id):
    structure_en = Rounds.objects.get(id=id)
    structure = structure_en.get_as_dict()
    xml = dicttoxml.dicttoxml(structure)
    dom = parseString(xml)
    data = {'type':"xml", 'id':id, 'text':dom.toprettyxml() }
    send_confimation_email("xacosa@gmail.com", data)
    return dom.toprettyxml()


import django
def close_inscriptions():
    django.setup()
    leagues = generate_leagues()
    generate_competition(leagues)
    state = Competition.objects.get(id=1)
    state.state = "Close"
    state.save()


def open_inscriptions():
    state = Competition.objects.get(id=1)
    state.state = "Open"
    state.save()


def close_competition():
    state = Competition.objects.get(id=1)
    state.is_active = False
    state.save()

# if __name__ == '__main__':


