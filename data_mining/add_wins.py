from NCAA.models import *

faults = 0
with open('team_wins.csv') as f:
	for line in f:
		line = line.split(',')
		try:
			season = Season.objects.get(teamname=line[1].upper(), year=int(line[0]))
			if not season.wins:
				season.wins = int(line[2])
				season.losses = int(line[3])
				#print season
				season.save()
		except:
			print line[0], line[1]
			faults += 1
print faults