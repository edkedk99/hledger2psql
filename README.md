# hledger2psql


Export a hledger journal file to a postgresql database. The data will be ready to be used in data visualization tools to extract information from your transaction record and better understand your financials using beautiful charts and dashboards. 

## Features

- Used postgresql instead of sqlite because it will have better support. Apache Superset doesn't support sqlite and has postgresql support built-in.
- Convert transactions and posting tags to column to used them as chart dimension
- Run it once or automatically *every x minutes*
- Export locally or to a remote server using postgres connection

## Comparison to built-in functionality

Hledger can export to sql with the command `hledger -f data.journal print --output-format=sql` but it has some limitations:

- It only output the sql command. This package send the command to the Postgresql
- The main reason hledger built-in feature is not ideal is because it insert all transaction and comment tags in a *comment* column. Sql needs each tag in a different column so you can filter and group by each tag. Also it insert the payee and the notes in the same *description* column. Splitting them in two different columns also allows better filtering and grouping

## Install

`pip install git+https://github.com/edkedk99/hledger2psql.git`


## How to use

See the package help with `hledger2psql --help`

```
Usage: hledger2psql [OPTIONS]

  Export a hledger journal file to a postgresql only once or repeat in
  interval. Transaction and posting tags will be converted to table columns

Options:
  -f, --file FILE               journal file to export  [required]
  -d, --db-url TEXT             Ex: postgresql://user:password@address:port/da
                                tabase  [required]
  -t, --table-name TEXT         table name to create  [required]
  -i, --interval INTEGER RANGE  Interval to export again. 0 or empty to run it
                                only once  [x>=0]
  --help                        Show this message and exit.
```

## Superset docker compose

A *docker-compose.yml* is available with superset and a postgresql container to make it easier to start creating dashboards at docker directory in this repo.

### Instructions

1. On the repository directory *superset_docker*, clone *Apache Superset* to the folder *repo*: `cd superset_docker && git clone https://github.com/apache/superset.git repo`
2. If needed, edit the *superset_docker/.env* file with your prefered ports
3. Start the containers: `cd superset_docker && docker-compose up -d`
4. Wait some minutes, then open *Superset* on your browser with your server address and configured port in the *.env* file. Username and password are *admin*.
5. Add exported tables to *Superset*. The database address is *user_db* and port is *5432*. Note you should use the database **internal port** and not the external. And remember to use the database **external port** when exporting using hledger2pysql 

### Tips

1. Remember to filter the data by account to avoid getting a total of 0 because in hledger all transactions sums to 0.


