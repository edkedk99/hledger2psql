import csv
import re
import subprocess
import time
from datetime import datetime
from io import StringIO
from typing import List, cast

import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import create_engine




def get_tag_item(comment: str):
    splitted = cast(List[str], comment.split(":", 1))
    if len(splitted) == 1:
        return None
    return (splitted[0].strip(), splitted[1].strip())


def get_tags(comment: str):
    comm_list = cast(List[str], re.split(r",|\n", comment))
    tags_list = [get_tag_item(item) for item in comm_list]
    tags_dict = {item[0]: item[1] for item in tags_list if item}
    return tags_dict


def split_description(description: str):
    splitted = description.split("|", 1)
    if len(splitted) == 1:
        return dict(payee="", note=description)
    else:
        return dict(payee=splitted[0], note=splitted[1])


def journal2df(journal_file: str) -> pd.DataFrame:
    comm = [
        "hledger",
        "-f",
        journal_file,
        "print",
        "--output-format=csv",
    ]

    journal_csv_str = subprocess.run(comm, capture_output=True).stdout.decode("utf8")
    journal_dicts = csv.DictReader(StringIO(journal_csv_str))

    txns_dicts = [
        {
            **txn,
            **split_description(txn["description"]),
            **get_tags(txn["comment"]),
            **get_tags(txn["posting-comment"]),
        }
        for txn in journal_dicts
    ]

    df = pd.DataFrame(txns_dicts)
    df = cast(pd.DataFrame, df.drop(["debit", "credit"], axis=1)).astype(
        dict(amount=float, date="datetime64[ns]", date2="datetime64[ns]")
    )
    return df


def save_db(
    df: pd.DataFrame, db_url: str, table_name: str, journal_file: str, start: float
) -> str:
    with create_engine(db_url).connect() as conn:
        df.to_sql(table_name, conn, if_exists="replace")
        command = text(f"select count(*) from {table_name}")
        rows_query = conn.execute(command).fetchone()

    rows = int(rows_query[0]) if rows_query else 0
    now = datetime.now()
    elapsed = time.time() - start
    log = f"{now} Added {rows} rows from {journal_file} to table {table_name} in {elapsed:.4f} seconds."
    return log
