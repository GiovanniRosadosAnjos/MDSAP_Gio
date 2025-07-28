import os
import sys

from flask import Flask, send_from_directory
from flask_cors import CORS

# Importar as rotas
from routes.mdsap import mdsap_bp

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Habilitar CORS para todas as rotas
CORS(app)

# Registrar blueprints
app.register_blueprint(mdsap_bp, url_prefix='/api/mdsap')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    try:
        return send_from_directory(app.static_folder, path)
    except:
        return send_from_directory(app.static_folder, 'index.html')

# Para Vercel
if __name__ != '__main__':
    # Quando executado no Vercel
    handler = app
else:
    # Para desenvolvimento local
    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000, debug=True)

