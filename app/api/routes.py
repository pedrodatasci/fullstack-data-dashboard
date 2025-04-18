from flask import Blueprint, jsonify, request
from app.db.models import Record, db
from datetime import datetime

api_bp = Blueprint("api", __name__)

@api_bp.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "pong"})

@api_bp.route("/records", methods=["POST"])
def create_record():
    data = request.get_json()
    timestamp = datetime.strptime(data["timestamp"], "%Y-%m-%d")
    record = Record(value=data["value"], timestamp=timestamp)
    db.session.add(record)
    db.session.commit()
    return jsonify({"message": "record created"}), 201

@api_bp.route("/records", methods=["GET"])
def get_records():
    records = Record.query.all()
    result = [{"id": r.id, "value": r.value, "timestamp": r.timestamp.strftime("%Y-%m-%d")} for r in records]
    return jsonify(result)