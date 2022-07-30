from myapp import app
from myapp import db, data_base
import datetime

CREATE_DB_EMPTY = False

print('Iniciando a aplicação SysFile')
# Dropa e recria o banco
try:
    if CREATE_DB_EMPTY:
        db.drop_all()
        db.create_all()
        db.session.commit()
        print(f'Data base {data_base} created with success!!')
    else:
        print(f'Data base {data_base} load successfully!')
        print(f'Hora: {datetime.datetime.now()}')
except Exception as e:
    print(f'Error creating {data_base} - {e}')

if __name__ == '__main__':
    app.run(debug=True)