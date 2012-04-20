from HTMLParser import HTMLParser, HTMLParseError
import urllib

#from NCAA.models import *

class ESPNParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
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
				if name == 'class' and value == 'table_body':
					print 'dude'
					self.inTable = True
					break
					
		elif tag == 'tr':
			for name, value in attrs:
				if self.inTable and name == 'class' and (value == 'table_data' or value == 'table_data_odd'):
					#print 'josh is awesome'
					if self.row:
						print self.row
						self.row = []
					self.inRow = True
					break
		
		elif tag == 'td':
			for name, value in attrs:
				if name == 'class' and value == 'table_sort':
					self.inRow = False
					if self.row:
						print self.row
						self.row = []
		
		elif tag == 'a':
			for name, value in attrs:
				if self.inRow: #and name == 'class' and value == 'cell5':
					self.isName = True
	
	def handle_endtag(self, tag):
		#print tag
		if tag == 'table':
			self.inTable = False
			if self.row:
				"""try:
					
				except Exception as inst:
					print "Error occured in parsing team : " + str(self.row[0])
					print inst
				"""
				print self.row
				self.row = []
				self.inRow = False
			
			
		#elif tag == 'tr' and self.inTable:
		#	print 'furk'
		#	self.row = []
		#	self.inRow = False
			
		#elif tag == 'a' and self.isName:
			#print self.name
		#	self.row.append(self.name)
		#	self.name = ''
		#	self.isName = False
	
	def handle_data(self, data):
		#if self.isName and data.strip():
		#	if not self.name and self.row:
		#		self.row = []
				
		#	self.name += (data.strip(' \n'))
		#el
		if self.inTable and self.inRow and data.strip():
			#print data.strip()
			self.row.append(data.strip())

if __name__ == '__main__':
	#def parse_pages():
	#for year in range(1998, 2012):
	year = 2012
	print "Reading standings from "+str(year)
	parser = ESPNParser()
	parser.year = year
	#http://www.statfox.com/cbb/standings~sortby~team~div~~season~2012~teamid~~sit~all.htm
	page = urllib.urlopen('http://www.statfox.com/cbb/standings~sortby~team~div~~season~'+str(year)+'~teamid~~sit~all.htm')

	for line in page.readlines():
		try:
			parser.feed(line)
			#print line
		except HTMLParseError as errorSucks:
			print errorSucks
	
	page = ''
