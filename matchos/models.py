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


class Player(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    team_id = models.IntegerField()
    position = models.CharField(max_length=50, blank=True, null=True)
    jersey_number = models.IntegerField( blank=True, null=True)
    date_of_birth = models.CharField(max_length=50, blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    contract_until = models.CharField(max_length=50, blank=True, null=True)
    market_value = models.CharField(max_length=50, blank=True, null=True)


class LeagueTable(models.Model):
    league_id = models.IntegerField()
    team_id = models.IntegerField()
    team_name = models.CharField(max_length=50, blank=True, null=True)
    rank = models.IntegerField()
    played_games = models.IntegerField()
    crest_uri = models.CharField(max_length=200)
    points = models.IntegerField()
    goals = models.IntegerField()
    goals_against = models.IntegerField()
    goal_difference = models.IntegerField()
