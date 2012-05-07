from NCAA.models import *


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
WINNERS = {2012: 'KENTUCKY',
		   2011: 'CONNECTICUT',
		   2010: 'DUKE',
		   2009: 'N CAROLINA',
		   2008: 'KANSAS',
		   2007: 'FLORIDA',
		   2006: 'FLORIDA',
		   2005: 'N CAROLINA',
		   2004: 'CONNECTICUT',
		   2003: 'SYRACUSE',
		   2002: 'MARYLAND',
		   2001: 'DUKE',
		   2000: 'MICHIGAN ST',
		   1999: 'CONNECTICUT',
		   1998: 'KENTUCKY'}
		   
print_string = ''
for field in Season.objects.all()[0]._meta.get_all_field_names():
	if field not in skip_fields and field not in strip_fields: print_string += field + ','

print_string += 'won_tournament'
print print_string
print_string = ''

for team in [team for team in Season.objects.all() if team.wins]:
	for field in team._meta.get_all_field_names():
		if field not in skip_fields and field not in strip_fields: print_string += str(getattr(team, field)) + ','
	if team.teamname == WINNERS[team.year]:
		print_string += '1'
	else: print_string += '0'
	print print_string
	print_string = ''