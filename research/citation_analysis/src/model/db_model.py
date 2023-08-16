from typing import List, Optional
from sqlalchemy import ForeignKey, String, Text, Integer, create_engine, select, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session
from sqlalchemy_utils import database_exists, create_database

class Base(DeclarativeBase):
	pass

class SystemParm(Base):
	__tablename__ = 'SYSTEM_PARM'

	key: Mapped[str] = mapped_column(String(50), primary_key=True)
	value: Mapped[str] = mapped_column(String(50))
	
	def __repr__(self) -> str:
		return f'key={self.key} : value={self.value}'
	
	def __str__(self) -> str:
		return f'key={self.key} : value={self.value}'

class PublicationType(Base):
	__tablename__ = 'PUBLICATION_TYPE'

	PUBTYPEID: Mapped[int] = mapped_column(Integer, primary_key=True)
	publication_type: Mapped[str] = mapped_column(String(45))

	publications: Mapped[List['Publication']] = relationship(back_populates='publication_type')


class Publication(Base):
	__tablename__ = 'PUBLICATION'

	PUBID: Mapped[int] = mapped_column(Integer, primary_key=True)
	title: Mapped[str] = mapped_column(String(255))
	publisher: Mapped[str] = mapped_column(String(255), nullable=True)
	year: Mapped[int] = mapped_column(Integer)

	PUBTYPEID: Mapped[int] = mapped_column(ForeignKey(PublicationType.PUBTYPEID))
	publication_type: Mapped['PublicationType'] = relationship(back_populates='publications')

	citation_number: Mapped[int] = mapped_column(Integer, nullable=True)


class Citation(Base):
	__tablename__ = 'CITATION'

	CITEID: Mapped[int] = mapped_column(Integer, primary_key=True)
	citing_pubid = mapped_column(Integer, ForeignKey('PUBLICATION.PUBID'))
	cited_pubid = mapped_column(Integer, ForeignKey('PUBLICATION.PUBID'))

	citing_publication = relationship('Publication', foreign_keys=[citing_pubid])
	cited_publication = relationship('Publication', foreign_keys=[cited_pubid])
	
class PublicationAbstract(Base):
	__tablename__ = 'PUBLICATION_ABSTRACT'

	PUBID: Mapped[int] = mapped_column(Integer, ForeignKey('PUBLICATION.PUBID'), primary_key=True)
	abstract: Mapped[str] = mapped_column(Text(20000))	

class Funding(Base):
	__tablename__ = 'FUNDING'

	PUBID: Mapped[int] = mapped_column(Integer, ForeignKey('PUBLICATION.PUBID'), primary_key=True)
	funding_text: Mapped[str] = mapped_column(String(2000), nullable=True)
	funding_achknowledgment: Mapped[str] = mapped_column(String(2000), nullable=True)

class Author(Base):
	__tablename__ = 'AUTHOR'

	AID: Mapped[int] = mapped_column(Integer, primary_key=True)
	ORCID: Mapped[str] = mapped_column(String(19), nullable=True)
	last_name: Mapped[str] = mapped_column(String(100), nullable=True)
	first_name: Mapped[str] = mapped_column(String(50), nullable=True)
	middle_name: Mapped[str] = mapped_column(String(50), nullable=True)
	initials: Mapped[str] = mapped_column(String(5), nullable=True)
	Scopus_ID: Mapped[str] = mapped_column(String(10), nullable=True)

class PublicationAuthor(Base):
	__tablename__ = 'PUBLICATION_AUTHOR'

	PUBID: Mapped[int] = mapped_column(Integer, ForeignKey('PUBLICATION.PUBID'), primary_key=True)
	AID: Mapped[int] = mapped_column(Integer, ForeignKey('AUTHOR.AID'), primary_key=True)
	author_order: Mapped[int] = mapped_column(Integer)
	corresponding_author: Mapped[int] = mapped_column(Integer, nullable=True)
	affiliation: Mapped[str] = mapped_column(String(255), nullable=True)
	email: Mapped[str] = mapped_column(String(255), nullable=True)

