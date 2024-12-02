import pathlib
import connexion
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

basedir = pathlib.Path(__file__).parent.resolve()
connex_app = connexion.App(__name__, specification_dir=basedir)

LOCAL = True

server = "localhost" if LOCAL else "dist-6-505.uopnet.plymouth.ac.uk"
driver = '{ODBC Driver 18 for SQL Server}'
database = "master" if LOCAL else 'COMP2001_BMannino'
username = "SA" if LOCAL else "BMannino"
password = "C0mp2001!" if LOCAL else "SofP734+"

app = connex_app.app
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mssql+pyodbc:///?odbc_connect="
    f'DRIVER={driver};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password};'
    'Encrypt=yes;'
    'TrustServerCertificate=Yes;'
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)
