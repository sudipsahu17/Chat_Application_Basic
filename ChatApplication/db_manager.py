from flask_sqlalchemy import SQLAlchemy

db_name = 'chat_app'
db = SQLAlchemy()

def create_db_cursor(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{user}:{password}@{server}/{database}'.format(user='root',
                                                                    password='Sudip17#', server='localhost', database=db_name)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

def create_schema(app):
    #database_dest = os.path.join('C:\\', 'ProgramData', 'MySQL', 'MySQL Server 8.0', 'Data', db_name)
    #if not os.path.exists(database_dest):
    #db.drop_all(app=app)
    db.create_all(app = app)
    print('All Schemas/ Tables are created successfully !!')
    #else:
    #    print('Database - ' + db_name + ' already exist !!')
    #print(database_dest)
