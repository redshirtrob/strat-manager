from bs4 import BeautifulSoup

REPORT_TYPE_LEAGUE_DAILY = 'League Daily'
REPORT_TYPE_GAME_DAILY = 'Game Daily'
REPORT_TYPE_GAME_SCOREBOOK = 'Game Scorebook'
REPORT_TYPE_LEAGUE_STANDINGS = 'League Standings'

def get_report_type(html):
    """Determine the report type for an HTML document"""
    attachment_type = "Unknown"
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('title')
    fonts = soup.find_all('font')
    if title is not None and title.string == 'Strat-O-Matic Daily Report':
        attachment_type = REPORT_TYPE_LEAGUE_DAILY
    elif fonts is not None:
        for font in fonts:
            contents = font.string
            if contents is None:
                continue
            
            if contents.startswith('BOXSCORE'):
                attachment_type = REPORT_TYPE_GAME_DAILY
                break
            elif contents.startswith('*** TOP OF INNING 1 ***'):
                attachment_type = REPORT_TYPE_GAME_SCOREBOOK
                break
            elif contents.startswith('LEAGUE STANDINGS'):
                attachment_type = REPORT_TYPE_LEAGUE_STANDINGS
                break
    return attachment_type

def get_title(html):
    """Extract the title from an HTML document"""
    soup = BeautifulSoup(html, 'html.parser')
    title = soup.find('title')
    if title is not None:
        return title.contents[0]
    return "No Title"

INT_KEYS = ('part', 'game_count', 'season_count', )
NAME_KEYS = ('name', 'player_name')

def clean(item, key, keypath):
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

def flatten(item, key=None, keypath=None, should_clean=True):
    """Remove redundant nesting"""
    flat_item = item
    if isinstance(item, dict):
        flat_item = dict()
        for k, v in item.iteritems():
            kp = k if key is None else '{}.{}'.format(keypath, k)
            flat_item[k] = flatten(v, k, kp, should_clean)
    elif isinstance(item, list):
        flat_item = list()
        index = 0
        for value in item:
            kp = '{}[{}]'.format(keypath, index)
            nv = flatten(value, keypath=kp, should_clean=should_clean)
            if isinstance(nv, list):
                flat_item += nv
            else:
                flat_item.append(nv)
            index += 1
    elif should_clean:
        flat_item = clean(item, key, keypath)
    return flat_item
