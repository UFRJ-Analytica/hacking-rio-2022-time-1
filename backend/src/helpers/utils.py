"""
This module implements the utility functions to help the major functions of the backend.
"""
from os import getenv
import datetime as dt
from typing import List, Union
import re

import sqlalchemy as sql
import jwt
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.orm import Session
from pandas.core.series import Series


def connect_db() -> Engine:
    """Create engine to connect to database.

    Returns:
        Engine: The connection engine to the database.
    """
    return sql.create_engine(
        "postgresql://" +
        getenv('SQL_USER') +
        ":" +
        getenv('SQL_PSWD') +
        "@" +
        getenv('SQL_HOST') +
        ":" +
        getenv('SQL_PORT') +
        "/" +
        getenv('SQL_DATABASE')
    )

def get_next_table_id(database: Engine, table: DeclarativeMeta) -> int:
    """Return next ID of a table.

    Args:
        database (Engine): The connection engine to the database.
        table (DeclarativeMeta): The class for the table to get the ID.

    Returns:
        int: The next ID of the table.
    """
    last_id = None
    with database.connect() as conn:
        selection = conn.execute(
            f"SELECT id FROM \"{table.__table__.name}\" ORDER BY id DESC LIMIT 1"
        )
    for i in selection:
        last_id = i[0]
    if last_id is None:
        return 1
    return int(last_id) + 1

def delete_and_reset(database: Engine, table: DeclarativeMeta) -> None:
    """Delete a table content and reset serial sequence for a table ID column.

    Args:
        database (Engine): The connection engine to the database.
        table (DeclarativeMeta): The class for the table to delete and reset.
    """
    with Session(database) as session:
        try:
            session.query(table).delete()
        except:
            session.rollback()
            raise
        else:
            session.commit()
    with database.connect() as conn:
        conn.execute(
            f"ALTER SEQUENCE \"{table.__table__.name}_id_seq\" RESTART WITH 1"
        )

def tuple_to_dict(tuple_lst: List[tuple], values_first: bool = True) -> dict:
    """Converts a tuple list into a dict.

    Args:
        tuple_lst (List[tuple]): A list of tuples.
        values_first (bool, optional): Whether to have the first element of the
        tuple as value, instead of key. Defaults to True.

    Returns:
        dict: A dict representation of the list of tuples.
    """
    if values_first:
        order = 0
    else:
        order = 1

    return {
        i[abs(1-order)]:i[abs(0-order)]
        for i in tuple_lst
    }

def replace_list(row: list, db_ids: dict) -> list:
    """Replaces database IDs in a list row.

    Args:
        row (list): Row containing list.
        db_ids (dict): The dictionary of database values and IDs.

    Returns:
        list: Row with replaced values.
    """
    if row is None:
        return []
    if len(row) == 0:
        return []
    return [db_ids[v] for v in row]

def get_db_ids(
    database: Engine,
    id_column: Union[InstrumentedAttribute, None],
    data_column: InstrumentedAttribute
) -> Union[dict, List]:
    """Gather data, and optionally the IDs, from a table as a dictionary or list
    for aggregation purposes.

    Args:
        database (Engine): The connection engine to the database.
        id_column (Union[InstrumentedAttribute, None]): The id column or None.
        data_column (InstrumentedAttribute): The data column.

    Returns:
        dict | list: Dictionary with ids and data from the table. List of data in case of
        None as id_column.
    """
    if id_column is None:
        with database.connect() as conn:
            return list(map(
                lambda x: x[0],
                conn.execute(
                    sql.select([
                        data_column
                    ])
                ).fetchall()
            ))
    else:
        with database.connect() as conn:
            return tuple_to_dict(
                conn.execute(
                    sql.select([
                        id_column,
                        data_column
                    ])
                ).fetchall()
            )

def to_db_id(column: Series, db_ids: dict) -> Series:
    """Returns a Pandas' Series converted from values to database IDs.

    Args:
        column (Series): The dataframe Series column.
        db_ids (dict): The dictionary of database values and IDs.

    Returns:
        Series: The converted column.
    """
    return column.replace(
        db_ids.keys(),
        db_ids.values()
    )

def generate_token(uid, email, role, exp=1):
    token = jwt.encode(
        {
            "uid": uid,
            "email": email,
            "role": role,
            "exp": dt.datetime.now() + dt.timedelta(days=exp)
        },
        getenv("SECRET"),
        "HS256"
    )
    return token

def validate_token(token):
    validate = jwt.decode(
        token,
        getenv("SECRET"),
        ["HS256"]
    )
    return validate["uid"]


def verify_status(status):
    if isinstance(status, str):
        if not status.isdigit():
            return True
        elif status not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            return True
    elif not isinstance(status, int):
        return True
    elif status > 9 or status < 1:
        return True


def verify_id(id):
    if isinstance(id, str):
        if not id.isdigit():
            return True
    elif not isinstance(id, int):
        return True 

def verify_date(date):
    if not isinstance(date, str):
        return True 
    if not bool(re.fullmatch('[0-9]{4}-[0-9]{2}-[0-9]{2}', date)):
        return True

def verify_vector(vector):


    if isinstance(vector, str):
        if not vector.isdigit():
            return True
        elif vector not in ["1", "2", "3"]:
            return True
    elif not isinstance(vector, int):
        return True
    elif vector > 3 or vector < 1:
        return True

def coordinates_extractor(coordinates, coordinates_ref):
    decimal_degrees = coordinates[0] + \
                      coordinates[1] / 60 + \
                      coordinates[2] / 3600
    
    if coordinates_ref == "S" or coordinates_ref == "W":
        decimal_degrees = -decimal_degrees
    
    return decimal_degrees