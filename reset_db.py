from __init__ import create_app
from models import db

app = create_app()

with app.app_context():
    db.drop_all()      # очищает структуру (на всякий случай)
    db.create_all()    # создаёт все таблицы заново
    print("База данных пересоздана")
