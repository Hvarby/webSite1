from webSite1 import create_app  # замени на имя твоего проекта
from models import db

app = create_app()

with app.app_context():
    db.create_all()
    print("База данных успешно создана.")
