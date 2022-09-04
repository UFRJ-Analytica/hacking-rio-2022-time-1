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
        imagem_cabeca_outra = sample.ultima_imagem_cabeca
        d2 = contour_matching(imagem_cabeca, imagem_cabeca_outra)
        if d2 <= 0.1:
            best_matches.append(d2)
            best_matches_identificadores.append(sample.identificador)
        # threshold = 60
        # if total_matches > threshold:
        #     best_matches.append(total_matches)
        #     best_matches_identificadores.append(sample.identificador)

    if len(best_matches) == 0:
        return None
    else:
        idx = np.argmin(best_matches)
        return best_matches_identificadores[idx]
    
def insert_new_turtle(request_data):
    with Session(database) as session:
        obj =  model.classes.tartaruga(
                   nome=request_data["turtle_name"],
                   ultimo_encontro=request_data["photo_date"],
                   ultima_imagem_cabeca=b64encode(b64decode(request_data['photo2']))
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
    # mais_similar = None
    if mais_similar is None:
        tartaruga_identificador = insert_new_turtle(request_data)
    else:
        tartaruga_identificador = mais_similar

    latitude = request_data['latitude']
    longitude = request_data['longitude']

    query = {
        'latitude': latitude,
        'longitude': longitude
    }
    geodecoding = requests.get("https://api.bigdatacloud.net/data/reverse-geocode-client", params=query)
    try:
        for adm in geodecoding.json()['localityInfo']['administrative']:
            if adm['adminLevel'] == 4:
                estado = adm['name']
            if adm['adminLevel'] == 8:
                cidade = adm['name']
    except:
        estado = "indefinido"
        cidade = "indefinido"


    with Session(database) as session:
        try:
            session.add(
                model.classes.encontro(
                    tartaruga_identificador=tartaruga_identificador,
                    latitude=latitude,
                    longitude=longitude,
                    cidade=cidade,
                    estado=estado,
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
        result = session.query(
            model.classes.tartaruga.nome
        ).filter( model.classes.tartaruga.identificador == mais_similar).first()

        return {
            "detail": 102,
            "error": f"Esta tartaruga já existe e se chama {result.nome}"
        }, 400


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
                "cidade": sample.cidade,
                "estado": sample.estado,
                "data": sample.data       
            })

        for sample in samples_list:
            result = session.query(
                model.classes.tartaruga.nome
            ).filter(model.classes.tartaruga.identificador == sample['id']).first()
            sample['nome'] = result.nome
            

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



@server.post("/filter-samples")
def filter_sample():
    samples_list = []
    request_data =  request.json
    date_range = request_data['date']
    selected_name =  request_data['nome']
    selected_city =  request_data['cidade']
    selected_state =  request_data['estado']


    with Session(database) as session:

        partial_result = session.query(model.classes.encontro)
        result = session.query(
                model.classes.tartaruga.identificador
            ).filter(model.classes.tartaruga.nome == selected_name).first()

        if selected_name:
            partial_result = partial_result.filter(
                model.classes.encontro.tartaruga_identificador == result.identificador
            )

        if date_range:
            if len(date_range) == 2:
                first_date = date_range[0]
                last_date = date_range[1]
                if first_date:
                    partial_result = partial_result.filter(
                        model.classes.encontro.data.between(first_date, last_date)
                    )
                else:
                    partial_result = partial_result.filter(
                        model.classes.encontro.data <= date_range[1]
                    )
            else:
                partial_result = partial_result.filter(
                    model.classes.encontro.data == date_range[0]
                )
        if selected_city:
            partial_result = partial_result.filter(
                model.classes.encontro.cidade == selected_city
            )
        if selected_state:
            partial_result = partial_result.filter(
                model.classes.encontro.estado == selected_state
            )


        results = partial_result.all()

        for sample in results:
            samples_list.append({
                "id": sample.identificador,
                "latitude": sample.latitude,
                "cidade" :sample.cidade,
                "estado": sample.estado,
                "longitude": sample.longitude,
                "tartaruga_identificador": sample.tartaruga_identificador,
                "imagem_corpo": f"{sample.imagem_corpo}",
                "imagem_cabeca": f"{sample.imagem_cabeca}",
                "data": sample.data   
            })

        for sample in samples_list:
            result = session.query(
                model.classes.tartaruga.nome
            ).filter(model.classes.tartaruga.identificador == sample['tartaruga_identificador']).first()
            sample['nome'] = result.nome
        
    return {
        "Samples": samples_list,
        # "Nome": result.nome
    }
