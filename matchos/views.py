from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse
from django.template import loader
from .models import Team, Match, MatchFootball, TeamFootball, Player, LeagueTable
from django.db.models import Q
from django.template import RequestContext
from matchos.search import get_query
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
    return render_to_response('matchos/index.html')


def dota(request):
    return render_to_response('matchos/dota2.html')


def dotarank(request):
    team_rank = Team.objects.all().extra(
        select={'winloss':'wins - loss'},
        order_by=('-winloss',)
    )
    template = loader.get_template('matchos/dotarank.html')
    context = {
        'team_rank': team_rank
    }
    return HttpResponse(template.render(context, request))


def teamdotadetail(request, team_id):

    team = get_object_or_404(Team, pk=team_id)
    matches = Match.objects.filter(Q(team1=team.name) | Q(team2=team.name))

    return render(request, 'matchos/teamdotadetail.html', {'team': team, 'matches': matches})


def dotamatches(request):
    matches = Match.objects.all()
    team = Team.objects.all()
    paginator = Paginator(matches, 25) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        matches = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        matches = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        matches = paginator.page(paginator.num_pages)

    context = {
        'matches': matches,
        'team': team,
    }
    template = loader.get_template('matchos/dotamatches.html')
    return HttpResponse(template.render(context, request))


def matchdotadetail(request, match_id):
    match = get_object_or_404(Match, pk=match_id)
    team1_name = match.team1
    team2_name = match.team2
    team1_object = get_object_or_404(Team, name=team1_name)
    team2_object = get_object_or_404(Team, name=team2_name)
    return render(request, 'matchos/matchdotadetail.html', {'match': match, 'team1_object': team1_object, 'team2_object': team2_object})


def football(request):
    matches = MatchFootball.objects.all()
    league_names = ['1. Bundesliga 15/16', '2. Bundesliga 15/16', 'Ligue 1 15/16', 'Ligue 2 15/16', 'Premier League 15/16',
                    'Primera Division 15/16', 'Segunda Division 15/16', 'Serie A 15/16', 'Primeira Liga 15/16',
                    '3. Bundesliga 15/16', 'Eredivisie 15/16', 'Champions League 15/16', 'League One 15/16']
    league_ids = [394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 425]
    template = loader.get_template('matchos/matchesfootball.html')
    context = {
        'matches': matches,
        'league_names': league_names,
        'league_ids': league_ids
    }
    return HttpResponse(template.render(context, request))


def season(request, season_id):
    matches = MatchFootball.objects.filter(season_id=season_id)
    table = LeagueTable.objects.filter(league_id=season_id)
    template = loader.get_template('matchos/leaguematches.html')
    context = {
        'matches': matches,
        'table': table
    }
    return HttpResponse(template.render(context, request))


def teamdetailfootball(request, team_id):
    team = TeamFootball.objects.get(teamid=team_id)
    team_name = TeamFootball.objects.filter(teamid=team_id).values('name')
    matches = MatchFootball.objects.filter(Q(hometeamname__in=team_name) | Q(awayteamname__in=team_name))
    players = Player.objects.filter(team_id=team_id)
    template = loader.get_template('matchos/teamfootballdetail.html')
    context = {
        'matches': matches,
        'team': team,
        'players': players,
    }
    return HttpResponse(template.render(context, request))


def searchview(request):
    query_string = ''
    found_entries = None
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']

        entry_query = get_query(query_string, ['hometeamname', 'awayteamname',])
        entry_query2 = get_query(query_string, ['team1', 'team2',])

        found_entries = MatchFootball.objects.filter(entry_query).order_by('date')
        found_entries2 = Match.objects.filter(entry_query2)

    return render_to_response('matchos/search_results.html',
                          { 'query_string': query_string, 'found_entries': found_entries, 'found_entries2': found_entries2 },
                          context_instance=RequestContext(request))


def about(request):
    return render_to_response('matchos/about.html')