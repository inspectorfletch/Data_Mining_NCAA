from NCAA.models import *

with open("tournament_results.csv") as f:
	for line in f:
		line = line.split(',')
		#print line[0] + ': ' + line[1].strip('" ') + ' ' + line[11] + ' , ' + line[15].strip('" ') + ' ' + line[12]
		add_game = True
		try:
			teamA = Season.objects.get(teamname=line[1].strip('" ').upper(), year=int(line[0]))
		except:
			#print line[1].strip('" '), int(line[0])
			add_game = False
			
		try:
			teamB = Season.objects.get(teamname=line[15].strip('" ').upper(), year=int(line[0]))
		except:
			#print line[15].strip('" '), int(line[0])
			add_game = False
		
		if add_game:
			game = Game(teamA=teamA, teamB=teamB, winner='A')
			print game
			game.save()