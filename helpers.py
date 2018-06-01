from suspect_scrape_app.settings import get_con_string
from sqlalchemy import create_engine, Column, Integer, String, DateTime, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.automap import automap_base

# class Suspect(object):
#     pass
# class Leaver(object):
#     pass

# def load_leavers():
#     """"""
#     cs = get_con_string()
#     engine = create_engine(cs, client_encoding='utf8')
#
#     metadata = MetaData(engine)
#     leavers_tbl = Table('leaver', metadata, autoload=True)
#     mapper(Leaver, leavers_tbl)
#     # suspects_tbl = Table('suspect', metadata, autoload=True)
#     # mapper(Suspect, suspects_tbl)
#
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     return session

def load_tables():
    """"""
    cs = get_con_string()
    # automap base
    Base = automap_base()

    # pre-declare User for the 'user' table
    class Leaver(Base):
        __tablename__ = 'leaver'


    # reflect
    engine = create_engine(cs)
    Base.prepare(engine, reflect=True)

    # we still have Address generated from the tablename "address",
    # but User is the same as Base.classes.User now

    Suspect = Base.classes.suspect
    Session = sessionmaker(bind=engine)
    session = Session()
    return session, Suspect, Leaver

# def load_suspects():
#     """"""
#     cs = get_con_string()
#     engine = create_engine(cs, client_encoding='utf8')
#
#     metadata = MetaData(engine)
#     suspects_tbl = Table('suspect', metadata, autoload=True)
#     mapper(Suspect, suspects_tbl)
#
#     Session = sessionmaker(bind=engine)
#     session = Session()
#     return session


def remove_html_markup(s):
    tag = False
    quote = False
    out = ""

    for c in s:
            if c == '<' and not quote:
                tag = True
            elif c == '>' and not quote:
                tag = False
            elif (c == '"' or c == "'") and tag:
                quote = not quote
            elif not tag:
                out = out + c

    return out


# def connect(string):
#     '''Returns a connection and a metadata object'''
#     # We connect with the help of the PostgreSQL URL
#     # postgresql://federer:grandestslam@localhost:5432/tennis
#     #url = 'postgresql://{}:{}@{}:{}/{}'
#     #url = url.format(user, password, host, port, db)
#
#     # The return value of create_engine() is our connection object
#     con = sqlalchemy.create_engine(string, client_encoding='utf8')
#
#     # We then bind the connection to MetaData()
#     meta = sqlalchemy.MetaData(bind=con, reflect=True)
#
#     return con, meta

# def getlvr(con):
#     metadata = MetaData()
#     leavers = Table('leaver', metadata, autoload=True, autoload_with=con)
#     stmt = select([leavers])
#     stmt = stmt.where(leavers.columns.llink == None)
#     stmt = stmt.order_by(leavers.columns.track_lst_update)
#     stmt = stmt.limit(1)
#     results = con.execute(stmt).fetchall()
#     return results
