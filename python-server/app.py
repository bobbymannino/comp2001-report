from flask import Flask, request, jsonify

app = Flask(__name__)

@app.get("/trails")
def users():
    return "<p>A list of users!</p>"

# TODO
# - admin create trail
# - admin delete trail
# - admin update trail
# - admin view trail
# - user view trail
# - user view all trails
# - admin view all trails
