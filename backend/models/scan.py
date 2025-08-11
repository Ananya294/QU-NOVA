from backend.extensions import db

class Scan(db.Model):
    __tablename__ = 'scan'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #FK constarint linking each scan to user(doctor)
    filename = db.Column(db.String(128), nullable=False)
    file_path = db.Column(db.String(256), nullable=False)
    upload_time = db.Column(db.DateTime, server_default=db.func.now())
    analysis_status = db.Column(db.String(32), default="pending")
    results_json = db.Column(db.JSON)