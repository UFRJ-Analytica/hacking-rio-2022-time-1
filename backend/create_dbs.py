import pandas as pd
import sqlalchemy as sql
from sqlalchemy.sql.schema import Column
import sqlalchemy.types as type
import os

df = pd.read_csv('./data/ds_salaries.csv', sep=",", index_col="Unnamed: 0")


engine = sql.create_engine('sqlite:///data/database.db', echo=False)

df.to_sql('ds_salaries', con=engine, if_exists='replace')
