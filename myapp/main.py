from myapp import app
from flask import render_template
from flask_login import login_required
from myapp.dao import Users
from myapp.uploads import update_list_images

@app.route('/myapp')
@login_required
def myapp_page():
    total_images = len(update_list_images())
    return render_template('users/dashboard.html', qtd_images=total_images)
    
@app.route('/dashboard')
@login_required
def dashboard_page():
    total_images = len(update_list_images())
    return render_template('users/dashboard.html', qtd_images=total_images)