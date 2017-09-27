from bs4 import BeautifulSoup
from GameReport import GameReportParser
from grako.exceptions import FailedParse
from grako.ast import AST

PITCHING_RESULTS = (
    'WIN', 'W',
    'LOSS','L',
    'HOLD', 'H',
    'SAVE', 'S',
    'BS', 'B'
)

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

    def annual_team(self, phrase):
        year = phrase.partition(' ')[0]
        city = self.find_city(phrase)
        nickname = self.find_nickname(phrase)
        if city is None or nickname is None:
            return None
        return AST(city=unicode(city), nickname=unicode(nickname), year=year)

    def validate_nickname(self, nickname):
        if nickname is None:
            raise Exception("Invalid nickname: None")

        tmp_nickname = self.find_nickname(nickname.lower())
        if tmp_nickname is None:
            raise Exception("Invalid nickname: {}".format(nickname))
        nickname = tmp_nickname

    def boxscore_matchup(self, ast):
        if ast.phrase is None:
            raise Exception
        
        phrase = ast.phrase.lower()
        away_phrase, home_phrase = phrase.split(' at ')

        home_parts = home_phrase.split()
        parser = GameReportParser()

        # Try to parse date of form mm/dd/yyyy
        # Sometimes it's not present so we just skip it
        try:
            mdy = parser.parse(home_parts[-1], rule_name='mdy')
        except Exception:
            mdy = ''
            pass
            
        away = self.annual_team(away_phrase)
        home = self.annual_team(home_phrase)

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

    #   Northsiders        AB  R  H RBI AVG     Monarchs           AB  R  H RBI AVG
    def boxscore_hitting_header(self, ast):
        def headers(phrase, nickname):
            return phrase[phrase.find(nickname)+len(nickname):].split()
        
        if ast.phrase is None:
            raise Exception

        phrase = ast.phrase.lower()

        # Find the two team nickames and save the indexes
        nickname_indexes = []
        for nickname in self.nicknames:
            if nickname in phrase:
                nickname_indexes.append(phrase.find(nickname))

        if len(nickname_indexes) != 2:
            raise Exception
        
        # Break the string into home and away sides, away is first
        nickname_indexes.sort()
        away_string = phrase[nickname_indexes[0]:nickname_indexes[1]]
        away_team = self.find_nickname(away_string)
        away_headers = headers(away_string, away_team)
        
        home_string = phrase[nickname_indexes[1]:]
        home_team = self.find_nickname(home_string)
        home_headers = headers(home_string, home_team)

        # Generate the AST
        away_ast = AST(nickname=unicode(away_team), headers=[unicode(h) for h in away_headers])
        home_ast = AST(nickname=unicode(home_team), headers=[unicode(h) for h in home_headers])
        return AST(away=away_ast, home=home_ast)

    # <font color="#000000">J.Lopez WIN(4-0) BS(1st)  1 1/3   1   0   0   1   0   0  24   2.96</font>
    # <font color="#000000">E.Santana WIN BS          8 1/3   5   3   3   3   6   2 113  A1 D6</font>
    def boxscore_pitching_stat_line(self, ast):
        # parser handled the name/result string properly
        if len(ast.result_stats) > 0:
            return ast

        result_stats = []
        name_parts = ast.player_name.split()
        for pr in PITCHING_RESULTS:
            if pr in name_parts:
                result_stats.append(unicode(pr))

        # didn't find any results embedded in the `player_name`
        if len(result_stats) == 0:
            return ast

        # filter out the matched results and restore the player name
        name_parts = [np for np in name_parts if not np in result_stats]
        player_name = u' '.join(name_parts)

        # build the new ast with the computed `result_stats`
        new_ast = AST(
            ip=ast.ip,
            statistics=ast.statistics,
            player_name=player_name,
            scoresheet=ast.scoresheet,
            result_stats=result_stats
        )

        return new_ast

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

    stories_ast = []
    for table in tables:
        try:
            stories_ast[-1:-1] = parser.parse(table.prettify(), 'game_story_table')
        except FailedParse:
            pass

    boxscores_ast = []
    for table in tables:
        try:
            boxscores_ast[-1:-1] = parser.parse(table.prettify(), 'boxscore_table')
        except FailedParse as e:
            pass

        if len(stories_ast) == 0 or len(boxscores_ast) == 0:
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

