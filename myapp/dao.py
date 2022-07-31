
from sqlalchemy import ForeignKey
from myapp import db, login_manager
from myapp import my_bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Estruturas (tabelas) de relacoes entre as classes
user_files = db.Table('user_files', 
    db.Column('user_id', db.Integer(), ForeignKey('user.id')), 
    db.Column('file_id', db.Integer(), ForeignKey('file.id')) 
)

# --- Classes base ---

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)
    my_files = db.relationship('File', secondary=user_files, backref='myfiles')

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = my_bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return my_bcrypt.check_password_hash(self.password_hash, attempted_password)

class File(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=100), nullable=False)

# --- Classes de servico (colecoes de classes bases) --- 

class Users:
    def insert_user(self, user):
        try:
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            raise Exception(f'Error during insert user - {e}')

    def query_user_by_username(self, p_username):
        user = User.query.filter_by(username=p_username).first()
        return user

    def query_user_by_id(self, p_id):
        user = User.query.filter_by(id=p_id).first()
        return user
    
    def list_all_users(self):
        return User.query.all()

    def update_user(self, id, username, email):
        try:
            user_to_update = self.query_user_by_id(id)
            user_to_update.username = username
            user_to_update.email_address = email
            db.session.commit()
        except Exception as e:
            raise Exception(f'Error during update user - {e}')

    def link_to_file(self, user_id, file):
        try:
            user = User.query.filter_by(id=user_id).first()
            file = File.query.filter_by(id=file.id).first()
            user.my_files.append(file)
            db.session.commit()
        except Exception as e:
            raise Exception(f'Error during file to user - {e}')

    def link_to_files(self, user_id, files):
        try:
            user = User.query.filter_by(id=user_id).first()
            for each in files:
                file = File.query.filter_by(id=each.id).first()
                user.my_files.append(file)    
            db.session.commit()
        except Exception as e:
            raise Exception(f'Error during files to user - {e}')

    def unlink_file(self, user_id, file):
        try:
            user = User.query.filter_by(id=user_id).first()
            file = File.query.filter_by(id=file.id).first()
            user.my_files.remove(file)
            db.session.commit()
        except Exception as e:
            raise Exception(f'Error during remove file from user - {e}')

    def list_all_files(self, user_id):
        user = User.query.filter_by(id=user_id).first()        
        return user.my_files

    def get_my_files_contains(self, user_id, query):
        # retorna todos os arquivos do user_id
        list_my_files = User.query.filter_by(id=user_id).first().my_files
        # retorna todos os arquivos que contem a query
        list_files_contains =  File.query.filter(File.name.contains(query))
        list_result = []
        # para cada item da lista que retorna contains checa se pertence a lista de arquivos do user_id
        for each_contains in list_files_contains: 
            if each_contains in list_my_files: 
                list_result.append(each_contains)
        return list_result

class Files:
    def insert_file(self, file):
        try:
            db.session.add(file)
            db.session.commit()
        except Exception as e:
            raise Exception(f'Error during insert file - {e}')

    def query_file_by_name(self, p_name):
        file = File.query.filter_by(name=p_name).first()
        return file
        
    def query_file_by_id(self, p_id):
        file = File.query.filter_by(id=p_id).first()
        return file
    
    def list_all_files(self):
        return File.query.all()

    def delete_file(self, file):
        try:
            file = File.query.filter_by(id=file.id).first()
            db.session.delete(file)
            db.session.commit()
        except Exception as e:
            raise Exception(f'Error during delete file - {e}')

    def search_file_by_name_contains(self, contains):
        try: 
            list_files =  File.query.filter(File.name.contains(contains))
            return list_files
        except Exception as e:
            raise Exception(f'Error during search file by name contains - {e}')