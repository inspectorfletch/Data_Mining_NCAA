from HTMLParser import HTMLParser, HTMLParseError
import urllib

class ESPNParser(HTMLParser):
	def __init__(self):
		#super(HTMLParser, self).__init__()
		HTMLParser.__init__(self)
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
				print self.row
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
				print self.row
				self.row = []
			#print
			self.name += (data.strip(' \n'))
			#print len(data.strip())
		elif self.inTable and self.inRow and data.strip():
			#print data.strip()
			self.row.append(data.strip())

if __name__ == '__main__':
	parser = ESPNParser()
	page = urllib.urlopen('http://www.statfox.com/cbb/defstats~sortby~team~conf~~season~1999~teamid~~sit~all.htm')
	
	for line in page.readlines():
		try:
			parser.feed(line)
			#print line
		except HTMLParseError: pass
		#	print 'site sucks'