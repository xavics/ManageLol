from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
from itertools import chain
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
    league = models.ForeignKey(League, related_name='league', blank=True, null=True)
    USERNAME_FIELD = 'name'
    # REQUIRED_FIELDS = ['email']
    is_admin = models.BooleanField(default=False)
    objects = UserManager()

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


class Rounds(models.Model):
    data = models.DateTimeField()
    # data = models.CharField(max_length=20)
    # hora = models.CharField(max_length=5)


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

class Statistics(models.Model):
    team = models.ForeignKey(Team, related_name='steam')
    match = models.ForeignKey(Match, related_name='smatch')
    killed = models.IntegerField(default=0)
    dead = models.IntegerField(default=0)

    def set_attributes(self, killed, dead):
        self.killed = killed
        self.dead = dead


class Notice(models.Model):
    text = models.TextField(max_length=250)

class Resolution(models.Model):
    match = models.ForeignKey(Match, related_name='rmatch')
    description = models.TextField(max_length=250)
    solved = models.BooleanField(default=False)
    resultat = models.TextField(max_length=250, blank=True, null=True)

