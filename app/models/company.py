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
    # if re.findall("[\d+\W+]{2,20}$", str):
    if len(str) < 2:
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


class Company:
    db = "dev_on_deck"

    def __init__(self, data):
        self.id = data['company_id']
        self.company_name = data['company_name']
        self.password = data['password']
        self.email = data['email']
        self.location = data['location']
        self.description = data['description']
        self.created_at = data['created_at']
        self.update_at = data['update_at']
        self.positions = []

    @staticmethod
    def validate_register(data):
        is_valid = True
        # VALIDATING FIRSTNAME
        if not validateName(data['company_name']) or len(data["company_name"]) < 2:
            is_valid = False

        # VALIDATING PASSWORD
        if not validatePasswd(data['password']):
            is_valid = False

        if not check(data['email']):
            is_valid = False

        if len(data["location"]) < 2:
            is_valid = False

        if len(data["description"]) < 2:
            is_valid = False

        return is_valid

    @staticmethod
    def validate_update(data):
        is_valid = True
        # VALIDATING FIRSTNAME
        if not validateName(data['company_name']):
            is_valid = False

        if not check(data['email']):
            is_valid = False

        if len(data["location"]) < 2:
            is_valid = False

        if len(data["description"]) < 2:
            is_valid = False

        return is_valid

    @classmethod
    def validate_login(cls, data):
        return check(data)

    @classmethod
    def save(cls, data):
        query = "INSERT INTO companies(company_name, password, email, location, description) VALUES (%(company_name)s, %(password)s, %(email)s, %(location)s, %(description)s);"
        result = connectToMySQL(cls.db).query_db(query, data)
        print("SAVE_COMP => ", result)
        return result

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM companies WHERE company_id = %(company_id)s"
        result = connectToMySQL(cls.db).query_db(query, data)
        print("DELETE_COMP => ", result)
        return result

    @classmethod
    def add_position(cls, data):
        query = "INSERT INTO positions(company_id, name, description, location) VALUES(%(company_id)s, %(name)s, %(description)s, %(location)s)"
        result = connectToMySQL(cls.db).query_db(query, data)
        print("ADD_POSITION => ", result)
        return result

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM companies JOIN positions ON companies.company_id = positions.company_id WHERE companies.company_id = %(company_id)s; "

        results = connectToMySQL(cls.db).query_db(query, data)
        companies = []
        for row in results:
            print("R O W =>", row)
            compData = {
                "company_id": row['company_id'],
                "company_name": row['company_name'],
                "password": row['password'],
                "email": row['email'],
                "location": row['location'],
                "position": row['position'],
                "description": row['description'],
                "created_at": row['created_at'],
                "update_at": row['update_at'],
                "positions": []
            }
            print("compData => ", compData)

            positionData = {
                "position_id": row['position_id'],
                "name": row['name'],
                "description": row['description'],
                "location": row['location'],
                "created_at": row['created_at'],
                "update_at": row['update_at']
            }
            print("positionData => ", positionData)

            index = findCompInArray(companies, row['developer_id'])
            if index == -1:
                print(index)
                compData['positions'].append(positionData)
                companies.append(compData)
            else:
                companies[index]['positions'].append(positionData)
        return companies

    @classmethod
    def get_profile_by_id(cls, data):
        query = "SELECT * FROM companies WHERE companies.company_id = %(company_id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        print("GET_COMP_PROFILE => ", result)
        return result

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT company_id, email, password, company_name FROM companies WHERE companies.email = %(email)s"
        result = connectToMySQL(cls.db).query_db(query, data)
        print("LOGIN_INFO => ", result)
        return result

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM companies JOIN positions ON companies.company_id = positions.company_id;"

        results = connectToMySQL(cls.db).query_db(query)
        companies = []
        for row in results:
            print("R O W =>", row)
            compData = {
                "company_id": row['company_id'],
                "company_name": row['company_name'],
                "password": row['password'],
                "email": row['email'],
                "location": row['location'],
                "position": row['position'],
                "description": row['description'],
                "created_at": row['created_at'],
                "update_at": row['update_at'],
                "positions": []
            }
            print("compData => ", compData)

            positionData = {
                "position_id": row['position_id'],
                "name": row['name'],
                "description": row['description'],
                "location": row['location'],
                "created_at": row['created_at'],
                "update_at": row['update_at']
            }
            print("positionData => ", positionData)

            index = findCompInArray(companies, row['developer_id'])
            if index == -1:
                print(index)
                compData['positions'].append(positionData)
                companies.append(compData)
            else:
                companies[index]['positions'].append(positionData)
        return companies

    @classmethod
    def update(cls, data):
        query = "UPDATE companies SET company_name = %(company_name)s, email=%(email)s, location=%(location)s, description= %(description)s WHERE companies.company_id = %(company_id)s;"

        result = connectToMySQL(cls.db).query_db(query, data)
        return result

    @classmethod
    def remove_positions(cls, data):
        query = "DELETE FROM positions WHERE positions.company_id = %(company_id)s"
        result = connectToMySQL(cls.db).query_db(query, data)
        print("DELETE_POSITIONS => ", result)
        return result

    @classmethod
    def get_comp_positions(cls, data):
        query = "SELECT * FROM companies JOIN positions ON companies.company_id = positions.company_id  WHERE companies.company_id = %(company_id)s"

        results = connectToMySQL(cls.db).query_db(query, data)
        print("POSITIONS_BY_COMPANY => ", results)
        compPositions = []
        for row in results:
            compPositions.append(
                {"id": row['position_id'], "name": row['name']})
        return compPositions


def findCompInArray(devs, developer_id):
    for i in range(0, len(devs), 1):
        if devs[i]['developer_id'] == developer_id:
            return i
    return -1
