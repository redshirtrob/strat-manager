# BLB Extractor

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

### Extract attachments from mbox file
This is an optional script for extracting dailies, scorebooks, and
standings files from an mbox file.  This script exists because I had a
large number of files stored as attachments in a gmail account.  The
easiest way to get access to them was to export the data as an mbox
file using Gmail's export tools.
```bash
$ ./extractor.py file.mbox
```

### Generating the Grako Parser
Before using the parsers you need to generate the Grako Parser file.
This file is pre-generated as a convenience, but if you need to make
changes you can generate a new version as follows:
```bash
$ grako GameReport.ebnf >GameReport.py
```

### Parsing attachments into AST
This is a helper script for parsing dailies.  
```bash
$ ./parse-data.py ./file.dat
```

### Parsing a single League Daily file
You can process a single League Daily file into an AST as follows:
```bash
$ ./parse-league-daily.py  --stash=./raw-asts ./file.dat
```

This will generate an AST from the HTML Report file and store it in a
file called `./raw-asts/file-ast.dat`.

You can also insert the AST into a MongoDB database with the
`--use-db` option.  You can skip the AST cleaning phase by passing the
`--skip-clean` option.

### Cleaning AST
```bash
$ ./clean-ast.py
```
