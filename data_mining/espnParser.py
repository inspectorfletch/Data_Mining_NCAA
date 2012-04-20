from HTMLParser import HTMLParser, HTMLParseError
import urllib

from NCAA.models import *

class ESPNParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.PARSE_MODE = ''
		self.year = 0
		
		self.inTable = False
		self.inRow = False
		self.isName = False
		
		self.name = ''
		self.row = []

	def handle_starttag(self, tag, attrs):
		if tag == 'table': 
			#print attrs
			for name, value in attrs:
				if name == 'class' and value == 'datatable':
					#print 'dude'
					self.inTable = True
					break
					
		elif tag == 'tr':
			for name, value in attrs:
				if self.inTable and name == 'class' and (value == 'cell1' or value == 'cell2'):
					#print 'josh is awesome'
					self.inRow = True
					break
		
		elif tag == 'a':
			for name, value in attrs:
				if self.inRow: #and name == 'class' and value == 'cell5':
					self.isName = True
	
	def handle_endtag(self, tag):
		#print tag
		if tag == 'table':
			self.inTable = False
			if self.row:
				if self.PARSE_MODE == 'def':
					season = Season(teamname=self.row[0],
									year=self.year,
									ppg_allowed=(self.row[1]),
									field_goal_percentage_allowed=(self.row[3].strip('%')),
									three_point_percentage_allowed=(self.row[5].strip('%')),
									free_throw_percentage_allowed=(self.row[7].strip('%')),
									rebounds_per_game_allowed=(self.row[8]),
									offensive_rebounds_per_game_allowed=(self.row[9]),
									assists_per_game_allowed=(self.row[10]),
									pf_per_game_allowed=(self.row[11]),
									steals_per_game_allowed=(self.row[12]),
									turnovers_per_game_against=(self.row[13]),
									blocks_per_game_against=(self.row[14]))
					#season.save()
					
					print season
				elif self.PARSE_MODE == 'off':
					try:
						season = Season.objects.get(teamname=self.row[0], year=self.year)
						
						season.ppg = (self.row[1])
						season.field_goal_percentage=(self.row[3].strip('%'))
						season.three_point_percentage=(self.row[5].strip('%'))
						season.free_throw_percentage=(self.row[7].strip('%'))
						season.rebounds_per_game=(self.row[8])
						season.offensive_rebounds_per_game=(self.row[9])
						season.assists_per_game=(self.row[10])
						season.pf_per_game=(self.row[11])
						season.steals_per_game=(self.row[12])
						season.turnovers_per_game=(self.row[13])
						season.blocks_per_game=(self.row[14])
						#print self.row
						
						#season.save()						
						print season
					except Exception as inst:
						print "Error occured in parsing team : " + str(self.row[0])
						print inst
				
				self.row = []
				self.inRow = False
			
		#elif tag == 'tr' and self.inTable:
		#	print 'furk'
		#	self.row = []
		#	self.inRow = False
			
		elif tag == 'a' and self.isName:
			#print self.name
			self.row.append(self.name)
			self.name = ''
			self.isName = False
	
	def handle_data(self, data):
		if self.isName and data.strip():
			if not self.name and self.row:
				if self.PARSE_MODE == 'def':
					season = Season(teamname=self.row[0],
									year=self.year,
									ppg_allowed=(self.row[1]),
									field_goal_percentage_allowed=(self.row[3].strip('%')),
									three_point_percentage_allowed=(self.row[5].strip('%')),
									free_throw_percentage_allowed=(self.row[7].strip('%')),
									rebounds_per_game_allowed=(self.row[8]),
									offensive_rebounds_per_game_allowed=(self.row[9]),
									assists_per_game_allowed=(self.row[10]),
									pf_per_game_allowed=(self.row[11]),
									steals_per_game_allowed=(self.row[12]),
									turnovers_per_game_against=(self.row[13]),
									blocks_per_game_against=(self.row[14]))
					#season.save()
					print season
				elif self.PARSE_MODE == 'off':
					try:
						season = Season.objects.get(teamname=self.row[0], year=self.year)
						
						season.ppg = (self.row[1])
						season.field_goal_percentage=(self.row[3].strip('%'))
						season.three_point_percentage=(self.row[5].strip('%'))
						season.free_throw_percentage=(self.row[7].strip('%'))
						season.rebounds_per_game=(self.row[8])
						season.offensive_rebounds_per_game=(self.row[9])
						season.assists_per_game=(self.row[10])
						season.pf_per_game=(self.row[11])
						season.steals_per_game=(self.row[12])
						season.turnovers_per_game=(self.row[13])
						season.blocks_per_game=(self.row[14])
						
						#season.save()						
						print season
					except Exception as inst:
						print "Error occured in parsing team : " + str(self.row[0])
						print inst
				
				self.row = []
				
			self.name += (data.strip(' \n'))
		elif self.inTable and self.inRow and data.strip():
			#print data.strip()
			self.row.append(data.strip())

#if __name__ == '__main__':
def parse_pages():
	#for year in range(1998, 2012):
	year = 2012
	for mode in ['def']:#, 'off']:
		print "Reading "+mode+"ensive statistics from "+str(year)
		parser = ESPNParser()
		parser.PARSE_MODE = mode
		parser.year = year
		page = urllib.urlopen('http://www.statfox.com/cbb/'+mode+'stats~sortby~team~div~~season~'+str(year)+'~teamid~~sit~all.htm')

		for line in page.readlines():
			try:
				parser.feed(line)
				#print line
			except HTMLParseError as errorSucks:
				print errorSucks
		
		page = ''
