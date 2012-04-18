from NCAA.models import *

wrong_names = []
right_names = []
lineNum = 1
"""with open("tournament_results.csv") as f:
	for line in f:
		if (len(line.split(',')) != 37): print str(lineNum) + ': ' + str(len(line.split(',')))
		lineNum = lineNum + 1
		
		teamname = line.split(',')[1].strip('" ')
		season = Season.objects.filter(teamname=teamname.upper())
		if len(season) == 0:
			if teamname not in wrong_names:
				wrong_names.append(teamname)
		else:
			if teamname not in right_names:
				right_names.append(teamname)
"""
with open("team_wins.csv") as f:
	for line in f:
		teamname = line.split(',')[1]
		season = Season.objects.filter(teamname=teamname.upper())
		if len(season) == 0:
			if teamname not in wrong_names:
				wrong_names.append(teamname)
		else:
			if teamname not in right_names:
				right_names.append(teamname)		

print "Teams with wrong names:"
for name in wrong_names:
	print name
print len(wrong_names)