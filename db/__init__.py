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
    Column("freq", Integer),
)

SOUNDS_TABLE = Table("sounds", metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("char", String),
    Column("sound_part_1", String),
    Column("sound_part_2", String),
    Column("tone", Integer),
)

conn = engine.connect()

conn.execute('CREATE SCHEMA IF NOT EXISTS naming')
metadata.create_all(engine)


def insert_char_sound_parts_and_tone(values):
    stmt = insert(SOUNDS_TABLE).values(values)
    return conn.execute(stmt)

def drop_all_sounds():
    return conn.execute(f'''TRUNCATE {metadata.schema}.{SOUNDS_TABLE.name}''')