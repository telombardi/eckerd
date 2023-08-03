from singleton_decorator import singleton
import crossref_commons.retrieval			#https://pypi.org/project/crossref-commons/

@singleton
class CrossrefCtrl:

	@staticmethod
	def lookup_doi(doi: str) -> str:
		json = crossref_commons.retrieval.get_publication_as_json(doi)
		return(json)

if __name__ == "__main__":
	cr = CrossrefCtrl()
	mydict = cr.lookup_doi('10.1073/pnas.1819449116')
	#print(mydict)  
	print(mydict.keys())
	print(mydict['type'])
	references = list(mydict['reference'])
	for r in references:
		print(r)
		print()
