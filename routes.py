from flask import render_template, redirect, url_for, request, abort
from flask_login import login_user, logout_user, login_required, current_user
from models import db
from models.user import User
from models.project import Project
from models.role import Role
from models.log import Log
from models.user_project import UserProject
from forms.login_form import LoginForm
from forms.register_form import RegisterForm
from forms.edit_profile_form import EditProfileForm
from forms.assign_project_form import AssignProjectForm
from forms.assign_manager_form import AssignManagerForm
from log_action import log_action
from __init__ import bcrypt

def register_routes(app):

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        error = None
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                log_action("Пользователь вошёл в систему")
                return redirect(url_for('profile'))
            else:
                error = "Неверный логин или пароль."
        return render_template('login.html', form=form, error=error)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(name=form.name.data, email=form.email.data, password_hash=hashed_pw, role_id=2)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        return render_template('register.html', form=form)

    @app.route('/profile')
    @login_required
    def profile():
        user_projects = [relation.project for relation in current_user.user_projects]
        return render_template('profile.html', user=current_user, projects=user_projects)

    @app.route('/edit_profile', methods=['GET', 'POST'])
    @login_required
    def edit_profile():
        form = EditProfileForm(name=current_user.name)
        if form.validate_on_submit():
            current_user.name = form.name.data
            db.session.commit()
            return redirect(url_for('profile'))
        return render_template('edit_profile.html', form=form)

    @app.route('/projects')
    @login_required
    def projects():
        projects = Project.query.all()
        return render_template('projects.html', projects=projects)

    @app.route('/assign_project', methods=['GET', 'POST'])
    @login_required
    def assign_project():
        if current_user.role_id not in [1, 2, 3]:  # Только те, кто выше сотрудника
            return redirect(url_for('profile'))

        form = AssignProjectForm()

        # Только тех, кто ниже по званию
        form.user_id.choices = [
            (u.id, u.name) for u in User.query.filter(User.role_id > current_user.role_id).all()
        ]
        form.project_id.choices = [(p.id, p.title) for p in Project.query.all()]

        if form.validate_on_submit():
            relation = UserProject(user_id=form.user_id.data, project_id=form.project_id.data)
            db.session.add(relation)
            db.session.commit()
            return redirect(url_for('projects'))

        return render_template('assign_project.html', form=form)

    @app.route('/admin/users')
    @login_required
    def admin_users():
        if current_user.role_id != 1:
            abort(403)  # Запрет доступа, если пользователь не админ
        users = User.query.all()
        return render_template('admin_users.html', users=users)

    @app.route('/admin/logs')
    @login_required
    def admin_logs():
        if current_user.role_id != 1:
            abort(403)  # Запрет доступа, если пользователь не админ
        logs = Log.query.order_by(Log.timestamp.desc()).all()
        return render_template('admin_logs.html', logs=logs)

    @app.route('/admin/hierarchy', methods=['GET', 'POST'])
    @login_required
    def manage_hierarchy():
        if current_user.role_id != 1:
            return redirect(url_for('profile'))

        form = AssignManagerForm()
        form.subordinate_id.choices = [(u.id, u.name) for u in User.query.filter(User.role_id > 1).all()]
        form.manager_id.choices = [(u.id, u.name) for u in User.query.filter(User.role_id < 4).all()]

        if form.validate_on_submit():
            subordinate = User.query.get(form.subordinate_id.data)
            subordinate.manager_id = form.manager_id.data
            db.session.commit()
            return redirect(url_for('manage_hierarchy'))

        users = User.query.filter(User.role_id > 1).all()
        return render_template('hierarchy.html', users=users, form=form)