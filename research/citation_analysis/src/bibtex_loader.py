from pybtex.database import parse_file
from bibtex_entry_handler import BibtexEntryHandler as BEH

class BibtexLoader:
	def __init__(self, bib_file_str: str):
		self.bib_data = parse_file(bib_file_str)

	def iterate(self):
		for entry in self.bib_data.entries.values():
			beh = BEH(entry)
			print(beh)
			exit()

if __name__ == "__main__":
	bl = BibtexLoader('C:/Users/lombardite/Documents/research/repo/savedrecs.bib')
	bl.iterate()
	
	#bib_data = parse_file('C:/Users/lombardite/Documents/research/repo/savedrecs.bib')
	#print(bib_data)
	#for entry in bib_data.entries.values():
	#	print(entry.key)
	#	print(entry.persons.keys())
	#	fields = list(entry.fields.keys())
	#	for f in fields:
	#		if f in ('DOI','Title','Year'):
	#			print(f , " : ", entry.fields[f]) 