import os
import uuid
from werkzeug.utils import secure_filename

def save_file(file, category):
    # Generar nombre único para el archivo
    filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
    upload_folder = os.path.join('uploads', category)
    file_path = os.path.join(upload_folder, filename)
    
    file.save(file_path)
    return filename

def delete_file(filename, category):
    file_path = get_file_path(filename, category)
    if os.path.exists(file_path):
        os.remove(file_path)

def get_file_path(filename, category):
    return os.path.join('uploads', category, filename)