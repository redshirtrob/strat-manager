from sqlalchemy import create_engine
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker

from blb.models.fangraphs import FGSeason, FGPlayer, \
    FGPlayerSeason, FGBatting, FGTeam

Session = sessionmaker()
engine = create_engine('sqlite:///blb.db')
Session.configure(bind=engine)
session = Session()
