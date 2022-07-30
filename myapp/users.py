from myapp import app
from flask import redirect, render_template, request, url_for, flash
from flask_login import login_required
from myapp.dao import Users, User
from flask_paginate import Pagination, get_page_args
from myapp.forms import UserForm
from myapp.uploads import update_list_images

users_service = Users()
all_users = users_service.list_all_users()

def get_users(offset=0, per_page=10, users=all_users):
    return users[offset: offset + per_page]

@app.route('/users')
@login_required
def pagination_page():
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    users_service = Users()
    users = users_service.list_all_users()
    total = len(users)
    pagination_users = get_users(offset=offset, per_page=per_page, users=users)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    return render_template('users/pagination.html', users=pagination_users, page=page, per_page=per_page, pagination=pagination)