# Create your views here.

from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.utils.datastructures import MultiValueDictKeyError

from django.shortcuts import render_to_response

from models import *
import math
import random
from decimal import *

from classifier import *

class Team: pass

skip_fields = ['teamA', 'teamB', 'id', 'teamname', 'year']
strip_fields = ['assists_per_game_allowed',
				'blocks_per_game_against',
				'free_throw_percentage',
				'free_throw_percentage_allowed',
				'offensive_rebounds_per_game_allowed',
				'pf_per_game_allowed',
				'ppg_allowed',
				'steals_per_game',
				'turnovers_per_game_against']
				
weights =  {"wins"	:	0.09975	,
			"losses"	:	0.08696	,
			"ppg"	:	0.07057	,
			"field_goal_percentage"	:	0.05187	,
			"assists_per_game"	:	0.03536	,
			"rebounds_per_game"	:	0.03227	,
			"field_goal_percentage_allowed"	:	0.02785	,
			"blocks_per_game"	:	0.02712	,
			"offensive_rebounds_per_game"	:	0.02621	,
			"turnovers_per_game"	:	0.01999	,
			"pf_per_game"	:	0.01806	,
			"three_point_percentage_allowed"	:	0.01702	,
			"three_point_percentage"	:	0.00494	,
			"steals_per_game_allowed"	:	0.00474	,
			"rebounds_per_game_allowed"	:	0.00453	,
			"assists_per_game_allowed"	:	0	,
			"blocks_per_game_against"	:	0	,
			"free_throw_percentage"	:	0	,
			"free_throw_percentage_allowed"	:	0	,
			"offensive_rebounds_per_game_allowed"	:	0	,
			"pf_per_game_allowed"	:	0	,
			"ppg_allowed"	:	0	,
			"steals_per_game"	:	0	,
			"turnovers_per_game_against"	:	0}

def index(request):
	teams = [team for team in Season.objects.all() if team.wins]
	numGames_list = [i for i in range(1, 33)]
	numGames = 8
	return render_to_response('bracket.html',
							  locals(),
							  context_instance=RequestContext(request))

def bracket(request):
	if request.POST:
		classifier = request.POST['classifier']
		try:
			request.POST['test']
			test(classifier)
			return HttpResponseRedirect('/NCAA/')
		except MultiValueDictKeyError: pass
		
		numGames = int(request.POST['number_of_games'])
		
		numGames_list = [i for i in range(1, 33)]
		selectedTeams = [request.POST['team'+str(i)] for i in range(1, numGames+1)]
		
		teams = []
		bracketTeams = []
		games = []
		for i in range(1, numGames+1, 2):
			teamSet = []
			
			teamstats = request.POST['team'+str(i)].split(' ')
			#print teamstats
			teamA = Team()
			teamA.year = teamstats[0]
			teamA.teamname = teamstats[1]
			if len(teamstats) > 2:
				teamA.teamname += ' '
				for j in range(2, len(teamstats)):
					teamA.teamname = teamA.teamname + teamstats[j]
					if j < len(teamstats)-1:
						teamA.teamname = teamA.teamname + ' '
			seasonA = Season.objects.get(teamname=teamA.teamname, year=teamA.year)
			teamSet.append(seasonA)
			#print seasonA
			#bracketTeams.append(str(seasonA.year) + ' ' + str(seasonA.teamname))
			
			teamstats = request.POST['team'+str(i+1)].split(' ')
			#print teamstats
			teamB = Team()
			teamB.year = teamstats[0]
			teamB.teamname = teamstats[1]
			if len(teamstats) > 2:
				teamB.teamname += ' '
				for j in range(2, len(teamstats)):
					teamB.teamname = teamB.teamname + teamstats[j]
					if j < len(teamstats)-1:
						teamB.teamname = teamB.teamname + ' '
			seasonB = Season.objects.get(teamname=teamB.teamname, year=teamB.year)
			teamSet.append(seasonB)
			#print seasonB
			#bracketTeams.append(str(seasonB.year) + ' ' + str(seasonB.teamname))

			season = Season(teamname='fun', year='0000')
			for field in seasonA._meta.get_all_field_names():
				if field not in skip_fields:
					if classifier.split('_')[len(classifier.split('_'))-1] == 'normalize':
						fieldA = getattr(seasonA, field)
						fieldB = getattr(seasonB, field)
						#setattr(season, field, (fieldA - fieldB)/(fieldA + fieldB))
						setattr(season, field, fieldA - fieldB)
					else: setattr(season, field, getattr(seasonA, field) - getattr(seasonB, field))
			#print season
			games.append(season)
			teams.append(teamSet)
		
		teamA = None; teamB = None
		tail = None
		while len(games) > 0:
			game = games.pop(0)
			teamSet = teams.pop(0)
			
			if classifier == 'cluster':
				(tail, winner) = classifyCluster(game)
			elif classifier == '3-cluster':
				(tail, winner) = classifyCluster(game, False, 3)
			elif classifier == '4-cluster':
				(tail, winner) = classifyCluster(game, False, 4)
			elif classifier == 'cluster_weighted':
				(_, winner) = classifyCluster(game, True)
			elif classifier == '3-cluster_weighted':
				(_, winner) = classifyCluster(game, True, 3)
			elif classifier == '4-cluster_weighted':
				(_, winner) = classifyCluster(game, True, 4)
			elif classifier == 'decision_tree':
				winner = classifyDecisionTree(game)
			elif classifier == 'naive_bayes':
				(tail, winner) = classifyNaiveBayes(game)
			elif classifier == 'naive_bayes_stripped':
				(tail, winner) = classifyNaiveBayesStripped(game)
			elif classifier == 'naive_bayes_ranking':
				(tail, winner) = classifyRanking(teamSet[0], teamSet[1])
			elif classifier == 'naive_bayes_ranking_stripped':
				(tail, winner) = classifyRankingStripped(teamSet[0], teamSet[1])
			
			if winner == 'A':
				if not teamA:
					teamA = teamSet[0]
					
					addString = str(teamA.year) + ' ' + str(teamA.teamname)
					if tail is not None: addString += ' (' + str(tail) + ')'
					bracketTeams.append(addString)
				else:
					teamB = teamSet[0]
					
					addString = str(teamB.year) + ' ' + str(teamB.teamname)
					if tail is not None: addString += ' (' + str(tail) + ')'
					bracketTeams.append(addString)
					
					t = [teamA, teamB]
					teams.append(t)
					
					season = Season(teamname='fun', year='0000')
					for field in teamA._meta.get_all_field_names():
						if field not in skip_fields:
							if classifier.split('_')[len(classifier.split('_'))-1] == 'normalize':
								fieldA = getattr(teamA, field)
								fieldB = getattr(teamB, field)
								#setattr(season, field, (fieldA - fieldB)/(fieldA + fieldB))
								setattr(season, field, fieldA - fieldB)
							else: setattr(season, field, getattr(teamA, field) - getattr(teamB, field))
					
					teamA = None; teamB = None
					games.append(season)
					#print season
			else:
				if not teamA:
					teamA = teamSet[1]
					
					addString = str(teamA.year) + ' ' + str(teamA.teamname)
					if tail is not None: addString += ' (' + str(tail) + ')'
					bracketTeams.append(addString)
				else:
					teamB = teamSet[1]
					
					addString = str(teamB.year) + ' ' + str(teamB.teamname)
					if tail is not None: addString += ' (' + str(tail) + ')'
					bracketTeams.append(addString)
					
					t = [teamA, teamB]
					teams.append(t)
					
					season = Season(teamname='fun', year='0000')
					for field in teamA._meta.get_all_field_names():
						if field not in skip_fields:
							if classifier.split('_')[len(classifier.split('_'))-1] == 'normalize':
								fieldA = getattr(teamA, field)
								fieldB = getattr(teamB, field)
								#setattr(season, field, (fieldA - fieldB)/(fieldA + fieldB))
								setattr(season, field, fieldA - fieldB)
							else: setattr(season, field, getattr(teamA, field) - getattr(teamB, field))
					
					teamA = None; teamB = None
					games.append(season)
			tail = None
		#games = [['Berks', 'Ohio State', 'Shit', 'Shit State'], ['Shit A&M', 'Terra Tech'], ['Kate']]
		games = []
		while numGames > 0:
			numGames /= 2
			round = []
			for i in range(numGames):
				round.append(bracketTeams.pop(0))
			games.append(round)
		teams = [team for team in Season.objects.all() if team.wins]
		numGames = int(request.POST['number_of_games'])
		return render_to_response('bracket.html',
								  locals(),
								  context_instance = RequestContext(request))
			
	else: return HttpResponseRedirect('/NCAA/')

