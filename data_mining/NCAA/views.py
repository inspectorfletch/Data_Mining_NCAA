# Create your views here.

from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404, HttpResponse

from django.shortcuts import render_to_response

from models import *

def index(request):
	return render_to_response('base.html',
							  locals(),
							  context_instance=RequestContext(request))

def clasifyDecisionTree(season):
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
						if season.pf_per_game > 2.4: A (6.0/1.0)
					if season.three_point_percentage_allowed > 0.2: return 'B'
			if season.ppg > 6.9:
				if season.ppg_allowed <= 10.8:
					if season.offensive_rebounds_per_game_allowed <= 3.3: return 'A'
					if season.offensive_rebounds_per_game_allowed > 3.3:
						if season.free_throw_percentage <= -1.6: return 'B'
						if season.free_throw_percentage > -1.6: return 'A'
				if season.ppg_allowed > 10.8:
					if season.pf_per_game <= 3.2: return 'B'
					if season.pf_per_game > 3.2: A (3.0)
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