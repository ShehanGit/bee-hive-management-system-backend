# app/controllers/hive_controller.py

from flask import Blueprint, request, jsonify
from app import db
from app.models.hive import Hive

hive_blueprint = Blueprint('hive_blueprint', __name__)

@hive_blueprint.route('/hives', methods=['GET'])
def get_all_hives():
    """Get a list of all hives."""
    hives = Hive.query.all()
    results = []
    for hive in hives:
        results.append({
            'id': hive.id,
            'name': hive.name,
            'location_lat': hive.location_lat,
            'location_lng': hive.location_lng,
            'created_at': hive.created_at
        })
    return jsonify(results), 200

@hive_blueprint.route('/hives', methods=['POST'])
def create_hive():
    """Create a new hive."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    name = data.get('name')
    lat = data.get('location_lat')
    lng = data.get('location_lng')

    if not all([name, lat, lng]):
        return jsonify({"error": "Missing required fields"}), 400

    new_hive = Hive(name=name, location_lat=lat, location_lng=lng)
    db.session.add(new_hive)
    db.session.commit()

    return jsonify({"message": f"Hive '{name}' created successfully"}), 201

@hive_blueprint.route('/hives/<int:hive_id>', methods=['GET'])
def get_hive(hive_id):
    """Get a single hive by ID."""
    hive = Hive.query.get_or_404(hive_id)
    return jsonify({
        'id': hive.id,
        'name': hive.name,
        'location_lat': hive.location_lat,
        'location_lng': hive.location_lng,
        'created_at': hive.created_at
    }), 200

@hive_blueprint.route('/hives/<int:hive_id>', methods=['PUT'])
def update_hive(hive_id):
    """Update an existing hive."""
    hive = Hive.query.get_or_404(hive_id)
    data = request.get_json()

    hive.name = data.get('name', hive.name)
    hive.location_lat = data.get('location_lat', hive.location_lat)
    hive.location_lng = data.get('location_lng', hive.location_lng)

    db.session.commit()
    return jsonify({"message": f"Hive '{hive.name}' updated successfully"}), 200

@hive_blueprint.route('/hives/<int:hive_id>', methods=['DELETE'])
def delete_hive(hive_id):
    """Delete a hive."""
    hive = Hive.query.get_or_404(hive_id)
    db.session.delete(hive)
    db.session.commit()
    return jsonify({"message": "Hive deleted successfully"}), 200