def simulate(request):
	if request.POST:
		classifier = request.POST['classifier']
		try:
			request.POST['test']
			test(classifier)
			return HttpResponseRedirect('/NCAA/')
		except MultiValueDictKeyError: pass
		
		teamstats = request.POST['team1'].split(' ')
		teamA = Team()
		teamA.year = teamstats[0]
		teamA.teamname = teamstats[1]
		if len(teamstats) > 2:
			teamA.teamname += ' '
			for i in range(2, len(teamstats)):
				teamA.teamname = teamA.teamname + teamstats[i]
				if i < len(teamstats)-1:
					teamA.teamname = teamA.teamname + ' '
		seasonA = Season.objects.get(teamname=teamA.teamname, year=teamA.year)
		
		teamstats = request.POST['team2'].split(' ')
		teamB = Team()
		teamB.year = teamstats[0]
		teamB.teamname = teamstats[1]
		if len(teamstats) > 2:
			teamB.teamname += ' '
			for i in range(2, len(teamstats)):
				teamB.teamname = teamB.teamname + teamstats[i]
				if i < len(teamstats)-1:
					teamB.teamname = teamB.teamname + ' '
		seasonB = Season.objects.get(teamname=teamB.teamname, year=teamB.year)
		
		season = Season(teamname='fun', year='0000')
		for field in seasonA._meta.get_all_field_names():
			if field not in skip_fields:
				if classifier.split('_')[len(classifier.split('_'))-1] == 'normalize':
					fieldA = getattr(seasonA, field)
					fieldB = getattr(seasonB, field)
					setattr(season, field, (fieldA - fieldB)/(fieldA + fieldB))
					#setattr(season, field, fieldA - fieldB)
				else: setattr(season, field, getattr(seasonA, field) - getattr(seasonB, field))
		print season
		
		if classifier == 'cluster':
			(_, winner) = classifyCluster(season)
		elif classifier == '3-cluster':
			(_, winner) = classifyCluster(season, False, 3)
		elif classifier == '4-cluster':
			(_, winner) = classifyCluster(season, False, 4)
		elif classifier == 'cluster_weighted':
			(_, winner) = classifyCluster(season, True)
		elif classifier == '3-cluster_weighted':
			(_, winner) = classifyCluster(season, True, 3)
		elif classifier == '4-cluster_weighted':
			(_, winner) = classifyCluster(season, True, 4)
		elif classifier == 'decision_tree':
			winner = classifyDecisionTree(season)
		elif classifier == 'naive_bayes':
			(_, winner) = classifyNaiveBayes(season)
		elif classifier == 'naive_bayes_stripped':
				(tail, winner) = classifyNaiveBayesStripped(season)
		elif classifier == 'naive_bayes_ranking':
			(_, winner) = classifyRanking(seasonA, seasonB)
		elif classifier == 'naive_bayes_ranking_stripped':
			(tail, winner) = classifyRankingStripped(seasonA, seasonB)
		print 'WINNER: ' + winner
		return HttpResponseRedirect('/NCAA/')
	else: raise Http404()

