from django.db import models

class Season(models.Model):
	# Primary keys
	teamname = models.CharField(max_length=25)
	year = models.IntegerField()
	
	# Team's record that year
	wins = models.IntegerField(blank=True, null=True, default=None)
	losses = models.IntegerField(blank=True, null=True, default=None)
	
	# Offensive statistics
	ppg = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, default=None)
	field_goal_percentage = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, default=None)
	three_point_percentage = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, default=None)
	free_throw_percentage = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, default=None)
	rebounds_per_game = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, default=None)
	offensive_rebounds_per_game = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, default=None)
	assists_per_game = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, default=None)
	pf_per_game = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, default=None)
	steals_per_game = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, default=None)
	turnovers_per_game = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, default=None)
	blocks_per_game = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, default=None)
	
	# Defensive statistics
	ppg_allowed = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, default=None)
	field_goal_percentage_allowed = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, default=None)
	three_point_percentage_allowed = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, default=None)
	free_throw_percentage_allowed = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, default=None)
	rebounds_per_game_allowed = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, default=None)
	offensive_rebounds_per_game_allowed = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, default=None)
	assists_per_game_allowed = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, default=None)
	pf_per_game_allowed = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, default=None)
	steals_per_game_allowed = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, default=None)
	turnovers_per_game_against = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, default=None)
	blocks_per_game_against = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, default=None)
	
	def __unicode__(self):
		return self.teamname + ', ' +  str(self.year) + '(' + str(self.wins) + '-' + str(self.losses) + '):\n' + \
			  '[' + str(self.ppg) + ', ' + str(self.field_goal_percentage) + ', ' + str(self.three_point_percentage)  + ', ' + \
			  str(self.free_throw_percentage) + ', ' + str(self.rebounds_per_game) + ', ' + \
			  str(self.offensive_rebounds_per_game) + ', ' + \
			  str(self.assists_per_game) + ', ' + str(self.pf_per_game) + ', ' + str(self.steals_per_game) + ', ' + \
			  str(self.turnovers_per_game) + ', ' + str(self.blocks_per_game) + ', ' + \
			  str(self.ppg_allowed) + ', ' + str(self.field_goal_percentage_allowed) + ', ' + \
			  str(self.three_point_percentage_allowed) + ', ' + str(self.free_throw_percentage_allowed) + ', ' + \
			  str(self.rebounds_per_game_allowed) + ', ' + str(self.offensive_rebounds_per_game_allowed) + ', ' + \
			  str(self.assists_per_game_allowed) + ', ' + str(self.pf_per_game_allowed) + ', ' + \
			  str(self.steals_per_game_allowed) + ', ' + str(self.turnovers_per_game_against) + ', ' + \
			  str(self.blocks_per_game_against) + ']'

class Game(models.Model):
	teamA = models.ForeignKey(Season, related_name="teamA")
	teamB = models.ForeignKey(Season, related_name="teamB")
	winner = models.CharField(max_length=1)
	
	def __unicode__(self):
		return str(self.teamA.year) + ': ' + self.teamA.teamname + ' vs. ' + self.teamB.teamname
	