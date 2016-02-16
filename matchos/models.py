from django.db import models


class Match(models.Model):
    team1 = models.CharField(max_length=50)
    team2 = models.CharField(max_length=50)
    winner = models.IntegerField()
    date = models.CharField(max_length=50)


class Team(models.Model):
    name = models.CharField(max_length=50)
    wins = models.IntegerField()
    loss = models.IntegerField()
    draw = models.IntegerField()


class MatchFootball(models.Model):
    hometeamname = models.CharField(max_length=50)
    hometeamid = models.IntegerField()
    awayteamname = models.CharField(max_length=50)
    awayteamid = models.IntegerField()
    goalshometeam = models.IntegerField(null=True)
    goalsawayteam = models.IntegerField(null=True)
    date = models.CharField(max_length=50)
    season_id = models.IntegerField()


class TeamFootball(models.Model):
    teamid = models.IntegerField()
    name = models.CharField(max_length=50)
    wins = models.IntegerField()
    loss = models.IntegerField()
    draw = models.IntegerField()
