from rest_framework import serializers
from Manager.models import Player, Team, League, Match, Rounds, Statistics


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('name','email','top','role','team')


class TeamSerializer(serializers.ModelSerializer):
    team = PlayerSerializer(many=True)
    class Meta:
        model = Team
        fields = ('name','points','email','team', 'league')


class LeagueSerializer(serializers.ModelSerializer):
    league = TeamSerializer(many=True)
    class Meta:
        model = League
        fields = ('league',)


class MatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Match
        fields = ('local_team','visitor_team','ip','winner')

class StatisticsSerializer(serializers.ModelSerializer):
    smatch = MatchSerializer()
    class Meta:
        model = Statistics
        fields = ('team','killed','dead')


class RoundSerializer(serializers.ModelSerializer):
    round = MatchSerializer(many=True)
    class Meta:
        model = Rounds
        fields = ('data','round')