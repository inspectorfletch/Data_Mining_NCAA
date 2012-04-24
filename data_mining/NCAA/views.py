# Create your views here.

from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404, HttpResponse

from django.shortcuts import render_to_response

from models import *
import math
import random
from decimal import *

class Team: pass

skip_fields = ['teamA', 'teamB', 'id', 'teamname', 'year']

def index(request):
	teams = [team for team in Season.objects.all() if team.wins]
	return render_to_response('bracket.html',
							  locals(),
							  context_instance=RequestContext(request))

def simulate(request):
	if request.POST:
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
			try:
				setattr(season, field, getattr(seasonA, field) - getattr(seasonB, field))
			except TypeError: pass
		print season
		
		#winner = classifyCluster(season)
		test_cluster()
		#print 'WINNER: ' + winner
		return HttpResponseRedirect('/NCAA/')
	else: raise Http404()

def test_cluster():
	#correct = [0, 0]
	#incorrect = [0, 0]
	correct = 0; incorrect = 0
	for game in Game.objects.all():
		seasonA = game.teamA
		seasonB = game.teamB
		
		season = Season(teamname='fun', year='0000')
		#flip = random.choice([True, False])
		#if flip:
		for field in seasonA._meta.get_all_field_names():
			try:
				setattr(season, field, getattr(seasonA, field) - getattr(seasonB, field))
			except TypeError: pass
		winner = classifyDecisionTree(season)
		#print winner
		#if winner == 'A': correct += 1
		#else: incorrect += 1
		
		
		#else:
		for field in seasonA._meta.get_all_field_names():
			try:
				setattr(season, field, getattr(seasonB, field) - getattr(seasonA, field))
			except TypeError: pass
		#print season
		winner1 = classifyDecisionTree(season)
		#if flip:
		#	if winner == 'B': correct += 1
		#	else: incorrect += 1
		#else:
		#if winner == 'B': correct[1] += 1
		#else: incorrect[1] += 1
		if winner == 'A' and winner1 == 'B': correct += 1
		else: incorrect += 1
	
	print "correct: " + str(correct)# + ' ' + str(correct[1])
	print "incorrect: " + str(incorrect)# + ' ' + str(incorrect[1])

def classifyCluster(season):
	cluster1 = Season(teamname="cluster1", year="0001",
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
					  wins=1.7136)
	cluster2 = Season(teamname="cluster2", year="0002",
					  assists_per_game	=	0.0025,					  
					  assists_per_game_allowed=	-0.8718,					  blocks_per_game=	-0.3486,					  
					  blocks_per_game_against=	-0.2873,					  field_goal_percentage=	0.8052,					  
					  field_goal_percentage_allowed=	-0.5511,					  free_throw_percentage=	1.4052,
					  free_throw_percentage_allowed=	0.6211,					  losses=	-1.5955,
					  offensive_rebounds_per_game=	-0.7314,					  offensive_rebounds_per_game_allowed=	-0.9782,					  pf_per_game=	-1.1964,					  pf_per_game_allowed=	-0.6286,					  ppg=	-1.5173,					  ppg_allowed=	-3.8555,					  rebounds_per_game=	-1.1434,					  rebounds_per_game_allowed=	-2.2555,					  steals_per_game=	-0.8982,					  steals_per_game_allowed=	-0.7543,					  three_point_percentage=	0.9016,					  three_point_percentage_allowed=	-0.4755,					  turnovers_per_game=	-1.3825,					  turnovers_per_game_against=	-1.3948,					  wins=	1.8523)
					  
	distanceACluster1 = 0
	for field in season._meta.get_all_field_names():
		if field not in skip_fields:
			val1 = float(getattr(season, field))
			val2 = getattr(cluster1, field)
			try: distanceACluster1 += math.exp((val1 - val2)/(val1 + val2))
			except OverflowError: break
	distanceACluster1 = math.sqrt(distanceACluster1)
	
	distanceACluster2 = 0
	for field in season._meta.get_all_field_names():
		if field not in skip_fields:
			val1 = float(getattr(season, field))
			val2 = getattr(cluster2, field)
			try: distanceACluster2 += math.exp((val1 - val2)/(val1 + val2))
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
			try: distanceBCluster1 += math.exp((val1 - val2)/(val1 + val2))
			except OverflowError: break
	distanceBCluster1 = math.sqrt(distanceBCluster1)
	
	distanceBCluster2 = 0
	for field in season._meta.get_all_field_names():
		if field not in skip_fields:
			val1 = float(getattr(season, field))
			val2 = getattr(cluster2, field)
			try:
				distanceBCluster2 += math.exp((val1 - val2)/(val1 + val2))
			except OverflowError: break
	distanceBCluster2 = math.sqrt(distanceBCluster2)
	
	print distanceACluster1
	print distanceACluster2
	print distanceBCluster1
	print distanceBCluster2
	
	minDistance = min(distanceACluster1, distanceACluster2, distanceBCluster1, distanceBCluster2)
	if (minDistance == distanceACluster1 or minDistance == distanceACluster2): return 'A'
	else: return 'B'
	
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