from flask import Flask
from flask_cors import CORS

from routes.pacientes import pacientes_bp

app = Flask(__name__)

CORS(app)

app.register_blueprint(pacientes_bp)

@app.route("/")
def inicio():
    return "Backend da UBS funcionando!"

if __name__ == "__main__":
    app.run(debug=True)