"""testpip11 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^dota2$', views.dota, name='dotaindex'),
    url(r'^dota2/rank$', views.dotarank, name='dotarank'),
    url(r'^dota2/matches$', views.dotamatches, name='dotamatches'),
    url(r'^dota2/team/(?P<team_id>[0-9]+)/$', views.teamdotadetail, name='teamdetail'),
    url(r'^dota2/match/(?P<match_id>[0-9]+)/$', views.matchdotadetail, name='matchdetail'),
    url(r'^football$', views.football, name='footballindex'),
    url(r'^football/season/(?P<season_id>[0-9]+)/$', views.season, name='season'),
    url(r'^football/team/(?P<team_id>[0-9]+)/$', views.teamdetailfootball, name='teamdetailfootball'),
    url(r'^search$', views.searchview, name='search'),
    url(r'^about$', views.about, name='about'),
]
