"""
Implements a backend server
"""
# Imports
from base64 import b64encode, b64decode
import requests
import re
import numpy as np

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

from vision_models.contour_recognition import contour_matching


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


def check_similarities(imagem_cabeca):
    with Session(database) as session:
        results = session.query(
            model.classes.tartaruga
        ).all()

    best_matches = []
    best_matches_identificadores = []
    for sample in results:
        imagem_cabeca_outra = b64decode(sample.imagem_cabeca)
        total_matches = contour_matching(imagem_cabeca, imagem_cabeca_outra)

        threshold = 60
        if total_matches > threshold:
            best_matches.append(total_matches)
            best_matches_identificadores.append(sample.identificador)

    if len(best_matches) == 0:
        return None
    else:
        idx = np.argmax(best_matches)
        return best_matches_identificadores[idx]
    
def insert_new_turtle(request_data):
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
            
        return obj.identificador    

@server.route("/submit-sample", methods=["POST"])
def submit_sample():
    request_data =  request.json
    imagem_corpo = b64encode(b64decode(request_data['photo1']))
    imagem_cabeca = b64encode(b64decode(request_data['photo2']))

    mais_similar = check_similarities(imagem_cabeca)

    if mais_similar is None:
        tartaruga_identificador = insert_new_turtle(request_data)
    else:
        tartaruga_identificador = mais_similar

    with Session(database) as session:
        try:
            session.add(
                model.classes.encontro(
                    tartaruga_identificador=tartaruga_identificador,
                    latitude="-22.90120000",
                    longitude="-43.10230000",
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

    if mais_similar is None:
        return {"status": 200}
    else:
        return {"status": 403}


# Check all samples in database
@server.get("/samples")
def log_sample():
    samples_list = []
    with Session(database) as session:
        results = session.query(
            model.classes.encontro
        ).order_by(
            model.classes.encontro.identificador.desc()
        ).limit(
            request.args.get('limit')
        ).offset(request.args.get('offset')).all()
        count = session.query(
            model.classes.encontro
        ).count()

        for sample in results:
            samples_list.append({
                "id": sample.tartaruga_identificador,
                "latitude": sample.latitude,
                "longitude": sample.longitude,
                "data": sample.data       
            })

        for sample in samples_list:
            result = session.query(
                model.classes.tartaruga.nome
            ).filter(model.classes.tartaruga.identificador == sample['id']).first()
                    
            query = {
                'latitude':  sample['latitude'],
                'longitude': sample['longitude']
            }
            geodecoding = requests.get("https://api.bigdatacloud.net/data/reverse-geocode-client", params=query)

            sample['nome'] = result.nome
            try:
                for adm in geodecoding.json()['localityInfo']['administrative']:
                    if adm['adminLevel'] == 4:
                        sample['estado'] = adm['name']
                    if adm['adminLevel'] == 8:
                        sample['cidade'] = adm['name']
            except:
                sample['estado'] = "indefinido"
                sample['cidade'] = "indefinido"

    return {
        "Samples": samples_list,
        "Count": count
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