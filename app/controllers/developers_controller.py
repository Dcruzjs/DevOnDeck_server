from app.models.developer import Developer
from app import app
from flask import render_template, request, redirect, session, jsonify, json
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route("/login", methods=['POST'])
def login():
    if(Developer.validate_login(request.form['email'])):
        data = {"email": request.form['email']}
        dev_db = Developer.get_by_email(data)
        if len(dev_db) == 1:
            encryptedPassword = dev_db[0]['password']

            if bcrypt.check_password_hash(encryptedPassword, request.form['password']):
                current_user = {
                    "id": dev_db[0]['developer_id'],
                    "name": dev_db[0]['first_name'],
                    "email": dev_db[0]['email']
                }
                access_token = create_access_token(identity=current_user)
                return jsonify(access_token)
            else:
                return jsonify(message="Invalid password."), "406 Invalid password."
        else:
            return jsonify(message="The email does not belong to any user."), "404 The email does not belong to any user."
    else:
        return jsonify(message="The email format is invalid."), 406


@app.route('/signup', methods=['POST'])
def signup():
    # print(request.form['email'])
    if(Developer.validate_register(request.form)):
        encryptedPassword = bcrypt.generate_password_hash(
            request.form['password'])
        devData = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "password": encryptedPassword,
            "email": request.form['email'],
            "location": request.form['location'],
            "position": request.form['position'],
            "genre": request.form['genre'],
            "description": request.form['description']
        }
        id = Developer.save(devData)
        # if not 'user' in session:
        current_user = {
            "id": id,
            "name": devData['first_name'],
            "email": devData['email']
        }
        # access_token = create_access_token(identity=user)

        access_token = create_access_token(identity=current_user)
        return jsonify(access_token)

    return jsonify(message="Invalid Data sent to the server...")


@app.route("/delete_dev_account", methods=['POST'])
@jwt_required()
def delete_dev_account():
    current_user = get_jwt_identity()
    data = {"developer_id": current_user['id']}
    Developer.remove_skills(data)
    rm = Developer.delete(data)
    return jsonify(rm)


@app.route('/get_dev_profile', methods=['GET'])
@jwt_required()
def get_profile():
    current_user = get_jwt_identity()
    print("TOKEN => ", current_user)
    data = {"id": current_user['id']}
    devInfo = Developer.get_by_id(data)
    # print("DEV_INFO => ", devInfo)
    return jsonify(devInfo)


@app.route("/get_dev_skills", methods=['GET'])
@jwt_required()
def get_dev_skills():
    current_user = get_jwt_identity()
    data = {"id": current_user['id']}
    return jsonify(Developer.get_dev_skills(data))


@app.route("/add_dev_skills", methods=['POST'])
@jwt_required()
def add_skills():
    # Access the identity of the current user with get_jwt_identity
    skills = json.loads(request.data.decode('UTF-8'))
    current_user = get_jwt_identity()
    print("TOKEN => ", current_user)
    dataR = {
        "developer_id": current_user['id']
    }
    Developer.remove_skills(dataR)
    for skill in skills:
        data = {"developer_id": int(
            current_user['id']), "skill_id": int(skill['id'])}
        print(Developer.add_skills(data))

    return jsonify(message="Skills were Added")


@app.route("/delete_dev_skills", methods=['POST'])
@jwt_required()
def delete_dev_skills():
    current_user = get_jwt_identity()
    data = {"id": current_user['id']}
    return jsonify(Developer.remove_skills(data))


@app.route('/update_dev_profile', methods=['POST'])
@jwt_required()
def create_user():
    current_user = get_jwt_identity()
    print("TOKEN => ", current_user)
    # data = {"id": current_user['id']}
    if(Developer.validate_update(request.form)):

        devData = {
            "developer_id": current_user['id'],
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['email'],
            "location": request.form['location'],
            "position": request.form['position'],
            "genre": request.form['genre'],
            "description": request.form['description']
        }
        result = Developer.update(devData)
        return jsonify(result)