def rankings_page(request):
	if request.POST:
		year = int(request.POST['year'])
		ranker = request.POST['ranker']
		rankings = []
		team = []
		if ranker == 'simple': nb = WekaClassifier('models/nb_tournamentResults.model', 'tournament_winners.arff')
		elif ranker == 'stripped':
			nb = WekaClassifier('models/nb_tournamentResultsStripped.model', 'stripped_data/tournament_winnersStripped.arff')
		for season in Season.objects.filter(year=year):
			if season.wins:
				for field in season._meta.get_all_field_names():
					if field not in skip_fields:
						if ranker == 'simple' or field not in strip_fields: team.append(getattr(season, field))
				rankings.append([nb.rank(team)[1], season.year, season.teamname])
				team = []
		rankings.sort()
		rankings.reverse()
		#for ranking in rankings:
		#	print ranking
	years = []
	for season in Season.objects.all():
		if season.year not in years: years.append(season.year)
	return render_to_response('rankings.html', 
							  locals(),
							  context_instance=RequestContext(request))
	
def test(classifier='cluster', startYear=2012, endYear=2012):
	correct = 0; incorrect = 0
	for game in Game.objects.all():
		if game.teamA.year >= startYear and game.teamA.year <= endYear:
			seasonA = game.teamA
			seasonB = game.teamB
			
			season = Season(teamname='fun', year='0000')
			for field in seasonA._meta.get_all_field_names():
				try:
					if classifier.split('_')[len(classifier.split('_'))-1] == 'normalize':
						fieldA = getattr(seasonA, field)
						fieldB = getattr(seasonB, field)
						setattr(season, field, (fieldA - fieldB)/(fieldA + fieldB))
						#setattr(season, field, fieldA - fieldB)
					else: setattr(season, field, getattr(seasonB, field) - getattr(seasonA, field))
				except TypeError: pass
			if classifier == 'cluster':
				(_, winner) = classifyCluster(season)
			elif classifier == '3-cluster':
				(_, winner) = classifyCluster(season, False, 3)
			elif classifier == '4-cluster':
				(_, winner) = classifyCluster(season, False, 4)
			elif classifier == 'cluster_weighted':
				(_, winner) = classifyCluster(season, True)
			elif classifier == '3-cluster_weighted':
				(_, winner) = classifyCluster(season, True, 3)
			elif classifier == '4-cluster_weighted':
				(_, winner) = classifyCluster(season, True, 4)
			elif classifier == 'decision_tree':
				winner = classifyDecisionTree(season)
			elif classifier == 'naive_bayes':
				(_, winner) = classifyNaiveBayes(season)
			elif classifier == 'naive_bayes_stripped':
				(tail, winner) = classifyNaiveBayesStripped(season)
			elif classifier == 'naive_bayes_ranking':
				(_, winner) = classifyRanking(seasonA, seasonB)
			elif classifier == 'naive_bayes_ranking_stripped':
				(tail, winner) = classifyRankingStripped(seasonA, seasonB)
			
			#else:
			#for field in seasonA._meta.get_all_field_names():
			#	try:
			#		setattr(season, field, getattr(seasonB, field) - getattr(seasonA, field))
			#	except TypeError: pass
			#print season
			#winner1 = classifyDecisionTree(season)
			#if flip:
			#	if winner == 'B': correct += 1
			#	else: incorrect += 1
			#else:
			if winner == 'B': correct += 1
			else: incorrect += 1
			#if winner == 'B': correct[1] += 1
			#else: incorrect[1] += 1
			#if winner == 'A' and winner1 == 'B': correct += 1
			#else: incorrect += 1
	
	print "correct: " + str(correct)# + ' ' + str(correct[1])
	print "incorrect: " + str(incorrect)# + ' ' + str(incorrect[1])

