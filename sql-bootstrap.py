from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_

from blb.models.core import Base
from blb.models.blb import (
    BLBLeague,
    BLBSeason,
    BLBDivision,
    BLBTeam,
    BLBPlayer,
    BLBRosterEntry,
    BLBGame,
    BLBGameBatting,
    BLBGamePitching)
from blb.models.fangraphs import (
    FGSeason,
    FGPlayer, 
    FGPlayerSeason,
    FGBatting,
    FGPitching,
    FGTeam)

from blb.models.util import (FG_BATTING_TO_DB,
    FG_PITCHING_TO_DB, clean_value, clean_key)

ENGINE = create_engine('sqlite:///blb.db')
Session = sessionmaker(bind=ENGINE)
session = Session()

Base.metadata.create_all(ENGINE)
