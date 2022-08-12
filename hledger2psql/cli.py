import time

import click

from .hledger2psql import journal2df, save_db


@click.command()
@click.option(
    "-f",
    "--file",
    type=click.Path(
        exists=True,
        file_okay=True,
        dir_okay=False,
        resolve_path=True,
    ),
    required=True,
    help="journal file to export",
)
@click.option(
    "-d",
    "--db-url",
    type=click.STRING,
    help="Ex: postgresql://user:password@address:port/database",
    required=True,
)
@click.option(
    "-t",
    "--table-name",
    type=click.STRING,
    help="table name to create",
    required=True,
)
@click.option(
    "-i",
    "--interval",
    help="Interval to export again. 0 or empty to run it only once",
    type=click.IntRange(min=0),
    required=False,
    default=0,
)
def hledger2psql(file: str, db_url: str, table_name: str, interval: int):
    """
    Help for this"""
    if interval == 0:
        start = time.time()
        df = journal2df(file)
        log = save_db(df, db_url, table_name, file, start)
        print(log)
    else:
        while True:
            start = time.time()
            df = journal2df(file)
            log = save_db(df, db_url, table_name, file, start)
            log += f" Next in {interval} minutes... (Ctrl-c to exit)"
            print(log)
            time.sleep(int(interval) * 60)
