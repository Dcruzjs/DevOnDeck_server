from app.models.company import Company
from app import app
from flask import render_template, request, redirect, session, jsonify, json
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route("/login_comp", methods=['POST'])
def login_comp():
    if(Company.validate_login(request.form['email'])):
        data = {"email": request.form['email']}
        comp_db = Company.get_by_email(data)
        if len(comp_db) == 1:
            encryptedPassword = comp_db[0]['password']

            if bcrypt.check_password_hash(encryptedPassword, request.form['password']):
                current_user = {
                    "id": comp_db[0]['company_id'],
                    "name": comp_db[0]['company_name'],
                    "email": comp_db[0]['email']
                }
                access_token = create_access_token(identity=current_user)
                return jsonify(access_token)
            else:
                return jsonify(message="Invalid password."), "406 Invalid password."
        else:
            return jsonify(message="The email does not belong to any user."), "404 The email does not belong to any user."
    else:
        return jsonify(message="The email format is invalid."), 406


@app.route('/signup_comp', methods=['POST'])
def signup_comp():
    # print(request.form['email'])
    if(Company.validate_register(request.form)):
        encryptedPassword = bcrypt.generate_password_hash(
            request.form['password'])
        # company_name, password, email, location, position, description
        compData = {
            "company_name": request.form['company_name'],
            "password": encryptedPassword,
            "email": request.form['email'],
            "location": request.form['location'],
            "description": request.form['description']
        }
        id = Company.save(compData)

        current_user = {
            "id": id,
            "name": compData['company_name'],
            "email": compData['email']
        }

        access_token = create_access_token(identity=current_user)
        return jsonify(access_token)

    return jsonify(message="Invalid Data sent to the server...")


@app.route("/delete_comp_account", methods=['POST'])
@jwt_required()
def delete_comp_account():
    current_user = get_jwt_identity()
    data = {"company_id": current_user['id']}
    Company.remove_skills(data)
    rm = Company.delete(data)
    return jsonify(rm)


@app.route('/get_comp_profile', methods=['GET'])
@jwt_required()
def get_comp_profile():
    current_user = get_jwt_identity()
    print("TOKEN => ", current_user)
    data = {"company_id": current_user['id']}
    compInfo = Company.get_profile_by_id(data)
    print("COMP_INFO => ", compInfo)
    return jsonify(compInfo)


@app.route("/get_comp_positions", methods=['GET'])
@jwt_required()
def get_comp_positions():
    current_user = get_jwt_identity()
    data = {"id": current_user['id']}
    return jsonify(Company.get_comp_positions(data))


@app.route("/add_position", methods=['POST'])
@jwt_required()
def add_position():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    skills = json.loads(request.data.decode('UTF-8'))
    print("TOKEN => ", current_user)
    dataR = {
        "developer_id": current_user['id']
    }
    Company.remove_skills(dataR)
    for skill in skills:
        data = {"company_id": int(
            current_user['id']), "skill_id": int(skill['id'])}
        print(Company.add_position(data))

    return jsonify(message="Skills were Added")


@app.route("/delete_comp_positions", methods=['POST'])
@jwt_required()
def delete_comp_positions():
    current_user = get_jwt_identity()
    data = {"id": current_user['id']}
    return jsonify(Company.remove_positions(data))


@app.route('/update_comp_profile', methods=['POST'])
@jwt_required()
def update_comp_profile():
    current_user = get_jwt_identity()
    print("TOKEN => ", current_user)
    # data = {"id": current_user['id']}
    if(Company.validate_update(request.form)):

        compData = {
            "company_id": current_user['id'],
            "company_name": request.form['company_name'],
            "email": request.form['email'],
            "location": request.form['location'],
            "position": request.form['position'],
            "description": request.form['description']
        }
        result = Company.update(compData)
        return jsonify(result)
    else:
        return jsonify(message="FATAL")