def classifyCluster(season, weight=False, num_clusters=2):
	clusters = []
	#if not normalize:
	if num_clusters == 2:
		clusters.append(Season(teamname="cluster1", year="0001",
						  assists_per_game=1.1914,
						  assists_per_game_allowed=0.6377,
						  blocks_per_game=1.1207,
						  blocks_per_game_against=0.3852,
						  field_goal_percentage=0.787,
						  field_goal_percentage_allowed=-0.6614,
						  free_throw_percentage=-0.4509,
						  free_throw_percentage_allowed=-0.8145,
						  losses=-1.4,
						  offensive_rebounds_per_game=1.6393,
						  offensive_rebounds_per_game_allowed=1.173,
						  pf_per_game=0.3923,
						  pf_per_game_allowed=0.8216,
						  ppg=6.0602,
						  ppg_allowed=2.7614,
						  rebounds_per_game=2.9518,
						  rebounds_per_game_allowed=1.678,
						  steals_per_game=1.0841,
						  steals_per_game_allowed=0.4589,
						  three_point_percentage=0.048,
						  three_point_percentage_allowed=-0.4152,
						  turnovers_per_game=0.6077,
						  turnovers_per_game_against=1.2564,
						  wins=1.7136))
		clusters.append(Season(teamname="cluster2", year="0002",
						  assists_per_game	=	0.0025,					  
						  assists_per_game_allowed=	-0.8718,						  blocks_per_game=	-0.3486,					  
						  blocks_per_game_against=	-0.2873,						  field_goal_percentage=	0.8052,					  
						  field_goal_percentage_allowed=	-0.5511,						  free_throw_percentage=	1.4052,
						  free_throw_percentage_allowed=	0.6211,						  losses=	-1.5955,
						  offensive_rebounds_per_game=	-0.7314,						  offensive_rebounds_per_game_allowed=	-0.9782,						  pf_per_game=	-1.1964,						  pf_per_game_allowed=	-0.6286,						  ppg=	-1.5173,						  ppg_allowed=	-3.8555,						  rebounds_per_game=	-1.1434,						  rebounds_per_game_allowed=	-2.2555,						  steals_per_game=	-0.8982,						  steals_per_game_allowed=	-0.7543,						  three_point_percentage=	0.9016,						  three_point_percentage_allowed=	-0.4755,						  turnovers_per_game=	-1.3825,						  turnovers_per_game_against=	-1.3948,						  wins=	1.8523))
	elif num_clusters == 3:
		clusters.append(Season(teamname="cluster1", year="0001",
						assists_per_game	=	0.5571	,
						assists_per_game_allowed	=	0.8971	,
						blocks_per_game	=	0.8206	,
						blocks_per_game_against	=	0.5716	,
						field_goal_percentage	=	-0.4439	,
						field_goal_percentage_allowed	=	0.0761	,
						free_throw_percentage	=	-0.7271	,
						free_throw_percentage_allowed	=	-0.7906	,
						losses	=	0.1774	,
						offensive_rebounds_per_game	=	1.6642	,
						offensive_rebounds_per_game_allowed	=	1.1781	,
						pf_per_game	=	0.8797	,
						pf_per_game_allowed	=	0.8542	,
						ppg	=	4.5032	,
						ppg_allowed	=	3.5942	,
						rebounds_per_game	=	2.3065	,
						rebounds_per_game_allowed	=	2.3687	,
						steals_per_game	=	1.2142	,
						steals_per_game_allowed	=	0.3974	,
						three_point_percentage	=	-0.9126	,
						three_point_percentage_allowed	=	-0.0348	,
						turnovers_per_game	=	0.63	,
						turnovers_per_game_against	=	1.6348	,
						wins	=	0.0097))
		clusters.append(Season(teamname="cluster2", year="0002",
						assists_per_game	=	-0.6822	,
						assists_per_game_allowed	=	-0.8997	,
						blocks_per_game	=	-0.71	,
						blocks_per_game_against	=	-0.2315	,
						field_goal_percentage	=	-0.0969	,
						field_goal_percentage_allowed	=	-0.033	,
						free_throw_percentage	=	1.5037	,
						free_throw_percentage_allowed	=	0.5956	,
						losses	=	-0.2399	,
						offensive_rebounds_per_game	=	-1.1564	,
						offensive_rebounds_per_game_allowed	=	-1.153	,
						pf_per_game	=	-0.9511	,
						pf_per_game_allowed	=	-0.8202	,
						ppg	=	-3.7321	,
						ppg_allowed	=	-3.8798	,
						rebounds_per_game	=	-2.1427	,
						rebounds_per_game_allowed	=	-2.0944	,
						steals_per_game	=	-1.0548	,
						steals_per_game_allowed	=	-0.8153	,
						three_point_percentage	=	0.3944	,
						three_point_percentage_allowed	=	-0.1206	,
						turnovers_per_game	=	-1.4782	,
						turnovers_per_game_against	=	-1.5143	,
						wins	=	0.2991))
		clusters.append(Season(teamname="cluster3", year="0003",
						assists_per_game	=	2.2956	,
						assists_per_game_allowed	=	-0.3707	,
						blocks_per_game	=	1.2578	,
						blocks_per_game_against	=	-0.2402	,
						field_goal_percentage	=	3.4912	,
						field_goal_percentage_allowed	=	-2.1948	,
						free_throw_percentage	=	0.653	,
						free_throw_percentage_allowed	=	-0.1253	,
						losses	=	-5.2048	,
						offensive_rebounds_per_game	=	1.0233	,
						offensive_rebounds_per_game_allowed	=	0.3639	,
						pf_per_game	=	-1.29	,
						pf_per_game_allowed	=	0.3349	,
						ppg	=	7.2325	,
						ppg_allowed	=	-1.4064	,
						rebounds_per_game	=	3.0863	,
						rebounds_per_game_allowed	=	-1.2695	,
						steals_per_game	=	0.1767	,
						steals_per_game_allowed	=	0.0341	,
						three_point_percentage	=	2.3056	,
						three_point_percentage_allowed	=	-1.3751	,
						turnovers_per_game	=	-0.2478	,
						turnovers_per_game_against	=	-0.3277	,
						wins	=	5.9036))
	elif num_clusters == 4:
		clusters.append(Season(teamname="cluster1", year="0001",
						assists_per_game	=	-0.0004	,
						assists_per_game_allowed	=	-0.0431	,
						blocks_per_game	=	1.3224	,
						blocks_per_game_against	=	0.4461	,
						field_goal_percentage	=	-0.9284	,
						field_goal_percentage_allowed	=	-1.8009	,
						free_throw_percentage	=	-2.5578	,
						free_throw_percentage_allowed	=	-1.3513	,
						losses	=	-0.694	,
						offensive_rebounds_per_game	=	1.9078	,
						offensive_rebounds_per_game_allowed	=	1.0319	,
						pf_per_game	=	0.4168	,
						pf_per_game_allowed	=	0.5806	,
						ppg	=	1.9573	,
						ppg_allowed	=	-0.1828	,
						rebounds_per_game	=	3.1573	,
						rebounds_per_game_allowed	=	1.9103	,
						steals_per_game	=	0.8246	,
						steals_per_game_allowed	=	0.1539	,
						three_point_percentage	=	-1.856	,
						three_point_percentage_allowed	=	-1.6496	,
						turnovers_per_game	=	0.3944	,
						turnovers_per_game_against	=	0.9841	,
						wins	=	0.9914))
		clusters.append(Season(teamname="cluster2", year="0002",
						assists_per_game	=	-0.8936	,
						assists_per_game_allowed	=	-0.2609	,
						blocks_per_game	=	-1.0694	,
						blocks_per_game_against	=	-0.0396	,
						field_goal_percentage	=	-0.4753	,
						field_goal_percentage_allowed	=	1.1996	,
						free_throw_percentage	=	2.3438	,
						free_throw_percentage_allowed	=	0.7285	,
						losses	=	1.3106	,
						offensive_rebounds_per_game	=	-1.4183	,
						offensive_rebounds_per_game_allowed	=	-0.9306	,
						pf_per_game	=	-0.5974	,
						pf_per_game_allowed	=	-0.723	,
						ppg	=	-3.3979	,
						ppg_allowed	=	-1.6055	,
						rebounds_per_game	=	-2.9732	,
						rebounds_per_game_allowed	=	-1.3613	,
						steals_per_game	=	-0.9157	,
						steals_per_game_allowed	=	-0.7421	,
						three_point_percentage	=	0.503	,
						three_point_percentage_allowed	=	0.7247	,
						turnovers_per_game	=	-1.3523	,
						turnovers_per_game_against	=	-1.157	,
						wins	=	-1.4043))
		clusters.append(Season(teamname="cluster3", year="0003",
						assists_per_game	=	2.3915	,
						assists_per_game_allowed	=	1.2261	,
						blocks_per_game	=	0.7854	,
						blocks_per_game_against	=	0.3487	,
						field_goal_percentage	=	2.5457	,
						field_goal_percentage_allowed	=	0.6688	,
						free_throw_percentage	=	1.7372	,
						free_throw_percentage_allowed	=	-0.1075	,
						losses	=	-2.5226	,
						offensive_rebounds_per_game	=	1.5075	,
						offensive_rebounds_per_game_allowed	=	1.198	,
						pf_per_game	=	0.406	,
						pf_per_game_allowed	=	1.3015	,
						ppg	=	10.5739	,
						ppg_allowed	=	5.7286	,
						rebounds_per_game	=	2.8457	,
						rebounds_per_game_allowed	=	1.2221	,
						steals_per_game	=	1.3181	,
						steals_per_game_allowed	=	0.7492	,
						three_point_percentage	=	1.8452	,
						three_point_percentage_allowed	=	0.5714	,
						turnovers_per_game	=	0.8352	,
						turnovers_per_game_against	=	1.5925	,
						wins	=	2.799))
		clusters.append(Season(teamname="cluster4", year="0004",
						assists_per_game	=	1.2126	,
						assists_per_game_allowed	=	-1.2883	,
						blocks_per_game	=	0.5977	,
						blocks_per_game_against	=	-0.5631	,
						field_goal_percentage	=	2.435	,
						field_goal_percentage_allowed	=	-2.4799	,
						free_throw_percentage	=	0.5458	,
						free_throw_percentage_allowed	=	0.3673	,
						losses	=	-4.5	,
						offensive_rebounds_per_game	=	-0.0458	,
						offensive_rebounds_per_game_allowed	=	-0.8103	,
						pf_per_game	=	-1.8266	,
						pf_per_game_allowed	=	-0.6491	,
						ppg	=	1.1173	,
						ppg_allowed	=	-5.6154	,
						rebounds_per_game	=	0.914	,
						rebounds_per_game_allowed	=	-2.9	,
						steals_per_game	=	-0.7318	,
						steals_per_game_allowed	=	-0.6561	,
						three_point_percentage	=	1.6963	,
						three_point_percentage_allowed	=	-1.3701	,
						turnovers_per_game	=	-1.3121	,
						turnovers_per_game_against	=	-1.5617	,
						wins	=	5.1963))
	"""
	else:
		clusters.append(Season(teamname="cluster1", year="0001",
						  assists_per_game	=	0.1357	,
						  assists_per_game_allowed	=	0.0785	,
						  blocks_per_game	=	0.1805	,
						  blocks_per_game_against	=	0.1561	,
						  field_goal_percentage	=	0.0658	,
						  field_goal_percentage_allowed	=	-0.0856	,
						  free_throw_percentage	=	-0.0299	,
						  free_throw_percentage_allowed	=	-0.0794	,
						  losses	=	-0.1332	,
						  offensive_rebounds_per_game	=	0.1998	,
						  offensive_rebounds_per_game_allowed	=	0.2202	,
						  pf_per_game	=	0.0609	,
						  pf_per_game_allowed	=	0.1274	,
						  ppg	=	0.2207	,
						  ppg_allowed	=	0.1145	,
						  rebounds_per_game	=	0.1643	,
						  rebounds_per_game_allowed	=	0.154	,
						  steals_per_game	=	0.159	,
						  steals_per_game_allowed	=	0.1157	,
						  three_point_percentage	=	0.0046	,
						  three_point_percentage_allowed	=	-0.0524	,
						  turnovers_per_game	=	0.0908	,
						  turnovers_per_game_against	=	0.1585	,
						  wins	=	0.0851))
		clusters.append(Season(teamname="cluster2", year="0002",
						  assists_per_game	=	-0.0014	,
						  assists_per_game_allowed	=	-0.1071	,
						  blocks_per_game	=	-0.0572	,
						  blocks_per_game_against	=	-0.1148	,
						  field_goal_percentage	=	0.0602	,
						  field_goal_percentage_allowed	=	-0.0624	,
						  free_throw_percentage	=	0.0879	,
						  free_throw_percentage_allowed	=	0.0604	,
						  losses	=	-0.1388	,
						  offensive_rebounds_per_game	=	-0.0896	,
						  offensive_rebounds_per_game_allowed	=	-0.182	,
						  pf_per_game	=	-0.186	,
						  pf_per_game_allowed	=	-0.0974	,
						  ppg	=	-0.0565	,
						  ppg_allowed	=	-0.1598	,
						  rebounds_per_game	=	-0.0651	,
						  rebounds_per_game_allowed	=	-0.2073	,
						  steals_per_game	=	-0.1311	,
						  steals_per_game_allowed	=	-0.1886	,
						  three_point_percentage	=	0.0731	,
						  three_point_percentage_allowed	=	-0.0501	,
						  turnovers_per_game	=	-0.2043	,
						  turnovers_per_game_against	=	-0.1755	,
						  wins	=	0.0853))
	"""
	
	distances = []
	# Get distance from instance to each cluster
	for cluster in clusters:
		distance = 0
		for field in season._meta.get_all_field_names():
			if field not in skip_fields:
				val1 = float(getattr(season, field))
				val2 = getattr(cluster, field)
				
				#distance += math.pow((val1 - val2)/(val1 + val2), 2)
				if not weight: distance += math.pow(val1 - val2, 2)
				else: distance += weights[field] * math.pow(val1 - val2, 2)
		distances.append(math.sqrt(distance))
	
	# Flip the instance around (switch teamA and teamB)
	for field in season._meta.get_all_field_names():
		if field not in skip_fields:
			setattr(season, field, getattr(season, field) * -1)
	
	# Get distances for the other way around
	for cluster in clusters:
		distance = 0
		for field in season._meta.get_all_field_names():
			if field not in skip_fields:
				val1 = float(getattr(season, field))
				val2 = getattr(cluster, field)
				
				#distance += math.pow((val1 - val2)/(val1 + val2), 2)
				if not weight: distance += math.pow(val1 - val2, 2)
				else: distance += weights[field] * math.pow(val1 - val2, 2)
		distances.append(math.sqrt(distance))
	
	"""distanceACluster1 = 0
	for field in season._meta.get_all_field_names():
		if field not in skip_fields:
			val1 = float(getattr(season, field))
			val2 = getattr(cluster1, field)
			try: 
				distanceACluster1 += math.pow((val1 - val2)/(val1 + val2), 2)
				#distanceACluster1 += math.pow((val1 - val2),2)
			except OverflowError: break
	distanceACluster1 = math.sqrt(distanceACluster1)
	
	distanceACluster2 = 0
	for field in season._meta.get_all_field_names():
		if field not in skip_fields:
			val1 = float(getattr(season, field))
			val2 = getattr(cluster2, field)
			try: 
				distanceACluster2 += math.pow((val1 - val2)/(val1 + val2), 2)
				#distanceACluster2 += math.pow((val1 - val2), 2)
			except OverflowError: break
	distanceACluster2 = math.sqrt(distanceACluster2)

	for field in season._meta.get_all_field_names():
		if field not in skip_fields:
			setattr(season, field, getattr(season, field) * -1)
	
	distanceBCluster1 = 0
	for field in season._meta.get_all_field_names():
		if field not in skip_fields:
			val1 = float(getattr(season, field))
			val2 = getattr(cluster1, field)
			try: 
				distanceBCluster1 += math.pow((val1 - val2)/(val1 + val2), 2)
				#distanceBCluster1 += math.pow((val1 - val2),2)
			except OverflowError: break
	distanceBCluster1 = math.sqrt(distanceBCluster1)
	
	distanceBCluster2 = 0
	for field in season._meta.get_all_field_names():
		if field not in skip_fields:
			val1 = float(getattr(season, field))
			val2 = getattr(cluster2, field)
			try:
				distanceBCluster2 += math.pow((val1 - val2)/(val1 + val2), 2)
				#distanceBCluster2 += math.pow((val1 - val2),2)
			except OverflowError: break
	distanceBCluster2 = math.sqrt(distanceBCluster2)
	
	print distanceACluster1
	print distanceACluster2
	print distanceBCluster1
	print distanceBCluster2
	"""
	
	#for distance in distances:
	#	print distance
	
	minCluster = 0; minDistance = float('inf')
	for i, distance in enumerate(distances):
		if distance < minDistance:
			minDistance = distance
			minCluster = i
	#print minDistance, minCluster, len(clusters)
	
	if minCluster < len(clusters): 
		#print 'A\n'
		return (minCluster, 'A')
	else:
		#print 'B\n'
		return (minCluster-num_clusters, 'B')

