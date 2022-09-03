# Imports
from flask import (
    Flask,
    request
)
import sqlalchemy as sql
import pandas as pd
from random import randint, sample
import pandas as pd
from sqlalchemy.sql.schema import Column
from flask_cors import CORS
import json
import numpy as np
import os
from sqlalchemy.sql import func
from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from flask_cors import CORS




# App & Server settings
server = Flask(__name__)
CORS(server)


# Connects to the database
database = sql.create_engine('sqlite:///data/database.db', echo=False)

# Map database tables as classes
model = automap_base()
model.prepare(database, reflect=True)




# metadata.create_all(engine)

# Routes

@server.route('/')
def home():
    return "Coe, broder"


@server.route('/getSalariesAverageBySize', methods=["GET"])
def getDesmatamentoData():
    size = request.args.get('size')
    
    query2 = f"""
        SELECT 
            work_year,
            salary
        FROM ds_salaries
        WHERE company_size = "{size}"
    """

    with database.connect() as connection:
        result = database.execute(query2)
        salary = result.all()

    df = pd.DataFrame(salary, columns=['year', 'salary'])
    grouped = df.groupby('year').mean()

    return {
        'x': grouped.index.to_list(),
        'y': grouped['salary'].to_list(),
        'mode': 'lines',
        'name': 'Lines'
    }
