from app.models.developer import Developer
from app import app
from flask import render_template, request, redirect, session, jsonify, json
from app.models.skill import Skill
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required


@app.route("/get_skills", methods=['GET'])
def get_skills():
    result = Skill.get_skills()
    # if len(result) > 0:

    return jsonify(result)
    # return jsonify(message=f"The server response: {result}")


# @app.route("/add_skills", methods=['POST'])
# def add_skills():
#     skills = json.loads(request.data.decode('UTF-8'))
#     print("from post", skills)
#     if 'user' in session:
#         print(session)
#         print(session['user']['id'])
#     return request.form
