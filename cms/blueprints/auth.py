# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, current_user, login_required, logout_user

from cms.models import Admin
from cms.forms import LoginForm
from cms.utils import redirect_back

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GEt', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        admin = Admin.query.first()
        if admin:
            if username == admin.username and admin.validate_password(password):
                login_user(admin, remember)
                flash('Welcom back.', 'info')
                return redirect_back()
            flash('Invalid username or password.', 'warning')
        else:
            flash('No account.','warning')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout Sucess.','info')
    return redirect_back()