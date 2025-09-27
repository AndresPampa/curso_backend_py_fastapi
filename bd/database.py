import os
from sqlalchemy import create_engine #se utiliza para crear conexiones a la base de datos
from sqlalchemy.orm import sessionmaker #se utiliza para crear sesiones de trabajo con la base de datos y utilizar clases declarativas.
from sqlalchemy.ext.declarative import declarative_base


sqlite_name: str = 'movies.sqlite'
base_dir: str = os.path.dirname(os.path.realpath(__file__))
database_url: str = f"sqlite:///{os.path.join(base_dir, sqlite_name)}"

Engine = create_engine(database_url, echo=True)

Session = sessionmaker(bind=Engine)
Base = declarative_base()