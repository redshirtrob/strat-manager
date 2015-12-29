from bs4 import BeautifulSoup
from GameReport import GameReportParser
from grako.exceptions import FailedToken

def parse_league_daily(html):
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table')

    parser = GameReportParser(parseinfo=False)

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

    return {'game_stories' : stories_ast, 'boxscores' : boxscores_ast}

def parse_game_daily(html):
    soup = BeautifulSoup(html, 'html.parser')
    full_recap = soup.find('pre')
    full_recap_string = full_recap.prettify()

    parser = GameReportParser(parseinfo=False)
    ast = parser.parse(full_recap_string, 'full_recap')
    return ast

