from app.config.MySQLConnection import connectToMySQL
from app.models import developer


class Skill:
    db = "dev_on_deck"

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.developers = []
        self.positions = []

    # @classmethod
    # def get(cls, data):
    #     query = "SELECT * FROM skills JOIN developers_skills ON skills.skill_id = developers_skills.skill_id JOIN developers ON developers.developer_id = developers_skills.developer_id WHERE skills.skill_id = %(id)s"

    #     developers = connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def save(cls, data):
        query = "INSERT INTO skills(name) VALUES(%(name)s)"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_skills(cls):
        query = "SELECT skill_id, name FROM skills;"
        result = connectToMySQL(cls.db).query_db(query)
        print("GET_SKILLS => ", result)
        return result

    # @classmethod
    # def add_skills(cls, data):
    #     query = "INSERT INTO developers_skills(developer_id, skill_id) VALUES(%(developer_id)s, %(skill_id)s)"
    #     result = connectToMySQL(cls.db).query_db(query, data)
    #     print("ADD_DEVELOPER_SKILLS => ", result)
    #     return result
