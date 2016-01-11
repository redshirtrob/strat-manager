from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_

from blb.models.core import Base
from blb.models.fangraphs import (Season, Player, 
    PlayerSeason, Batting, Pitching, Team)

from blb.models.util import (FG_BATTING_TO_DB,
    FG_PITCHING_TO_DB, clean_value, clean_key)

ENGINE = create_engine('sqlite:///blb.db')
Session = sessionmaker(bind=ENGINE)
session = Session()
