# Map Fangraphs column names to our column names
FG_BATTING_TO_DB = {
    'G': 'g',
    'PA': 'pa',
    'HR': 'hr',
    'R': 'r',
    'RBI': 'rbi',
    'SB': 'sb',
    'BB%': 'bb_pct',
    'K%': 'k_pct',
    'ISO': 'iso',
    'BABIP': 'babip',
    'AVG': 'avg',
    'OBP': 'obp',
    'SLG': 'slg',
    'wOBA': 'woba',
    'wRC+': 'wrc_plus',
    'BsR': 'bsr',
    'Off': 'off',
    'Def': 'defense',
    'WAR': 'war',
    'AB': 'ab',
    'H': 'h',
    '1B': 'single',
    '2B': 'double',
    '3B': 'triple',
    'BB': 'bb',
    'IBB': 'ibb',
    'SO': 'so',
    'HBP': 'hbp',
    'GDP': 'gdp',
    'CS': 'cs',
    'GB': 'gb',
    'FB': 'fb',
    'LD': 'ld',
    'IFFB': 'iffb'
}

FG_PITCHING_TO_DB = {
    'W': 'w',
    'L': 'l',
    'SV': 'sv',
    'G': 'g',
    'GS': 'gs',
    'IP': 'ip',
    'K/9': 'k_per_9',
    'BB/9': 'bb_per_9',
    'HR/9': 'hr_per_9',
    'BABIP': 'babip',
    'LOB%': 'lob_pct',
    'GB%': 'gb_pct',
    'HR/FB': 'hr_per_fb',
    'ERA': 'era',
    'FIP': 'fip',
    'xFIP': 'xfip',
    'WAR': 'war',
    'CG': 'cg',
    'H': 'h',
    'R': 'r',
    'ER': 'er',
    'HR': 'hr',
    'BB': 'bb',
    'IBB': 'ibb',
    'HBP': 'hbp',
    'WP': 'wp',
    'BK': 'bk',
    'SO': 'so',
    'GB': 'gb',
    'FB': 'fb',
    'LD': 'ld'
}

def clean_key(key):
    return key.strip().strip('"')

def clean_value(value):
    return value.strip().strip('"').strip('%').strip()