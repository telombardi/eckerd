from collections import defaultdict

class BibtexEntryHandler:
	def __init__(self, entry: str):
		self.entry = entry
		self.fields_of_interest = ('Unique-ID','Article-Number',
			'DOI','ISSN','EISSN','Type','Title','Year','Journal',
			'Journal-ISO','Volume','Number','Month','Pages',
			'Publisher', 'Abstract', 'Language',
			'Cited-References','Author-Email','Affiliation',
			'Affiliations','ORCID-Numbers','Keywords','Keywords-Plus','Research-Areas',
			'Web-of-Science-Categories','Research-Areas',
			'Funding-Acknowledgement','Funding-Text')
		self.person_list = list(self.entry.persons.keys())
		self.field_list = list(self.entry.fields.keys())
		self.persons = defaultdict(self.dkey)
		for p in self.person_list:
			if p in self.person_list:
				self.persons[p]=self.entry.persons[p]
		self.fields = defaultdict(self.dkey)
		for f in self.field_list:
			if f in self.fields_of_interest:
				self.fields[f]=self.entry.fields[f]

	def dkey(self):
		return 'missing_key'

	def __str__(self) -> str:
		return str(self.fields)

	def getFieldDict(self) -> defaultdict:
		return self.fields

	def getFieldValue(self, key: str) -> str:
		return self.fields[key]

	def getPersonValue(self, key: str) -> str:
		return self.persons[key]

	def getBibtexObj(self) -> object:
		pass