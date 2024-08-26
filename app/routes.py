from flask import Blueprint, jsonify, request
from .models import QueryHistory
from app import db
import socket
import os, time
import prometheus_client

main = Blueprint('main', __name__)

@main.route('/')
def root():
    return jsonify({
        "version": "0.1.0",
        "date": int(time.time()),
        "kubernetes": os.getenv('KUBERNETES_SERVICE_HOST') is not None
    })

@main.route('/health')
def health():
    return jsonify({"status": "healthy"})

@main.route('/metrics')
def metrics():
    return prometheus_client.generate_latest()

@main.route('/v1/tools/lookup', methods=['POST'])
def lookup():
    domain = request.json.get('domain')
    try:
        ip_addresses = [socket.gethostbyname(domain)]
        query = QueryHistory(query=domain, result=str(ip_addresses))
        db.session.add(query)
        db.session.commit()
        return jsonify(ip_addresses)
    except socket.error as e:
        return jsonify({"error": str(e)}), 500

@main.route('/v1/tools/validate', methods=['POST'])
def validate():
    address = request.json.get('address')
    try:
        socket.inet_pton(socket.AF_INET, address)
        return jsonify({"valid": True})
    except socket.error:
        return jsonify({"valid": False})

@main.route('/v1/history', methods=['GET'])
def history():
    queries = db.session.query(QueryHistory).order_by(QueryHistory.timestamp.desc()).limit(20).all()
    return jsonify([{
        "query": query.query,
        "result": query.result,
        "timestamp": query.timestamp.isoformat()
    } for query in queries])
