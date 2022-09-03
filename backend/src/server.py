"""
Implements a backend server
"""
# Imports
from base64 import b64encode
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

# Placeholder photo
with open("/usr/app/src/assets/no-pic.png", "rb") as img_file:
    no_pic = b64encode(img_file.read())



"""
    General Routes
    - signup
    - samples-ids
    - samples-selected-info
"""


# Page "Cadastro" sign up route
@server.route("/signup", methods=["POST"])
def signup_root():
    request_data =  request.json
    with Session(database) as session:
        exists = session.query(
            model.classes.Users
        ).filter(
            or_(
                model.classes.Users.cpf == request_data["cpf"],
                model.classes.Users.email == request_data["email"]
            )
        ).all()
        if len(exists) != 0:
            return {
                "error": "User exists for this CPF or Email."
            }, 401
        try:
            session.add(
                model.classes.Users(
                    name = request_data["name"],
                    cpf = request_data["cpf"],
                    email = request_data["email"],
                    password = generate_password_hash(
                        request_data["password"],
                        method="sha256"
                    ),
                    role = request_data["role"],
                    state = request_data["state"],
                    city = request_data["city"]
                )
            )
        except:
            session.rollback()
            raise
        else:
            session.commit()
    return {
        "ok": True
    }

# Page "Login" login route
@server.route("/login", methods=["POST"])
def login_root():
    request_data =  request.json
    with Session(database) as session:
        user = session.query(
            model.classes.Users
        ).filter(
            model.classes.Users.cpf == request_data["username"]
        ).first()
    if user is None:
        return {
            "error": "User not found."
        }, 401
    if check_password_hash(
        user.password,
        request_data["password"]
    ):
        return {
            "token": generate_token(
                user.id,
                user.email,
                user.role,
                30
            ),
            "user_data": {
                "uid": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role
            }
        }
    return {
        "error": "Wrong password."
    }, 401

# Get all info from a sample
@server.route("/samples-info", methods=["GET"])
def sample_by_id():

    if verify_id(request.args.get('id')):
        return {
            "error": "Invalid id" 
        }, 400
 

    with Session(database) as session:
        results = session.query(
            model.classes.Samples
        ).filter(
            model.classes.Samples.id ==  request.args.get('id')
        ).first()
        sample = {
            "id": results.id,
            "lab_ide_id": results.lab_ide_id,
            "lab_dia_id": results.lab_dia_id,
            "agent_id": results.agent_id,
            "neighborhood": results.neighborhood,
            "latitude": results.latitude,
            "longitude": results.longitude,
            "photo_date": results.photo_date,
            "agent_send_date": results.agent_send_date,
            "pathogen":  results.pathogen,
            "pathogen_type": results.pathogen_type,
            "vector":  results.vector,
            "specie": results.species,
            "sex": results.sex,
            "lab_ide_recieve_date": results.lab_ide_recieve_date,
            "lab_ide_send_date": results.lab_ide_send_date,
            "lab_ide_observations": results.lab_ide_observations,
            "lab_dia_observations": results.lab_dia_observations,
            "lab_dia_recieve_date": results.lab_dia_recieve_date,
            "status": results.status,
            "sample_photo_1": f"{results.sample_photo_1}",
            "sample_photo_2": f"{results.sample_photo_2}",
            "sample_photo_3": f"{results.sample_photo_3}"
        }

    return sample


# Get all samples id
@server.get("/samples-ids")
def samples_ids():
    samples_list = []
    if(request.args.get('status') != None):
        if verify_status(request.args.get('status')):
            return {
                'error': 'Invalid Status'
            }, 400

        with Session(database) as session:
            results = session.query(
                model.classes.Samples
            ).filter(
                model.classes.Samples.status == request.args.get('status')
            ).all()
            for sample in results:
                samples_list.append(sample.id)
    else:
         with Session(database) as session:
            results = session.query(
                model.classes.Samples
            ).all()
            for sample in results:
                samples_list.append(sample.id)
    samples_list.sort()
    return {
        "Ids": samples_list
    }



