from NCAA.models import *
import random

trainingFile = open('cluster_data.csv', 'w')
#testFile = open('testData.csv', 'w')
skip_fields = ['teamA', 'teamB', 'id', 'teamname', 'year']

games = Game.objects.all()
print_string = ''
for field in games[0].teamA._meta.get_all_field_names():
	if field not in skip_fields:
		print_string = print_string + field.strip('\n ') + ','
print_string = print_string.strip(',')
trainingFile.write(print_string+'\n')
#testFile.write(print_string+'\n')

for game in games:
	game_data = ''
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
	
	for i in range(0, len(teamA_data)):
		game_data = game_data + str(teamA_data[i] - teamB_data[i]) + ','
	game_data = game_data.strip(',')
	
	#if game.teamA.year < 2009:
	trainingFile.write(game_data.strip()+'\n')
	#else:
	#	testFile.write(game_data.strip()+'\n')
	#print game_data.strip()

trainingFile.close()
#testFile.close()