def classifyNaiveBayes(season):
	nbClassifier = WekaClassifier('models/nb_trainingOnly.model', 'trainingData.arff')
	s = []
	for field in season._meta.get_all_field_names():
		if field not in skip_fields:
			s.append(getattr(season, field))
	percentage = nbClassifier.rank(s)
	if percentage[0] > percentage[1]:
		return ("%.2f" % percentage[0], 'B')
	else: return ("%.2f" % percentage[1], 'A')

def classifyNaiveBayesStripped(season):
	nbClassifier = WekaClassifier('models/nb_stripped.model', 'stripped_data/stripped_dataBayes.arff')
	s = []
	for field in season._meta.get_all_field_names():
		if field not in skip_fields and field not in strip_fields:
			s.append(getattr(season, field))
	percentage = nbClassifier.rank(s)
	if percentage[0] > percentage[1]:
		return ("%.2f" % percentage[0], 'B')
	else: return ("%.2f" % percentage[1], 'A')

def classifyRanking(teamA, teamB):
	nb = WekaClassifier('models/nb_tournamentResults.model', 'tournament_winners.arff')
	teamAStats = []
	teamBStats = []
	for field in teamA._meta.get_all_field_names():
		if field not in skip_fields:
			teamAStats.append(getattr(teamA, field))
			teamBStats.append(getattr(teamB, field))
	percentA = nb.rank(teamAStats)
	percentB = nb.rank(teamBStats)
	#print percentA, percentB
	
	if percentA[1] > percentB[1]: return ('%.2f-%.2f' % (percentA[1], percentB[1]), 'A')
	else: return ('%.2f-%.2f' % (percentB[1], percentA[1]), 'B')

