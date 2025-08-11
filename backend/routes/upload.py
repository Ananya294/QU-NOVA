import os
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from backend.extensions import db
from backend.models.scan import Scan
import numpy as np

upload_bp = Blueprint('upload', __name__, url_prefix='/api')

ALLOWED_EXTENSIONS = {'npy'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route("/upload", methods=["POST"])
@login_required

def upload_file():
    if 'file' not in request.files:
        return jsonify({"error":"No file part"}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({"error":"No selected file"}), 400
    
    if not allowed_file(file.filename):
        return jsonify({"error":"Only .npy files allowed"}), 400
    
    filename = secure_filename(file.filename)
    user_folder = os.path.join(current_app.config['UPLOAD_FOLDER'], f"user_{current_user.id}")
    os.makedirs(user_folder, exist_ok=True)

    file_path = os.path.join(user_folder, filename)
    file.save(file_path)

    #check if its real npy file
    try:
        _ = np.load(file_path)
    except Exception:
        os.remove(file_path)
        return jsonify({"error":"Invalid .npy file"}), 400
    
    #record in database
    scan = Scan(
        user_id=current_user.id,
        filename=filename,
        file_path=file_path
    )
    db.session.add(scan)
    db.session.commit()

    return jsonify({"mesage": "File uploaded", "scan_id": scan.id})