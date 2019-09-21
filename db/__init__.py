from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.sql import select
from sqlalchemy.dialects.postgresql import insert


engine = create_engine('postgres+psycopg2://postgres:mysecret@playground-postgres:5432/db', echo=True)
metadata = MetaData(schema="naming")
names_table = Table('names', metadata,
    Column('name', String, primary_key=True),
    Column('score', Integer),
    Column('luck', String),
)

CHARACTERS_TABLE = Table("characters", metadata,
    Column("char", String, primary_key=True),
    Column("sound_part_1", String),
    Column("sound_part_2", String),
    Column("tone", Integer),
    Column("freq", Integer),
)

conn = engine.connect()

conn.execute('CREATE SCHEMA IF NOT EXISTS naming')
metadata.create_all(engine)