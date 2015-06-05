from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, Group
from itertools import chain
from collections import OrderedDict
# Create your models here.


class League(models.Model):
    id = models.AutoField(primary_key=True)

    def get_teams(self):
        team_list = []
        for team in Team.objects.filter(league=self):
            team_dict = {'name': team.name, 'points': team.points, 'dead': team.get_total_deaths(),
                         'killed': team.get_total_kills()}
            team_list.append(team_dict)
        return team_list


class Team(AbstractBaseUser):
    name = models.CharField(max_length=100, unique=True)
    points = models.IntegerField(default=0)
    email = models.CharField(max_length=100)
    group = models.ManyToManyField(Group)
    league = models.ForeignKey(League, related_name='league', blank=True, null=True)
    USERNAME_FIELD = 'name'
    # REQUIRED_FIELDS = ['email']
    is_admin = models.BooleanField(default=False)
    objects = UserManager()
    is_referee = models.BooleanField(default=False)

    def set_email(self,email):
        self.email = email

    def get_full_name(self):
        # The user is identified by their email address
        return self.name

    def get_short_name(self):
        # The user is identified by their email address
        return self.name

    def __unicode__(self):
        return self.name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def set_league(self, league):
        self.league = league

    def set_date(self, date):
        self.last_login = date

    def get_total_deaths(self):
        statistics = Statistics.objects.filter(team=self)
        dead = 0
        for statistic in statistics:
            dead += statistic.dead
        return dead

    def get_total_kills(self):
        statistics = Statistics.objects.filter(team=self)
        killed = 0
        for statistic in statistics:
            killed += statistic.killed
        return killed

    def get_statistics(self):
        return {'dead': self.get_total_deaths(), 'killed': self.get_total_kills()}

    def get_as_dict(self):
        return OrderedDict([('name',self.name),('email',self.email),('players',self.get_players_of_team_as_dict())])

    def get_players_of_team_as_dict(self):
        players_list = []
        for player in Player.objects.filter(team=self):
            players_list.append(player.get_as_dict())
        return players_list

class Player(models.Model):
    ROLES = (
        ('SU','Support'),
        ('JU','Jungle'),
        ('ADC','Attack damage carry'),
        ('MID','Middle'),
        ('SOLO','Solo')
    )
    name = models.CharField(max_length=100, unique=True)
    email = models.CharField(max_length=100)
    top = models.BooleanField(default=False)
    role = models.CharField(max_length=4, choices=ROLES)
    team = models.ForeignKey(Team, related_name='team')

    def __unicode__(self):
        return self.name

    def set_team(self, team):
        self.team = team

    def get_as_dict(self):
        return {'name':self.name,'email': self.email,'role':self.role}

class Rounds(models.Model):
    data = models.DateTimeField()
    # data = models.CharField(max_length=20)
    # hora = models.CharField(max_length=5)


    def get_as_dict(self):
        matches_en = Match.objects.filter(round=self.id)
        matches_count = matches_en.count()
        matches = []
        for match in matches_en:
            serial = match.get_as_dict()
            matches.append(serial)
        # d = {'id': self.id, 'data':str(self.data), 'matches_count':matches_count,'matches':matches}
        return OrderedDict([('id', self.id),('data',str(self.data)),('matches_count',matches_count),('matches',matches)])
        # return OrderedDict(sorted(d.items(), key=lambda x:x[1], reverse=True))


class Match(models.Model):
    local_team = models.ForeignKey(Team, related_name='local_team')
    visitor_team = models.ForeignKey(Team, related_name='visitor_team')
    round = models.ForeignKey(Rounds, related_name='round_')
    ip = models.CharField(max_length=20, blank=True, null=True)
    winner = models.IntegerField(blank=True, null=True)

    def get_statistics(self):
        local_st = Statistics.objects.filter(match=self, team=self.local_team)
        visitor_st = Statistics.objects.filter(match=self, team=self.visitor_team)
        return local_st, visitor_st

    def set_ip(self, ip):
        self.ip = ip

    def have_ip(self):
        if self.ip == '' or self.ip == None:
            return False
        else:
            return True

    def get_as_dict(self):
        local_st = Statistics.objects.get(match=self, team=self.local_team)
        visitor_st = Statistics.objects.get(match=self, team=self.visitor_team)
        statistics = [local_st.get_as_dict(),visitor_st.get_as_dict()]
        d = {'id': self.id, 'local': self.local_team.id,'visitor': self.visitor_team.id,'ip': self.ip, 'winner':self.winner,
                'statistics': statistics}
        return OrderedDict([('id', self.id),('local',self.local_team.id),('visitor',self.visitor_team.id),('ip',self.ip),
                    ('winner', self.winner), ('statistics', statistics)])
        # return OrderedDict(sorted(d.items(), key=lambda x:x[1], reverse=True))

class Statistics(models.Model):
    team = models.ForeignKey(Team, related_name='steam')
    match = models.ForeignKey(Match, related_name='smatch')
    killed = models.IntegerField(default=0)
    dead = models.IntegerField(default=0)

    def set_attributes(self, killed, dead):
        self.killed = killed
        self.dead = dead

    def get_as_dict(self):
        # d = {'id':self.id,'team':self.team.id,'dead':self.dead, 'killed':self.killed}
        return OrderedDict([('id',self.id),('team',self.team.id),('dead',self.dead),('killed',self.killed)])
        # return OrderedDict(sorted(d.items(), key=lambda x:x[1], reverse=True))



class Notice(models.Model):
    text = models.TextField(max_length=250)

class Reclamation(models.Model):
    match = models.ForeignKey(Match, related_name='rmatch')
    team = models.ForeignKey(Team, related_name='rteam')
    description = models.TextField(max_length=250)
    solved = models.BooleanField(default=False)
    result = models.TextField(max_length=250, blank=True, null=True)

    def resolve(self, result):
        self.solved = True
        self.result = result

class Competition(models.Model):
    state = models.CharField(max_length=10)
    generated = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)