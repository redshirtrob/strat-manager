# Strat-O-Matic Extractor

This is a series of scripts for extracting and processing data from
Strat-O-Matic game files.  The game data is stored in three types of
files: dailies, scorebooks, and standings.  This pipeline only handles
dailies and standings files as I only have a very small number of
scorebook files relative to dailies and standings.

The scripts can use the filesystem, mongodb or both as an intermediate
data store.  If you want to use mongo be sure to have a server
running:

```bash
$ mongod --config /usr/local/etc/mongod.conf
```

### Extract reports from mbox file
This is an optional script for extracting dailies, scorebooks, and
standings files from an mbox file.  This script exists because I had a
large number of files stored as reports in a gmail account.  The
easiest way to get access to them was to export the data as an mbox
file using Gmail's export tools.
```bash
$ mkdir ./data-files
$ ./extractor.py --stash=./data-files --use-db sample/gmail.mbox
```

### Generating the Grako Parser
Before using the parsers you need to generate the Grako Parser file.
This file is pre-generated as a convenience, but if you need to make
changes you can generate a new version as follows:
```bash
$ grako GameReport.ebnf >GameReport.py
```

### Batch parsing all reports
You can batch process all report files.
```bash
$ ./parse-data.py
```

Use the `-r` option to reprocess all the files.
```bash
$ ./parse-data.py -r
```

### Parsing a single report
You can process a single report file into an AST as follows:
```bash
$ mkdir ./raw-asts
$ ./parse-report.py --stash=./raw-asts ./sample/league-daily.report
$ ./parse-report.py --stash=./raw-asts ./sample/game-daily.report
```

This will generate an AST from the HTML Report file and store it in a
file called `./raw-asts/file-ast.dat`.

You can also insert the AST into a MongoDB database with the
`--use-db` option.  You can skip the AST cleaning phase by passing the
`--skip-clean` option.

# Importers

This is a series of scripts to import team and statistical data into a
database.  It uses a sqlite database for now, called `blb.db`.

### Team Importer

Generate a table of baseball teams.  This table is a prerequisite for
the Fangraphs importer, found below.
```bash
$ ./mlb-importer.py ./fixtures/mlb.csv
```

### Fangraphs Importer

Import a CSV from [Fangraphs](http://www.fangraphs.com).  See the
`Batting` and `Pitching` models for a list of the supported
statistical categories.  It's easy to add more, but these are the ones
I found most interesting.
```bash
$ ./fg-importer.py ./fixtures/fg-batting-2008.csv
$ ./fg-importer.py ./fixtures/fg-pitching-2008.csv
```

Or, import all Fangraph's data with:
```bash
$ ./import-fangraphs.sh
```

### Working with the Database

Create the virtual environment
```bash
$ mkvirtualenv strat-manager
$ workon strat-manager
$ pip install -r requirements.txt
```

Launch iPython and load the query file
```bash
$ ipython
In [1]: %load sql-bootstrap.py
```

Get all `PlayerSeason` records for a Player with `id` = 1
```python
In [5]: player_seasons = session.query(FGPlayerSeason).filter(FGPlayerSeason.player_id == 1)
In [7]: for ps in player_seasons:
  ...:     print ps
    ...:
    FGPlayerSeason(FGPlayer=Alfredo Amezaga, Season=2008)>
    FGPlayerSeason(FGPlayer=Alfredo Amezaga, Season=2009)>
    FGPlayerSeason(FGPlayer=Alfredo Amezaga, Season=2011)>
```

### Working with the SQL Store API

Launch iPython
```bash
$ ipython
```

Prepare Store
```python
In [21]: %load store-bootstrap.py
```

Query the Store
```python
In [21]: players = store.get_players_by_year('2009')
In [21]: p = players.result() # resolve Future
```

### Running the HTTP Server
```bash
$ PYTHONPATH=./ python web/server.py
```