class KeywordType(Base):
	__tablename__ = 'KEYWORD_TYPE'

	KWTYPEID: Mapped[int] = mapped_column(Integer, primary_key=True)
	keyword_type: Mapped[int] = mapped_column(String(50))

class PublicationKeyword(Base):
	__tablename__ = 'PUBLICATION_KEYWORD'

	PUBID: Mapped[int] = mapped_column(Integer, ForeignKey('PUBLICATION.PUBID'), primary_key=True)
	KWTYPEID: Mapped[int] = mapped_column(Integer, ForeignKey('KEYWORD_TYPE.KWTYPEID'), primary_key=True)
	keyword: Mapped[int] = mapped_column(String(50))

class PublicationPeriodical(Base):
	__tablename__ = 'PUBLICATION_PERIODICAL'

	PUBID: Mapped[int] = mapped_column(Integer, ForeignKey('PUBLICATION.PUBID'), primary_key=True)
	periodical_title: Mapped[str] = mapped_column(String(255))
	journal_iso: Mapped[str] = mapped_column(String(50), nullable=True)
	month: Mapped[int] = mapped_column(Integer, nullable=True)
	day: Mapped[int] = mapped_column(Integer, nullable=True)
	volumne: Mapped[int] = mapped_column(Integer, nullable=True)
	issue: Mapped[int] = mapped_column(Integer, nullable=True)
	number: Mapped[int] = mapped_column(Integer, nullable=True)
	pages: Mapped[str] = mapped_column(String(20), nullable=True)
	publication_data: Mapped[str] = mapped_column(Date, nullable=True)

class PublicationMonograph(Base):
	__tablename__ = 'PUBLICATION_MONOGRAPH'
	PUBID: Mapped[int] = mapped_column(Integer, ForeignKey('PUBLICATION.PUBID'), primary_key=True)
	edition: Mapped[str] = mapped_column(String(50))

class PubIdentifierType(Base):
	__tablename__ = 'PUB_IDENTIFIER_TYPE'

	PITYPEID: Mapped[int] = mapped_column(Integer, primary_key=True)
	identifier_type: Mapped[str] = mapped_column(String(45))
	identifier_desc: Mapped[str] = mapped_column(String(255))
	identifier_src: Mapped[str] = mapped_column(String(255))

class PublicationIdentifier(Base):
	__tablename__ = 'PUBLICATION_IDENTIFIER'

	PUBID: Mapped[int] = mapped_column(Integer, ForeignKey('PUBLICATION.PUBID'), primary_key=True)
	PITYPEID: Mapped[int] = mapped_column(Integer, ForeignKey('PUB_IDENTIFIER_TYPE.PITYPEID'), primary_key=True)
	publication_identifier: Mapped[int] = mapped_column(String(255))

if __name__ == '__main__':
	engine = create_engine("mysql+pymysql://root:$tup1dity@localhost/citation?charset=utf8mb4", echo=True)
	if not database_exists(engine.url):
		create_database(engine.url)

	Base.metadata.create_all(engine)
	with Session(engine) as session:
		version = SystemParm(key='version',value='0.1')
		dbuser = SystemParm(key='dbuser', value='cite')
		dbpass = SystemParm(key='dbpass', value='elegant_baker')
		#session.add_all([version,dbuser,dbpass])
		#session.commit()

		article = PublicationType(publication_type='Article')
		book = PublicationType(publication_type='Book')
		#session.add_all([article,book])
		#session.commit()



		stmt = select(SystemParm).where(SystemParm.key=='version')
		#print(type(stmt))
		#print(stmt)

		row = session.execute(select(SystemParm).where(SystemParm.key=='version')).first()
		#print(row)
		print(f'{row.SystemParm.key} : {row.SystemParm.value}')
		
		sp = SystemParm(key=row.SystemParm.key,value=row.SystemParm.value)
		print(sp)




