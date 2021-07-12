from app import app, db
from app import views, models

# db.create_all()
if __name__ == '__main__':

    app.run(debug=True)
