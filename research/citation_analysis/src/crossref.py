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
	print(cr.lookup_doi('10.1080/02626667.2018.1560449'))   

