from flask import Flask, request, jsonify
import pyodbc
import atexit

app = Flask(__name__)

server = "dist-6-505.uopnet.plymouth.ac.uk"
driver = '{ODBC Driver 18 for SQL Server}'
database = 'COMP2001_BMannino'
username = "BMannino"
password = "SofP734+"

connection_string = (
    f'DRIVER={driver};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password};'
    'Encrypt=yes;'
    'TrustServerCertificate=Yes;'
    'Connection Timeout=30;'
    'Trusted_Connection=No;'
)

connection = pyodbc.connect(connection_string)
cursor = connection.cursor()

def close_connection():
    connection.close()

atexit.register(close_connection)

class Trail:
    def __init__(self, trailId: int, title: str, createdAt: str | None = None):
        self.trailId = trailId
        self.title = title
        self.createdAt = createdAt

@app.get("/trails")
def trails():
    limit = request.args.get('limit', default=0, type=int)

    trails = []

    for row in cursor.execute("select trail_id, title from CW1.trails;").fetchmany(limit if limit > 0 else 96):
        trails.append(Trail(row[0], row[1]))

    return jsonify([trail.__dict__ for trail in trails])

@app.get("/trails/<trailId>")
def trail(trailId):
    # header: Authorization <email>;<password>
    # email, password = request.headers['Authorization'].split(';')

    # if email.strip() == "" or password.strip() == "":
        # return jsonify({"error": "Invalid email or password"}), 401

    row = cursor.execute("select * from CW1.trails where trail_id = ?", (trailId)).fetchone()
    if row == None:
        return jsonify({"message": "Trail not found"}), 404

    trail = Trail(row[0], row[1], row[2])

    return jsonify(trail.__dict__)

# TODO
# - admin create trail
# - admin delete trail
# - admin update trail
# - admin view trail
# - user view trail
