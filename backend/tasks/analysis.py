import numpy as np
import os
from backend.celery_app import celery
from backend.extensions import db
from backend.models.scan import Scan
from backend.ml.model import load_brats_model
from backend.scripts.predict import predict_segmentation
from backend.scripts.utils import generate_pdf_report

#resolves upload file from backend root directory
def resolve_path(relative_path):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    return os.path.abspath(os.path.join(base_dir, relative_path))


@celery.task(name="backend.tasks.analysis.analyze_scan_task")
def analyze_scan_task(scan_id):
    scan = Scan.query.get(scan_id)
    if not scan:
        print(f"Scan {scan_id} not found.")
        return f"Scan {scan_id} not found"

    try:
        full_path = resolve_path(scan.file_path)
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Scan file not found at: {full_path}")

        volume = np.load(full_path)
        model = load_brats_model()
        mask = predict_segmentation(model, volume)

        scan.analysis_status = "completed"
        scan.results_json = {"shape": list(mask.shape)}
        db.session.commit()

        os.makedirs("reports", exist_ok=True)
        report_path = os.path.abspath(os.path.join("reports", f"report_scan_{scan.id}.pdf"))
        generate_pdf_report(volume, mask, report_path)

        return f"Scan {scan_id} processed"
    except Exception as e:
        print(f"Error: {e}")
        scan.analysis_status = "error"
        db.session.commit()
        return f"Failed: {str(e)}"