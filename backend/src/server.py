"""
Implements a backend server
"""
# Imports
from base64 import b64encode, b64decode
from exif import Image
import requests
import re
from helpers.utils import (
    connect_db,
    generate_token,
    validate_token,
    verify_status,
    verify_date,
    verify_id,
    verify_vector,
    coordinates_extractor
)

from flask import Flask, request
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from sqlalchemy import or_
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from flask_cors import CORS

# Server instantiation and configuration
server = Flask(__name__)
CORS(server)
server.config['JSON_SORT_KEYS'] = False

# Create connection engine with database
database = connect_db()

# Map database tables as classes
model = automap_base()
model.prepare(database, reflect=True)

@server.route("/get_all_turtles", methods=["GET"])
def get_samples_turtles():
    samples_list = []
    with Session(database) as session:
        results = session.query(
            model.classes.tartaruga
        ).all()
        for sample in results:
            samples_list.append({
                "id": sample.identificador,
                "nome": sample.nome,
                "ultimo_encontro": sample.ultimo_encontro,
                "forma": sample.forma,
            })

    return {
        "Samples": samples_list,
    }

    
@server.route("/get_all_findings", methods=["GET"])
def get_samples_fingings():

    samples_list = []
    with Session(database) as session:
        results = session.query(
            model.classes.encontro
        ).all()
   

        for sample in results:
            samples_list.append({
                "id": sample.identificador,
                "latitude": sample.latitude,
                "longitude": sample.longitude,
                "tartaruga_identificador": sample.tartaruga_identificador,
                "imagem_corpo": f"{sample.imagem_corpo}",
                "imagem_cabeca": f"{sample.imagem_corpo}",
                "data": sample.data
            })

    return {
        "Samples": samples_list,
    }



@server.route("/submit-sample", methods=["POST"])
def submit_sample():
    request_data =  request.json
    imagem_corpo = b64encode(b64decode(request_data['photo1']))
    imagem_cabeca = b64encode(b64decode(request_data['photo2']))

    with Session(database) as session:
        obj =  model.classes.tartaruga(
                   nome=request_data["turtle_name"],
                   ultimo_encontro=request_data["photo_date"],
                   forma="[1, 2, 3]",
                )

        try:
            session.add(
               obj
            )
        except:
            session.rollback()
            raise
        else:
            session.commit()
            session.refresh(obj)
            
    with Session(database) as session:
        try:
            session.add(
                model.classes.encontro(
                    tartaruga_identificador=obj.identificador,
                    latitude="30.2",
                    longitude="50.32",
                    imagem_corpo=imagem_corpo,
                    imagem_cabeca=imagem_cabeca,
                    data=request_data["photo_date"]
                )
            )
        except:
            session.rollback()
            raise
        else:
            session.commit()

    return {
        "status": 200
    }


# Get all samples names
@server.get("/samples-names")
def samples_names():
    samples_list = []
  
    with Session(database) as session:
        results = session.query(
            model.classes.tartaruga
        ).all()

    for sample in results:
        samples_list.append(sample.nome)
    samples_list.sort()
    
    return {
        "nomes": samples_list
    }