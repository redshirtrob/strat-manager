from bs4 import BeautifulSoup
from GameReport import GameReportParser
from grako.exceptions import FailedToken
from grako.ast import AST

class GameReportSemanticActions(object):
    def __init__(self, cities, nicknames):
        self.cities = [city.lower() for city in cities]
        self.nicknames = [nickname.lower() for nickname in nicknames]

    def find_city(self, fragment):
        for city in self.cities:
            if city in fragment:
                return city
        return None

    def find_nickname(self, fragment):
        for nickname in self.nicknames:
            if nickname in fragment:
                return nickname
        return None

    def annual_team(self, phrase, year):
        city = self.find_city(phrase)
        nickname = self.find_nickname(phrase)
        if city is None or nickname is None:
            return None
        return AST(city=unicode(city), nickname=unicode(nickname), year=year)

    def validate_nickname(self, nickname):
        if nickname is None:
            raise Exception

        nickname = self.find_nickname(nickname.lower())
        if nickname is None:
            raise Exception

    def boxscore_matchup(self, ast):
        if ast.phrase is None:
            raise Exception
        
        phrase = ast.phrase.lower()
        away_phrase, home_phrase = phrase.split(' at ')

        home_parts = home_phrase.split()
        parser = GameReportParser()
        mdy = parser.parse(home_parts[-1], rule_name='mdy')
        month, day, year = mdy.split('/')
            
        away = self.annual_team(away_phrase, year)
        home = self.annual_team(home_phrase, year)

        if away is None or home is None:
            raise Exception

        return AST(home=home, away=away, date=mdy)

    def game_story_header(self, ast):
        if ast.phrase is None:
            return Exception

        phrase = ast.phrase.lower()
        away, home = phrase.split(' at ')

        return AST(home=unicode(home), away=unicode(away))

    def boxscore_pitching_header_team(self, ast):
        self.validate_nickname(ast.nickname)
        return ast

    def boxscore_hitting_header_team(self, ast):
        self.validate_nickname(ast.nickname)
        return ast

    def boxscore_team(self, ast):
        self.validate_nickname(ast.nickname)
        return ast

    def boxscore_team_count_colon(self, ast):
        self.validate_nickname(ast.nickname)
        return ast

    def boxscore_team_basic_rate(self, ast):
        self.validate_nickname(ast.nickname)
        return ast


def parse_league_daily(html, cities=None, nicknames=None):
    if cities is None or nicknames is None:
        raise Exception
    
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table')

    semantics = GameReportSemanticActions(cities=cities, nicknames=nicknames)
    parser = GameReportParser(parseinfo=False, semantics=semantics)

    stories_ast = None
    for table in tables:
        try:
            stories_ast = parser.parse(table.prettify(), 'game_story_table')
            break
        except FailedToken:
            pass

    boxscores_ast = None
    for table in tables:
        try:
            boxscores_ast = parser.parse(table.prettify(), 'boxscore_table')
            break
        except FailedToken:
            pass

    if stories_ast is None or boxscores_ast is None:
        raise Exception

    return AST(game_stories=stories_ast, boxscores=boxscores_ast)

def parse_game_daily(html, cities=None, nicknames=None):
    soup = BeautifulSoup(html, 'html.parser')
    full_recap = soup.find('pre')
    full_recap_string = full_recap.prettify()

    semantics = GameReportSemanticActions(cities=cities, nicknames=nicknames)
    parser = GameReportParser(parseinfo=False, semantics=semantics)
    ast = parser.parse(full_recap_string, 'full_recap')
    return ast

