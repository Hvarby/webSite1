from __init__ import create_app
from models import db
from models.user import User
from models.project import Project
from models.role import Role
from models.user_project import UserProject
import bcrypt

app = create_app()

with app.app_context():
    db.session.query(UserProject).delete()
    db.session.query(User).delete()
    db.session.query(Project).delete()
    db.session.query(Role).delete()

    roles = [
        Role(id=1, name='Администратор'),
        Role(id=2, name='Генеральный директор'),
        Role(id=3, name='Руководитель отдела'),
        Role(id=4, name='Сотрудник')
    ]
    db.session.add_all(roles)

    admin = User(
        name='Admin',
        email='admin@example.com',
        password_hash=bcrypt.hashpw('adminpass'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        role_id=1
    )

    ceo = User(
        name='Генеральный директор',
        email='ceo@example.com',
        password_hash=bcrypt.hashpw('ceopass'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        role_id=2
    )

    head = User(
        name='Руководитель Иван',
        email='head@example.com',
        password_hash=bcrypt.hashpw('headpass'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        role_id=3,
        manager_id=ceo.id
    )

    staff = User(
        name='Сотрудник Алексей',
        email='alexey@example.com',
        password_hash=bcrypt.hashpw('staffpass'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
        role_id=4,
        manager_id=head.id
    )

    db.session.add_all([admin, ceo])
    db.session.flush()

    head.manager_id = ceo.id
    db.session.add(head)
    db.session.flush()

    staff.manager_id = head.id
    db.session.add(staff)

    project1 = Project(title='Сайт компании')
    project2 = Project(title='Мобильное приложение')
    db.session.add_all([project1, project2])
    db.session.flush()

    relation = UserProject(user_id=staff.id, project_id=project1.id)
    db.session.add(relation)
    db.session.commit()

    print("База заполнена начальными данными.")
