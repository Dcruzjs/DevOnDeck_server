from flask.globals import request
from app.config.MySQLConnection import connectToMySQL
from app.models import skill
import re


def check(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.fullmatch(regex, email)):
        print("Valid Email")
        return True

    else:
        print("Invalid Email")
        return False


def validateName(str):
    if re.findall("[\d+\W+]{2,20}$", str):
        print("Invalid Name")
        return False

    else:
        print("Valid Name")
        return True


def validatePasswd(str):
    validPass = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"
    if re.findall(validPass, str):
        print("Valid PassWord")
        return True

    else:
        print("Invalid PassWord")
        return False


class Developer:
    db = "dev_on_deck"

    def __init__(self, data):
        self.id = data['developer_id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.password = data['password']
        self.email = data['email']
        self.location = data['location']
        self.position = data['position']
        self.genre = data['genre']
        self.description = data['description']
        self.created_at = data['created_at']
        self.update_at = data['update_at']
        self.skills = []

    @staticmethod
    def validate_register(data):
        is_valid = True
        # VALIDATING FIRSTNAME
        if not validateName(data['first_name']) or len(data["first_name"]) < 2:

            is_valid = False

        # VALIDATING LASTNAME
        if not validateName(data['last_name']) or len(data["last_name"]) < 2:
            is_valid = False

        # VALIDATING PASSWORD
        if not validatePasswd(data['password']):
            is_valid = False

        if not check(data['email']):
            is_valid = False

        if len(data["location"]) < 2:
            is_valid = False

        if len(data["position"]) < 2:
            is_valid = False

        if len(data["position"]) < 2:
            is_valid = False

        if len(data["genre"]) < 2:
            is_valid = False

        return is_valid

    @staticmethod
    def validate_update(data):
        is_valid = True
        # VALIDATING FIRSTNAME
        if not validateName(data['first_name']) or len(data["first_name"]) < 2:
            is_valid = False

        # VALIDATING LASTNAME
        if not validateName(data['last_name']) or len(data["last_name"]) < 2:
            is_valid = False

        if not check(data['email']):
            is_valid = False

        if len(data["location"]) < 2:
            is_valid = False

        if len(data["position"]) < 2:
            is_valid = False

        if len(data["position"]) < 2:
            is_valid = False

        if len(data["genre"]) < 2:
            is_valid = False

        return is_valid

    @classmethod
    def validate_login(cls, data):
        return check(data)

    @classmethod
    def save(cls, data):
        query = "INSERT INTO developers(first_name, last_name, password, email, location, position, genre, description) VALUES (%(first_name)s,%(last_name)s, %(password)s, %(email)s, %(location)s, %(position)s, %(genre)s, %(description)s);"
        result = connectToMySQL(cls.db).query_db(query, data)
        print("SAVE_DEV => ", result)
        return result

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM developers WHERE developer_id = %(developer_id)s"
        result = connectToMySQL(cls.db).query_db(query, data)
        print("DELETE_DEV => ", result)
        return result

    @classmethod
    def add_skills(cls, data):
        query = "INSERT INTO developers_skills(developer_id, skill_id) VALUES(%(developer_id)s, %(skill_id)s)"
        result = connectToMySQL(cls.db).query_db(query, data)
        print("ADD_DEVELOPER_SKILLS => ", result)
        return result

    # @classmethod
    # def get_by_id(cls, data):
        # query = "SELECT * FROM developers  WHERE developers.developer_id = %(id)s;"
        # results = connectToMySQL(cls.db).query_db(query, data)
        # print("DEVELOPER_BY_ID => ", results)
        # # return cls(results[0])
        # return results

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM developers JOIN developers_skills ON developers.developer_id = developers_skills.developer_id JOIN skills ON developers_skills.skill_id = skills.skill_id WHERE developers.developer_id = %(id)s; "

        results = connectToMySQL(cls.db).query_db(query, data)
        devs = []
        for row in results:
            print("R O W =>", row)
            devData = {
                "developer_id": row['developer_id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "password": row['password'],
                "email": row['email'],
                "location": row['location'],
                "position": row['position'],
                "genre": row['genre'],
                "description": row['description'],
                "created_at": row['created_at'],
                "update_at": row['update_at'],
                "skills": []
            }
            print("devData => ", devData)

            skillData = {
                "id": row['skill_id'],
                "name": row['name']
            }
            print("skillData => ", skillData)

            index = findUserInArray(devs, row['developer_id'])
            if index == -1:
                print(index)
                devData['skills'].append(skillData)
                devs.append(devData)
                # newDev = cls(devData)
                # newDev.skills.append(
                #     skill.Skill(skillData))
                # devs.append(newDev)
            else:
                devs[index]['skills'].append(skillData)
                #         devs[index].skills.append(
                #             skill.Skill(skillData))
        return devs

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT developer_id, email, password, first_name FROM developers WHERE developers.email = %(email)s"
        result = connectToMySQL(cls.db).query_db(query, data)
        print("LOGIN_INFO => ", result)
        return result

    @classmethod
    def get_all_dev(cls):
        query = "SELECT * FROM developers JOIN developers_skills ON developers.developer_id = developers_skills.developer_id JOIN skills ON developers_skills ON skills.skill_id = developers_skills.skill_id;"

        results = connectToMySQL(cls.db).query_db(query)
        devs = []
        for row in results:
            # print("R O W =>", row)
            devData = {
                "developer_id": row['developer_id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "password": row['password'],
                "email": row['email'],
                "location": row['location'],
                "position": row['position'],
                "genre": row['genre'],
                "description": row['description'],
                "created_at": row['created_at'],
                "update_at": row['update_at'],
                "skills": []
            }
            print("devData => ", devData)

            skillData = {
                "id": row['skill_id'],
                "name": row['name']
            }
            print("skillData => ", skillData)

            index = findUserInArray(devs, row['developer_id'])
            if index == -1:
                devData['skills'].append(skillData)
                devs.append(devData)
                # newDev = cls(devData)
                # newDev.skills.append(
                #     skill.Skill(skillData))
                # devs.append(newDev)
            else:
                devs[index]['skills'].append(skillData)
                #         devs[index].skills.append(
                #             skill.Skill(skillData))
        return devs

    @classmethod
    def update(cls, data):
        query = "UPDATE developers SET developer_id = %(developer_id)s, first_name = %(first_name)s, last_name = %(last_name)s, email=%(email)s, location=%(location)s, position= %(position)s, genre=%(genre)s, description= %(description)s WHERE developers.developer_id = %(developer_id)s;"

        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    @classmethod
    def remove_skills(cls, data):
        query = "DELETE FROM developers_skills WHERE developers_skills.developer_id = %(developer_id)s"
        result = connectToMySQL(cls.db).query_db(query, data)
        print("DELETE_SKILLS => ", result)
        return result

    @classmethod
    def get_dev_skills(cls, data):
        query = "SELECT skills.skill_id, skills.name FROM developers JOIN developers_skills ON developers.developer_id = developers_skills.developer_id JOIN skills ON developers_skills.skill_id = skills.skill_id WHERE developers.developer_id = %(id)s"

        results = connectToMySQL(cls.db).query_db(query, data)
        print("SKILLS_BY_DEV => ", results)
        devSkills = []
        for row in results:
            devSkills.append({"id": row['skill_id'], "name": row['name']})
        return devSkills


def findUserInArray(devs, developer_id):
    for i in range(0, len(devs), 1):
        if devs[i]['developer_id'] == developer_id:
            return i
    return -1
