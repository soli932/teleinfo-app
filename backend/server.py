from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from database import init_db, get_guides, add_guide, delete_guide, get_guide
from auth import auth_bp, jwt, requires_roles
from storage import save_file, delete_file, get_file_path

app = Flask(__name__)
app.config['SECRET_KEY'] = 'teleinfo_secret_key_2023'  # Cambiar en producción
app.config['JWT_SECRET_KEY'] = 'jwt_teleinfo_secret_2023'  # Cambiar en producción
app.config['UPLOAD_FOLDER'] = 'uploads'

# Configurar CORS
CORS(app)

# Inicializar base de datos
init_db()

# Registrar blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')

# Inicializar JWT
jwt.init_app(app)

# Rutas de la API
@app.route('/api/guides', methods=['GET'])
def get_guides_route():
    try:
        guides = get_guides()
        return jsonify(guides)
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/api/guides', methods=['POST'])
@requires_roles('admin', 'editor')
def upload_guide():
    try:
        if 'file' not in request.files:
            return jsonify({'message': 'No se proporcionó archivo'}), 400
        
        file = request.files['file']
        name = request.form.get('name')
        category = request.form.get('category')
        
        if not name or not category:
            return jsonify({'message': 'Nombre y categoría son requeridos'}), 400
        
        if file.filename == '':
            return jsonify({'message': 'Nombre de archivo vacío'}), 400
        
        if file and file.filename.lower().endswith('.pdf'):
            # Guardar archivo
            filename = save_file(file, category)
            
            # Guardar en base de datos
            guide_id = add_guide(name, category, filename)
            
            return jsonify({'message': 'Archivo subido exitosamente', 'id': guide_id}), 201
        else:
            return jsonify({'message': 'Solo se permiten archivos PDF'}), 400
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/api/guides/<guide_id>', methods=['DELETE'])
@requires_roles('admin')
def delete_guide_route(guide_id):
    try:
        guide = get_guide(guide_id)
        if not guide:
            return jsonify({'message': 'Guía no encontrada'}), 404
        
        # Eliminar archivo
        delete_file(guide['filename'], guide['category'])
        
        # Eliminar de base de datos
        delete_guide(guide_id)
        
        return jsonify({'message': 'Guía eliminada exitosamente'})
    except Exception as e:
        return jsonify({'message': str(e)}), 500

@app.route('/api/guides/<guide_id>/download')
def download_guide(guide_id):
    try:
        guide = get_guide(guide_id)
        if not guide:
            return jsonify({'message': 'Guía no encontrada'}), 404
        
        file_path = get_file_path(guide['filename'], guide['category'])
        return send_file(file_path, as_attachment=True, download_name=guide['name'] + '.pdf')
    except Exception as e:
        return jsonify({'message': str(e)}), 500

if __name__ == '__main__':
    # Crear carpetas de uploads si no existen
    categories = ['HOB', 'AWS', 'WINDOWS', 'LINUX', 'CBB']
    for category in categories:
        os.makedirs(os.path.join(app.config['UPLOAD_FOLDER'], category), exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
