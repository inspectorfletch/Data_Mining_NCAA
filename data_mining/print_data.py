from NCAA.models import *
import random
#from __future__ import print_function

skip_fields = ['teamA', 'teamB', 'id', 'teamname', 'year']

games = Game.objects.all()
print_string = ''
for field in games[0].teamA._meta.get_all_field_names():
	if field not in skip_fields:
		#print_fields.append(field)
		#print (field, end=' ')
		print_string = print_string + field.strip('\n ') + ','
print_string = print_string + 'winner'
print print_string
	
	#print "".join(field+' ' for field in print_fields).strip()

for game in games:
	game_data = ''
	teamA_data = []
	teamB_data = []
	for field in game.teamA._meta.get_all_field_names():
		if field not in skip_fields:
			#print field + ': ' + str(getattr(game.teamA, field))
			#game_data.append(getattr(game.teamA, field))
			#game_data = game_data + str(getattr(game.teamA, field)) + ' '
			teamA_data.append(getattr(game.teamA, field))
	for field in game.teamB._meta.get_all_field_names():
		if field not in skip_fields:
			#print field + ': ' + str(getattr(game.teamA, field))
			#game_data.append(getattr(game.teamB, field))
			teamB_data.append(getattr(game.teamB, field))
	
	winner = 'A'
	if random.choice([True, False]):
		winner = 'B'
		temp = teamA_data
		teamA_data = teamB_data
		teamB_data = temp
	
	for i in range(0, len(teamA_data)):
		game_data = game_data + str(teamA_data[i] - teamB_data[i]) + ','
	game_data = game_data + winner
	print game_data.strip()