"""
    Agent Routes
    - submit-sample
    - agent-send-sample
    - result-agent
"""

# Page "Enviar amostra fotográfica"
@server.route("/submit-sample", methods=["POST"])
def agent_sample_root():


    if verify_date(request.form.get("photo_date")):
        return {
            "error": "Invalid photo date" 
        }, 400
    

    if verify_id(request.form.get("agent_id")):
        return {
            "error": "Invalid agent id" 
        }, 400


    latitude_list = []
    longitude_list = []
    photo_error_count = 0
    
    # Check photo 1 exif data
    try:
        raw_photo1 = request.files["sample_photo_1"].read()
        photo1 = b64encode(raw_photo1)
    except:
        photo1 = no_pic
        photo_error_count += 1
    else:
        exif1 = Image(raw_photo1)
        try:
            lat = coordinates_extractor(exif1.gps_latitude, exif1.gps_latitude_ref)
            long = coordinates_extractor(exif1.gps_longitude, exif1.gps_longitude_ref)
            latitude_list.append(lat)
            longitude_list.append(long)
        except:
            pass

    # Check photo 2 exif data
    try:
        raw_photo2 = request.files["sample_photo_2"].read()
        photo2 = b64encode(raw_photo2)
    except:
        photo2 = no_pic
        photo_error_count += 1
    else:
        exif2 = Image(raw_photo2)
        try:
            lat = coordinates_extractor(exif2.gps_latitude, exif2.gps_latitude_ref)
            long = coordinates_extractor(exif2.gps_longitude, exif2.gps_longitude_ref)
            latitude_list.append(lat)
            longitude_list.append(long)
        except:
            pass

    # Check photo 3 exif data
    try:
        raw_photo3 = request.files["sample_photo_3"].read()
        photo3 = b64encode(raw_photo3)
    except:
        photo3 = no_pic
        photo_error_count += 1
    else:
        exif3 = Image(raw_photo3)
        try:
            lat = coordinates_extractor(exif3.gps_latitude, exif3.gps_latitude_ref)
            long = coordinates_extractor(exif3.gps_longitude, exif3.gps_longitude_ref)
            latitude_list.append(lat)
            longitude_list.append(long)
        except:
            pass

    if (photo_error_count == 3):
        return {
            "error": "At least 1 photo needs to be sent."
        }, 400

    if (
        len(latitude_list) == 0 and
        request.form.get("latitude") != None and
        request.form.get("longitude") != None
    ):
        final_latitude = request.form.get("latitude")
        final_longitude = request.form.get("longitude")
    else:
        if len(latitude_list) > 0:
            final_latitude = latitude_list[0]
            final_longitude = longitude_list[0]
        else:
            return {
                "detail": 101,
                "error": "Server could not extract coordinates from photo."
            }, 400

    query = {
        'latitude': final_latitude,
        'longitude': final_longitude
    }
    geodecoding = requests.get("https://api.bigdatacloud.net/data/reverse-geocode-client", params=query)

    neighborhood = request.form.get("neighborhood")
    try:
        for adm in geodecoding.json()['localityInfo']['administrative']:
            if adm['adminLevel'] == 10:
                neighborhood = adm['name']
    except:
        return {
            "detail": 102,
            "error": "Server could not extract neighborhood from coordenates."
        }, 400
    
    if neighborhood == None:
        return {
            "detail": 102,
            "error": "Server could not extract neighborhood from coordenates."
        }, 400
    with Session(database) as session:
        try:
            session.add(
                model.classes.Samples(
                   latitude=final_latitude,
                   longitude=final_longitude,
                   photo_date=request.form.get("photo_date"),
                   agent_id=request.form.get("agent_id"),
                   neighborhood=neighborhood,
                   sample_photo_1=photo1,
                   sample_photo_2=photo2,
                   sample_photo_3=photo3,
                   status=1
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

# Page "Enviar Amostra Física - Agente"
@server.route("/agent-send-sample", methods=["POST"])
def agent_send_root():
    request_data =  request.json



    if verify_id(request_data["id"]):
        return {
            "error": "Invalid sample id" 
        }, 400


    if verify_date(request_data["agent_send_date"]):
        return {
            "error": "Invalid date" 
        }, 400

    
    with Session(database) as session:
        try:
            session.query(
                model.classes.Samples
            ).filter(
                model.classes.Samples.id == request_data["id"]
            ).update({
                "agent_send_date": request_data["agent_send_date"],
                "status": 3
            })
        except:
            session.rollback()
            raise
        else:
            session.commit()
    return {
        "status": 200
    }

"""
    Identification Lab Routes
    - lab-identify-sample
    - lab-send-sample
    - lab-ide-result
"""

# Page "Identificar Amostra Física"
@server.route("/lab-identify-sample", methods=["POST"])
def lab_identify_root():

    specie_list = ["alberprozenia malheiroi", 
        "belminus laportei",
        "cavernicola pilosa",
        "eratyrus mucronatus",
        "microtriatoma trinidadensis",
        "panstrongylus geniculatus",
        "panstrongylus lignarius",
        "panstrongylus megistus",
        'panstrongylus rufotuberculatus',
        "psammolestes tertius",
        "rhodnius milesi",
        'rhodnius paraensis',
        "rhodnius pictipes",
        'rhodnius robustus',
        'triatoma rubrofasciata']
    request_data =  request.json

    if verify_id(request_data["id"]):
        return {
            "error": "Invalid sample id" 
        }, 400


    if not isinstance(request_data['misplaced'], bool):
        return {
            "error": "Invalid misplaced type" 
        }, 400
    
    if request_data['misplaced'] == True:
        status = 8

        with Session(database) as session:
            try:
                session.query(
                    model.classes.Samples
                ).filter(
                    model.classes.Samples.id == request_data["id"]
                ).update({
                    "lab_ide_observations": request_data["lab_ide_observations"],
                    "status": status
                })
            except:
                session.rollback()
                raise
            else:
                session.commit()
    else:
        status = 4
        if verify_date(request_data["lab_ide_recieve_date"]):
            return {
                "error": "Invalid date" 
            }, 400
        if request_data["sex"].lower() not in ['fêmea', "macho"]:
            return {
                "error": "Invalid sex" 
            }, 400
        sex = request_data["sex"].capitalize()
        if request_data["specie"].lower() not in specie_list:
            return {
                "error": "Invalid specie" 
            }, 400
        specie = request_data["specie"].capitalize()
        with Session(database) as session:
            try:
                session.query(
                    model.classes.Samples
                ).filter(
                    model.classes.Samples.id == request_data["id"]
                ).update({
                    "species": specie,
                    "sex": sex,
                    "lab_ide_observations": request_data["lab_ide_observations"],
                    "lab_ide_recieve_date": request_data["lab_ide_recieve_date"],
                    "status": status
                })
            except:
                session.rollback()
                raise
            else:
                session.commit()
    return {
        "status": 200
    }


# Page "Enviar Amostra Física - Laboratório de Identificação"
@server.route("/lab-send-sample", methods=["POST"])
def lab_send_root():
    request_data =  request.json



    if verify_id(request_data["id"]):
        return {
            "error": "Invalid sample id" 
        }, 400


    if verify_date(request_data["lab_ide_send_date"]):
        return {
            "error": "Invalid date" 
        }, 400


    with Session(database) as session:
        try:
            session.query(
                model.classes.Samples
            ).filter(
                model.classes.Samples.id == request_data["id"]
            ).update({
                "lab_ide_send_date": request_data["lab_ide_send_date"],
                "status": 5
            })
        except:
            session.rollback()
            raise
        else:
            session.commit()
    return {
        "status": 200
    }


# Page "Analisar amostra fotográfica - Laboratório de Identificação"
@server.route("/lab-ide-result", methods=["POST"])
def lab_ide_result_root():
    request_data = request.json



    if verify_id(request_data["lab_ide_id"]):
        return {
            "error": "Invalid lab id" 
        }, 400

    if verify_id(request_data["id"]):
        return {
            "error": "Invalid sample id" 
        }, 400
    

    if verify_vector(request_data["vector"]):
        return {
            "error": "Invalid Vector"
        },
    request_data =  request.json
    status = 2
    if request_data["vector"] == 2:
        status = 7
    with Session(database) as session:
        try:
            session.query(
                model.classes.Samples
            ).filter(
                model.classes.Samples.id == request_data["id"]
            ).update({
                "vector": request_data["vector"],
                "lab_ide_id": request_data["lab_ide_id"],
                "status": status
            })
        except:
            session.rollback()
            raise
        else:
            session.commit()
    return {
        "status": 200
    }


"""
    
    Diagnosis Lab
    - lab-dia-result
"""


# Page "Analisar amostra física - Laboratório de Diagnóstico"
@server.route("/lab-dia-result", methods=["POST"])
def lab_dia_result_root():
    request_data =  request.json

    if not isinstance(request_data['misplaced'], bool):
        return {
            "error": "Invalid misplaced type" 
        }, 400

    if verify_id(request_data["lab_dia_id"]):
        return {
            "error": "Invalid lab id" 
        }, 400

    if verify_id(request_data["id"]):
        return {
            "error": "Invalid sample id" 
        }, 400
    if request_data['misplaced']:
        with Session(database) as session:
            try:
                session.query(
                    model.classes.Samples
                ).filter(
                    model.classes.Samples.id == request_data["id"]
                ).update({
                    "lab_dia_id":  request_data["lab_dia_id"],
                    "lab_dia_observations": request_data["lab_dia_observations"],
                    "status": 8
                })
            except:
                session.rollback()
                raise
            else:
                session.commit()
    else:
        if verify_date(request_data["lab_dia_recieve_date"]):
            return {
                "error": "Invalid date" 
            }, 400

        if not isinstance(request_data["pathogen"], bool):
            return {
                "error": "Invalid pathogen type" 
            }, 400
        
        pathogens_list = ["trypanosoma cruzi", "trypanosoma rangeli"]
        if request_data["pathogen_type"].lower() not in pathogens_list:
            return {
                "error": "Invalid pathogen" 
            }, 400
        pat_type = request_data["pathogen_type"].capitalize()

        if request_data["pathogen"]:
            status_code = 6
        else:
            status_code = 7
        with Session(database) as session:
            try:
                session.query(
                    model.classes.Samples
                ).filter(
                    model.classes.Samples.id == request_data["id"]
                ).update({
                    "pathogen": request_data["pathogen"],
                    "pathogen_type": pat_type,
                    "lab_dia_id":  request_data["lab_dia_id"],
                    "lab_dia_observations": request_data["lab_dia_observations"],
                    "lab_dia_recieve_date": request_data["lab_dia_recieve_date"],
                    "status": status_code
                })
            except:
                session.rollback()
                raise
            else:
                session.commit()
    return {
        "status": 200
    }






"""
    Log Routes
    - samples
    - user
"""

# Check all samples in database
@server.get("/samples")
def log_sample():
    samples_list = []
    with Session(database) as session:
        results = session.query(
            model.classes.Samples
        ).order_by(
            model.classes.Samples.id.asc()
        ).limit(
            request.args.get('limit')
        ).offset(request.args.get('offset')).all()
        count = session.query(
            model.classes.Samples
        ).count()

        for sample in results:
            samples_list.append({
                "id": sample.id,
                "lab_ide_id": sample.lab_ide_id,
                "lab_dia_id": sample.lab_dia_id,
                "agent_id": sample.agent_id,
                "neighborhood": sample.neighborhood,
                "latitude": sample.latitude,
                "longitude": sample.longitude,
                "photo_date": sample.photo_date,
                "agent_send_date": sample.agent_send_date,
                "pathogen":  sample.pathogen,
                "pathogen_type": sample.pathogen_type,
                "vector":  sample.vector,
                "specie": sample.species,
                "sex": sample.sex,
                "lab_ide_recieve_date": sample.lab_ide_recieve_date,
                "lab_ide_send_date": sample.lab_ide_send_date,
                "lab_ide_observations": sample.lab_ide_observations,
                "lab_dia_observations": sample.lab_dia_observations,
                "lab_dia_recieve_date": sample.lab_dia_recieve_date,
                "status": sample.status
            })

    return {
        "Samples": samples_list,
        "Count": count
    }


@server.post("/filter-samples")
def filter_sample():
    samples_list = []
    request_data =  request.json
    date_range = request_data['date_range']

    #Filtering Status
    


    selected_status =  request_data['status']
    with Session(database) as session:

        partial_result = session.query(model.classes.Samples)
        if selected_status:

            if verify_status(selected_status):
                return {
                    "error": "Invalid status" 
                }, 400
            partial_result = partial_result.filter(
                model.classes.Samples.status == selected_status
            )

        if date_range:
            if len(date_range) == 2:
                first_date = date_range[0]
                last_date = date_range[1]
                if first_date:
                    partial_result = partial_result.filter(
                        model.classes.Samples.photo_date.between(first_date, last_date)
                    )
                else:
                    partial_result = partial_result.filter(
                        model.classes.Samples.photo_date <= date_range[1]
                    )
            else:
                partial_result = partial_result.filter(
                    model.classes.Samples.photo_date == date_range[0]
                )

        results = partial_result.all()

        for sample in results:
            samples_list.append({
                "id": sample.id,
                "lab_ide_id": sample.lab_ide_id,
                "lab_dia_id": sample.lab_dia_id,
                "agent_id": sample.agent_id,
                "neighborhood": sample.neighborhood,
                "latitude": sample.latitude,
                "longitude": sample.longitude,
                "photo_date": sample.photo_date,
                "agent_send_date": sample.agent_send_date,
                "pathogen":  sample.pathogen,
                "pathogen_type": sample.pathogen_type,
                "vector":  sample.vector,
                "specie": sample.species,
                "sex": sample.sex,
                "lab_ide_recieve_date": sample.lab_ide_recieve_date,
                "lab_ide_send_date": sample.lab_ide_send_date,
                "lab_ide_observations": sample.lab_ide_observations,
                "lab_dia_observations": sample.lab_dia_observations,
                "lab_dia_recieve_date": sample.lab_dia_recieve_date,
                "status": sample.status
            })

    return {
        "Samples": samples_list,
    }




# Check every user in database
@server.get("/users")
def log_users():
    uid = request.args.get("id")
    if uid is None:
        users_list = []
        with Session(database) as session:
            results = session.query(
                model.classes.Users
            ).all()
            for user in results:
                users_list.append({
                    "id": user.id,
                    "name": user.name,
                    "cpf": user.cpf,
                    "email": user.email,
                    "role": user.role,
                    "state": user.state,
                    "city": user.city
                })
        return {
            "Users": users_list
        }
    try:
        with Session(database) as session:
            results = session.query(
                model.classes.Users
            ).where(model.classes.Users.id == uid)
            user = results[0]
        return {
            "id": user.id,
            "name": user.name,
            "cpf": user.cpf,
            "email": user.email,
            "role": user.role,
            "state": user.state,
            "city": user.city
        }
    except IndexError:
        return {
            "error": "User not found."
        }, 401


# Generate token
@server.post("/auth/validate_token")
def auth_get_token():
    request_data = request.get_json()
    try:
        _ = validate_token(
            request_data["token"]
        )
        return {
            "validation": True
        }, 200
    except Exception as e:
        return {
            "validation": False,
            "error": e.__str__()
        }, 401

# Retrieve user data from token
@server.post("/auth/get_user_data")
def auth_get_user_data():
    request_data = request.get_json()
    try:
        uid = validate_token(
            request_data["token"]
        )
        with Session(database) as session:
            results = session.query(
                model.classes.Users
            ).where(model.classes.Users.id == uid)
            user = results[0]
        return {
            "user_data": {
                "uid": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role
            }
        }
    except Exception as e:
        return {
            "user_data": False,
            "error": e.__str__()
        }, 401
