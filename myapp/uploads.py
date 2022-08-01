import json
import os
from myapp import app
from flask import flash, jsonify, redirect, render_template, request, send_from_directory, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from os import listdir
from os.path import isfile, join
from PIL import Image
from flask_paginate import Pagination, get_page_args
from myapp.dao import Users, Files, File

users_service = Users()
files_service = Files()

class MyImage: # This represents your class
    def __init__(self, id, name):
        self.id = id
        self.name = name
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name
        }

def user_directory(path_temp, user_id):
    user_path = path_temp + '/' + str(user_id)

    if os.path.exists(user_path):
        return user_path
    else: 
        os.makedirs(user_path)
    return user_path 

# Carrega uma lista atualzada com os nomes dos arquivos da pasta UPLOAD_FOLDER
def update_list_images():
    path_user_images = user_directory(app.config['UPLOAD_FOLDER'], current_user.get_id())
    list_images = []
    onlyfiles = [f for f in listdir(path_user_images) if isfile(join(path_user_images, f))]
    for each in onlyfiles:
        list_images.append(each)
    return list_images

# Converte lista de nomes de arquivos em lista de objetos MyImage
def convert_to_list_objects(list_images):
  list_objects_images = []
  for index, each in enumerate(list_images):
    elemento = MyImage(index+1, each)
    list_objects_images.append(elemento)
  return list_objects_images

# Converte lista de files em lista de objetos MyImage serializado
def convert_to_list_objects_serializado(list_images):
    list_objects_images = []
    for each in list_images:
        elemento = MyImage(each.id, each.name)
        list_objects_images.append(elemento)
    return list_objects_images

def convert_list_objects_to_json(list_images):
    my_dict = {}
    list_objects_images = []
    for each in list_images:
        elemento = MyImage(each.id, each.name)
        list_objects_images.append(elemento)
    for index, each in enumerate(list_objects_images): 
        my_dict[index] = each.serialize()
    my_json = json.dumps(my_dict)
    return my_json

# retorna a paginacao da lista de objetos images
def get_images(offset=0, per_page=10, images=None):
    return images[offset: offset + per_page]

# dado um arquivo cria o thumbnail correspondente e salva na pasta de thumbnails
def tnails(filename, filename_path, thumbnail_path):
    try:
        filename_complete = filename_path + '/' + filename
        image = Image.open(filename_complete)
        image.thumbnail((90,90))        
        new_thumbnail = thumbnail_path + '/' + filename
        image.save(new_thumbnail)
    except IOError as io:
        raise Exception(f'Erro in tnails - {io}')

@app.route('/uploads/users/<int:id>/images')
@login_required
def pagination_list_files_page(id):
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    # Carrega a lista de objetos images
    images = convert_to_list_objects(update_list_images())
    total = len(images)
    pagination_images = get_images(offset=offset, per_page=per_page, images=images)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    if total == 0: 
        msg = f'You dont have any image yet!'
        flash(msg, category='success')
    return render_template('uploads/pagination_list_files.html', images=pagination_images, page=page, per_page=per_page, pagination=pagination)

@app.route('/uploads/users/<int:id>/images/<name>')
@login_required
def download_file(id, name):
    path_image_saved = user_directory(app.config['UPLOAD_FOLDER'], str(id))
    return send_from_directory(path_image_saved, name)

@app.route("/uploads/users/<int:id>/images/<name>/delete")
@login_required
def delete_image(id, name):

    path_image_saved = user_directory(app.config['UPLOAD_FOLDER'], id)
    path_image_thumbnail_saved = user_directory(app.config['UPLOAD_FOLDER_THUMBNAILS'], id)
    
    image_name_uploads = path_image_saved +  '/' + name
    image_name_thubnails = path_image_thumbnail_saved + '/' + name

    if os.path.exists(image_name_uploads):
        try:
            os.remove(image_name_uploads)
            os.remove(image_name_thubnails)
            file_to_delete = files_service.query_file_by_name(name)
            users_service.unlink_file(user_id=current_user.get_id(), file=file_to_delete)
            files_service.delete_file(file_to_delete)
            flash(f'{name} deleted successfully!', category='success')
        except Exception as e:
            flash(f'Error {e} during deletion of {name}!', category='danger')
    else:
        flash(f'The file {name} does not exist!', category='danger')        
    return redirect(url_for('pagination_list_files_page', id=id))

@app.route('/uploads/progress', methods=['GET'])
@login_required
def load_upload_classic_progress_page():
    return render_template('uploads/upload_classic_progress.html')

@app.route('/uploads/progress', methods=['POST'])
@login_required
def upload_classic_progress():    
    # Faz o upload do arquivo
    uploaded_file = request.files['uploadFile']
    try: 
        filename_secure = secure_filename(uploaded_file.filename)
        path_to_save_image = user_directory(app.config['UPLOAD_FOLDER'], current_user.get_id())
        uploaded_file.save(os.path.join(path_to_save_image, filename_secure))
        filenameimage = filename_secure
        file_to_save = File(name=filename_secure)
        files_service.insert_file(file_to_save)
        path_to_save_image_thumbnail = user_directory(app.config['UPLOAD_FOLDER_THUMBNAILS'], current_user.get_id())
        tnails(filename_secure, path_to_save_image, path_to_save_image_thumbnail)
        users_service.link_to_file(user_id=current_user.get_id(), file=file_to_save)
        msg = f'Upload {filename_secure} accomplished with success!'
    except Exception as e:
        flash(f'Error in Upload - {e}', category='danger')
        return redirect(url_for('list_files_page'))

    return jsonify({'htmlresponse': render_template('uploads/response.html', msg=msg, filenameimage=filenameimage)})

@app.route('/uploads/progress/multiple/files', methods=['GET'])
@login_required
def load_upload_progress_multiple_files_page():
    return render_template('uploads/upload_progress_multiple_files.html')

@app.route('/uploads/progress/multiple/files', methods=['POST'])
@login_required
def upload_progress_multiple_files():    
    # Faz o upload do arquivo
    uploaded_file = request.files['file']
    try: 
        filename_secure = secure_filename(uploaded_file.filename)
        path_to_save_image = user_directory(app.config['UPLOAD_FOLDER'], current_user.get_id())
        uploaded_file.save(os.path.join(path_to_save_image, filename_secure))
        file_to_save = File(name=filename_secure)
        files_service.insert_file(file_to_save)
        path_to_save_image_thumbnail = user_directory(app.config['UPLOAD_FOLDER_THUMBNAILS'], current_user.get_id())
        tnails(filename_secure, path_to_save_image, path_to_save_image_thumbnail)
        users_service.link_to_file(user_id=current_user.get_id(), file=file_to_save)
        flash(f'Upload {filename_secure} accomplished with success!', category='success')
    except Exception as e:
        flash(f'Error in Upload - {e}', category='danger')
        return redirect(url_for('list_files_page'))

    return '', 204

@app.route('/uploads/users/<int:id>/search/my', methods=['GET'])
@login_required
def load_search_my_images(id):
    return render_template('uploads/my_search_images.html', id=id)

@app.route('/uploads/users/<int:id>/search/myimages', methods=['GET'])
def search_my_images(id):
    query = request.args.get('query')
    list_files = users_service.get_my_files_contains(id, query)    
    json_string = convert_list_objects_to_json(list_files)
    return {"result":json_string}