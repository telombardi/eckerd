from collections import defaultdict

class BibtexEntryHandler:
	def __init__(self, entry: str):
		self.entry = entry
		self.fields_of_interest = ('Unique-ID','Article-Number',
			'DOI','ISSN','EISSN','Type','Title','Year','Journal',
			'Journal-ISO','Volume','Number','Month','Pages',
			'Publisher', 'Abstract','Cited-References')
		self.field_list = list(self.entry.fields.keys())
		self.fields = defaultdict(self.dkey)
		for f in self.field_list:
			if f in self.fields_of_interest:
				self.fields[f]=self.entry.fields[f]

	def dkey(self):
		return 'missing_key'

	def __str__(self) -> str:
		return str(self.fields)

	def getBibtexObj(self) -> object:
		pass