from models import db
from models.log import Log
from flask_login import current_user

def log_action(action: str):
    if current_user.is_authenticated:
        new_log = Log(action=action, user_id=current_user.id)
        db.session.add(new_log)
        db.session.commit()