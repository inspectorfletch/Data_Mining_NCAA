from NCAA.models import *
import random
from decimal import *

#trainingFile = open('bayes_dataB.csv', 'w')
#testFile = open('testData.csv', 'w')
skip_fields = ['teamA', 'teamB', 'id', 'teamname', 'year']

games = Game.objects.all()
print_string = ''
for field in games[0].teamA._meta.get_all_field_names():
	if field not in skip_fields:
		print_string = print_string + field.strip('\n ') + ','
print_string = print_string.strip(',')
print print_string
#trainingFile.write(print_string+'\n')
#testFile.write(print_string+'\n')

games_data = []
for game in games:
	#game_data = ''
	game_data = []
	teamA_data = []
	teamB_data = []
	for field in game.teamA._meta.get_all_field_names():
		if field not in skip_fields:
			teamA_data.append(getattr(game.teamA, field))
	for field in game.teamB._meta.get_all_field_names():
		if field not in skip_fields:
			teamB_data.append(getattr(game.teamB, field))
	
	#winner = 'A'
	#if random.choice([True, False]):
	#	winner = 'B'
	#	temp = teamA_data
	#	teamA_data = teamB_data
	#	teamB_data = temp
	
	#for i in range(0, len(teamA_data)):
	#	game_data = game_data + str(teamB_data[i] - teamA_data[i]) + ','
	#game_data = game_data.strip(',')
	#game_data += 'B'
	
	for i in range(0, len(teamA_data)):
		game_data.append(float(str(teamA_data[i])) - float(str(teamB_data[i])))
	games_data.append(game_data)
	
	#if game.teamA.year < 2009:
	#trainingFile.write(game_data.strip()+'\n')
	#else:
	#	testFile.write(game_data.strip()+'\n')
	#print game_data.strip()

field_maxes = []
for i in range(0, len(games_data[0])):
	field_maxes.append(games_data[0][i])

for game in games_data:
	for i in range(0, len(game)):
		if game[i] > field_maxes[i]: field_maxes[i] = game[i]

#print field_maxes
#print games_data[0]

#getcontext().prec = 3
for game in games_data:
	for i in range(0, len(game)):
		game[i] /= field_maxes[i]
		
for game in games_data:
	game_string = ''
	for data in game:
		game_string += "%.2f," % data
	print game_string.strip(',')
#trainingFile.close()
#testFile.close()