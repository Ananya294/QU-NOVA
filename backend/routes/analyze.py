from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from backend.extensions import db
from backend.models.scan import Scan
from backend.tasks.analysis import analyze_scan_task

analyze_bp = Blueprint('analyze', __name__, url_prefix='/api')

@analyze_bp.route("/analyze/<int:scan_id>", methods=["GET"])
@login_required   #before calling function, flask login checks if current_user autheticated or not (is_autheticated provided by user-mixin - inherited by user model)
def analyze(scan_id):
    scan = Scan.query.filter_by(id=scan_id, user_id=current_user.id).first()
    if not scan:
        return jsonify({"error":"Scan not found"}), 404
    
    scan.analysis_status = "processing"
    db.session.commit()

    analyze_scan_task.delay(scan.id)

    return jsonify({"message": "Analysis started", "scan_id": scan.id})

@analyze_bp.route("/status/<int:scan_id>", methods=["GET"])
@login_required
def get_status(scan_id):
    scan = Scan.query.filter_by(id=scan_id, user_id=current_user.id).first()
    if not scan:
        return jsonify({"error": "Scan not found"}), 404
    return jsonify({"status": scan.analysis_status})
