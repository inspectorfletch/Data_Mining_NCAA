#from NCAA.models import *

lines = []
with open('2012winners.csv') as f:
	for line in f:
		line = line.split(',')
		#print line[0], line[1].strip()
		try:
			#teamA = Season.objects.get(year=2012, teamname=line[0])
			#teamB = Season.objects.get(year=2012, teamname=line[1].strip())
			#game = Game(teamA=teamA, teamB=teamB, winner='A')
			#game.save()
			lines.append(line[0] + ' ' + line[1].strip())
		except:
			print line[0], line[1].strip()

lines.sort()
for line in lines:
	print line