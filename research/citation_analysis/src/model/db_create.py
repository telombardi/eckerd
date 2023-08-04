from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select

class Base(DeclarativeBase):
	pass

class SystemParm(Base):
	__tablename__ = 'SYSTEM_PARM'

	key: Mapped[str] = mapped_column(String(50), primary_key=True)
	value: Mapped[str] = mapped_column(String(50))

if __name__ == '__main__':
	engine = create_engine("mysql+pymysql://root:$tup1dity@localhost/cite?charset=utf8mb4", echo=True)
	Base.metadata.create_all(engine)
	with Session(engine) as session:
		version = SystemParm(key='version',value='0.1')
		dbuser = SystemParm(key='dbuser', value='cite')
		dbpass = SystemParm(key='dbpass', value='elegant_baker')
		#session.add_all([version,dbuser,dbpass])
		#session.commit()
		stmt = select(SystemParm).where(SystemParm.key=='version')
		print(type(stmt))
		print(stmt)

		row = session.execute(select(SystemParm).where(SystemParm.key=='version')).first()
		print(row)
		print(f'{row.SystemParm.key} : {row.SystemParm.value}')




