from app import app

from app.controllers import developers_controller
from app.controllers import skills_controller
from app.controllers import companies_controller

if __name__ == "__main__":
    app.run(debug=True)
