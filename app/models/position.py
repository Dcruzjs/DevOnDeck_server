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


class Position:
    db = "dev_on_deck"

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.location = data['location']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.skills = []

    @staticmethod
    def validate_register(data):
        is_valid = True

        if not validateName(data['name']) or len(data["name"]) < 2:

            is_valid = False

        if len(data["description"]) < 2:
            is_valid = False

        if len(data["location"]) < 2:
            is_valid = False

        return is_valid

    @classmethod
    def save(cls, data):
        query = "INSERT INTO positions(name, location, description) VALUES (%(name)s, %(location)s, %(description)s);"
        result = connectToMySQL(cls.db).query_db(query, data)
        print("SAVE_POSITION => ", result)
        return result

    @classmethod
    def add_skills(cls, data):
        query = "INSERT INTO positions_skills(position_id, skill_id) VALUES(%(position_id)s, %(skill_id)s)"
        result = connectToMySQL(cls.db).query_db(query, data)
        print("ADD_POSITIONS_SKILLS => ", result)
        return result

    @classmethod
    def get_by_id(cls, data):
        # query = "SELECT * FROM positions  WHERE positions.position_id = %(id)s;"
        # results = connectToMySQL(cls.db).query_db(query, data)
        # print("POSITION_BY_ID => ", results)
        # return cls(results[0])

        query = "SELECT * FROM positions JOIN positions_skills ON positions.position_id = positions_skills.position_id JOIN skills ON positions_skills ON skills.skill_id = developers_skills.position_id WHERE positions.position_id = %(id)s;"

        results = connectToMySQL(cls.db).query_db(query)
        positions = []
        for row in results:

            posData = {
                "position_id": row['position_id'],
                "name": row['name'],
                "description": row['description'],
                "location": row['location'],
                "created_at": row['created_at'],
                "updated_at": row['updated_at']
            }
            print("posData => ", posData)

            skillData = {
                "id": row['skill_id'],
                "name": row['name']
            }
            print("skillData => ", skillData)

            index = findPosInArray(positions, row['developer_id'])
            if index == -1:
                newDev = cls(posData)
                newDev.skills.append(
                    skill.Skill(skillData))
                positions.append(newDev)
            else:
                positions[index].skills.append(
                    skill.Skill(skillData))
        return positions

    @classmethod
    def get_all_positions(cls):
        query = "SELECT * FROM positions JOIN positions_skills ON positions.position_id = positions_skills.position_id JOIN skills ON positions_skills ON skills.skill_id = developers_skills.position_id;"

        results = connectToMySQL(cls.db).query_db(query)
        positions = []
        for row in results:

            posData = {
                "position_id": row['position_id'],
                "name": row['name'],
                "description": row['description'],
                "location": row['location'],
                "created_at": row['created_at'],
                "updated_at": row['updated_at']
            }
            print("posData => ", posData)

            skillData = {
                "id": row['skill_id'],
                "name": row['name']
            }
            print("skillData => ", skillData)

            index = findPosInArray(positions, row['position_id'])
            if index == -1:
                newDev = cls(posData)
                newDev.skills.append(
                    skill.Skill(skillData))
                positions.append(newDev)
            else:
                positions[index].skills.append(
                    skill.Skill(skillData))
        return positions

    @classmethod
    def update(cls, data):
        query = "UPDATE positions SET name = %(name)s, location=%(location)s, description= %(description)s;"

        result = connectToMySQL(cls.db).query_db(query, data)
        return result


def findPosInArray(positions, position_id):
    for i in range(0, len(positions), 1):
        if positions[i].developer_id == position_id:
            return i
    return -1
