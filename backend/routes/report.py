import os
from flask import Blueprint, send_file
from flask_login import login_required, current_user
from backend.models.scan import Scan
from backend.config import Config

report_bp = Blueprint('report', __name__, url_prefix='/api')

@report_bp.route("/download-report/<int:scan_id>", methods=["GET"])
@login_required
def download_report(scan_id):
    scan = Scan.query.filter_by(id=scan_id, user_id=current_user.id).first()
    if not scan:
        return {"error": "scan not found"}, 404
    
    report_path = os.path.join(Config.REPORT_FOLDER, f"report_scan{scan.id}.pdf")
    if not os.path.exists(report_path):
        return {"error": "report not yet generated yet"}, 404
    
    return send_file(report_path, as_attachment=True)