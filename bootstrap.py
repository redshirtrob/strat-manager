from GameReport import GameReportParser
from strat.parse import GameReportSemanticActions
from bs4 import BeautifulSoup

CITIES = [
    'Atlanta',
    'Boston',
    'Charlotte',
    'Chicago',
    'Cincinnati',
    'Cleveland',
    'Columbus',
    'Detroit',
    'Miami',
    'Montreal',
    'Nashville',
    'New Orleans',
    'New York',
    'Philadelphia',
    'St. Louis',
    'Saint Louis',
    'Steel City'
]

NICKNAMES = [
    'Crackers',
    'Blues',
    'Monarchs',
    'Northsiders',
    'Steamers',
    'Spiders',
    'Explorers',
    'Clutch',
    'Toros',
    'Souterrains',
    'Cats',
    'Mudbugs',
    'Knights',
    'Admirals',
    'Clydesdales',
    'Stogies',
]

HOF_CITIES = [
    'Mt. Washington',
    'Mudville',
    'Sirk City',
    'Hackensack',
    'Motor City',
    'Cook County',
    'Vegas',
    'New Milan'
]

HOF_NICKNAMES = [
    'Wonders',
    'Grey Eagles',
    'Spikes',
    'Monuments',
    'Bulls',
    'Robber Barons',
    'Sultans',
    'Rajahs'
]

semantics = GameReportSemanticActions(cities=CITIES, nicknames=NICKNAMES)
parser = GameReportParser(parseinfo=False, semantics=semantics)

hof_semantics = GameReportSemanticActions(cities=HOF_CITIES, nicknames=HOF_NICKNAMES)
hof_parser = GameReportParser(parseinfo=False, semantics=hof_semantics)

with open('sample/test.txt', 'r') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
