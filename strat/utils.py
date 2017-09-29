from bs4 import BeautifulSoup

REPORT_TYPE_LEAGUE_DAILY = 'League Daily'
REPORT_TYPE_GAME_DAILY = 'Game Daily'
REPORT_TYPE_GAME_SCOREBOOK = 'Game Scorebook'
REPORT_TYPE_LEAGUE_STANDINGS = 'League Standings'

def get_report_type(html):
    """Determine the report type for an HTML document"""
    report_type = "Unknown"
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('title')
    fonts = soup.find_all('font')
    if title is not None and title.string == 'Strat-O-Matic Daily Report':
        report_type = REPORT_TYPE_LEAGUE_DAILY
    elif fonts is not None:
        for font in fonts:
            contents = font.string
            if contents is None:
                continue
            
            if contents.startswith('BOXSCORE'):
                report_type = REPORT_TYPE_GAME_DAILY
                break
            elif contents.startswith('*** TOP OF INNING 1 ***'):
                report_type = REPORT_TYPE_GAME_SCOREBOOK
                break
            elif contents.startswith('LEAGUE STANDINGS'):
                report_type = REPORT_TYPE_LEAGUE_STANDINGS
                break
    return report_type

def get_title(html):
    """Extract the title from an HTML document"""
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('title')
    if title is not None:
        return title.contents[0]
    return "No Title"

def is_game_report(report_type):
    return report_type in [REPORT_TYPE_LEAGUE_DAILY, REPORT_TYPE_GAME_DAILY]

INT_KEYS = ('part', 'game_count', 'season_count', )
NAME_KEYS = ('name', 'player_name')

def clean(item, key):
    """Sanitize some parsing artifacts"""

    # These keys should have null values converted to '1'
    if item is None and key in INT_KEYS:
        item = '1'
    elif isinstance(item, str) or isinstance(item, unicode):
        # Some strings have trailing whitespace, kill this off
        item = item.strip()

        # These values could end with a '-', but we don't want that
        if (key in NAME_KEYS) and item.endswith('-'):
            item = item.rstrip('-')
    return item

def flatten(item, key=None, should_clean=True):
    """Remove redundant nesting"""
    flat_item = item
    if isinstance(item, dict):
        flat_item = dict()
        for k, v in item.iteritems():
            flat_item[k] = flatten(v, k, should_clean)
    elif isinstance(item, list):
        flat_item = list()
        index = 0
        for value in item:
            nv = flatten(value, should_clean=should_clean)
            if isinstance(nv, list):
                flat_item += nv
            else:
                flat_item.append(nv)
            index += 1
    elif should_clean:
        flat_item = clean(item, key)
    return flat_item