def classifyRankingStripped(teamA, teamB):
	nb = WekaClassifier('models/nb_tournamentResultsStripped.model', 'stripped_data/tournament_winnersStripped.arff')
	teamAStats = []
	teamBStats = []
	for field in teamA._meta.get_all_field_names():
		if field not in skip_fields and field not in strip_fields:
			teamAStats.append(getattr(teamA, field))
			teamBStats.append(getattr(teamB, field))
	percentA = nb.rank(teamAStats)
	percentB = nb.rank(teamBStats)
	#print percentA, percentB
	
	if percentA[1] > percentB[1]: return ('%.2f-%.2f' % (percentA[1], percentB[1]), 'A')
	else: return ('%.2f-%.2f' % (percentB[1], percentA[1]), 'B')
	
def classifyDecisionTree(season):
	if season.wins <= 1:
		if season.wins <= -7:
			if season.blocks_per_game <= 0.8:
				if season.steals_per_game <= -3.4:
					if season.three_point_percentage_allowed <= 1.8: return 'B'
					if season.three_point_percentage_allowed > 1.8: return 'A'
				if season.steals_per_game > -3.4: return 'B'
			if season.blocks_per_game > 0.8:
				if season.assists_per_game_allowed <= -0.5: return 'A'
				if season.assists_per_game_allowed > -0.5:
					if season.blocks_per_game <= 1.1: return 'A'
					if season.blocks_per_game > 1.1: return 'B'
		if season.wins > -7:
			if season.ppg <= 6.9:
				if season.turnovers_per_game <= 2.4:
					if season.blocks_per_game_against <= 0.1: return 'B'
					if season.blocks_per_game_against > 0.1:
						if season.pf_per_game <= 3.6:
							if season.field_goal_percentage_allowed <= -0.2:
								if season.free_throw_percentage <= 3.9:
									if season.turnovers_per_game_against <= -2.4: return 'B'
									if season.turnovers_per_game_against > -2.4:
										if season.assists_per_game_allowed <= -1.4: return 'A'
										if season.assists_per_game_allowed > -1.4:
											if season.assists_per_game_allowed <= -0.2:
												if season.three_point_percentage <= -2.6: return 'A'
												if season.three_point_percentage > -2.6: return 'B'
											if season.assists_per_game_allowed > -0.2:
												if season.losses <= 2: return 'A'
												if season.losses > 2:
													if season.steals_per_game <= 0.6: return 'B'
													if season.steals_per_game > 0.6: return 'A'
								if season.free_throw_percentage > 3.9: return 'A'
							if season.field_goal_percentage_allowed > -0.2:
								if season.three_point_percentage <= -2.9:
									if season.three_point_percentage <= -7.6: return 'A'
									if season.three_point_percentage > -7.6: return 'B'
								if season.three_point_percentage > -2.9:
									if season.free_throw_percentage_allowed <= -2.1:
										if season.three_point_percentage_allowed <= -2.4: return 'B'
										if season.three_point_percentage_allowed > -2.4: return 'A'
									if season.free_throw_percentage_allowed > -2.1:
										if season.free_throw_percentage <= 8.2:
											if season.assists_per_game_allowed <= 2.3:
												if season.steals_per_game_allowed <= -0.7:
													if season.rebounds_per_game_allowed <= 1.2: return 'A'
													if season.rebounds_per_game_allowed > 1.2: return 'B'
												if season.steals_per_game_allowed > -0.7:
													if season.offensive_rebounds_per_game_allowed <= 0.4:
														if season.pf_per_game <= 2.3: return 'B'
														if season.pf_per_game > 2.3: return 'A'
													if season.offensive_rebounds_per_game_allowed > 0.4:
														if season.field_goal_percentage_allowed <= 1.2: return 'B'
														if season.field_goal_percentage_allowed > 1.2: return 'A'
											if season.assists_per_game_allowed > 2.3: return 'B'
										if season.free_throw_percentage > 8.2: return 'A'
						if season.pf_per_game > 3.6: return 'B'
				if season.turnovers_per_game > 2.4:
					if season.three_point_percentage_allowed <= 0.2:
						if season.pf_per_game <= 2.4:
							if season.field_goal_percentage <= 2.1:
								if season.field_goal_percentage_allowed <= -3.5: return 'A'
								if season.field_goal_percentage_allowed > -3.5: return 'B'
							if season.field_goal_percentage > 2.1: return 'A'
						if season.pf_per_game > 2.4: return 'A'
					if season.three_point_percentage_allowed > 0.2: return 'B'
			if season.ppg > 6.9:
				if season.ppg_allowed <= 10.8:
					if season.offensive_rebounds_per_game_allowed <= 3.3: return 'A'
					if season.offensive_rebounds_per_game_allowed > 3.3:
						if season.free_throw_percentage <= -1.6: return 'B'
						if season.free_throw_percentage > -1.6: return 'A'
				if season.ppg_allowed > 10.8:
					if season.pf_per_game <= 3.2: return 'B'
					if season.pf_per_game > 3.2: return 'A'
	if season.wins > 1:
		if season.wins <= 5:
			if season.pf_per_game <= 2.1:
				if season.rebounds_per_game <= 5:
					if season.losses <= -5:
						if season.assists_per_game_allowed <= 2.1: return 'A'
						if season.assists_per_game_allowed > 2.1: return 'B'
					if season.losses > -5:
						if season.free_throw_percentage_allowed <= -0.5:
							if season.three_point_percentage_allowed <= -1.2:
								if season.ppg_allowed <= 0.8:
									if season.steals_per_game_allowed <= -1.8: return 'B'
									if season.steals_per_game_allowed > -1.8:
										if season.field_goal_percentage_allowed <= -3.2:
											if season.blocks_per_game_against <= -0.6: return 'B'
											if season.blocks_per_game_against > -0.6: return 'A'
										if season.field_goal_percentage_allowed > -3.2: return 'A'
								if season.ppg_allowed > 0.8: return 'B'
							if season.three_point_percentage_allowed > -1.2:
								if season.pf_per_game_allowed <= -3.1:
									if season.blocks_per_game_against <= -0.3: return 'B'
									if season.blocks_per_game_against > -0.3: return 'A'
								if season.pf_per_game_allowed > -3.1:
									if season.offensive_rebounds_per_game_allowed <= 1.9: return 'A'
									if season.offensive_rebounds_per_game_allowed > 1.9: return 'B'
						if season.free_throw_percentage_allowed > -0.5:
							if season.wins <= 2:
								if season.three_point_percentage <= -0.5: return 'B'
								if season.three_point_percentage > -0.5:
									if season.free_throw_percentage_allowed <= 1.8:
										if season.pf_per_game_allowed <= 1.5: return 'B'
										if season.pf_per_game_allowed > 1.5: return 'A'
									if season.free_throw_percentage_allowed > 1.8: return 'A'
							if season.wins > 2:
								if season.offensive_rebounds_per_game <= -0.3:
									if season.losses <= 0:
										if season.pf_per_game <= 0: return 'B'
										if season.pf_per_game > 0:
											if season.free_throw_percentage_allowed <= 5.3: return 'A'
											if season.free_throw_percentage_allowed > 5.3: return 'B'
									if season.losses > 0: return 'A'
								if season.offensive_rebounds_per_game > -0.3:
									if season.offensive_rebounds_per_game <= 2.4: return 'A'
									if season.offensive_rebounds_per_game > 2.4: return 'B'
				if season.rebounds_per_game > 5: return 'A'
			if season.pf_per_game > 2.1:
				if season.three_point_percentage <= -1.3:
					if season.offensive_rebounds_per_game <= 1.6: return 'B'
					if season.offensive_rebounds_per_game > 1.6: return 'A'
				if season.three_point_percentage > -1.3: return 'B'
		if season.wins > 5:
			if season.offensive_rebounds_per_game_allowed <= -0.7:
				if season.field_goal_percentage_allowed <= 1.5:
					if season.field_goal_percentage <= -1.7: return 'B'
					if season.field_goal_percentage > -1.7:
						if season.steals_per_game_allowed <= 1.2: return 'A'
						if season.steals_per_game_allowed > 1.2: return 'B'
				if season.field_goal_percentage_allowed > 1.5: return 'B'
			if season.offensive_rebounds_per_game_allowed > -0.7:
				if season.three_point_percentage_allowed <= -4.1:
					if season.offensive_rebounds_per_game <= -2: return 'B'
					if season.offensive_rebounds_per_game > -2:
						if season.three_point_percentage <= 0.6:
							if season.assists_per_game <= 0: return 'A'
							if season.assists_per_game > 0: return 'B'
						if season.three_point_percentage > 0.6: return 'A'
				if season.three_point_percentage_allowed > -4.1: return 'A'